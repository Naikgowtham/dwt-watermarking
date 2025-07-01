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
)
from core.dwt_engine import embed_bits_in_dwt, extract_bits_from_dwt
from utils.logger import setup_logger
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

        # Extract existing bits
        logger.debug("Extracting existing parity bitstream via DWT engine")
        extracted_bits = extract_bits_from_dwt(image)
        total_bits = len(extracted_bits)
        logger.info(f"Extracted total bitstream length: {total_bits} bits")
        logger.debug(f"First 32 bits of extracted stream: {extracted_bits[:32]}")

        # Detect signature
        signature = get_signature_bits()
        logger.debug(f"Expected signature bits: {signature}")
        has_signature = extracted_bits[:16] == signature
        logger.info(f"Signature {'found' if has_signature else 'not found'} in existing bitstream")

        # Parse old messages if signature present
        all_messages = []
        cursor = 16 if has_signature else 0
        if has_signature:
            logger.debug("Parsing existing messages from extracted bitstream")
            while cursor + 16 <= total_bits:
                header_bits = extracted_bits[cursor : cursor + 16]
                length = bits_to_int(header_bits)
                logger.debug(f"Header at cursor {cursor}: length={length} bits")
                
                # Validate header
                if length <= 0 or length % 8 != 0 or cursor + 16 + length > total_bits:
                    logger.warning(f"Invalid or out-of-bounds header at cursor {cursor}: length={length}. Stopping parse.")
                    break
                
                cursor += 16
                message_bits = extracted_bits[cursor : cursor + length]
                try:
                    old_msg = bits_to_string(message_bits)
                    all_messages.append(old_msg)
                    logger.info(f"Parsed existing message: '{old_msg}' (length={length} bits)")
                except ValueError as e:
                    logger.warning(f"Failed to decode message at cursor {cursor}: {e}. Stopping parse.")
                    break
                
                cursor += length
            logger.info(f"Total existing messages parsed: {len(all_messages)}")
        else:
            logger.debug("No existing watermark messages to parse")

        # Append new message
        all_messages.append(message)
        logger.info(f"Appending new message. Total messages to embed: {len(all_messages)}")

        # Prepare combined bitstream
        logger.debug("Preparing combined bitstream with headers and signature")
        combined_stream = prepare_bitstream_with_headers(all_messages)
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

        # Encode watermarked image to base64
        logger.debug(f"Encoding watermarked image at {wm_path} to base64")
        b64_data = image_to_base64(wm_path)
        logger.info("Base64 encoding complete")

        logger.info("POST /watermark completed successfully")
        return jsonify({
            "original_filename": orig_filename,
            "watermarked_filename": wm_filename,
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

        # Check signature
        signature = get_signature_bits()
        logger.debug(f"Expected signature bits: {signature}")
        if raw_bits[:16] != signature:
            logger.info("Signature not found in bitstream; no watermark present")
            return jsonify({"messages": []}), 200
        logger.info("Valid signature detected; proceeding to parse messages")

        # Parse messages
        messages = []
        cursor = 16
        while cursor + 16 <= total_bits:
            header_bits = raw_bits[cursor : cursor + 16]
            length = bits_to_int(header_bits)
            logger.debug(f"Header at cursor {cursor}: length={length} bits")

            if length <= 0 or length % 8 != 0 or cursor + 16 + length > total_bits:
                logger.warning(f"Invalid or out-of-bounds header at cursor {cursor}: length={length}. Stopping parse.")
                break

            cursor += 16
            segment_bits = raw_bits[cursor : cursor + length]
            try:
                msg = bits_to_string(segment_bits)
                messages.append(msg)
                logger.info(f"Extracted message: '{msg}'")
            except ValueError as e:
                logger.warning(f"Failed to decode message at cursor {cursor}: {e}. Stopping parse.")
                break

            cursor += length

        logger.info(f"Extraction complete: {len(messages)} messages found")
        return jsonify({"messages": messages}), 200

    except Exception as e:
        logger.exception("Extraction failed due to unexpected error")
        return jsonify({"error": "Failed to extract watermark."}), 500
