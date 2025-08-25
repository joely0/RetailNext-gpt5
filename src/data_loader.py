"""
data_loader.py
Utility for loading clothing data from GCP Cloud Storage or local files
"""

import pandas as pd
import requests
from config import EMBEDDINGS_FILE_URL, LOCAL_DATA_PATH
import ast

def load_clothing_data():
    """
    Load clothing data with embeddings from GCP Cloud Storage or local file.
    
    Returns:
        pandas.DataFrame: Clothing data with embeddings
    """
    try:
        # Try to load from GCP Cloud Storage first
        print(f"🔄 Loading data from GCP: {EMBEDDINGS_FILE_URL}")
        response = requests.get(EMBEDDINGS_FILE_URL)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Read CSV from the response content
        from io import StringIO
        csv_content = StringIO(response.text)
        styles_df = pd.read_csv(csv_content, on_bad_lines="skip")
        
        print(f"✅ Successfully loaded {len(styles_df)} items from GCP Cloud Storage")
        
    except Exception as e:
        print(f"⚠️  GCP load failed: {e}")
        print("🔄 Falling back to local file...")
        
        try:
            # Fallback to local file
            styles_df = pd.read_csv(LOCAL_DATA_PATH, on_bad_lines="skip")
            print(f"✅ Successfully loaded {len(styles_df)} items from local file")
        except Exception as local_error:
            print(f"❌ Local file load also failed: {local_error}")
            raise Exception("Could not load clothing data from either GCP or local file")
    
    # Convert embeddings from string to list of floats
    print("🔄 Converting embeddings...")
    styles_df["embeddings"] = styles_df["embeddings"].apply(ast.literal_eval)
    
    print(f"🎯 Data loaded successfully! Shape: {styles_df.shape}")
    print(f"📊 Columns: {list(styles_df.columns)}")
    
    return styles_df

def get_sample_data_info():
    """Get basic information about the loaded data."""
    try:
        df = load_clothing_data()
        print("\n📊 Sample Data Information:")
        print(f"   Total items: {len(df)}")
        print(f"   Gender distribution: {df['gender'].value_counts().to_dict()}")
        print(f"   Categories: {df['articleType'].unique()[:5].tolist()}...")
        print(f"   Colors: {df['baseColour'].unique()[:5].tolist()}...")
        return df
    except Exception as e:
        print(f"❌ Error getting data info: {e}")
        return None
