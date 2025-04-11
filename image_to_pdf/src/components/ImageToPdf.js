import React, { useState } from 'react';
import { PDFDocument } from 'pdf-lib';  // Changed from @react-pdf/renderer to pdf-lib
import { Button, Container, Box, Typography } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

function ImageToPdf() {
  const [images, setImages] = useState([]);
  const { currentUser, logout } = useAuth();

  const handleImageUpload = (event) => {
    const files = Array.from(event.target.files);
    setImages(files);
  };

  const convertToPdf = async () => {
    if (images.length === 0) return;

    const pdfDoc = await PDFDocument.create();
    
    for (const image of images) {
      const imageBytes = await image.arrayBuffer();
      let img;
      
      if (image.type.includes('jpeg') || image.type.includes('jpg')) {
        img = await pdfDoc.embedJpg(imageBytes);
      } else if (image.type.includes('png')) {
        img = await pdfDoc.embedPng(imageBytes);
      }

      const page = pdfDoc.addPage([img.width, img.height]);
      page.drawImage(img, {
        x: 0,
        y: 0,
        width: img.width,
        height: img.height,
      });
    }

    const pdfBytes = await pdfDoc.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'converted-images.pdf';
    link.click();
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Image to PDF Converter
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Welcome, {currentUser.email}
        </Typography>
        <Button
          variant="contained"
          component="label"
          sx={{ mr: 2 }}
        >
          Upload Images
          <input
            type="file"
            hidden
            multiple
            accept="image/*"
            onChange={handleImageUpload}
          />
        </Button>
        <Button
          variant="contained"
          onClick={convertToPdf}
          disabled={images.length === 0}
        >
          Convert to PDF
        </Button>
        <Button
          variant="outlined"
          onClick={logout}
          sx={{ ml: 2 }}
        >
          Logout
        </Button>
      </Box>
    </Container>
  );
}

export default ImageToPdf;