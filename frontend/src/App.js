import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://access-control-backend-izwo.onrender.com') // Replace with your Render URL
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  const API_URL = "https://access-control-backend-izwo.onrender.com";

useEffect(() => {
  fetch(`${API_URL}/api/test`)
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => setData(data))
    .catch(error => console.error('Error:', error));
}, []);

  return (
    <div className="App">
      <h1>Access Control Simulator</h1>
      {loading ? (
        <p>Loading access policies...</p>
      ) : data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Failed to load data from backend</p>
      )}
    </div>
  );
}

export default App;