import React, { useState } from 'react';
import axios from 'axios';

function ExtractPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setMessage('');
  };

  const handleExtract = async () => {
    if (!image) return alert("Select a watermarked image.");

    const formData = new FormData();
    formData.append('image', image);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/extract', formData);
      setMessage((res.data.messages || []).join('\n'));  // join all messages (if any)
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Extract Watermark</h2>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {preview && <img src={preview} alt="Watermarked Preview" className="preview" />}
      <button onClick={handleExtract} disabled={loading}>
        {loading ? "Extracting..." : "Extract"}
      </button>
      {message && (
        <>
          <h4>Extracted Message:</h4>
          <textarea readOnly value={message} rows={4} style={{ width: '100%' }} />
        </>
      )}
    </div>
  );
}

export default ExtractPanel;
