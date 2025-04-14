import React, { useCallback, useState } from 'react';
import { uploadFile, downloadFile } from '../../utils/api';
import { validateFile } from '../../utils/validation';
import ErrorDisplay from '../ErrorDisplay';
import ProcessingStatus from '../ProcessingStatus';
import './styles.css';

const FileUpload = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState(null);
  const [errors, setErrors] = useState(null);
  const [filename, setFilename] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback(async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    setErrors(null);

    const file = e.dataTransfer.files[0];
    await processFile(file);
  }, []);

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    await processFile(file);
  };

  const processFile = async (file) => {
    const validation = validateFile(file);
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    try {
      setStatus('uploading');
      const response = await uploadFile(file);
      setStatus('success');
      setFilename(response.filename);
    } catch (error) {
      setStatus('error');
      setErrors(error.message);
    }
  };

  const handleDownload = async () => {
    if (!filename) return;

    try {
      await downloadFile(filename);
    } catch (error) {
      setErrors(error.message);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`upload-area ${isDragging ? 'dragging' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="upload-prompt">
          <p>Drag and drop your CSV file here</p>
          <p>or</p>
          <label className="button button-primary">
            Browse Files
            <input
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </label>
        </div>
      </div>

      <ErrorDisplay errors={errors} />
      <ProcessingStatus status={status} filename={filename} />

      {status === 'success' && filename && (
        <button
          className="button button-primary download-button"
          onClick={handleDownload}
        >
          Download Processed File
        </button>
      )}
    </div>
  );
};

export default FileUpload; 