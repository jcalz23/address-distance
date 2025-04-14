/**
 * Validate a file for upload
 * @param {File} file - The file to validate
 * @returns {Object} - Validation result
 */
export const validateFile = (file) => {
  const errors = [];
  
  // Check if file exists
  if (!file) {
    errors.push('No file selected');
    return { isValid: false, errors };
  }

  // Check file type
  if (!file.name.toLowerCase().endsWith('.csv')) {
    errors.push('Only CSV files are allowed');
  }

  // Check file size (max 5MB)
  const maxSize = 5 * 1024 * 1024; // 5MB in bytes
  if (file.size > maxSize) {
    errors.push('File size must be less than 5MB');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}; 