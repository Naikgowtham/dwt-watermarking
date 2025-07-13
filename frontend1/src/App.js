import React from 'react';
import './App.css';
import EmbedPanel from './components/EmbedPanel';
import ExtractPanel from './components/ExtractPanel';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


function App() {
  return (
    <Router>
      <div className="App">
        <h1>DCT Watermarking Tool</h1>
        <nav style={{ marginBottom: '20px' }}>
          <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
        </nav>
        <Routes>
          <Route path="/" element={
            <div className="panel-container">
              <EmbedPanel />
              <ExtractPanel />
            </div>
          } />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
