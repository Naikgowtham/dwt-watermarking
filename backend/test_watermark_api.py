import requests
import base64
import sys

# === CONFIGURATION ===
API_URL = "http://localhost:5000"
ORIGINAL_IMAGE_PATH = "test_image.png"  # Change to your test image path
MESSAGE = "Test watermark message"
WATERMARKED_IMAGE_PATH = "watermarked_test_image.png"

# === TEST /watermark ===
print("[TEST] Uploading image to /watermark...")
with open(ORIGINAL_IMAGE_PATH, "rb") as img_file:
    files = {"image": img_file}
    data = {"message": MESSAGE}
    resp = requests.post(f"{API_URL}/watermark", files=files, data=data)
    print("/watermark response status:", resp.status_code)
    print("/watermark response JSON:", resp.json())
    resp_json = resp.json()
    b64_img = resp_json.get("image")
    if b64_img:
        with open(WATERMARKED_IMAGE_PATH, "wb") as out_img:
            out_img.write(base64.b64decode(b64_img))
        print(f"Watermarked image saved to {WATERMARKED_IMAGE_PATH}")
    else:
        print("No watermarked image in response!")
        sys.exit(1)

# === TEST /extract ===
print("[TEST] Uploading watermarked image to /extract...")
with open(WATERMARKED_IMAGE_PATH, "rb") as img_file:
    files = {"image": img_file}
    resp = requests.post(f"{API_URL}/extract", files=files)
    print("/extract response status:", resp.status_code)
    print("/extract response JSON:", resp.json()) 