// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default {
  API_BASE_URL,
  ENDPOINTS: {
    WATERMARK: `${API_BASE_URL}/watermark`,
    EXTRACT: `${API_BASE_URL}/extract`,
    BLOCKCHAIN_CHAIN: `${API_BASE_URL}/blockchain/chain`,
    BLOCKCHAIN_LOGS: `${API_BASE_URL}/blockchain/logs`,
  }
}; 