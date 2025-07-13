import cv2
import numpy as np
import base64
from utils.logger import setup_logger
from io import BytesIO

logger = setup_logger(__name__)

def load_image(file) -> np.ndarray:
    logger.debug("Attempting to load image from uploaded file...")
    try:
        if file is None:
            logger.warning("No file provided to load_image().")
            raise ValueError("No file provided.")

        image_bytes = file.read()
        if not image_bytes:
            logger.warning("Uploaded file is empty.")
            raise ValueError("Uploaded file is empty.")

        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("cv2.imdecode() returned None. Possibly unsupported format or corrupted file.")
            raise ValueError("Unable to decode image. Unsupported format or corrupted file.")

        logger.debug(f"Image successfully loaded. Shape: {image.shape}")
        return image

    except Exception as e:
        logger.exception("Exception occurred in load_image().")
        raise

def save_image(array, path: str) -> None:
    logger.debug(f"Attempting to save image to path: {path}")
    try:
        if array is None or not isinstance(array, np.ndarray):
            logger.warning("Invalid image array provided to save_image().")
            raise ValueError("Invalid image array provided.")

        success = cv2.imwrite(path, array)
        if not success:
            logger.error("cv2.imwrite() failed to write image. Check path permissions or array format.")
            raise IOError(f"Failed to write image to {path}")

        logger.debug("Image saved successfully.")

    except Exception as e:
        logger.exception("Exception occurred in save_image().")
        raise

def image_to_base64(path: str) -> str:
    logger.debug(f"Attempting to convert image to base64 from path: {path}")
    try:
        if not path:
            logger.warning("Empty path provided to image_to_base64().")
            raise ValueError("Image path is empty.")

        with open(path, "rb") as img_file:
            image_bytes = img_file.read()
            if not image_bytes:
                logger.warning("Image file is empty.")
                raise ValueError("Image file is empty.")

            base64_str = base64.b64encode(image_bytes).decode('utf-8')
            logger.debug("Image successfully encoded to base64.")
            return base64_str

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except Exception as e:
        logger.exception("Exception occurred in image_to_base64().")
        raise

def base64_to_image(base64_str: str) -> np.ndarray:
    logger.debug("Attempting to decode base64 string into image...")
    try:
        if not base64_str:
            logger.warning("No base64 string provided.")
            raise ValueError("Base64 input is empty.")

        img_data = base64.b64decode(base64_str)
        nparr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            logger.error("cv2.imdecode() failed. Possibly invalid base64 string.")
            raise ValueError("Decoded image is None — possibly invalid base64 input.")

        logger.debug(f"Image successfully decoded from base64. Shape: {image.shape}")
        return image

    except base64.binascii.Error as b64_err:
        logger.error(f"Base64 decoding error: {b64_err}")
        raise
    except Exception as e:
        logger.exception("Exception occurred in base64_to_image().")
        raise
