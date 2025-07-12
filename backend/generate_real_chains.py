#!/usr/bin/env python3
"""
Script to generate real watermark chains from your blockchain data.
Uses the existing API endpoints to fetch and build chains.
"""

import os
import sys
import requests
import json
from datetime import datetime

def get_chain_from_api(hash_value):
    """
    Get a watermark chain from the API using a hash.
    """
    try:
        url = f"http://localhost:5000/blockchain/chain/{hash_value}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get chain for {hash_value}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching chain for {hash_value}: {e}")
        return None

def get_watermark_from_api(hash_value):
    """
    Get a specific watermark from the API.
    """
    try:
        url = "http://localhost:5000/get_watermark"
        data = {"original_hash": hash_value}
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get watermark for {hash_value}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching watermark for {hash_value}: {e}")
        return None

def build_chain_from_entries(entries):
    """
    Build a chain string from watermark entries.
    """
    if not entries:
        return None
    
    # Extract hashes in order (entries are in reverse order from API)
    hashes = []
    for entry in reversed(entries):
        if entry and "original_hash" in entry:
            hashes.append(entry["original_hash"])
    
    if len(hashes) == 1:
        return hashes[0]
    else:
        return "->".join(hashes)

def generate_real_chain_file(known_hashes=None, output_file="real_watermark_chains.txt"):
    """
    Generate a chain file from real blockchain data.
    """
    if known_hashes is None:
        # Add your known watermark hashes here
        known_hashes = [
            # Example hashes - replace with your actual hashes
            # "your_actual_hash_here",
            # "another_hash_here",
        ]
    
    if not known_hashes:
        print("⚠️  No known hashes provided. Please add some hashes to known_hashes list.")
        return None
    
    print(f"🔗 Generating real chain file from {len(known_hashes)} known hashes...")
    
    chains = []
    successful_chains = 0
    
    for i, hash_value in enumerate(known_hashes, 1):
        print(f"\n📋 Processing hash {i}/{len(known_hashes)}: {hash_value[:16]}...")
        
        # Get the chain for this hash
        chain_entries = get_chain_from_api(hash_value)
        
        if chain_entries:
            chain_str = build_chain_from_entries(chain_entries)
            if chain_str:
                chains.append(f"{successful_chains + 1}){chain_str}")
                successful_chains += 1
                print(f"✅ Chain {successful_chains}: {len(chain_entries)} entries")
            else:
                print(f"⚠️  No valid chain data for {hash_value}")
        else:
            print(f"❌ No chain found for {hash_value}")
    
    # Write to file
    try:
        with open(output_file, 'w') as f:
            f.write("Real Watermark Chains from Blockchain\n")
            f.write("=" * 50 + "\n\n")
            f.write("Format: chain_number)hash1->hash2->hash3...\n")
            f.write("Note: Single hashes represent genesis watermarks\n\n")
            
            for chain in chains:
                f.write(chain + "\n")
            
            f.write(f"\nTotal chains: {len(chains)}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source: Polygon Amoy Testnet\n")
        
        print(f"\n✅ Real chain file generated: {output_file}")
        print(f"📊 Total chains: {len(chains)}")
        
        # Print chains to console
        print("\n📋 Generated Chains:")
        print("=" * 50)
        for chain in chains:
            print(chain)
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return None

def scan_for_genesis_watermarks():
    """
    Try to find genesis watermarks by scanning common patterns.
    This is a basic approach - you might want to implement a more sophisticated scanner.
    """
    print("🔍 Scanning for genesis watermarks...")
    
    # This is a very basic approach - in reality, you'd need:
    # 1. A database of all watermarks
    # 2. Event scanning from the blockchain
    # 3. Or maintain a list of known watermarks
    
    genesis_hashes = []
    
    # You can add some known genesis hashes here
    # genesis_hashes = [
    #     "your_known_genesis_hash_1",
    #     "your_known_genesis_hash_2",
    # ]
    
    if not genesis_hashes:
        print("⚠️  No genesis hashes found. Please add known hashes manually.")
    
    return genesis_hashes

def main():
    """
    Main function to generate real chain file.
    """
    print("🔗 Real Watermark Chain Generator")
    print("=" * 40)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print("✅ Backend is running")
    except:
        print("❌ Backend is not running. Please start the Flask server first.")
        print("   Run: cd backend && python app.py")
        return
    
    # Option 1: Use known hashes
    print("\n1. Using known hashes...")
    
    # Add your known watermark hashes here
    known_hashes = [
        # Replace these with your actual watermark hashes
        # "your_actual_hash_1",
        # "your_actual_hash_2",
    ]
    
    if known_hashes:
        generate_real_chain_file(known_hashes, "watermark_chains_known.txt")
    else:
        print("⚠️  No known hashes provided. Please add some hashes to the known_hashes list.")
    
    # Option 2: Try to scan for genesis watermarks
    print("\n2. Scanning for genesis watermarks...")
    genesis_hashes = scan_for_genesis_watermarks()
    
    if genesis_hashes:
        generate_real_chain_file(genesis_hashes, "watermark_chains_genesis.txt")
    
    print("\n📝 To get real data:")
    print("1. Add your actual watermark hashes to the known_hashes list")
    print("2. Or implement a proper scanner for all blockchain events")
    print("3. Or maintain a database of all watermarks")

if __name__ == "__main__":
    main() 