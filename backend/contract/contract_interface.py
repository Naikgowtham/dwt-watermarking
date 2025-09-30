# backend/contract/contract_interface.py
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Connect to Alchemy
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_URL")))
assert w3.is_connected(), "❌ Web3 is not connected"

# Load ABI
abi_path = os.path.join(os.path.dirname(__file__), "WatermarkContractABI.json")
with open(abi_path, "r") as f:
    abi = json.load(f)

# Set contract address (Amoy deployment)
contract_address = Web3.to_checksum_address("0x659796FC10ba0aa719fB42A2d7E2BeEC04F31436")

# Instantiate contract
contract = w3.eth.contract(address=contract_address, abi=abi)

print("✅ Contract interface loaded.")
