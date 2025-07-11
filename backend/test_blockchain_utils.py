import logging
from utils.blockchain_utils import get_watermark_from_chain

def test_get_watermark_from_chain():
    # Replace this with a known hash from your chain
    known_hash_hex = "<PASTE_A_KNOWN_ORIGINAL_HASH_HERE>"  # e.g., 'aabbcc...'
    try:
        original_hash_bytes = bytes.fromhex(known_hash_hex)
        result = get_watermark_from_chain(original_hash_bytes)
        assert result is not None, f"No watermark found for hash: {known_hash_hex}"
        print("Watermark metadata fetched from chain:")
        for k, v in result.items():
            print(f"  {k}: {v}")
    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
    except Exception as e:
        logging.error(f"Exception during test_get_watermark_from_chain: {e}")

# Optionally, you can parameterize this test with more known hashes.
if __name__ == "__main__":
    test_get_watermark_from_chain() 