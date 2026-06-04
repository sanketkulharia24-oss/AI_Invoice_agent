# AI Invoice Agent

A Python-based system that extracts key fields from invoice images using two independent approaches and validates the results.

## 📋 Overview

This project implements a dual-pipeline approach for invoice data extraction:
- **Pipeline A**: Tesseract OCR + Rule-based Parsing
- **Pipeline B**: Azure Computer Vision / OpenAI Vision API + LLM-based Extraction

The system validates results by comparing both approaches and generating detailed comparison reports.

## 🎯 Objectives

Extract the following required fields from invoice images:
- Seller Name
- Seller Tax ID
- Client Name
- Client Tax ID
- Invoice Number
- Invoice Date
- Net Worth
- VAT
- Gross Worth

## 📁 Project Structure

```
AI_Invoice_agent/
├── data/
│   ├── invoices/              # Raw invoice images
│   └── processed/             # Preprocessed images
├── src/
│   ├── pipelines/
│   │   ├── pipeline_a.py      # OCR + Rule-based extraction
│   │   ├── pipeline_b.py      # Vision API + LLM extraction
│   │   └── __init__.py
│   ├── extractors/
│   │   ├── ocr_extractor.py   # Tesseract OCR wrapper
│   │   ├── vision_extractor.py# Azure/OpenAI Vision wrapper
│   │   ├── llm_extractor.py   # LLM-based extraction
│   │   └── rule_parser.py     # Rule-based field parsing
│   ├── validators/
│   │   ├── field_validator.py # Validate extracted fields
│   │   ├── comparison.py      # Compare Pipeline A vs B
│   │   └── quality_metrics.py # Calculate quality scores
│   ├── utils/
│   │   ├── image_processor.py # Image preprocessing
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging utility
│   └── main.py                # Main execution script
├── output/
│   ├── output.csv             # Final extracted fields
│   └── comparison_report.csv  # Pipeline A vs B comparison
├── tests/
│   ├── test_pipelines.py
│   ├── test_extractors.py
│   └── test_validators.py
├── notebooks/
│   ├── 01_eda.ipynb           # Exploratory data analysis
│   ├── 02_pipeline_a_demo.ipynb
│   └── 03_pipeline_b_demo.ipynb
├── config/
│   ├── settings.yaml          # Configuration file
│   └── field_patterns.yaml    # Regex patterns for rule-based parsing
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanketkulharia24-oss/AI_Invoice_agent.git
   cd AI_Invoice_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and paths
   ```

5. **Prepare data**
   ```bash
   # Download dataset from Kaggle
   # Extract invoice images to: data/invoices/
   ```

### Usage

```bash
# Run full pipeline
python src/main.py

# Run specific pipeline
python src/main.py --pipeline a
python src/main.py --pipeline b

# Process single image
python src/main.py --image path/to/invoice.jpg

# Generate comparison report
python src/main.py --compare
```

## 🔧 Configuration

Edit `.env` file with:
- Azure credentials (if using Computer Vision)
- OpenAI API key (if using Vision API)
- Data paths
- Processing parameters

See `.env.example` for all available options.

## 📊 Pipelines

### Pipeline A: OCR + Rule-Based Parsing
- **OCR**: Tesseract OCR for text extraction
- **Parsing**: Regex patterns and rule-based field extraction
- **Advantages**: Fast, deterministic, no external API calls
- **Limitations**: May struggle with poor quality images

### Pipeline B: Vision API + LLM Extraction
- **Vision**: Azure Computer Vision or OpenAI Vision API
- **Extraction**: GPT-4/Claude for intelligent field extraction
- **Advantages**: Better handling of varied layouts, context-aware
- **Limitations**: API costs, latency, rate limits

## 📈 Outputs

### output.csv
Contains all extracted fields for each invoice:
```
image_name, seller_name, seller_tax_id, client_name, client_tax_id, 
invoice_number, invoice_date, net_worth, vat, gross_worth, 
pipeline_a_confidence, pipeline_b_confidence
```

### comparison_report.csv
Compares Pipeline A vs B results:
```
image_name, field, pipeline_a_value, pipeline_b_value, match, 
confidence_a, confidence_b, discrepancy_reason
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_pipelines.py

# Run with coverage
pytest --cov=src tests/
```

## 📝 Dataset

**Source**: [Kaggle - High Quality Invoice Images for OCR](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr)

**Structure**: 
- batch_1 > batch_1 > batch1_1 > batch1-0331 to batch1-0381 (50 images)

**Format**: High-quality invoice images in JPG/PNG format

## 🔐 Security

- Never commit `.env` files with real credentials
- Use `.env.example` as template
- Store API keys securely
- Use managed identity where possible (Azure)

## 📚 Resources

- [Tesseract OCR Documentation](https://github.com/UB-Mannheim/tesseract/wiki)
- [Azure Computer Vision API](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Kaggle Dataset](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr)

## 📋 Bonus Features (Optional)

- Custom deep learning model training (PyTorch/TensorFlow)
- Invoice image quality assessment
- Handwritten field detection
- Multi-language support
- Web API interface
- Real-time processing dashboard

## 📄 License

[Add your license here]

## 👤 Author

sanketkulharia24-oss

## 🤝 Contributing

Contributions are welcome! Please create a PR with your improvements.

## 📞 Support

For issues and questions, please open a GitHub issue.
