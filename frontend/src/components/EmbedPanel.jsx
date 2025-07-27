import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';

function EmbedPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState('');
  const [watermarked, setWatermarked] = useState(null);
  const [loading, setLoading] = useState(false);
  const [embedResult, setEmbedResult] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setWatermarked(null);
    setEmbedResult(null);
  };

  const handleSubmit = async () => {
    if (!image || !message) return alert("Image and message required.");

    const formData = new FormData();
    formData.append('image', image);
    formData.append('message', message);

    setLoading(true);
    try {
      const res = await axios.post(config.ENDPOINTS.WATERMARK, formData);
      setWatermarked(`data:image/png;base64,${res.data.image}`);
      setEmbedResult(res.data);
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
      <h2>Embed Watermark</h2>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {preview && <img src={preview} alt="Preview" className="preview" />}
      <textarea placeholder="Enter message" value={message} onChange={e => setMessage(e.target.value)} rows={4} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Watermark"}
      </button>
      
      {watermarked && (
        <>
          <h4>Watermarked Image:</h4>
          <img src={watermarked} alt="Watermarked" />
        </>
      )}

      {embedResult && (
        <div className="embed-results">
          <h4>Embedding Results:</h4>
          
          <div className="result-section">
            <h5>File Information:</h5>
            <p><strong>Original Filename:</strong> {embedResult.original_filename}</p>
            <p><strong>Watermarked Filename:</strong> {embedResult.watermarked_filename}</p>
          </div>

          <div className="result-section">
            <h5>IPFS Storage:</h5>
            <p><strong>Original CID:</strong> {embedResult.original_cid || 'N/A'}</p>
            <p><strong>Watermarked CID:</strong> {embedResult.watermarked_cid || 'N/A'}</p>
          </div>

          <div className="result-section">
            <h5>Chain Status:</h5>
            <p style={{ color: 'green' }}>
              ✓ Watermark successfully embedded and logged to blockchain
            </p>
            <p>
              <strong>Note:</strong> The system automatically detects if this is a new watermark 
              (genesis) or chains to an existing watermark in the image.
            </p>
          </div>

          <div className="result-section">
            <h5>Next Steps:</h5>
            <ul style={{ textAlign: 'left', paddingLeft: '20px' }}>
              <li>Download the watermarked image above</li>
              <li>Use the "Extract Watermark" panel to verify the embedding</li>
              <li>Check the "Watermark Chain" page to see the complete chain</li>
              <li>View "Blockchain Logs" for detailed transaction information</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default EmbedPanel;
