# RetailNext00 - AI Fashion Recommendation System

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's latest GPT-5 API and embedding-based similarity search.

## 🎯 Features

- **AI Image Analysis**: GPT-5 Vision analyzes clothing images
- **Semantic Search**: Finds similar items using OpenAI embeddings
- **Smart Filtering**: Recommends complementary items from different categories
- **AI Validation**: Guardrails system validates outfit compatibility
- **Web Interface**: Streamlit app for easy interaction

## 🚀 Quick Start

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

# Run the Streamlit app
python run_streamlit.py
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
├── streamlit_app/           # Web interface
│   ├── main.py              # Main Streamlit application
│   ├── components/          # UI components
│   ├── pages/               # Multi-page navigation
│   └── utils/               # Utility functions
├── data/                    # Sample clothing data
└── scripts/                 # Utility scripts
    └── run_demo.py          # Command-line demo script
```

## 🔑 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for GPT-5 and embeddings

## 🎨 Built With

- **OpenAI GPT-5**: Image analysis and understanding
- **OpenAI Embeddings**: Semantic similarity search
- **Streamlit**: Web interface
- **Pandas**: Data manipulation and analysis
- **Python**: Core functionality

## 📝 License

N/A - Demo project for OpenAI Solutions Engineer interview