import os
import logging
from web3 import Web3
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

logger = logging.getLogger("blockchain_utils.store_watermark_on_chain")

# Load ABI and contract
ABI_PATH = os.path.join(os.path.dirname(__file__), '../contract/WatermarkContractABI.json')
CONTRACT_ADDRESS = Web3.to_checksum_address("0x659796FC10ba0aa719fB42A2d7E2BeEC04F31436")

with open(ABI_PATH, 'r') as f:
    abi = json.load(f)

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


def store_watermark_on_chain(
    original_hash: bytes,
    watermarked_hash: bytes,
    watermark_data: str,
    original_cid: str,
    watermarked_cid: str,
    crc: int,  # uint16
    parent_hash: bytes
) -> str:
    """
    Calls the storeWatermark method on the contract and returns the transaction hash.
    """
    try:
        # Nonce management
        nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS, 'pending')
        logger.info(f"Using nonce: {nonce}")

        # Build transaction
        txn = contract.functions.storeWatermark(
            original_hash,
            watermarked_hash,
            watermark_data,
            original_cid,
            watermarked_cid,
            int(crc),
            parent_hash
        )

        # Gas estimation
        try:
            gas_estimate = txn.estimate_gas({'from': PUBLIC_ADDRESS})
        except Exception as e:
            logger.warning(f"Gas estimation failed, using default gas: {e}")
            gas_estimate = 300000
        gas_price = w3.eth.gas_price
        logger.info(f"Gas estimate: {gas_estimate}, Gas price: {w3.from_wei(gas_price, 'gwei')} gwei")

        # Build transaction dict
        tx = txn.build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': nonce,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'chainId': 80002  # Polygon Amoy
        })

        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = w3.to_hex(tx_hash)
        logger.info(f"Transaction sent. Hash: {tx_hash_hex}")
        print(f"Transaction sent. Hash: {tx_hash_hex}")

        # Wait for receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        logger.info(f"Transaction mined in block {receipt.blockNumber} with status {receipt.status}")
        print(f"Transaction mined in block {receipt.blockNumber} with status {receipt.status}")
        return tx_hash_hex
    except Exception as e:
        logger.error(f"Error in store_watermark_on_chain: {e}", exc_info=True)
        print(f"Error in store_watermark_on_chain: {e}")
        return None

def get_watermark_from_chain(parent_hash):
    """
    Fetch watermark metadata from the blockchain contract using getWatermark.
    Returns a dict with all fields, or None on failure.
    """
    try:
        # Convert hex string to bytes32
        if isinstance(parent_hash, str):
            parent_hash_bytes = bytes.fromhex(parent_hash)
        else:
            parent_hash_bytes = parent_hash
        entry = contract.functions.getWatermark(parent_hash_bytes).call()
        # Check if entry is empty (all bytes32 fields are zero)
        if not entry or (hasattr(entry[0], 'hex') and entry[0] == b'\x00' * 32):
            logger.warning("No watermark entry found for given hash.")
            return None
        result = {
            "original_hash": entry[0].hex() if hasattr(entry[0], 'hex') else str(entry[0]),
            "watermarked_hash": entry[1].hex() if hasattr(entry[1], 'hex') else str(entry[1]),
            "watermark_data": entry[2],
            "original_cid": entry[3],
            "watermarked_cid": entry[4],
            "crc": entry[5],
            "parent_hash": entry[6].hex() if hasattr(entry[6], 'hex') else str(entry[6]),
        }
        logger.info(f"Fetched watermark from chain: {result}")
        return result
    except Exception as e:
        logger.error(f"Error fetching watermark from chain: {e}", exc_info=True)
        return None

def get_all_watermark_logs():
    """
    Get all watermark entries from the blockchain.
    Returns a list of watermark metadata dictionaries.
    """
    try:
        # Get all watermark entries from the contract
        # Note: This is a simplified implementation. In a real scenario,
        # you might need to scan events or maintain a separate database
        logs = []
        
        # For now, we'll return an empty list since the contract doesn't have
        # a direct method to get all entries. In a production system, you would:
        # 1. Scan WatermarkStored events from the contract
        # 2. Maintain a database of all watermarks
        # 3. Or implement a method in the contract to return all entries
        
        logger.info("Retrieved 0 watermark logs (functionality not fully implemented)")
        return logs
        
    except Exception as e:
        logger.error(f"Error fetching all watermark logs: {e}", exc_info=True)
        return []

def get_watermark_chain(parent_hash):
    """
    Get the complete chain of watermarks starting from a given parent hash.
    Returns a list of watermark entries in chain order.
    """
    try:
        chain = []
        current_hash = parent_hash
        
        # Follow the chain by following parent_hash references
        max_iterations = 100  # Prevent infinite loops
        iteration = 0
        
        while current_hash and iteration < max_iterations:
            entry = get_watermark_from_chain(current_hash)
            if entry:
                chain.append(entry)
                # Move to the parent hash
                current_hash = entry.get("parent_hash")
                if current_hash == "0" * 64:  # Genesis watermark
                    break
            else:
                break
            iteration += 1
        
        logger.info(f"Retrieved watermark chain with {len(chain)} entries")
        return chain
        
    except Exception as e:
        logger.error(f"Error fetching watermark chain: {e}", exc_info=True)
        return []

# Blockchain logic for watermarking is now handled by store_watermark_on_chain.
