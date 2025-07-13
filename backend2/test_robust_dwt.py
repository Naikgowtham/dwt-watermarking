#!/usr/bin/env python3
"""
Test script for robust DWT watermarking
Tests embedding and extraction functionality
"""

import cv2
import numpy as np
from core.robust_dwt_engine import RobustDWTWatermarkEngine
from utils.bit_utils import string_to_bits, bits_to_string
import os

def create_test_image(size=(512, 512)):
    """Create a test image with some texture"""
    # Create a gradient image with some noise for texture
    x = np.linspace(0, 255, size[1])
    y = np.linspace(0, 255, size[0])
    X, Y = np.meshgrid(x, y)
    
    # Create RGB channels
    r = X.astype(np.uint8)
    g = Y.astype(np.uint8)
    b = ((X + Y) / 2).astype(np.uint8)
    
    # Add some noise for texture
    noise = np.random.randint(0, 30, size, dtype=np.uint8)
    r = np.clip(r + noise, 0, 255)
    g = np.clip(g + noise, 0, 255)
    b = np.clip(b + noise, 0, 255)
    
    return cv2.merge([r, g, b])

def test_basic_embedding():
    """Test basic embedding and extraction"""
    print("=== Testing Basic Embedding and Extraction ===")
    
    # Create test image
    image = create_test_image()
    print(f"Created test image: {image.shape}")
    
    # Create watermark engine
    engine = RobustDWTWatermarkEngine(alpha=15.0)
    
    # Test message
    message = "Hello, this is a test watermark!"
    print(f"Test message: {message}")
    
    # Convert message to bits
    message_bits = string_to_bits(message)
    print(f"Message bits: {len(message_bits)} bits")
    
    # Embed watermark
    print("Embedding watermark...")
    watermarked_image = engine.embed_watermark(image, message_bits)
    print("Watermark embedded successfully")
    
    # Extract watermark
    print("Extracting watermark...")
    extracted_bits = engine.extract_watermark(watermarked_image, len(message_bits))
    print(f"Extracted {len(extracted_bits)} bits")
    
    # Convert bits back to string
    extracted_message = bits_to_string(extracted_bits)
    print(f"Extracted message: {extracted_message}")
    
    # Check if extraction was successful
    if extracted_message == message:
        print("✓ SUCCESS: Message extracted correctly!")
        return True
    else:
        print("✗ FAILED: Message extraction failed!")
        print(f"Expected: {message}")
        print(f"Got: {extracted_message}")
        return False

def test_compression_resistance():
    """Test resistance to JPEG compression"""
    print("\n=== Testing Compression Resistance ===")
    
    # Create test image
    image = create_test_image()
    
    # Create watermark engine
    engine = RobustDWTWatermarkEngine(alpha=20.0)  # Higher alpha for robustness
    
    # Test message
    message = "Compression test message"
    message_bits = string_to_bits(message)
    
    # Embed watermark
    watermarked_image = engine.embed_watermark(image, message_bits)
    
    # Apply JPEG compression
    print("Applying JPEG compression...")
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]  # 70% quality
    _, compressed_data = cv2.imencode('.jpg', watermarked_image, encode_param)
    compressed_image = cv2.imdecode(compressed_data, cv2.IMREAD_COLOR)
    
    # Extract from compressed image
    print("Extracting from compressed image...")
    extracted_bits = engine.extract_watermark(compressed_image, len(message_bits))
    extracted_message = bits_to_string(extracted_bits)
    
    # Check result
    if extracted_message == message:
        print("✓ SUCCESS: Message survived JPEG compression!")
        return True
    else:
        print("✗ FAILED: Message lost during compression!")
        print(f"Expected: {message}")
        print(f"Got: {extracted_message}")
        return False

def test_capacity():
    """Test embedding capacity"""
    print("\n=== Testing Embedding Capacity ===")
    
    # Create test image
    image = create_test_image()
    
    # Create watermark engine
    engine = RobustDWTWatermarkEngine()
    
    # Get maximum capacity
    max_capacity = engine.get_max_capacity(image)
    print(f"Maximum capacity: {max_capacity} bits")
    
    # Test with different message lengths
    test_messages = [
        "Short",
        "This is a medium length message for testing",
        "A" * 100,  # 100 character message
        "A" * 200   # 200 character message
    ]
    
    for msg in test_messages:
        print(f"\nTesting message length: {len(msg)} characters")
        message_bits = string_to_bits(msg)
        
        if len(message_bits) > max_capacity:
            print(f"✗ Message too long ({len(message_bits)} bits > {max_capacity} bits)")
            continue
        
        try:
            # Embed and extract
            watermarked = engine.embed_watermark(image, message_bits)
            extracted_bits = engine.extract_watermark(watermarked, len(message_bits))
            extracted_msg = bits_to_string(extracted_bits)
            
            if extracted_msg == msg:
                print(f"✓ SUCCESS: {len(msg)} characters embedded and extracted correctly")
            else:
                print(f"✗ FAILED: Extraction failed for {len(msg)} characters")
        except Exception as e:
            print(f"✗ ERROR: {e}")

def main():
    """Run all tests"""
    print("Robust DWT Watermarking Test Suite")
    print("=" * 50)
    
    # Run tests
    basic_success = test_basic_embedding()
    compression_success = test_compression_resistance()
    test_capacity()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"Basic embedding/extraction: {'✓ PASS' if basic_success else '✗ FAIL'}")
    print(f"Compression resistance: {'✓ PASS' if compression_success else '✗ FAIL'}")
    
    if basic_success and compression_success:
        print("\n🎉 All critical tests passed! Robust DWT watermarking is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main() 