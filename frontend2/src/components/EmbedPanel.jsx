import React, { useState } from 'react';
import axios from 'axios';

function EmbedPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState('');
  const [watermarked, setWatermarked] = useState(null);
  const [loading, setLoading] = useState(false);
  const [embedResult, setEmbedResult] = useState(null);
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setWatermarked(null);
    setEmbedResult(null);
    setError("");
  };

  const handleSubmit = async () => {
    setError("");
    if (!image || !message) {
      setError("Image and message required.");
      return;
    }

    const formData = new FormData();
    formData.append('image', image);
    formData.append('message', message);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/watermark', formData);
      setWatermarked(`data:image/png;base64,${res.data.image}`);
      setEmbedResult(res.data);
    } catch (err) {
      let msg = "Failed to embed watermark.";
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
      <h2>Embed Watermark</h2>
      {error && (
        <div style={{ color: 'red', marginBottom: '1em', fontWeight: 'bold' }}>{error}</div>
      )}
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
            <h5>Algorithm Information:</h5>
            <p><strong>Algorithm:</strong> {embedResult.algorithm || 'Robust DWT'}</p>
            <p><strong>Timestamp:</strong> {embedResult.timestamp || 'N/A'}</p>
          </div>

          <div className="result-section">
            <h5>Hash Information:</h5>
            <p><strong>Original Hash:</strong> {formatHash(embedResult.original_hash)}</p>
            <p><strong>Watermarked Hash:</strong> {formatHash(embedResult.watermarked_hash)}</p>
            <p><strong>Parent Hash:</strong> {formatHash(embedResult.parent_hash)}</p>
          </div>

          <div className="result-section">
            <h5>Embedded Messages:</h5>
            <ul style={{ textAlign: 'left', paddingLeft: '20px' }}>
              {embedResult.embedded_messages && embedResult.embedded_messages.map((msg, index) => (
                <li key={index}><strong>Message {index + 1}:</strong> {msg}</li>
              ))}
            </ul>
          </div>

          <div className="result-section">
            <h5>Next Steps:</h5>
            <ul style={{ textAlign: 'left', paddingLeft: '20px' }}>
              <li>Download the watermarked image above</li>
              <li>Use the "Extract Watermark" panel to verify the embedding</li>
              <li>The robust DWT algorithm provides better resistance to compression and noise</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default EmbedPanel;
