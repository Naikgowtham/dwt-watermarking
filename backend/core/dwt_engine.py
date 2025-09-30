import numpy as np
import pywt
import cv2
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# -----------------------------------
# 🔧 Parity-Based Embedding in Y
# -----------------------------------
def embed_bits_into_y_parity(Y_channel: np.ndarray, bitstream: list[int]) -> np.ndarray:
    flat = Y_channel.flatten()
    if len(bitstream) > len(flat):
        raise ValueError("Bitstream too long for Y channel")

    for i, bit in enumerate(bitstream):
        val = flat[i]
        if bit == 0:
            flat[i] = val - (val % 2)  # force even
        else:
            flat[i] = val - (val % 2) + 1  # force odd

    # ✅ Parity verification
    recovered = [int(val % 2) for val in flat[:len(bitstream)]]
    mismatches = sum(a != b for a, b in zip(recovered, bitstream))
    logger.debug(f"Y-parity embed check: {len(bitstream)} bits embedded, {mismatches} mismatches")

    return flat.reshape(Y_channel.shape)

# -----------------------------------
# 🔧 Parity-Based Extraction from Y
# -----------------------------------
def extract_bits_from_y_parity(Y_channel: np.ndarray, bit_count: int) -> list[int]:
    flat = Y_channel.flatten()
    return [int(val % 2) for val in flat[:bit_count]]

# -----------------------------------
# 📥 Embed bits in Y after DWT-IDWT
# -----------------------------------
def embed_bits_in_dwt(image_rgb: np.ndarray, bitstream: list[int]) -> np.ndarray:
    ycrcb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb)

    # DWT-IDWT simulation (to simulate compression effects if needed later)
    LL, (LH, HL, HH) = pywt.dwt2(Y, 'haar')
    coeffs = (LL, (LH, HL, HH))
    recovered_Y = pywt.idwt2(coeffs, 'haar')
    recovered_Y = np.clip(np.round(recovered_Y), 0, 255).astype(np.uint8)

    logger.debug(f"Embedding {len(bitstream)} bits in Y channel parity")
    modified_Y = embed_bits_into_y_parity(recovered_Y, bitstream)

    # --- PATCH: Ensure all channels have the same shape and dtype ---
    if modified_Y.shape != Cr.shape:
        logger.warning(f"Resizing Cr from {Cr.shape} to {modified_Y.shape}")
        Cr = cv2.resize(Cr, (modified_Y.shape[1], modified_Y.shape[0]), interpolation=cv2.INTER_NEAREST)
    if modified_Y.shape != Cb.shape:
        logger.warning(f"Resizing Cb from {Cb.shape} to {modified_Y.shape}")
        Cb = cv2.resize(Cb, (modified_Y.shape[1], modified_Y.shape[0]), interpolation=cv2.INTER_NEAREST)
    # Ensure dtype matches
    if Cr.dtype != modified_Y.dtype:
        logger.warning(f"Casting Cr from {Cr.dtype} to {modified_Y.dtype}")
        Cr = Cr.astype(modified_Y.dtype)
    if Cb.dtype != modified_Y.dtype:
        logger.warning(f"Casting Cb from {Cb.dtype} to {modified_Y.dtype}")
        Cb = Cb.astype(modified_Y.dtype)
    # --- END PATCH ---How dwt works

    merged = cv2.merge([modified_Y, Cr, Cb])
    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2RGB)

# -----------------------------------
# 📤 Extract bits from Y channel parity
# -----------------------------------
def extract_bits_from_dwt(image_rgb: np.ndarray) -> list[int]:
    ycrcb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb)
    Y, _, _ = cv2.split(ycrcb)

    flat = Y.flatten()
    bits = [int(val % 2) for val in flat]

    logger.debug(f"Extracted first 32 bits: {bits[:32]}")
    logger.debug(f"Total bits extracted: {len(bits)}")
    return bits
