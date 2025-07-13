import numpy as np
import cv2
from scipy.fft import dct, idct
from utils.logger import setup_logger
import random

logger = setup_logger(__name__)

class DCTWatermarkEngine:
    """
    Robust DCT-based watermarking engine
    - Embeds watermark in DCT coefficients
    - Resistant to compression, noise, and common attacks
    - Simple to implement and very effective
    """
    
    def __init__(self, block_size=8, alpha=30.0, seed=42):
        """
        Initialize DCT watermarking engine
        
        Args:
            block_size: Size of DCT blocks (8x8 is standard)
            alpha: Embedding strength (higher = more robust but more visible)
            seed: Random seed for reproducible embedding positions
        """
        self.block_size = block_size
        self.alpha = alpha
        self.seed = seed
        random.seed(seed)
        
        # Use a single position for simplicity and reliability
        self.embed_position = (4, 4)  # Middle frequency position
        
        logger.info(f"DCT Watermark Engine initialized: block_size={block_size}, alpha={alpha}")
    
    def _get_blocks(self, image):
        """Split image into blocks"""
        height, width = image.shape
        blocks = []
        positions = []
        
        for i in range(0, height - self.block_size + 1, self.block_size):
            for j in range(0, width - self.block_size + 1, self.block_size):
                block = image[i:i+self.block_size, j:j+self.block_size]
                blocks.append(block)
                positions.append((i, j))
        
        return blocks, positions
    
    def _reconstruct_image(self, blocks, positions, original_shape):
        """Reconstruct image from blocks"""
        result = np.zeros(original_shape, dtype=np.float64)
        count = np.zeros(original_shape, dtype=np.float64)
        
        for block, (i, j) in zip(blocks, positions):
            result[i:i+self.block_size, j:j+self.block_size] += block
            count[i:i+self.block_size, j:j+self.block_size] += 1
        
        # Average overlapping regions
        count[count == 0] = 1  # Avoid division by zero
        result = result / count
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def embed_watermark(self, image, watermark_bits):
        """
        Embed watermark bits into image using DCT
        
        Args:
            image: Input image (RGB)
            watermark_bits: List of binary values [0, 1, 0, 1, ...]
        
        Returns:
            Watermarked image
        """
        logger.info(f"Embedding {len(watermark_bits)} bits using DCT watermarking")
        
        # Convert to YCbCr and work on Y channel
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        Y, Cr, Cb = cv2.split(ycrcb)
        
        # Get blocks
        blocks, positions = self._get_blocks(Y.astype(np.float64))
        
        if len(blocks) < len(watermark_bits):
            raise ValueError(f"Image too small: need {len(watermark_bits)} blocks, got {len(blocks)}")
        
        # Embed watermark
        watermarked_blocks = []
        for i, block in enumerate(blocks):
            if i < len(watermark_bits):
                # Apply DCT
                dct_block = dct(dct(block, axis=0), axis=1)
                
                # Embed bit using simple quantization
                bit = watermark_bits[i]
                current_value = dct_block[self.embed_position]
                
                if bit == 1:
                    # Force to positive and above threshold
                    dct_block[self.embed_position] = abs(current_value) + self.alpha
                else:
                    # Force to negative or below threshold
                    dct_block[self.embed_position] = -abs(current_value) - self.alpha
                
                # Apply inverse DCT
                watermarked_block = idct(idct(dct_block, axis=0), axis=1)
                watermarked_blocks.append(watermarked_block)
            else:
                watermarked_blocks.append(block)
        
        # Reconstruct Y channel
        watermarked_Y = self._reconstruct_image(watermarked_blocks, positions, Y.shape)
        
        # Merge channels
        merged = cv2.merge([watermarked_Y, Cr, Cb])
        watermarked_image = cv2.cvtColor(merged, cv2.COLOR_YCrCb2RGB)
        
        logger.info("DCT watermark embedding completed")
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
        logger.info(f"Extracting {bit_count} bits using DCT watermarking")
        
        # Convert to YCbCr and work on Y channel
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        Y, _, _ = cv2.split(ycrcb)
        
        # Get blocks
        blocks, _ = self._get_blocks(Y.astype(np.float64))
        
        if len(blocks) < bit_count:
            logger.warning(f"Image too small: need {bit_count} blocks, got {len(blocks)}")
            bit_count = len(blocks)
        
        extracted_bits = []
        
        for i in range(bit_count):
            block = blocks[i]
            
            # Apply DCT
            dct_block = dct(dct(block, axis=0), axis=1)
            
            # Extract bit using simple threshold
            coeff_value = dct_block[self.embed_position]
            bit = 1 if coeff_value > 0 else 0
            extracted_bits.append(bit)
        
        logger.info(f"DCT watermark extraction completed: {extracted_bits[:10]}...")
        return extracted_bits
    
    def get_max_capacity(self, image):
        """Calculate maximum number of bits that can be embedded"""
        height, width = image.shape[:2]
        blocks_h = height // self.block_size
        blocks_w = width // self.block_size
        return blocks_h * blocks_w

# Convenience functions for easy integration
def embed_watermark_dct(image, watermark_bits, alpha=30.0):
    """Simple function to embed watermark using DCT"""
    engine = DCTWatermarkEngine(alpha=alpha)
    return engine.embed_watermark(image, watermark_bits)

def extract_watermark_dct(image, bit_count, alpha=30.0):
    """Simple function to extract watermark using DCT"""
    engine = DCTWatermarkEngine(alpha=alpha)
    return engine.extract_watermark(image, bit_count) 