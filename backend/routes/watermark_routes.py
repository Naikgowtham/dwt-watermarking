import os
import uuid
import logging
from flask import Blueprint, request, jsonify
from utils.image_utils import load_image, save_image, image_to_base64
from utils.bit_utils import (
    string_to_bits,
    bits_to_string,
    int_to_bits,
    bits_to_int,
    get_signature_bits,
    prepare_bitstream_with_headers,
    image_to_sha256_bits,
    prepare_bitstream_with_hash_and_messages,
    parse_bitstream_with_hash_and_messages,
)
from utils.ipfs_utils import upload_to_pinata
import zlib
from core.dwt_engine import embed_bits_in_dwt, extract_bits_from_dwt
from utils.logger import setup_logger
import time
from utils.blockchain_utils import store_watermark_on_chain, get_watermark_from_chain
from web3 import Web3
logger = setup_logger(__name__)
watermark_bp = Blueprint("watermark", __name__)

# Configure upload folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")
ORIGINAL_FOLDER = os.path.join(UPLOAD_FOLDER, "original")
WATERMARKED_FOLDER = os.path.join(UPLOAD_FOLDER, "watermarked")
os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
os.makedirs(WATERMARKED_FOLDER, exist_ok=True)

@watermark_bp.route("/watermark", methods=["POST"])
def watermark_image():
    logger.info("POST /watermark called")
    try:
        # Validate inputs
        if "image" not in request.files:
            logger.error("No 'image' field in request.files")
            return jsonify({"error": "Image file is required."}), 400
        image_file = request.files["image"]
        message = request.form.get("message", "")
        if not message:
            logger.error("No 'message' field in request.form or empty message")
            return jsonify({"error": "Message is required."}), 400
        logger.debug(f"Received file: filename={image_file.filename}, content_type={image_file.content_type}")
        logger.debug(f"Received message of length {len(message)} characters")

        # Load image
        logger.debug("Loading original image from uploaded file")
        image = load_image(image_file)
        logger.info(f"Original image loaded: shape={image.shape}, dtype={image.dtype}")

        # Try to extract existing hash and messages
        logger.debug("Attempting to extract existing hash and messages for appending support")
        try:
            raw_bits = extract_bits_from_dwt(image)
            hash_bits, existing_messages = parse_bitstream_with_hash_and_messages(raw_bits)
            logger.info(f"Found existing watermark with {len(existing_messages)} messages. Appending new message.")
        except Exception as e:
            logger.info(f"No valid existing watermark found or parse failed: {e}. Starting new watermark.")
            existing_messages = []
        # Append new message
        all_messages = existing_messages + [message]
        logger.info(f"Total messages to embed: {len(all_messages)}")

        # Prepare bitstream: [256-bit hash][16-bit length][msg bits] ...
        logger.debug("Preparing bitstream with SHA256 hash and multi-message framing")
        combined_stream = prepare_bitstream_with_hash_and_messages(image, all_messages)
        combined_length = len(combined_stream)
        logger.info(f"Combined bitstream length: {combined_length} bits")

        # Embed into image
        logger.debug("Embedding combined bitstream into image via DWT parity")
        watermarked_image = embed_bits_in_dwt(image, combined_stream)
        logger.info("Embedding complete without mismatches")

        # Save original and watermarked images
        uid = uuid.uuid4().hex
        orig_filename = f"{uid}_orig.png"
        wm_filename   = f"{uid}_wm.png"
        orig_path = os.path.join(ORIGINAL_FOLDER, orig_filename)
        wm_path   = os.path.join(WATERMARKED_FOLDER, wm_filename)

        logger.debug(f"Saving original image to {orig_path}")
        save_image(image, orig_path)
        logger.info("Original image saved successfully")

        logger.debug(f"Saving watermarked image to {wm_path}")
        save_image(watermarked_image, wm_path)
        logger.info("Watermarked image saved successfully")

        # Upload both images to Pinata
        logger.info("Starting upload of original and watermarked images to Pinata Cloud (IPFS)...")
        ipfs_start_time = time.time()
        try:
            orig_cid = upload_to_pinata(orig_path)
            logger.info(f"Original image uploaded to Pinata. CID: {orig_cid}")
        except Exception as e:
            logger.error(f"Failed to upload original image to Pinata: {e}", exc_info=True)
            orig_cid = None
        try:
            wm_cid = upload_to_pinata(wm_path)
            logger.info(f"Watermarked image uploaded to Pinata. CID: {wm_cid}")
        except Exception as e:
            logger.error(f"Failed to upload watermarked image to Pinata: {e}", exc_info=True)
            wm_cid = None
        ipfs_elapsed = time.time() - ipfs_start_time
        logger.info(f"IPFS upload step completed in {ipfs_elapsed:.2f} seconds.")

        # --- Blockchain logging integration ---
        try:
            # Compute SHA256 hashes for both images (hex string)
            orig_hash_bits = image_to_sha256_bits(image)
            original_hash = bytearray(int(''.join(str(b) for b in orig_hash_bits[i:i+8]), 2) for i in range(0, 256, 8)).hex()
            wm_hash_bits = image_to_sha256_bits(watermarked_image)
            watermarked_hash = bytearray(int(''.join(str(b) for b in wm_hash_bits[i:i+8]), 2) for i in range(0, 256, 8)).hex()
            logger.info(f"Original image SHA256 hash: {original_hash}")
            logger.info(f"Watermarked image SHA256 hash: {watermarked_hash}")

            # Prepare message string and CRC
            combined_message_string = ''.join(all_messages)
            crc_value = zlib.crc32(combined_message_string.encode()) & 0xFFFF
            logger.info(f"Combined message string: {combined_message_string}")
            logger.info(f"CRC value: {crc_value}")

            # Parent hash (zero hash for now)
            parent_hash = '00' * 32
            logger.info(f"Parent hash (hex): {parent_hash}")

            # Convert hex hashes to bytes32
            original_hash_bytes = bytes.fromhex(original_hash)
            watermarked_hash_bytes = bytes.fromhex(watermarked_hash)
            parent_hash_bytes = bytes.fromhex(parent_hash)

            tx_hash = store_watermark_on_chain(
                original_hash=original_hash_bytes,
                watermarked_hash=watermarked_hash_bytes,
                watermark_data=combined_message_string,
                original_cid=orig_cid or '',
                watermarked_cid=wm_cid or '',
                crc=crc_value,
                parent_hash=parent_hash_bytes
            )
            logger.info(f"Logged watermark to blockchain. Tx hash: {tx_hash}")
        except Exception as e:
            logger.error(f"Blockchain logging failed: {e}")
        # --- End blockchain logging integration ---

        # Encode watermarked image to base64
        logger.debug(f"Encoding watermarked image at {wm_path} to base64")
        b64_data = image_to_base64(wm_path)
        logger.info("Base64 encoding complete")
        logger.info("POST /watermark completed successfully")
        return jsonify({
            "original_filename": orig_filename,
            "watermarked_filename": wm_filename,
            "original_cid": orig_cid,
            "watermarked_cid": wm_cid,
            "image": b64_data
        }), 200
    except Exception as e:
        logger.exception("Embedding failed due to unexpected error")
        return jsonify({"error": "Failed to embed watermark."}), 500


@watermark_bp.route("/extract", methods=["POST"])
def extract_watermark():
    logger.info("POST /extract called")
    try:
        if "image" not in request.files:
            logger.error("No 'image' field in request.files")
            return jsonify({"error": "Image file is required."}), 400
        image_file = request.files["image"]

        logger.debug(f"Loading watermarked image: filename={image_file.filename}")
        image = load_image(image_file)
        logger.info(f"Watermarked image loaded: shape={image.shape}, dtype={image.dtype}")

        # Extract full bitstream
        logger.debug("Extracting full parity bitstream via DWT engine")
        raw_bits = extract_bits_from_dwt(image)
        total_bits = len(raw_bits)
        logger.info(f"Extracted total bitstream length: {total_bits} bits")
        logger.debug(f"First 32 bits of bitstream: {raw_bits[:32]}")

        # Parse hash and messages
        try:
            hash_bits, messages = parse_bitstream_with_hash_and_messages(raw_bits)
            # Convert hash bits to hex string for return
            hash_bytes = bytearray()
            for i in range(0, 256, 8):
                byte = 0
                for b in raw_bits[i:i+8]:
                    byte = (byte << 1) | b
                hash_bytes.append(byte)
            hash_hex = hash_bytes.hex()
            logger.info(f"Extracted SHA256 hash: {hash_hex}")
        except Exception as e:
            logger.warning(f"Failed to parse bitstream: {e}")
            return jsonify({"messages": [], "hash": None, "crc_match": False, "on_chain": None}), 200

        # Query blockchain using extracted hash
        on_chain = None
        crc_match = False
        try:
            entry = contract.functions.getWatermark(Web3.to_bytes(hexstr=hash_hex)).call()
            if entry and entry[0] != b'\x00' * 32:
                original_hash_hex     = entry[0].hex()
                watermarked_hash_hex  = entry[1].hex()
                watermark_data        = entry[2]
                original_cid          = entry[3]
                watermarked_cid       = entry[4]
                crc_on_chain          = entry[5]
                parent_hash_hex       = entry[6].hex()
                # Compute CRC from extracted messages
                full_message = ''.join(messages)
                crc_actual = zlib.crc32(full_message.encode()) & 0xFFFF
                crc_match = crc_actual == crc_on_chain
                on_chain = {
                    "originalHash": original_hash_hex,
                    "watermarkedHash": watermarked_hash_hex,
                    "watermarkData": watermark_data,
                    "originalCID": original_cid,
                    "watermarkedCID": watermarked_cid,
                    "crc": crc_on_chain,
                    "parentHash": parent_hash_hex
                }
            else:
                on_chain = None
        except Exception as e:
            logger.warning(f"Blockchain query failed: {e}")
            on_chain = None

        logger.info(f"Extraction complete: {len(messages)} messages found")
        return jsonify({
            "messages": messages,
            "hash": hash_hex,
            "crc_match": crc_match,
            "on_chain": on_chain
        }), 200

    except Exception as e:
        logger.exception("Extraction failed due to unexpected error")
        return jsonify({"error": "Failed to extract watermark."}), 500


@watermark_bp.route("/blockchain/logs", methods=["GET"])
def blockchain_logs():
    try:
        logs = get_all_watermark_logs()
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@watermark_bp.route("/get_watermark", methods=["POST"])
def get_watermark():
    try:
        data = request.get_json()
        logger.debug(f"Received /get_watermark request data: {data}")
        if not data or 'original_hash' not in data:
            logger.error("No 'original_hash' provided in request JSON.")
            return jsonify({"error": "'original_hash' is required in JSON body."}), 400
        original_hash = data['original_hash']
        try:
            original_hash_bytes = bytes.fromhex(original_hash)
            logger.debug(f"Converted original_hash to bytes32: {original_hash_bytes.hex()}")
        except Exception as e:
            logger.error(f"Invalid hex for original_hash: {e}")
            return jsonify({"error": "Invalid hex string for original_hash."}), 400
        try:
            entry = get_watermark_from_chain(original_hash_bytes)
            if entry is None:
                logger.warning("Watermark not found on chain.")
                return jsonify({"error": "Watermark not found or blockchain error"}), 404
            logger.info(f"Fetched watermark from chain for hash {original_hash}: {entry}")
            return jsonify(entry), 200
        except Exception as e:
            logger.error(f"Blockchain error: {e}")
            return jsonify({"error": "Watermark not found or blockchain error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in /get_watermark: {e}")
        return jsonify({"error": "Watermark not found or blockchain error"}), 500
