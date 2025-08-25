# RetailNext00

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's latest GPT-5-mini API and embedding-based similarity search.

Built with clean architecture principles and production-ready structure.

Original cookbook - https://cookbook.openai.com/examples/how_to_combine_gpt4o_with_rag_outfit_assistant

## Installation & Setup Guide

```bash
# Clone the repository
git clone https://github.com/joely0/RetailNext00.git
cd RetailNext00

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## ▶Usage

```bash
# Test your setup
python test_setup.py

# Run the main demo
python scripts/run_demo.py
```

## Folder Structure

```
RetailNext00/
├── src/                           # Core application code
│   ├── main.py                    # Main entry point
│   ├── config.py                  # Configuration
│   ├── analysis.py                # Image analysis
│   ├── data_loader.py            # Data loading
│   ├── guardrails.py             # Content validation
│   ├── image_match.py            # Image matching
│   └── search_similar_items.py   # Semantic search
│
├── scripts/                       # Utility scripts
│   ├── run_demo.py               # Main demo
│   └── download_sample_images.py # Download images
│
├── streamlit_app/                 # Web interface
├── data/                          # Sample data
└── tests/                         # Test suite
```


## License

N/A - just testing this cookbook