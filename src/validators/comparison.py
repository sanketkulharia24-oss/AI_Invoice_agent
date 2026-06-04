"""
Comparison Validator - Compare results from Pipeline A and B
"""
import logging
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ComparisonValidator:
    """
    Validate and compare results from both pipelines
    Generate comparison reports
    """
    
    def __init__(self, output_path: str = './output'):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, results: List[Dict[str, Any]]):
        """
        Generate comparison report from pipeline results
        
        Args:
            results: List of results from both pipelines
        """
        try:
            # Separate results by pipeline
            pipeline_a_results = [r for r in results if r.get('pipeline') == 'A']
            pipeline_b_results = [r for r in results if r.get('pipeline') == 'B']
            
            logger.info(f"Pipeline A: {len(pipeline_a_results)} results")
            logger.info(f"Pipeline B: {len(pipeline_b_results)} results")
            
            # Generate consolidated output
            self._generate_output_csv(results)
            
            # Generate comparison report
            self._generate_comparison_csv(pipeline_a_results, pipeline_b_results)
            
            logger.info(f"Reports generated in {self.output_path}")
            
        except Exception as e:
            logger.error(f"Error generating comparison report: {str(e)}")
    
    def _generate_output_csv(self, results: List[Dict[str, Any]]):
        """Generate consolidated output.csv with all extracted fields"""
        try:
            rows = []
            
            for result in results:
                if result.get('success'):
                    row = {
                        'image_name': Path(result['image_path']).name,
                        'pipeline': result['pipeline'],
                        'seller_name': result['fields'].get('seller_name'),
                        'seller_tax_id': result['fields'].get('seller_tax_id'),
                        'client_name': result['fields'].get('client_name'),
                        'client_tax_id': result['fields'].get('client_tax_id'),
                        'invoice_number': result['fields'].get('invoice_number'),
                        'invoice_date': result['fields'].get('invoice_date'),
                        'net_worth': result['fields'].get('net_worth'),
                        'vat': result['fields'].get('vat'),
                        'gross_worth': result['fields'].get('gross_worth'),
                        'confidence': result['confidence'],
                    }
                    rows.append(row)
            
            df = pd.DataFrame(rows)
            output_file = self.output_path / 'output.csv'
            df.to_csv(output_file, index=False)
            logger.info(f"Output saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error generating output.csv: {str(e)}")
    
    def _generate_comparison_csv(self, pipeline_a_results: List, pipeline_b_results: List):
        """Generate comparison_report.csv comparing both pipelines"""
        try:
            comparison_rows = []
            
            # Create mapping by image name for easier comparison
            a_map = {Path(r['image_path']).name: r for r in pipeline_a_results}
            b_map = {Path(r['image_path']).name: r for r in pipeline_b_results}
            
            all_images = set(a_map.keys()) | set(b_map.keys())
            
            fields = [
                'seller_name', 'seller_tax_id', 'client_name', 'client_tax_id',
                'invoice_number', 'invoice_date', 'net_worth', 'vat', 'gross_worth'
            ]
            
            for image_name in sorted(all_images):
                result_a = a_map.get(image_name)
                result_b = b_map.get(image_name)
                
                for field in fields:
                    value_a = result_a['fields'].get(field) if result_a and result_a.get('success') else None
                    value_b = result_b['fields'].get(field) if result_b and result_b.get('success') else None
                    
                    match = value_a == value_b if (value_a and value_b) else 'N/A'
                    confidence_a = result_a['confidence'] if result_a and result_a.get('success') else 0.0
                    confidence_b = result_b['confidence'] if result_b and result_b.get('success') else 0.0
                    
                    row = {
                        'image_name': image_name,
                        'field': field,
                        'pipeline_a_value': value_a,
                        'pipeline_b_value': value_b,
                        'match': match,
                        'confidence_a': confidence_a,
                        'confidence_b': confidence_b,
                        'discrepancy': 'No' if match == True else ('Yes' if match == False else 'Incomplete'),
                    }
                    comparison_rows.append(row)
            
            df = pd.DataFrame(comparison_rows)
            comparison_file = self.output_path / 'comparison_report.csv'
            df.to_csv(comparison_file, index=False)
            logger.info(f"Comparison report saved to {comparison_file}")
            
        except Exception as e:
            logger.error(f"Error generating comparison_report.csv: {str(e)}")
