/**
 * Upload a CSV file to the server
 * @param {File} file - The CSV file to upload
 * @returns {Promise<Object>} - Response from the server
 */
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload file');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Error uploading file');
  }
};

/**
 * Download the processed CSV file
 * @param {string} filename - The name of the file to download
 */
export const downloadFile = async (filename) => {
  try {
    const response = await fetch(`/api/download/${filename}`);
    
    if (!response.ok) {
      throw new Error('Failed to download file');
    }

    // Create a blob from the response
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    
    // Create a temporary link and click it to start the download
    const link = document.createElement('a');
    link.href = url;
    link.download = `processed_${filename}`;
    document.body.appendChild(link);
    link.click();
    
    // Clean up
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(error.message || 'Error downloading file');
  }
}; 