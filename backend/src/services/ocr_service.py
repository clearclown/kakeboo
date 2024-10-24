# backend/src/services/ocr_service.py

from google.cloud import vision
import os
import io
from typing import Dict, Any, Optional
from pathlib import Path
from ..core.logger import setup_logger

logger = setup_logger(__name__)

class OCRService:
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if self.credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
        self.client = vision.ImageAnnotatorClient()

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process image with OCR"""
        try:
            # Read image file
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            # Create image object
            image = vision.Image(content=content)

            # Perform OCR
            response = self.client.text_detection(image=image)
            texts = response.text_annotations

            # Check if any text was detected
            if not texts:
                return {
                    'success': False,
                    'error': 'No text detected in the image',
                    'text': '',
                    'locale': None
                }

            # Extract results
            result = {
                'success': True,
                'error': None,
                'text': texts[0].description,
                'locale': texts[0].locale,
                'blocks': []
            }

            # Extract text blocks
            for text in texts[1:]:
                vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
                result['blocks'].append({
                    'text': text.description,
                    'bounds': vertices
                })

            return result

        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'locale': None
            }

    def extract_receipt_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data from OCR text"""
        # This is a simplified version - you would need to implement
        # more sophisticated parsing logic based on your needs
        lines = text.split('\n')
        data = {
            'store_name': '',
            'total_amount': 0.0,
            'items': []
        }

        try:
            # Basic parsing logic (you should enhance this)
            data['store_name'] = lines[0]

            for line in lines:
                if '合計' in line or 'TOTAL' in line:
                    # Extract total amount (assuming format like "合計: 1000円")
                    amount_str = ''.join(filter(str.isdigit, line))
                    data['total_amount'] = float(amount_str)
                    break

            return data

        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}", exc_info=True)
            return data
