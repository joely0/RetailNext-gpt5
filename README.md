# RetailNext00

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's API and embedding-based similarity search.

Built for basic local demo. 

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
python run_demo.py
```

## Folder Structure

```
RetailNext00/
├── main.py
├── config.py
├── requirements.txt
│
├── match/
│   ├── image_match.py
│   └── search_similar_items.py
│
├── embeddings/
│   ├── generate_embeddings.py
│   └── embed_samples_load.py
│
├── utils/
│   └── guardrails.py
│
├── data/
│   └── sample_clothes/
│       ├── sample_images/
│       ├── sample_styles.csv
│       └── sample_styles_with_embeddings.csv
│
├── run_demo.py
└── README.md
```


## License

N/A - just testing this cookbook