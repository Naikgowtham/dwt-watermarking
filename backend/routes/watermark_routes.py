import os
import uuid
from flask import Blueprint, request, jsonify
from utils.logger import setup_logger
from utils.image_utils import load_image, save_image, image_to_base64
from utils.bit_utils import string_to_bits, bits_to_string, add_header
from core.dwt_engine import embed_bits_in_dwt, extract_bits_from_dwt

logger = setup_logger(__name__)
watermark_bp = Blueprint("watermark", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")
ORIGINAL_FOLDER = os.path.join(UPLOAD_FOLDER, "original")
WATERMARKED_FOLDER = os.path.join(UPLOAD_FOLDER, "watermarked")

os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
os.makedirs(WATERMARKED_FOLDER, exist_ok=True)

# -----------------------------------
# 🔧 Route: /watermark
# -----------------------------------
@watermark_bp.route("/watermark", methods=["POST"])
def embed_watermark():
    logger.info("POST /watermark called")

    try:
        image_file = request.files.get("image")
        message = request.form.get("message")

        if not image_file:
            logger.error("No image file provided for embedding.")
            return jsonify({"error": "Image file is required."}), 400

        if not message:
            logger.error("No message provided for embedding.")
            return jsonify({"error": "Message is required."}), 400

        logger.debug("Loading image from request...")
        image = load_image(image_file)
        logger.debug("Converting message to bitstream...")
        message_bits = string_to_bits(message)
        full_bitstream = add_header(message_bits)

        logger.debug("Embedding bitstream into image using DWT...")
        watermarked_image = embed_bits_in_dwt(image, full_bitstream, band='LH')

        # Save images
        uid = str(uuid.uuid4())
        original_path = os.path.join(ORIGINAL_FOLDER, f"{uid}_original.png")
        watermarked_path = os.path.join(WATERMARKED_FOLDER, f"{uid}_watermarked.png")

        logger.debug(f"Saving original image to: {original_path}")
        save_image(image, original_path)

        logger.debug(f"Saving watermarked image to: {watermarked_path}")
        save_image(watermarked_image, watermarked_path)

        logger.debug("Encoding watermarked image to base64...")
        watermarked_base64 = image_to_base64(watermarked_path)

        logger.info("Watermark embedding successful.")
        return jsonify({
            "image": watermarked_base64,
            "filename": f"{uid}_watermarked.png"
        }), 200

    except Exception as e:
        logger.exception("Watermark embedding failed due to an internal error.")
        return jsonify({"error": "Failed to embed watermark."}), 500

# -----------------------------------
# 🔧 Route: /extract
# -----------------------------------
@watermark_bp.route("/extract", methods=["POST"])
def extract_watermark():
    logger.info("POST /extract called")

    try:
        image_file = request.files.get("image")

        if not image_file:
            logger.error("No image file provided for extraction.")
            return jsonify({"error": "Image file is required."}), 400

        logger.debug("Loading watermarked image from request...")
        image = load_image(image_file)

        logger.debug("Extracting bits from DWT band...")
        message_bits = extract_bits_from_dwt(image, band='LH')

        logger.debug("Converting extracted bits back to string...")
        message = bits_to_string(message_bits)

        logger.info("Watermark extraction successful.")
        return jsonify({"message": message}), 200

    except Exception as e:
        logger.exception("Watermark extraction failed due to an internal error.")
        return jsonify({"error": "Failed to extract watermark."}), 500
