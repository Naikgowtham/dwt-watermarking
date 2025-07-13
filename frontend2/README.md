# Frontend2 - Robust DWT Watermarking Interface

A React-based frontend for the robust DWT watermarking system, providing a clean and intuitive interface for embedding and extracting watermarks.

## Features

- **Embed Watermark**: Upload an image and embed text messages using robust DWT
- **Extract Watermark**: Upload a watermarked image to extract embedded messages
- **Real-time Preview**: See image previews before processing
- **Detailed Results**: View comprehensive embedding/extraction results
- **Hash Information**: Display SHA256 hashes for verification
- **Multi-message Support**: Handle multiple embedded messages

## How to Use

### Embedding a Watermark

1. **Upload Image**: Click "Choose File" and select an image (PNG, JPG, etc.)
2. **Enter Message**: Type the text message you want to embed
3. **Process**: Click "Watermark" to embed the message using robust DWT
4. **View Results**: 
   - Download the watermarked image
   - View hash information and embedded messages
   - See algorithm details and timestamp

### Extracting a Watermark

1. **Upload Watermarked Image**: Select the image containing the watermark
2. **Extract**: Click "Extract" to recover embedded messages
3. **View Results**:
   - See all extracted messages
   - View hash information for verification
   - Check algorithm details and validation status

## Technical Details

### Robust DWT Algorithm
- Uses Discrete Wavelet Transform for embedding
- Embeds in LH and HL subbands (middle frequencies)
- Provides better resistance to compression and noise
- More robust than traditional LSB watermarking

### Response Format
The frontend expects responses from backend2 in this format:

**Embed Response:**
```json
{
  "success": true,
  "message": "Watermark embedded successfully using robust DWT",
  "image": "base64_encoded_image",
  "original_filename": "filename.png",
  "watermarked_filename": "filename_wm.png",
  "original_hash": "sha256_hash",
  "watermarked_hash": "sha256_hash",
  "parent_hash": "parent_hash",
  "embedded_messages": ["message1", "message2"],
  "timestamp": "2024-01-01T12:00:00",
  "algorithm": "Robust DWT"
}
```

**Extract Response:**
```json
{
  "success": true,
  "message": "Watermark extracted successfully using robust DWT",
  "messages": ["extracted_message1", "extracted_message2"],
  "hash": "sha256_hash",
  "format": "hash_based",
  "timestamp": "2024-01-01T12:00:00",
  "algorithm": "Robust DWT",
  "on_chain": {...},
  "crc_match": true
}
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Backend Integration

This frontend is designed to work with backend2, which provides:
- Robust DWT watermarking engine
- RESTful API endpoints
- No blockchain dependencies
- Clean, focused functionality

Make sure backend2 is running on `http://localhost:5000` before using the frontend.

## Advantages

- **Simplified Interface**: Clean, focused UI without blockchain complexity
- **Better Robustness**: DWT algorithm provides superior resistance to attacks
- **Multi-message Support**: Can embed and extract multiple messages
- **Hash Verification**: SHA256 hashes for integrity checking
- **Real-time Feedback**: Immediate preview and results display

## Limitations

- Requires minimum image size of 256x256 pixels
- Best results with images containing texture
- Limited capacity compared to LSB but much more robust
- No blockchain/IPFS integration (by design)
