"""
Main execution script for AI Invoice Agent
"""
import argparse
import logging
from pathlib import Path
from src.pipelines.pipeline_a import PipelineA
from src.pipelines.pipeline_b import PipelineB
from src.validators.comparison import ComparisonValidator
from src.utils.config import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='AI Invoice Agent - Extract invoice fields using dual pipelines')
    parser.add_argument('--pipeline', choices=['a', 'b', 'both'], default='both', 
                        help='Which pipeline to run')
    parser.add_argument('--image', type=str, help='Path to single invoice image')
    parser.add_argument('--compare', action='store_true', help='Generate comparison report')
    parser.add_argument('--data-path', type=str, help='Path to invoice images directory')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    logger.info(f"Configuration loaded from {config}")
    
    if args.image:
        # Process single image
        logger.info(f"Processing single image: {args.image}")
        process_single_image(args.image, args.pipeline)
    else:
        # Process batch
        data_path = args.data_path or config.get('DATA_PATH', './data/invoices')
        logger.info(f"Processing invoices from: {data_path}")
        process_batch(data_path, args.pipeline, args.compare)


def process_single_image(image_path: str, pipeline: str = 'both'):
    """Process a single invoice image"""
    logger.info(f"Starting single image processing: {image_path}")
    
    if pipeline in ['a', 'both']:
        logger.info("Running Pipeline A (OCR + Rule-based)")
        pipeline_a = PipelineA()
        result_a = pipeline_a.process(image_path)
        logger.info(f"Pipeline A results: {result_a}")
    
    if pipeline in ['b', 'both']:
        logger.info("Running Pipeline B (Vision API + LLM)")
        pipeline_b = PipelineB()
        result_b = pipeline_b.process(image_path)
        logger.info(f"Pipeline B results: {result_b}")


def process_batch(data_path: str, pipeline: str = 'both', compare: bool = False):
    """Process batch of invoice images"""
    logger.info(f"Starting batch processing from: {data_path}")
    
    invoice_path = Path(data_path)
    if not invoice_path.exists():
        logger.error(f"Data path does not exist: {data_path}")
        return
    
    # Get all image files
    image_files = list(invoice_path.glob('**/*.jpg')) + list(invoice_path.glob('**/*.png'))
    logger.info(f"Found {len(image_files)} invoice images")
    
    results = []
    
    if pipeline in ['a', 'both']:
        logger.info("Running Pipeline A on batch")
        pipeline_a = PipelineA()
        for img_file in image_files:
            try:
                result = pipeline_a.process(str(img_file))
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {img_file} with Pipeline A: {e}")
    
    if pipeline in ['b', 'both']:
        logger.info("Running Pipeline B on batch")
        pipeline_b = PipelineB()
        for img_file in image_files:
            try:
                result = pipeline_b.process(str(img_file))
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {img_file} with Pipeline B: {e}")
    
    if compare:
        logger.info("Generating comparison report")
        validator = ComparisonValidator()
        validator.generate_report(results)


if __name__ == '__main__':
    main()
