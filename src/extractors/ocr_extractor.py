"""
Tesseract OCR Extractor
"""
import logging
import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)


class TesseractOCRExtractor:
    """
    Extract text from invoice images using Tesseract OCR
    """
    
    def __init__(self):
        self.extractor_name = "Tesseract OCR"
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from invoice image using Tesseract OCR
        
        Args:
            image_path: Path to invoice image
            
        Returns:
            Extracted text string
        """
        try:
            # Preprocess image for better OCR
            processed_image = self._preprocess_image(image_path)
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(processed_image)
            
            logger.info(f"Successfully extracted text from {image_path}")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            return ""
    
    def _preprocess_image(self, image_path: str) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image_path: Path to invoice image
            
        Returns:
            Preprocessed PIL Image
        """
        try:
            # Read image using OpenCV
            img = cv2.imread(image_path)
            
            if img is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Denoise
            denoised = cv2.bilateralFilter(thresh, 9, 75, 75)
            
            # Convert back to PIL Image
            pil_image = Image.fromarray(denoised)
            
            logger.debug(f"Image preprocessed successfully: {image_path}")
            return pil_image
            
        except Exception as e:
            logger.warning(f"Error preprocessing image {image_path}, using original: {e}")
            return Image.open(image_path)
