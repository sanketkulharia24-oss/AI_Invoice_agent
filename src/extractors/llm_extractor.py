"""
LLM Extractor - Extract fields using Large Language Models
"""
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LLMExtractor:
    """
    Extract invoice fields using Large Language Models
    Supports: OpenAI GPT, Anthropic Claude
    """
    
    def __init__(self):
        self.llm_type = self._detect_llm_type()
        self.extractor_name = f"LLM Extractor ({self.llm_type})"
    
    def _detect_llm_type(self) -> str:
        """Detect which LLM to use based on available credentials"""
        if os.getenv('OPENAI_API_KEY'):
            return "OpenAI GPT"
        elif os.getenv('ANTHROPIC_API_KEY'):
            return "Anthropic Claude"
        else:
            logger.warning("No LLM API credentials found. Using placeholder.")
            return "Placeholder"
    
    def extract_fields(self, text: str, image_path: str = None) -> Dict[str, Any]:
        """
        Extract invoice fields using LLM
        
        Args:
            text: Extracted text from invoice
            image_path: Optional path to image for context
            
        Returns:
            Dictionary with extracted fields and confidence score
        """
        try:
            if self.llm_type == "OpenAI GPT":
                return self._extract_openai(text)
            elif self.llm_type == "Anthropic Claude":
                return self._extract_anthropic(text)
            else:
                return self._extract_placeholder(text)
        except Exception as e:
            logger.error(f"Error extracting fields with LLM: {str(e)}")
            return {'error': str(e), '_confidence': 0.0}
    
    def _extract_openai(self, text: str) -> Dict[str, Any]:
        """Extract fields using OpenAI GPT"""
        try:
            from openai import OpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            client = OpenAI(api_key=api_key)
            
            prompt = f"""Extract the following fields from this invoice text and return as JSON:
- seller_name
- seller_tax_id
- client_name
- client_tax_id
- invoice_number
- invoice_date
- net_worth
- vat
- gross_worth

Invoice text:
{text}

Return only valid JSON with these exact field names. For missing fields, use null."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an invoice data extraction expert. Extract fields accurately and return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            import json
            fields = json.loads(response_text)
            fields['_confidence'] = 0.85  # LLM-based extraction typically has high confidence
            
            logger.info("Successfully extracted fields using OpenAI GPT")
            return fields
            
        except ImportError:
            logger.warning("OpenAI SDK not installed")
            return {'error': 'OpenAI SDK not installed', '_confidence': 0.0}
        except Exception as e:
            logger.error(f"OpenAI extraction error: {str(e)}")
            return {'error': str(e), '_confidence': 0.0}
    
    def _extract_anthropic(self, text: str) -> Dict[str, Any]:
        """Extract fields using Anthropic Claude"""
        try:
            from anthropic import Anthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            client = Anthropic(api_key=api_key)
            
            prompt = f"""Extract the following fields from this invoice text and return as JSON:
- seller_name
- seller_tax_id
- client_name
- client_tax_id
- invoice_number
- invoice_date
- net_worth
- vat
- gross_worth

Invoice text:
{text}

Return only valid JSON with these exact field names. For missing fields, use null."""
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = response.content[0].text
            
            # Parse JSON response
            import json
            fields = json.loads(response_text)
            fields['_confidence'] = 0.85
            
            logger.info("Successfully extracted fields using Anthropic Claude")
            return fields
            
        except ImportError:
            logger.warning("Anthropic SDK not installed")
            return {'error': 'Anthropic SDK not installed', '_confidence': 0.0}
        except Exception as e:
            logger.error(f"Anthropic extraction error: {str(e)}")
            return {'error': str(e), '_confidence': 0.0}
    
    def _extract_placeholder(self, text: str) -> Dict[str, Any]:
        """Placeholder extraction when no LLM is configured"""
        logger.warning("No LLM configured. Using placeholder extraction")
        return {
            'seller_name': 'PLACEHOLDER',
            'seller_tax_id': 'PLACEHOLDER',
            'client_name': 'PLACEHOLDER',
            'client_tax_id': 'PLACEHOLDER',
            'invoice_number': 'PLACEHOLDER',
            'invoice_date': 'PLACEHOLDER',
            'net_worth': 'PLACEHOLDER',
            'vat': 'PLACEHOLDER',
            'gross_worth': 'PLACEHOLDER',
            '_confidence': 0.0,
            'warning': 'No LLM credentials configured'
        }
