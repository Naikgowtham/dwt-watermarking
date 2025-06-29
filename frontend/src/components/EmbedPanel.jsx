import React, { useState } from 'react';
import axios from 'axios';

function EmbedPanel() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState('');
  const [watermarked, setWatermarked] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setWatermarked(null);
  };

  const handleSubmit = async () => {
    if (!image || !message) return alert("Image and message required.");

    const formData = new FormData();
    formData.append('image', image);
    formData.append('message', message);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/watermark', formData);
      setWatermarked(`data:image/png;base64,${res.data.image}`);
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
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
    </div>
  );
}

export default EmbedPanel;
