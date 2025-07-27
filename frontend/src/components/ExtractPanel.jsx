import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';

function ExtractPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [extractResult, setExtractResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setExtractResult(null);
  };

  const handleExtract = async () => {
    if (!image) return alert("Select a watermarked image.");

    const formData = new FormData();
    formData.append('image', image);

    setLoading(true);
    try {
      const res = await axios.post(config.ENDPOINTS.EXTRACT, formData);
      setExtractResult(res.data);
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatHash = (hash) => {
    if (!hash) return 'N/A';
    return `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}`;
  };

  return (
    <div className="panel">
      <h2>Extract Watermark</h2>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {preview && <img src={preview} alt="Watermarked Preview" className="preview" />}
      <button onClick={handleExtract} disabled={loading}>
        {loading ? "Extracting..." : "Extract"}
      </button>
      
      {extractResult && (
        <div className="extract-results">
          <h4>Extraction Results:</h4>
          
          {/* Messages */}
          <div className="result-section">
            <h5>Extracted Messages ({extractResult.messages?.length || 0}):</h5>
            {extractResult.messages && extractResult.messages.length > 0 ? (
              <textarea 
                readOnly 
                value={extractResult.messages.join('\n')} 
                rows={4} 
                style={{ width: '100%' }} 
              />
            ) : (
              <p>No messages found</p>
            )}
          </div>

          {/* Hash Information */}
          <div className="result-section">
            <h5>Image Hash:</h5>
            <p>{formatHash(extractResult.hash)}</p>
          </div>

          {/* Format Information */}
          <div className="result-section">
            <h5>Watermark Format:</h5>
            <p>{extractResult.format || 'Unknown'}</p>
          </div>

          {/* Blockchain Information */}
          {extractResult.on_chain && (
            <div className="result-section">
              <h5>Blockchain Information:</h5>
              <div className="blockchain-info">
                <p><strong>Original Hash:</strong> {formatHash(extractResult.on_chain.original_hash)}</p>
                <p><strong>Watermarked Hash:</strong> {formatHash(extractResult.on_chain.watermarked_hash)}</p>
                <p><strong>Parent Hash:</strong> {formatHash(extractResult.on_chain.parent_hash)}</p>
                <p><strong>Original CID:</strong> {extractResult.on_chain.original_cid || 'N/A'}</p>
                <p><strong>Watermarked CID:</strong> {extractResult.on_chain.watermarked_cid || 'N/A'}</p>
                <p><strong>CRC:</strong> {extractResult.on_chain.crc || 'N/A'}</p>
              </div>
            </div>
          )}

          {/* Validation Status */}
          <div className="result-section">
            <h5>Validation Status:</h5>
            <div className="validation-status">
              <p>
                <strong>CRC Match:</strong> 
                <span style={{ color: extractResult.crc_match ? 'green' : 'red' }}>
                  {extractResult.crc_match ? '✓ Valid' : '✗ Invalid'}
                </span>
              </p>
              <p>
                <strong>On Blockchain:</strong> 
                <span style={{ color: extractResult.on_chain ? 'green' : 'orange' }}>
                  {extractResult.on_chain ? '✓ Found' : '⚠ Not Found'}
                </span>
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ExtractPanel;
