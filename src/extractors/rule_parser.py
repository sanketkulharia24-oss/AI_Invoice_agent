"""
Rule-based Parser for extracting invoice fields
"""
import logging
import re
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class RuleBasedParser:
    """
    Extract invoice fields using predefined rules and regex patterns
    """
    
    def __init__(self):
        self.parser_name = "Rule-based Parser"
        self.patterns = self._define_patterns()
    
    def parse(self, text: str) -> Dict[str, Optional[str]]:
        """
        Parse extracted text to extract invoice fields
        
        Args:
            text: Extracted text from invoice
            
        Returns:
            Dictionary with extracted fields
        """
        fields = {
            'seller_name': self._extract_seller_name(text),
            'seller_tax_id': self._extract_seller_tax_id(text),
            'client_name': self._extract_client_name(text),
            'client_tax_id': self._extract_client_tax_id(text),
            'invoice_number': self._extract_invoice_number(text),
            'invoice_date': self._extract_invoice_date(text),
            'net_worth': self._extract_net_worth(text),
            'vat': self._extract_vat(text),
            'gross_worth': self._extract_gross_worth(text),
        }
        
        return fields
    
    def _define_patterns(self) -> Dict[str, str]:
        """Define regex patterns for field extraction"""
        return {
            'tax_id': r'(?:VAT|TAX|TIN|SIRET|SIREN|GST)\s*[:#]?\s*([A-Z0-9\-\s]+)',
            'invoice_number': r'(?:Invoice|INVOICE|Number|No\.?|#)\s*[:#]?\s*([A-Z0-9\-]+)',
            'date': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'amount': r'(?:€|\$|£|Rs\.?)\s*([0-9,.\s]+)',
            'percentage': r'(\d+\.?\d*)\s*%',
        }
    
    def _extract_seller_name(self, text: str) -> Optional[str]:
        """Extract seller/vendor name"""
        try:
            # Look for common patterns
            patterns = [
                r'(?:From|Vendor|Seller|Company|Business)[:\s]+([A-Za-z\s&\.]+?)(?:\n|,|$)',
                r'^([A-Za-z\s&\.]+?)(?:\n|$)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    if len(name) > 3 and len(name) < 100:
                        return name
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting seller name: {e}")
            return None
    
    def _extract_seller_tax_id(self, text: str) -> Optional[str]:
        """Extract seller tax ID"""
        try:
            pattern = r'(?:Seller|Vendor|Company)\s+(?:Tax|VAT|ID)[:\s]+([A-Z0-9\-\s]+?)(?:\n|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return None
        except Exception as e:
            logger.warning(f"Error extracting seller tax ID: {e}")
            return None
    
    def _extract_client_name(self, text: str) -> Optional[str]:
        """Extract client/customer name"""
        try:
            patterns = [
                r'(?:Bill|Ship)?(?:\s)?To[:\s]+([A-Za-z\s&\.]+?)(?:\n|$)',
                r'(?:Customer|Client|Buyer)[:\s]+([A-Za-z\s&\.]+?)(?:\n|$)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    if len(name) > 3 and len(name) < 100:
                        return name
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting client name: {e}")
            return None
    
    def _extract_client_tax_id(self, text: str) -> Optional[str]:
        """Extract client tax ID"""
        try:
            pattern = r'(?:Bill|Customer|Client)\s+(?:To)?\s+(?:Tax|VAT|ID)[:\s]+([A-Z0-9\-\s]+?)(?:\n|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return None
        except Exception as e:
            logger.warning(f"Error extracting client tax ID: {e}")
            return None
    
    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice number"""
        try:
            patterns = [
                r'(?:Invoice|INVOICE|No\.?|Number|#)\s*[:#]?\s*([A-Z0-9\-]+)',
                r'INV[:\s-]*([A-Z0-9\-]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting invoice number: {e}")
            return None
    
    def _extract_invoice_date(self, text: str) -> Optional[str]:
        """Extract invoice date"""
        try:
            patterns = [
                r'(?:Date|Invoice Date|Date of Invoice)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting invoice date: {e}")
            return None
    
    def _extract_net_worth(self, text: str) -> Optional[str]:
        """Extract net worth/subtotal"""
        try:
            patterns = [
                r'(?:Subtotal|Sub Total|Net|Net Total|Net Amount)[:\s]*([0-9,.\s]+?)(?:\n|VAT)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount = re.search(r'([0-9]+\.?[0-9]*)', match.group(1))
                    if amount:
                        return amount.group(1)
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting net worth: {e}")
            return None
    
    def _extract_vat(self, text: str) -> Optional[str]:
        """Extract VAT amount"""
        try:
            patterns = [
                r'(?:VAT|Tax|GST)[:\s]*([0-9,.\s]+?)(?:\n|$|Total)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount = re.search(r'([0-9]+\.?[0-9]*)', match.group(1))
                    if amount:
                        return amount.group(1)
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting VAT: {e}")
            return None
    
    def _extract_gross_worth(self, text: str) -> Optional[str]:
        """Extract gross worth/total amount"""
        try:
            patterns = [
                r'(?:Total|Grand Total|Amount Due|TOTAL)[:\s]*([0-9,.\s]+?)(?:\n|$)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount = re.search(r'([0-9]+\.?[0-9]*)', match.group(1))
                    if amount:
                        return amount.group(1)
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting gross worth: {e}")
            return None
