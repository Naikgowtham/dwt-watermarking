# DCT Watermarking Frontend

This is the frontend for the DCT (Discrete Cosine Transform) watermarking system. It's designed to work with backend1 which provides robust DCT-based watermarking without blockchain/IPFS dependencies.

## 🎯 Features

- **DCT Watermarking**: Robust watermarking using Discrete Cosine Transform
- **Simple Interface**: Clean, user-friendly interface for embedding and extracting watermarks
- **Real-time Processing**: Immediate feedback on watermark operations
- **Image Preview**: Preview images before and after watermarking
- **Detailed Results**: Comprehensive information about watermarking operations

## 🚀 Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## 📡 API Integration

This frontend connects to backend1 running on port 5000:

- **Embed Watermark**: `POST http://localhost:5000/watermark`
- **Extract Watermark**: `POST http://localhost:5000/extract`
- **Health Check**: `GET http://localhost:5000/health`

## 🎨 Interface

### Embed Panel
- Upload image file
- Enter watermark message
- View original and watermarked images
- See DCT algorithm information
- Display embedding results

### Extract Panel
- Upload watermarked image
- Extract embedded messages
- View DCT extraction details
- Validate message integrity

## 🔧 Configuration

The frontend is configured to work with backend1's response format:

- Expects `image` field for watermarked image (base64)
- Uses `messages` array for extracted messages
- Displays DCT-specific algorithm information
- Shows robustness metrics

## 🛡️ DCT Advantages

- **Compression Resistant**: Survives JPEG compression
- **Noise Resistant**: Robust against image noise
- **Scaling Resistant**: Works with scaled images
- **Industry Standard**: Widely used in professional watermarking

## 📁 Project Structure

```
frontend1/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── EmbedPanel.jsx
│   │   └── ExtractPanel.jsx
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

## 🔄 Usage Workflow

1. **Embed Watermark**:
   - Upload an image (minimum 256x256 pixels)
   - Enter your message
   - Click "Watermark" to embed
   - Download the watermarked image

2. **Extract Watermark**:
   - Upload a watermarked image
   - Click "Extract" to retrieve messages
   - View extracted content and validation

## 🚨 Important Notes

- **Minimum Image Size**: 256x256 pixels required for reliable DCT watermarking
- **Supported Formats**: JPEG, PNG, BMP
- **Message Length**: Limited by image size (typically 1000-5000 bits)
- **Robustness**: Best results with high-quality images

## 🔗 Backend Requirements

Make sure backend1 is running with:
- Port 5000
- CORS enabled
- DCT watermarking engine active
- Proper response format

## 🧪 Testing

Test the complete system:
1. Start backend1: `cd backend1 && python3 app.py`
2. Start frontend1: `cd frontend1 && npm start`
3. Upload an image and test embedding/extraction
