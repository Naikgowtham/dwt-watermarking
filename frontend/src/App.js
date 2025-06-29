import React from 'react';
import './App.css';
import EmbedPanel from './components/EmbedPanel';
import ExtractPanel from './components/ExtractPanel';

function App() {
  return (
    <div className="App">
      <h1>DWT Watermarking Tool</h1>
      <div className="panel-container">
        <EmbedPanel />
        <ExtractPanel />
      </div>
    </div>
  );
}

export default App;
