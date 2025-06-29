import os
import uuid
from flask import Blueprint, request, jsonify
from utils.logger import setup_logger
from utils.image_utils import load_image, save_image, image_to_base64
from utils.bit_utils import string_to_bits, bits_to_string, add_header, extract_header
from core.dwt_engine import embed_bits_in_dwt, extract_bits_from_dwt  # ✅ now parity-based

logger = setup_logger(__name__)
watermark_bp = Blueprint("watermark", __name__)

# File storage setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")
ORIGINAL_FOLDER = os.path.join(UPLOAD_FOLDER, "original")
WATERMARKED_FOLDER = os.path.join(UPLOAD_FOLDER, "watermarked")
os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
os.makedirs(WATERMARKED_FOLDER, exist_ok=True)

# -----------------------------------
# 🔧 Route: /watermark (Embed)
# -----------------------------------
@watermark_bp.route("/watermark", methods=["POST"])
def embed_watermark():
    logger.info("POST /watermark called")
    try:
        image_file = request.files.get("image")
        message = request.form.get("message", "")

        if not image_file:
            logger.error("No image file provided.")
            return jsonify({"error": "Image file is required."}), 400
        if not message:
            logger.error("No message provided.")
            return jsonify({"error": "Message is required."}), 400

        logger.debug("Loading image for embedding...")
        image = load_image(image_file)

        logger.debug("Converting message to bits and adding header...")
        msg_bits = string_to_bits(message)
        full_bits = add_header(msg_bits)

        logger.debug(f"Embedding {len(full_bits)} bits using Y-channel parity...")
        watermarked_img = embed_bits_in_dwt(image, full_bits)  # ✅ No band argument

        uid = uuid.uuid4().hex
        orig_path = os.path.join(ORIGINAL_FOLDER, f"{uid}_orig.png")
        wm_path   = os.path.join(WATERMARKED_FOLDER, f"{uid}_wm.png")
        save_image(image, orig_path)
        save_image(watermarked_img, wm_path)

        logger.info("Embedding successful, encoding to base64...")
        wm_b64 = image_to_base64(wm_path)
        logger.info("POST /watermark completed successfully.")
        return jsonify({"image": wm_b64, "filename": f"{uid}_wm.png"}), 200

    except Exception as e:
        logger.exception("Embedding failed.")
        return jsonify({"error": "Failed to embed watermark."}), 500

# -----------------------------------
# 🔧 Route: /extract (Retrieve)
# -----------------------------------
@watermark_bp.route("/extract", methods=["POST"])
def extract_watermark():
    logger.info("POST /extract called")
    try:
        image_file = request.files.get("image")
        if not image_file:
            logger.error("No image file provided.")
            return jsonify({"error": "Image file is required."}), 400

        logger.debug("Loading watermarked image for extraction...")
        image = load_image(image_file)

        logger.debug("Extracting full bitstream from Y-channel parity...")
        full_bits = extract_bits_from_dwt(image)  # ✅ No band argument
        logger.debug(f"First 32 bits extracted: {full_bits[:32]}")
        logger.debug(f"Total bits extracted: {len(full_bits)}")

        logger.debug("Parsing header and message bits...")
        msg_length, msg_bits = extract_header(full_bits)
        logger.debug(f"Message length from header: {msg_length} bits")

        logger.debug("Converting message bits to string...")
        message = bits_to_string(msg_bits)
        logger.info("POST /extract completed successfully.")
        return jsonify({"message": message}), 200

    except Exception as e:
        logger.exception("Extraction failed.")
        return jsonify({"error": "Failed to extract watermark."}), 500
