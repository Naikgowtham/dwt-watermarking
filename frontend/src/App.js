import React from 'react';
import './App.css';
import EmbedPanel from './components/EmbedPanel';
import ExtractPanel from './components/ExtractPanel';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import BlockchainLogs from './components/BlockchainLogs';
import WatermarkChain from './components/WatermarkChain';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>DWT Watermarking Tool</h1>
        <nav style={{ marginBottom: '20px' }}>
          <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
          <Link to="/blockchain-logs" style={{ marginRight: '10px' }}>Blockchain Logs</Link>
          <Link to="/watermark-chain">Watermark Chain</Link>
        </nav>
        <Routes>
          <Route path="/" element={
            <div className="panel-container">
              <EmbedPanel />
              <ExtractPanel />
            </div>
          } />
          <Route path="/blockchain-logs" element={<BlockchainLogs />} />
          <Route path="/watermark-chain" element={<WatermarkChain />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
