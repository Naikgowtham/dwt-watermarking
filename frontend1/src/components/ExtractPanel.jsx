import React, { useState } from 'react';
import axios from 'axios';

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
      const res = await axios.post('http://localhost:5000/extract', formData);
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

          {/* DCT Algorithm Information */}
          <div className="result-section">
            <h5>DCT Algorithm Information:</h5>
            <p><strong>Algorithm:</strong> {extractResult.algorithm || 'DCT'}</p>
            <p><strong>Format Type:</strong> {extractResult.format || 'Unknown'}</p>
            <p><strong>Extraction Method:</strong> DCT coefficient analysis</p>
          </div>

          {/* Validation Status */}
          <div className="result-section">
            <h5>DCT Validation Status:</h5>
            <div className="validation-status">
              <p>
                <strong>DCT Extraction:</strong> 
                <span style={{ color: 'green' }}>
                  ✓ Successful
                </span>
              </p>
              <p>
                <strong>Message Integrity:</strong> 
                <span style={{ color: extractResult.messages && extractResult.messages.length > 0 ? 'green' : 'orange' }}>
                  {extractResult.messages && extractResult.messages.length > 0 ? '✓ Valid' : '⚠ No Messages'}
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
