import os
import requests
from dotenv import load_dotenv
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)
load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

if not PINATA_API_KEY or not PINATA_SECRET_API_KEY:
    logger.error("Pinata API keys are not set in environment.")
    raise EnvironmentError("Pinata API keys are not set in environment.")

def upload_to_pinata(file_path):
    logger.info(f"Uploading {file_path} to Pinata Cloud...")
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
    }
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        cid = response.json()["IpfsHash"]
        logger.info(f"File uploaded successfully to Pinata. CID: {cid}")
        return cid
    else:
        logger.error(f"Pinata upload failed: {response.status_code}, {response.text}")
        raise RuntimeError(f"Pinata upload failed: {response.status_code}, {response.text}")
