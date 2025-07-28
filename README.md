# DWT Watermarking Tool

A comprehensive digital watermarking system that uses Discrete Wavelet Transform (DWT) to embed and extract watermarks from images. The system includes blockchain integration for watermark verification and IPFS storage for decentralized file management.

## 🚀 Features

- **DWT-based Watermarking**: Uses Discrete Wavelet Transform for robust watermark embedding
- **Blockchain Integration**: Stores watermark metadata on blockchain for verification
- **IPFS Storage**: Decentralized storage for original and watermarked images
- **Chain Verification**: Supports watermark chaining for tracking image lineage
- **Multiple Backend Implementations**: 
  - `backend/`: Y Channel-based watermarking
  - `backend1/`: DCT-based watermarking
  - `backend2/`: Robust DWT watermarking
- **React Frontend**: Modern web interface for watermark operations
- **Attack Resistance**: Built-in resistance against common image attacks

## 🏗️ Architecture

```
dwt-watermarking/
├── backend/          # Y Channel-based watermarking backend
├── backend1/         # DCT-based watermarking backend  
├── backend2/         # Robust DWT watermarking backend
├── frontend/         # React frontend application
├── frontend1/        # Alternative frontend
├── frontend2/        # Alternative frontend
└── README.md         # This file
```

## 🛠️ Technology Stack

### Backend
- **Python 3.10**
- **Flask**: Web framework
- **OpenCV**: Image processing
- **PyWavelets**: DWT implementation
- **Web3.py**: Blockchain integration
- **IPFS/Pinata**: Decentralized storage
- **Gunicorn**: Production server

### Frontend
- **React 19**
- **Axios**: HTTP client
- **React Router**: Navigation
- **CSS3**: Styling

### Blockchain
- **Polygon Amoy Testnet**: Smart contract deployment
- **Solidity**: Smart contract language

## 📋 Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd dwt-watermarking
```

### 2. Backend Setup

#### For Y-Channel Backend (backend/)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```


### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```


## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```
ALCHEMY_URL=your alchemy url
PRIVATE_KEY=your_private_key of your wallet
PUBLIC_ADDRESS=your public address of wallet
PINATA_API_KEY=your pinata api key
PINATA_SECRET_API_KEY=your pinata secret key
```



## 📖 API Endpoints

### Watermark Operations
- `POST /watermark`: Embed watermark in image
- `POST /extract`: Extract watermark from image
- `POST /get_watermark`: Get watermark metadata from blockchain

### Blockchain Operations
- `GET /blockchain/chain/{hash}`: Get watermark chain

## 🔍 Usage

### Embedding Watermarks
1. Upload an image through the frontend
2. Enter a message to embed
3. Click "Watermark" to embed the watermark
4. Download the watermarked image

### Extracting Watermarks
1. Upload a watermarked image
2. Click "Extract" to extract the watermark
3. View extracted messages and metadata

### Chain Verification
1. Navigate to "Watermark Chain" page
2. Enter a watermark hash
3. View the complete chain of watermarks

## 🛡️ Security Features

- **Hash-based Verification**: SHA256 hashing for image integrity
- **CRC Validation**: Cyclic redundancy check for data integrity
- **Blockchain Verification**: On-chain metadata storage
- **Chain Validation**: Parent-child relationship verification
