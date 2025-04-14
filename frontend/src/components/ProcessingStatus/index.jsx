import React from 'react';
import './styles.css';

const ProcessingStatus = ({ status, filename }) => {
  if (!status) return null;

  const statusMessages = {
    uploading: 'Uploading file...',
    processing: 'Processing addresses...',
    success: 'File processed successfully!',
    error: 'An error occurred'
  };

  const message = statusMessages[status] || status;
  const isProcessing = status === 'uploading' || status === 'processing';

  return (
    <div className={`processing-status ${status}`}>
      {isProcessing && <div className="spinner" />}
      <p>{message}</p>
      {status === 'success' && filename && (
        <p className="success-text">
          Your file is ready for download
        </p>
      )}
    </div>
  );
};

export default ProcessingStatus; 