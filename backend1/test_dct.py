#!/usr/bin/env python3
"""
Test script for DCT watermarking engine
"""

import numpy as np
import cv2
from core.dct_engine import DCTWatermarkEngine
from utils.bit_utils import string_to_bits, bits_to_string
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_test_image(width=256, height=256):
    """Create a simple test image"""
    # Create a gradient image
    x = np.linspace(0, 255, width)
    y = np.linspace(0, 255, height)
    X, Y = np.meshgrid(x, y)
    
    # Create RGB channels
    r = X.astype(np.uint8)
    g = Y.astype(np.uint8)
    b = ((X + Y) / 2).astype(np.uint8)
    
    image = cv2.merge([r, g, b])
    return image

def test_dct_watermarking():
    """Test the DCT watermarking functionality"""
    logger.info("Starting DCT watermarking test...")
    
    # Create test image
    test_image = create_test_image(256, 256)
    logger.info(f"Created test image: {test_image.shape}")
    
    # Create DCT engine
    engine = DCTWatermarkEngine(alpha=20.0)
    logger.info("DCT engine initialized")
    
    # Test message
    test_message = "Hello DCT Watermarking!"
    message_bits = string_to_bits(test_message)
    logger.info(f"Test message: '{test_message}' ({len(message_bits)} bits)")
    
    # Check capacity
    max_capacity = engine.get_max_capacity(test_image)
    logger.info(f"Maximum capacity: {max_capacity} bits")
    
    if len(message_bits) > max_capacity:
        logger.error(f"Message too long: {len(message_bits)} > {max_capacity}")
        return False
    
    # Embed watermark
    logger.info("Embedding watermark...")
    watermarked_image = engine.embed_watermark(test_image, message_bits)
    logger.info("Watermark embedded successfully")
    
    # Extract watermark
    logger.info("Extracting watermark...")
    extracted_bits = engine.extract_watermark(watermarked_image, len(message_bits))
    logger.info(f"Extracted {len(extracted_bits)} bits")
    
    # Compare original and extracted
    if len(extracted_bits) >= len(message_bits):
        extracted_message = bits_to_string(extracted_bits[:len(message_bits)])
        logger.info(f"Extracted message: '{extracted_message}'")
        
        if extracted_message == test_message:
            logger.info("✅ Test PASSED: Message extracted correctly!")
            return True
        else:
            logger.error(f"❌ Test FAILED: Message mismatch!")
            logger.error(f"Original: '{test_message}'")
            logger.error(f"Extracted: '{extracted_message}'")
            return False
    else:
        logger.error(f"❌ Test FAILED: Not enough bits extracted!")
        return False

def test_compression_resistance():
    """Test resistance to JPEG compression"""
    logger.info("Testing compression resistance...")
    
    # Create test image and embed watermark
    test_image = create_test_image(512, 512)
    engine = DCTWatermarkEngine(alpha=25.0)  # Higher alpha for robustness
    test_message = "Compression Test Message"
    message_bits = string_to_bits(test_message)
    
    # Embed watermark
    watermarked_image = engine.embed_watermark(test_image, message_bits)
    
    # Apply JPEG compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]  # 70% quality
    _, compressed_data = cv2.imencode('.jpg', watermarked_image, encode_param)
    compressed_image = cv2.imdecode(compressed_data, cv2.IMREAD_COLOR)
    
    # Extract from compressed image
    extracted_bits = engine.extract_watermark(compressed_image, len(message_bits))
    
    if len(extracted_bits) >= len(message_bits):
        extracted_message = bits_to_string(extracted_bits[:len(message_bits)])
        if extracted_message == test_message:
            logger.info("✅ Compression resistance test PASSED!")
            return True
        else:
            logger.error(f"❌ Compression resistance test FAILED!")
            logger.error(f"Original: '{test_message}'")
            logger.error(f"Extracted: '{extracted_message}'")
            return False
    else:
        logger.error("❌ Compression resistance test FAILED: Not enough bits extracted!")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("DCT Watermarking Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Basic functionality
    test1_passed = test_dct_watermarking()
    
    # Test 2: Compression resistance
    test2_passed = test_compression_resistance()
    
    # Summary
    logger.info("=" * 50)
    logger.info("Test Results Summary:")
    logger.info(f"Basic Functionality: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    logger.info(f"Compression Resistance: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        logger.info("🎉 All tests PASSED! DCT watermarking is working correctly.")
    else:
        logger.error("💥 Some tests FAILED! Please check the implementation.")
    
    logger.info("=" * 50)

if __name__ == "__main__":
    main() 