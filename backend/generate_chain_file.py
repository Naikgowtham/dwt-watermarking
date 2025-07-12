#!/usr/bin/env python3
"""
Script to generate a text file containing all watermark hashes in chain format.
Format: 1)hash1->hash2->hash3 (for same chain)
        2)hash1->hash2 (for different chain)
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.blockchain_utils import get_watermark_from_chain, get_all_watermark_logs
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_all_watermark_hashes():
    """
    Get all watermark hashes from the blockchain.
    Since get_all_watermark_logs() is not fully implemented,
    we'll need to scan through known hashes or implement a different approach.
    """
    # For now, we'll use a placeholder approach
    # In a real implementation, you would:
    # 1. Scan blockchain events
    # 2. Maintain a database of all watermarks
    # 3. Or implement a method to get all entries
    
    logger.info("Scanning for watermark hashes...")
    
    # This is a placeholder - you'll need to implement based on your data
    # For demonstration, we'll create some sample chains
    sample_chains = [
        # Chain 1
        [
            "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456"
        ],
        # Chain 2
        [
            "1111111111111111111111111111111111111111111111111111111111111111",
            "2222222222222222222222222222222222222222222222222222222222222222"
        ],
        # Chain 3 (single watermark)
        [
            "3333333333333333333333333333333333333333333333333333333333333333"
        ]
    ]
    
    return sample_chains

def build_chains_from_hashes(hashes_list):
    """
    Build chains from a list of hash lists.
    Each sublist represents a chain.
    """
    chains = []
    
    for i, hash_chain in enumerate(hashes_list, 1):
        if len(hash_chain) == 1:
            # Single watermark (no chain)
            chain_str = f"{i}){hash_chain[0]}"
        else:
            # Multiple watermarks in chain
            chain_str = f"{i}){'->'.join(hash_chain)}"
        
        chains.append(chain_str)
    
    return chains

def generate_chain_file(output_file="watermark_chains.txt"):
    """
    Generate a text file containing all watermark chains.
    """
    try:
        logger.info(f"Generating chain file: {output_file}")
        
        # Get all watermark hashes (placeholder implementation)
        hash_chains = get_all_watermark_hashes()
        
        # Build chain strings
        chains = build_chains_from_hashes(hash_chains)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write("Watermark Chains\n")
            f.write("=" * 50 + "\n\n")
            f.write("Format: chain_number)hash1->hash2->hash3...\n")
            f.write("Note: Single hashes represent genesis watermarks\n\n")
            
            for chain in chains:
                f.write(chain + "\n")
            
            f.write(f"\nTotal chains: {len(chains)}\n")
            f.write(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        logger.info(f"Chain file generated successfully: {output_file}")
        logger.info(f"Total chains written: {len(chains)}")
        
        # Print to console as well
        print(f"\nGenerated {output_file}:")
        print("=" * 50)
        for chain in chains:
            print(chain)
        print(f"\nTotal chains: {len(chains)}")
        
        return output_file
        
    except Exception as e:
        logger.error(f"Error generating chain file: {e}")
        print(f"Error: {e}")
        return None

def scan_real_blockchain_data():
    """
    Attempt to scan real blockchain data for watermarks.
    This is a more realistic approach but requires known starting points.
    """
    logger.info("Scanning real blockchain data...")
    
    # You would need to implement this based on your specific needs
    # Here are some approaches:
    
    # 1. Start with known genesis watermarks
    known_genesis_hashes = [
        # Add your known genesis watermark hashes here
        # "your_genesis_hash_here",
    ]
    
    # 2. Scan through a range of possible hashes (not recommended for production)
    # This is just for demonstration
    chains = []
    chain_id = 1
    
    for genesis_hash in known_genesis_hashes:
        try:
            # Build chain starting from genesis
            chain_hashes = [genesis_hash]
            current_hash = genesis_hash
            
            # Follow the chain
            max_iterations = 100
            for _ in range(max_iterations):
                entry = get_watermark_from_chain(current_hash)
                if entry and entry.get("parent_hash") != "0" * 64:
                    parent_hash = entry.get("parent_hash")
                    chain_hashes.append(parent_hash)
                    current_hash = parent_hash
                else:
                    break
            
            # Add chain to results
            if len(chain_hashes) == 1:
                chains.append(f"{chain_id}){chain_hashes[0]}")
            else:
                chains.append(f"{chain_id}){'->'.join(chain_hashes)}")
            
            chain_id += 1
            
        except Exception as e:
            logger.warning(f"Error processing genesis hash {genesis_hash}: {e}")
            continue
    
    return chains

def main():
    """
    Main function to generate the chain file.
    """
    print("🔗 Watermark Chain File Generator")
    print("=" * 40)
    
    # Option 1: Generate with sample data (for testing)
    print("\n1. Generating with sample data...")
    output_file = generate_chain_file("watermark_chains_sample.txt")
    
    if output_file:
        print(f"✅ Sample chain file created: {output_file}")
    
    # Option 2: Try to scan real blockchain data
    print("\n2. Attempting to scan real blockchain data...")
    try:
        real_chains = scan_real_blockchain_data()
        if real_chains:
            with open("watermark_chains_real.txt", 'w') as f:
                f.write("Real Blockchain Watermark Chains\n")
                f.write("=" * 50 + "\n\n")
                for chain in real_chains:
                    f.write(chain + "\n")
            print("✅ Real blockchain chain file created: watermark_chains_real.txt")
        else:
            print("⚠️  No real blockchain data found. Add known genesis hashes to scan_real_blockchain_data()")
    except Exception as e:
        print(f"❌ Error scanning blockchain: {e}")
    
    print("\n📝 To get real data, you need to:")
    print("1. Add known genesis watermark hashes to scan_real_blockchain_data()")
    print("2. Or implement get_all_watermark_logs() to scan all events")
    print("3. Or maintain a database of all watermarks")

if __name__ == "__main__":
    main() 