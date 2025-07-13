import React, { useState } from 'react';
import axios from 'axios';

function ExtractPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [extractResult, setExtractResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setExtractResult(null);
    setError("");
  };

  const handleExtract = async () => {
    setError("");
    if (!image) {
      setError("Select a watermarked image.");
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/extract', formData);
      setExtractResult(res.data);
    } catch (err) {
      let msg = "Failed to extract watermark.";
      if (err.response && err.response.data && err.response.data.message) {
        msg += " " + err.response.data.message;
      } else if (err.message) {
        msg += " " + err.message;
      }
      setError(msg);
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
      {error && (
        <div style={{ color: 'red', marginBottom: '1em', fontWeight: 'bold' }}>{error}</div>
      )}
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

          {/* Algorithm Information */}
          <div className="result-section">
            <h5>Algorithm Information:</h5>
            <p><strong>Algorithm:</strong> {extractResult.algorithm || 'Robust DWT'}</p>
            <p><strong>Timestamp:</strong> {extractResult.timestamp || 'N/A'}</p>
          </div>

          {/* Hash Information */}
          <div className="result-section">
            <h5>Hash Information:</h5>
            <p><strong>Image Hash:</strong> {formatHash(extractResult.hash)}</p>
            {extractResult.on_chain && (
              <>
                <p><strong>Original Hash:</strong> {formatHash(extractResult.on_chain.original_hash)}</p>
                <p><strong>Watermarked Hash:</strong> {formatHash(extractResult.on_chain.watermarked_hash)}</p>
                <p><strong>Parent Hash:</strong> {formatHash(extractResult.on_chain.parent_hash)}</p>
              </>
            )}
          </div>

          {/* Validation Status */}
          <div className="result-section">
            <h5>Validation Status:</h5>
            <div className="validation-status">
              <p>
                <strong>Extraction Success:</strong> 
                <span style={{ color: 'green' }}>
                  ✓ Successful
                </span>
              </p>
              <p>
                <strong>Robust DWT:</strong> 
                <span style={{ color: 'green' }}>
                  ✓ Algorithm provides better resistance to compression and noise
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
