import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
`;

const UploadArea = styled.div`
  border: 2px dashed #ccc;
  padding: 20px;
  margin: 20px 0;
  cursor: pointer;
`;

const Button = styled.button`
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px;
  
  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

const Preview = styled.img`
  max-width: 100%;
  max-height: 400px;
  margin: 20px 0;
`;

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setProcessedImage(null);
  };

  const removeBackground = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('image_file', selectedFile);

    try {
      const response = await axios({
        method: 'post',
        url: 'https://api.remove.bg/v1.0/removebg',
        data: formData,
        responseType: 'arraybuffer',
        headers: {
          'X-Api-Key': 'jgwp3vfroSZsCfw7HxKHaWYA',
        },
      });

      const blob = new Blob([response.data], { type: 'image/png' });
      const url = URL.createObjectURL(blob);
      setProcessedImage(url);
    } catch (error) {
      console.error('Error removing background:', error);
      alert('Error processing image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadImage = () => {
    if (!processedImage) return;

    const link = document.createElement('a');
    link.href = processedImage;
    link.download = 'processed-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Container>
      <h1>Image Background Remover</h1>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        id="fileInput"
      />
      <UploadArea onClick={() => document.getElementById('fileInput').click()}>
        <p>Click to upload an image</p>
        {preview && <Preview src={preview} alt="Preview" />}
      </UploadArea>
      
      <Button 
        onClick={removeBackground} 
        disabled={!selectedFile || loading}
      >
        {loading ? 'Processing...' : 'Remove Background'}
      </Button>

      {processedImage && (
        <>
          <h2>Result:</h2>
          <Preview src={processedImage} alt="Processed" />
          <Button onClick={downloadImage}>Download</Button>
        </>
      )}
    </Container>
  );
}

export default App;