"""
Vision API Extractor - Azure Computer Vision or OpenAI Vision
"""
import logging
import os
from typing import Dict, Any
import base64

logger = logging.getLogger(__name__)


class VisionAPIExtractor:
    """
    Extract text from invoices using Vision APIs
    Supports: Azure Computer Vision, OpenAI Vision API
    """
    
    def __init__(self):
        self.api_type = self._detect_api_type()
        self.extractor_name = f"Vision API ({self.api_type})"
    
    def _detect_api_type(self) -> str:
        """Detect which Vision API to use based on available credentials"""
        if os.getenv('AZURE_SUBSCRIPTION_KEY') and os.getenv('AZURE_ENDPOINT'):
            return "Azure Computer Vision"
        elif os.getenv('OPENAI_API_KEY'):
            return "OpenAI Vision"
        else:
            logger.warning("No Vision API credentials found. Using placeholder.")
            return "Placeholder"
    
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from invoice image using Vision API
        
        Args:
            image_path: Path to invoice image
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            if self.api_type == "Azure Computer Vision":
                return self._extract_azure(image_path)
            elif self.api_type == "OpenAI Vision":
                return self._extract_openai(image_path)
            else:
                return self._extract_placeholder(image_path)
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            return {'text': '', 'error': str(e)}
    
    def _extract_azure(self, image_path: str) -> Dict[str, Any]:
        """Extract text using Azure Computer Vision API"""
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
            from msrest.authentication import CognitiveServicesCredentials
            
            subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
            endpoint = os.getenv('AZURE_ENDPOINT')
            
            client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
            
            with open(image_path, 'rb') as image_file:
                read_image_results = client.read_in_stream(image_file, raw=True)
            
            operation_id = read_image_results.headers["Operation-Location"].split("/")[-1]
            
            # Wait for result
            while read_image_results.status == OperationStatusCodes.not_started or read_image_results.status == OperationStatusCodes.running:
                import time
                time.sleep(1)
                read_image_results = client.get_read_result(operation_id)
            
            # Extract text
            extracted_text = ""
            for text_result in read_image_results.analyze_results:
                for line in text_result.read_results[0].lines:
                    extracted_text += line.text + "\n"
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters using Azure Vision API")
            return {'text': extracted_text, 'source': 'Azure Computer Vision'}
            
        except ImportError:
            logger.warning("Azure SDK not installed. Install with: pip install azure-cognitiveservices-vision-computervision")
            return {'text': '', 'error': 'Azure SDK not installed'}
        except Exception as e:
            logger.error(f"Azure Vision API error: {str(e)}")
            return {'text': '', 'error': str(e)}
    
    def _extract_openai(self, image_path: str) -> Dict[str, Any]:
        """Extract text using OpenAI Vision API"""
        try:
            from openai import OpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            client = OpenAI(api_key=api_key)
            
            with open(image_path, 'rb') as image_file:
                image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
            
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}",
                                },
                            },
                            {
                                "type": "text",
                                "text": "Please extract all text from this invoice image. Provide the complete text content."
                            }
                        ],
                    }
                ],
                max_tokens=2000,
            )
            
            extracted_text = response.choices[0].message.content
            logger.info(f"Successfully extracted text using OpenAI Vision API")
            return {'text': extracted_text, 'source': 'OpenAI Vision'}
            
        except ImportError:
            logger.warning("OpenAI SDK not installed. Install with: pip install openai")
            return {'text': '', 'error': 'OpenAI SDK not installed'}
        except Exception as e:
            logger.error(f"OpenAI Vision API error: {str(e)}")
            return {'text': '', 'error': str(e)}
    
    def _extract_placeholder(self, image_path: str) -> Dict[str, Any]:
        """Placeholder for when no Vision API is configured"""
        logger.warning(f"No Vision API configured. Using placeholder extraction for {image_path}")
        return {
            'text': 'PLACEHOLDER TEXT - Configure Azure or OpenAI credentials',
            'source': 'Placeholder',
            'warning': 'No Vision API credentials configured'
        }
