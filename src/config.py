"""
config.py
Contains basic OpenAI configs and cloud storage settings
"""

GPT_MODEL = "gpt-5-mini"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_COST_PER_1K_TOKENS = 0.00013

# GCP Cloud Storage Configuration
GCP_BUCKET_URL = "https://storage.googleapis.com/retailnext00"
EMBEDDINGS_FILE_URL = f"{GCP_BUCKET_URL}/sample_styles_with_embeddings.csv"

# Local fallback (for development)
LOCAL_DATA_PATH = "data/sample_clothes/sample_styles_with_embeddings.csv"
