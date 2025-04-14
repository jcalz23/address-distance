import React from 'react';
import './styles.css';

const ErrorDisplay = ({ errors }) => {
  if (!errors || (Array.isArray(errors) && errors.length === 0)) {
    return null;
  }

  const errorMessages = Array.isArray(errors) ? errors : [errors];

  return (
    <div className="error-display">
      {errorMessages.map((error, index) => (
        <p key={index} className="error-text">{error}</p>
      ))}
    </div>
  );
};

export default ErrorDisplay; 