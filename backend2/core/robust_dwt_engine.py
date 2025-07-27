import numpy as np
import cv2
import pywt
from utils.logger import setup_logger
import random

logger = setup_logger(__name__)

class RobustDWTWatermarkEngine:
    """
    Robust DWT-based watermarking engine
    - Embeds watermark in wavelet coefficients
    - Resistant to compression, noise, and common attacks
    - Better than LSB approach with proper coefficient selection
    """
    
    def __init__(self, wavelet='haar', level=2, alpha=15.0, seed=42):
        """
        Initialize DWT watermarking engine
        
        Args:
            wavelet: Wavelet type ('haar', 'db2', 'db4', etc.)
            level: Decomposition level (1-3 recommended)
            alpha: Embedding strength (higher = more robust but more visible)
            seed: Random seed for reproducible embedding
        """
        self.wavelet = wavelet
        self.level = level
        self.alpha = alpha
        self.seed = seed
        random.seed(seed)
        
        logger.info(f"Robust DWT Watermark Engine initialized: wavelet={wavelet}, level={level}, alpha={alpha}")
    
    def _get_robust_coefficients(self, coeffs):
        """
        Select robust coefficients for embedding
        Returns list of (subband, position) tuples
        """
        robust_positions = []
        
        # Support multi-level DWT coefficient unpacking
        # For level=2: coeffs = [LL2, (LH2, HL2, HH2), (LH1, HL1, HH1)]
        if len(coeffs) >= 3 and isinstance(coeffs[1], tuple):
            # 2-level DWT (default)
            LL2 = coeffs[0]
            (LH2, HL2, HH2) = coeffs[1]
            # Use LH2 and HL2 as robust subbands
            subbands = [('LH', LH2), ('HL', HL2)]
        elif len(coeffs) == 2 and isinstance(coeffs[1], tuple):
            # 1-level DWT
            LL, (LH, HL, HH) = coeffs
            subbands = [('LH', LH), ('HL', HL)]
        else:
            logger.warning(f"Unexpected DWT coeffs structure: {type(coeffs)}, len={len(coeffs)}")
            return robust_positions

        for subband_name, subband in subbands:
            height, width = subband.shape
            for i in range(0, height, 4):
                for j in range(0, width, 4):
                    if i < height and j < width:
                        robust_positions.append((subband_name, (i, j)))
        return robust_positions
    
    def embed_watermark(self, image, watermark_bits):
        """
        Embed watermark bits into image using robust DWT
        
        Args:
            image: Input image (RGB)
            watermark_bits: List of binary values [0, 1, 0, 1, ...]
        
        Returns:
            Watermarked image
        """
        logger.info(f"Embedding {len(watermark_bits)} bits using robust DWT watermarking")
        
        # Convert to YCbCr and work on Y channel
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        Y, Cr, Cb = cv2.split(ycrcb)
        
        # Apply DWT
        coeffs = pywt.wavedec2(Y.astype(np.float64), self.wavelet, level=self.level)
        
        # Get robust coefficient positions
        robust_positions = self._get_robust_coefficients(coeffs)
        
        if len(robust_positions) < len(watermark_bits):
            raise ValueError(f"Not enough robust positions: need {len(watermark_bits)}, got {len(robust_positions)}")
        
        # Embed watermark in robust positions
        for i, (subband, (row, col)) in enumerate(robust_positions):
            if i >= len(watermark_bits):
                break
                
            bit = watermark_bits[i]
            
            # Get the appropriate subband
            if subband == 'LH':
                coeff = coeffs[1][0]  # LH subband
            elif subband == 'HL':
                coeff = coeffs[1][1]  # HL subband
            else:
                continue
            
            # Embed bit using quantization
            current_value = coeff[row, col]
            
            if bit == 1:
                # Force to positive and above threshold
                coeff[row, col] = abs(current_value) + self.alpha
            else:
                # Force to negative or below threshold
                coeff[row, col] = -abs(current_value) - self.alpha
        
        # Apply inverse DWT
        watermarked_Y = pywt.waverec2(coeffs, self.wavelet)
        
        # Ensure values are in valid range
        watermarked_Y = np.clip(watermarked_Y, 0, 255).astype(np.uint8)
        
        # --- PATCH: Ensure all channels have the same shape before merging ---
        logger.debug(f"Shapes before merge: Y={watermarked_Y.shape}, Cr={Cr.shape}, Cb={Cb.shape}")
        target_shape = watermarked_Y.shape
        if Cr.shape != target_shape:
            logger.warning(f"Resizing Cr from {Cr.shape} to {target_shape} for merge.")
            Cr = cv2.resize(Cr, (target_shape[1], target_shape[0]), interpolation=cv2.INTER_AREA)
        if Cb.shape != target_shape:
            logger.warning(f"Resizing Cb from {Cb.shape} to {target_shape} for merge.")
            Cb = cv2.resize(Cb, (target_shape[1], target_shape[0]), interpolation=cv2.INTER_AREA)
        logger.debug(f"Shapes after resize: Y={watermarked_Y.shape}, Cr={Cr.shape}, Cb={Cb.shape}")
        # Merge channels
        merged = cv2.merge([watermarked_Y, Cr, Cb])
        watermarked_image = cv2.cvtColor(merged, cv2.COLOR_YCrCb2RGB)
        
        logger.info("Robust DWT watermark embedding completed")
        return watermarked_image
    
    def extract_watermark(self, image, bit_count):
        """
        Extract watermark bits from image
        
        Args:
            image: Watermarked image (RGB)
            bit_count: Number of bits to extract
        
        Returns:
            List of extracted bits
        """
        logger.info(f"Extracting {bit_count} bits using robust DWT watermarking")
        
        # Convert to YCbCr and work on Y channel
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        Y, _, _ = cv2.split(ycrcb)
        
        # Apply DWT
        coeffs = pywt.wavedec2(Y.astype(np.float64), self.wavelet, level=self.level)
        
        # Get robust coefficient positions
        robust_positions = self._get_robust_coefficients(coeffs)
        
        if len(robust_positions) < bit_count:
            logger.warning(f"Not enough robust positions: need {bit_count}, got {len(robust_positions)}")
            bit_count = len(robust_positions)
        
        extracted_bits = []
        
        # Extract watermark from robust positions
        for i, (subband, (row, col)) in enumerate(robust_positions):
            if i >= bit_count:
                break
                
            # Get the appropriate subband
            if subband == 'LH':
                coeff = coeffs[1][0]  # LH subband
            elif subband == 'HL':
                coeff = coeffs[1][1]  # HL subband
            else:
                continue
            
            # Extract bit using threshold
            coeff_value = coeff[row, col]
            bit = 1 if coeff_value > 0 else 0
            extracted_bits.append(bit)
        
        logger.info(f"Robust DWT watermark extraction completed: {extracted_bits[:10]}...")
        return extracted_bits
    
    def get_max_capacity(self, image):
        """Calculate maximum number of bits that can be embedded"""
        height, width = image.shape[:2]
        
        # Calculate number of robust positions
        robust_positions = self._get_robust_coefficients(None)  # Dummy call to get count
        # For simplicity, estimate based on image size
        estimated_positions = (height // 4) * (width // 4) * 2  # LH and HL subbands
        
        return min(estimated_positions, 1000)  # Cap at 1000 bits for safety

# Convenience functions for easy integration
def embed_watermark_robust_dwt(image, watermark_bits, alpha=15.0):
    """Simple function to embed watermark using robust DWT"""
    engine = RobustDWTWatermarkEngine(alpha=alpha)
    return engine.embed_watermark(image, watermark_bits)

def extract_watermark_robust_dwt(image, bit_count, alpha=15.0):
    """Simple function to extract watermark using robust DWT"""
    engine = RobustDWTWatermarkEngine(alpha=alpha)
    return engine.extract_watermark(image, bit_count) 