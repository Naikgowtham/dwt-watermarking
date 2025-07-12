#!/usr/bin/env python3
import requests
import os

def test_extract():
    # Test the extract endpoint with the existing watermarked image
    image_path = "uploads/watermarked/d13a5181737844049f329a7171b4f7f7_wm.png"
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return
    
    print("Testing extract functionality...")
    print(f"Using image: {image_path}")
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {"image": img_file}
            response = requests.post("http://localhost:5000/extract", files=files)
            
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Extract response:")
            print(f"  Messages: {data.get('messages', [])}")
            print(f"  Hash: {data.get('hash', 'None')}")
            print(f"  Format: {data.get('format', 'None')}")
            print(f"  CRC Match: {data.get('crc_match', False)}")
            print(f"  On Chain: {data.get('on_chain', 'None')}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_extract() 