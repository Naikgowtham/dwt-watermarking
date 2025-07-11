import React, { useEffect, useState } from 'react';

function BlockchainLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/blockchain/logs')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch logs');
        return res.json();
      })
      .then((data) => {
        setLogs(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading blockchain logs...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!logs.length) return <div>No blockchain logs found.</div>;

  // Get all unique keys for table headers
  const allKeys = Array.from(
    logs.reduce((keys, log) => {
      Object.keys(log).forEach((k) => keys.add(k));
      return keys;
    }, new Set())
  );

  return (
    <div>
      <h2>Blockchain Logs</h2>
      <table border="1" cellPadding="6" style={{ margin: '20px auto', minWidth: 600 }}>
        <thead>
          <tr>
            {allKeys.map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {logs.map((log, idx) => (
            <tr key={idx}>
              {allKeys.map((key) => (
                <td key={key}>{log[key] !== undefined ? String(log[key]) : ''}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BlockchainLogs; 