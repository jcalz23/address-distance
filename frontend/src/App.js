import React from 'react';
import FileUpload from './components/FileUpload';
import './styles/global.css';

function App() {
  return (
    <div className="container">
      <div className="card">
        <h1>Address Distance Calculator</h1>
        <p>Upload a CSV file with address pairs to calculate driving distances.</p>
        <FileUpload />
      </div>
    </div>
  );
}

export default App;
