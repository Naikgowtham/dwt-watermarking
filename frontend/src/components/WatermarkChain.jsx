import React, { useState, useEffect } from 'react';
import axios from 'axios';

function WatermarkChain() {
  const [chain, setChain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchHash, setSearchHash] = useState('');
  const [currentHash, setCurrentHash] = useState('');

  const fetchChain = async (hash) => {
    if (!hash) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:5000/blockchain/chain/${hash}`);
      setChain(response.data);
      setCurrentHash(hash);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
      setChain([]);
    } finally {
      setLoading(false);
    }
  };

  const formatHash = (hash) => {
    if (!hash) return 'N/A';
    return `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}`;
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp * 1000).toLocaleString();
  };

  const isGenesis = (parentHash) => {
    return parentHash === '0' * 64 || parentHash === '0000000000000000000000000000000000000000000000000000000000000000';
  };

  return (
    <div className="watermark-chain">
      <h2>Watermark Chain Visualization</h2>
      
      {/* Search Section */}
      <div className="search-section">
        <h3>Search Chain by Hash</h3>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <input
            type="text"
            placeholder="Enter watermark hash to trace chain..."
            value={searchHash}
            onChange={(e) => setSearchHash(e.target.value)}
            style={{ flex: 1, padding: '8px' }}
          />
          <button 
            onClick={() => fetchChain(searchHash)}
            disabled={!searchHash || loading}
          >
            {loading ? 'Loading...' : 'Trace Chain'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          Error: {error}
        </div>
      )}

      {/* Chain Display */}
      {chain.length > 0 && (
        <div className="chain-display">
          <h3>Chain Results ({chain.length} entries)</h3>
          <p>Starting from: {formatHash(currentHash)}</p>
          
          <div className="chain-timeline">
            {chain.map((entry, index) => (
              <div key={index} className="chain-entry">
                <div className="entry-header">
                  <span className="entry-number">#{chain.length - index}</span>
                  <span className="entry-type">
                    {isGenesis(entry.parent_hash) ? 'Genesis' : 'Chained'}
                  </span>
                </div>
                
                <div className="entry-content">
                  <div className="hash-info">
                    <p><strong>Original Hash:</strong> {formatHash(entry.original_hash)}</p>
                    <p><strong>Watermarked Hash:</strong> {formatHash(entry.watermarked_hash)}</p>
                    <p><strong>Parent Hash:</strong> {formatHash(entry.parent_hash)}</p>
                  </div>
                  
                  <div className="metadata-info">
                    <p><strong>Watermark Data:</strong> {entry.watermark_data || 'N/A'}</p>
                    <p><strong>CRC:</strong> {entry.crc || 'N/A'}</p>
                    <p><strong>Original CID:</strong> {entry.original_cid || 'N/A'}</p>
                    <p><strong>Watermarked CID:</strong> {entry.watermarked_cid || 'N/A'}</p>
                  </div>
                </div>
                
                {index < chain.length - 1 && (
                  <div className="chain-arrow">↓</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Results */}
      {!loading && chain.length === 0 && !error && currentHash && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <p>No chain found for hash: {formatHash(currentHash)}</p>
          <p>This might be a genesis watermark or the hash doesn't exist on the blockchain.</p>
        </div>
      )}

      {/* Instructions */}
      {!currentHash && (
        <div className="instructions">
          <h3>How to use:</h3>
          <ol>
            <li>Enter a watermark hash in the search box above</li>
            <li>Click "Trace Chain" to see the complete chain of watermarks</li>
            <li>The chain will show all parent watermarks up to the genesis</li>
            <li>Each entry shows the original and watermarked image hashes, metadata, and IPFS CIDs</li>
          </ol>
        </div>
      )}
    </div>
  );
}

export default WatermarkChain; 