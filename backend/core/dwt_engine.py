import numpy as np
import pywt
import cv2
from utils.logger import setup_logger
from utils.bit_utils import bits_to_int, extract_header

logger = setup_logger(__name__)

def embed_bits_in_dwt(image_array: np.ndarray, bitstream: list, band='LH') -> np.ndarray:
    logger.info("Starting DWT watermark embedding")

    try:
        if image_array is None:
            logger.error("Input image array is None.")
            raise ValueError("Image input is missing.")

        if len(image_array.shape) != 3 or image_array.shape[2] != 3:
            logger.warning("Image is not a 3-channel (color) image. Converting to grayscale.")
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        logger.debug(f"Image shape for DWT: {image_array.shape}")
        coeffs2 = pywt.dwt2(image_array, 'haar')
        LL, (LH, HL, HH) = coeffs2

        band_map = {'LH': LH, 'HL': HL}
        if band not in band_map:
            logger.error(f"Invalid band selected: '{band}'. Use 'LH' or 'HL'.")
            raise ValueError("Band must be 'LH' or 'HL'")

        target_band = band_map[band]
        flat_band = target_band.flatten()
        logger.debug(f"Embedding into band: {band}, shape = {target_band.shape}, coefficients = {flat_band.size}")

        if len(bitstream) > flat_band.size:
            logger.error("Bitstream too large to embed in selected band.")
            raise ValueError("Not enough coefficients to embed all bits.")

        # Embed each bit into the LSB of the coefficient (rounded to int)
        for i, bit in enumerate(bitstream):
            coeff = flat_band[i]
            int_coeff = int(coeff)
            flat_band[i] = (int_coeff & ~1) | bit  # set LSB to bit

        # Rebuild modified band
        modified_band = flat_band.reshape(target_band.shape)

        # Update coefficients
        if band == 'LH':
            new_coeffs = (LL, (modified_band, HL, HH))
        else:
            new_coeffs = (LL, (LH, modified_band, HH))

        watermarked_image = pywt.idwt2(new_coeffs, 'haar')
        watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)
        logger.info("Watermark embedding complete.")

        return watermarked_image

    except Exception as e:
        logger.exception("Exception occurred during watermark embedding.")
        raise

def extract_bits_from_dwt(image_array: np.ndarray, band='LH') -> list:
    logger.info("Starting DWT watermark extraction")

    try:
        if image_array is None:
            logger.error("Input image array is None.")
            raise ValueError("Image input is missing.")

        if len(image_array.shape) != 3 or image_array.shape[2] != 3:
            logger.debug("Image is grayscale or single-channel. Proceeding as-is.")
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        coeffs2 = pywt.dwt2(image_array, 'haar')
        LL, (LH, HL, HH) = coeffs2

        band_map = {'LH': LH, 'HL': HL}
        if band not in band_map:
            logger.error(f"Invalid band selected: '{band}'. Use 'LH' or 'HL'.")
            raise ValueError("Band must be 'LH' or 'HL'")

        target_band = band_map[band]
        flat_band = target_band.flatten()
        logger.debug(f"Extracting from band: {band}, shape = {target_band.shape}, total coefficients = {flat_band.size}")

        # Extract header (first 16 bits)
        header_bits = [(int(val) & 1) for val in flat_band[:16]]
        message_length = bits_to_int(header_bits)
        logger.debug(f"Extracted message length from header: {message_length}")

        total_bits_needed = 16 + message_length
        if total_bits_needed > len(flat_band):
            logger.error("Not enough DWT coefficients to extract full message.")
            raise ValueError("Insufficient data in DWT band.")

        message_bits = [(int(val) & 1) for val in flat_band[16:16 + message_length]]
        logger.info("Watermark extraction complete.")

        return message_bits

    except Exception as e:
        logger.exception("Exception occurred during watermark extraction.")
        raise
