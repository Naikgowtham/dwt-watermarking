import os
from web3 import Web3
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# Connect to Alchemy Amoy
web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# Verify connection
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Polygon Amoy via Alchemy")

# Wallet info
CHAIN_ID = 80002  # Amoy testnet chain ID

print("🔗 Connected to Amoy Testnet ✅")
