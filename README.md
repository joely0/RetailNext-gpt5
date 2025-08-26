# RetailNext00 - AI Fashion Recommendation System

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's latest GPT-5 API and embedding-based similarity search.

## 🎯 Features

- **AI Image Analysis**: GPT-5 Vision analyzes clothing images
- **Semantic Search**: Finds similar items using OpenAI embeddings
- **Smart Filtering**: Recommends complementary items from different categories
- **AI Validation**: Guardrails system validates outfit compatibility

## 🛠️ Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/RetailNext00.git
cd RetailNext00

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the demo
python scripts/run_demo.py
```



## 📁 Project Structure

```
RetailNext00/
├── requirements.txt          # Python dependencies
├── src/                     # Core AI modules
│   ├── analysis.py          # Image analysis with GPT-5
│   ├── search_similar_items.py # Semantic search engine
│   ├── guardrails.py        # AI validation system
│   └── data_loader.py       # Data loading utilities
├── data/                    # Sample clothing data
└── scripts/                 # Utility scripts
    └── run_demo.py          # Main demo script
```

## 🔑 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for GPT-5 and embeddings

## 📊 How It Works

1. **Image Analysis**: GPT-5 Vision analyzes clothing images and suggests complementary items
2. **Semantic Search**: System finds similar items using OpenAI embeddings
3. **Smart Filtering**: Recommends items from different categories for complete outfits
4. **AI Validation**: Guardrails system validates outfit compatibility with detailed reasoning

## 🎨 Built With

- **OpenAI GPT-5**: Image analysis and understanding
- **OpenAI Embeddings**: Semantic similarity search
- **Pandas**: Data manipulation and analysis
- **Python**: Command-line interface

## 📝 License

N/A - Demo project for OpenAI Solutions Engineer interview