# Backend2 - Robust DWT Watermarking API

A Flask-based API for robust Discrete Wavelet Transform (DWT) watermarking, designed to be more resilient than traditional LSB approaches.

## Features

- **Robust DWT Watermarking**: Embeds watermarks in wavelet coefficients for better resistance to compression and noise
- **Multi-message Support**: Can embed multiple messages in a single image
- **Hash-based Chaining**: Supports watermark chaining with SHA256 hashes
- **RESTful API**: Clean endpoints for embedding and extracting watermarks
- **No Blockchain Dependencies**: Simplified implementation without blockchain/IPFS complexity

## How Robust DWT Works

### Embedding Process
1. **Color Space Conversion**: Convert RGB image to YCbCr and work on Y (luminance) channel
2. **DWT Decomposition**: Apply 2-level Haar wavelet transform to get subbands (LL, LH, HL, HH)
3. **Coefficient Selection**: Select robust positions in LH and HL subbands (middle frequencies)
4. **Quantization Embedding**: Modify coefficients using positive/negative quantization:
   - Bit 1: Force coefficient to positive value + alpha
   - Bit 0: Force coefficient to negative value - alpha
5. **Inverse DWT**: Reconstruct image from modified coefficients
6. **Color Space Restoration**: Convert back to RGB

### Extraction Process
1. **DWT Decomposition**: Apply same wavelet transform to watermarked image
2. **Coefficient Reading**: Read from same robust positions used during embedding
3. **Threshold Detection**: Extract bits based on coefficient sign (positive = 1, negative = 0)
4. **Bitstream Parsing**: Parse extracted bits to recover messages and hash

### Advantages Over LSB
- **Compression Resistance**: Survives JPEG compression better than LSB
- **Noise Resistance**: More robust against image processing operations
- **Invisibility**: Less visible artifacts compared to LSB manipulation
- **Capacity**: Can embed more data reliably

## API Endpoints

### POST /watermark
Embed a watermark into an image.

**Form Data:**
- `image`: Image file (PNG, JPG, etc.)
- `message`: Text message to embed

**Response:**
```json
{
  "success": true,
  "message": "Watermark embedded successfully using robust DWT",
  "image": "base64_encoded_watermarked_image",
  "original_filename": "uuid_orig.png",
  "watermarked_filename": "uuid_wm.png",
  "original_hash": "sha256_hash_of_original",
  "watermarked_hash": "sha256_hash_of_watermarked",
  "parent_hash": "parent_hash_for_chaining",
  "embedded_messages": ["message1", "message2"],
  "timestamp": "2024-01-01T12:00:00",
  "algorithm": "Robust DWT",
  "original_cid": null,
  "watermarked_cid": null,
  "on_chain": true
}
```

### POST /extract
Extract watermark from an image.

**Form Data:**
- `image`: Watermarked image file

**Response:**
```json
{
  "success": true,
  "message": "Watermark extracted successfully using robust DWT",
  "messages": ["extracted_message1", "extracted_message2"],
  "hash": "sha256_hash_of_original_image",
  "format": "hash_based",
  "timestamp": "2024-01-01T12:00:00",
  "algorithm": "Robust DWT",
  "on_chain": {
    "original_hash": "hash",
    "watermarked_hash": "hash",
    "parent_hash": "parent_hash",
    "original_cid": null,
    "watermarked_cid": null,
    "crc": 0
  },
  "crc_match": true
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Robust DWT Watermarking API",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Configuration

The robust DWT engine can be configured with these parameters:

- **wavelet**: Wavelet type ('haar', 'db2', 'db4', etc.) - default: 'haar'
- **level**: Decomposition level (1-3 recommended) - default: 2
- **alpha**: Embedding strength (higher = more robust but more visible) - default: 15.0
- **seed**: Random seed for reproducible embedding - default: 42

## Technical Details

### Wavelet Transform
- Uses PyWavelets library for DWT operations
- 2-level decomposition provides good balance of capacity and robustness
- Haar wavelet is simple and effective for watermarking

### Coefficient Selection
- Embeds in LH (horizontal details) and HL (vertical details) subbands
- Avoids LL (low frequency) and HH (high frequency) for better robustness
- Skips every 4th position to avoid interference

### Quantization Strategy
- Uses positive/negative quantization for bit representation
- Alpha parameter controls embedding strength
- Higher alpha = more robust but potentially more visible

### Bitstream Format
```
[256-bit SHA256 hash][16-bit message count][message1 length][message1][message2 length][message2]...
```

## Performance

- **Embedding Time**: ~1-3 seconds for typical images
- **Extraction Time**: ~0.5-1 second
- **Capacity**: Up to 1000 bits for 512x512 images
- **Robustness**: Survives JPEG compression (quality 70+)

## Limitations

- Requires minimum image size of 256x256 pixels
- Best results with images that have good texture content
- May be visible in very smooth areas of images
- Limited capacity compared to LSB but much more robust 