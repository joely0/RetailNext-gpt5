"""
RetailNext00 GPT-5 Fashion Matching System - Streamlit App
A modern, Material Design-inspired web interface for AI-powered fashion recommendations.
"""

import streamlit as st
import sys
import os
import base64
import json
from pathlib import Path
import pandas as pd

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import our AI modules
try:
    from analysis import analyze_image
    from data_loader import load_clothing_data
    from search_similar_items import find_matching_items_with_rag
    from guardrails import check_match
except ImportError as e:
    st.error(f"Error importing AI modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="RetailNext00 - AI Fashion Matching",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Material Design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1976D2;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Roboto', sans-serif;
    }
    
    .sub-header {
        font-size: 1.3rem;
        font-weight: 400;
        color: #424242;
        margin-bottom: 1rem;
        font-family: 'Roboto', sans-serif;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #1976D2;
    }
    
    .upload-area {
        border: 2px dashed #1976D2;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: #F5F5F5;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #E8F5E8;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #4CAF50;
    }
    
    .info-message {
        background: #E3F2FD;
        color: #1976D2;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #2196F3;
    }
    
    .result-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
    }
    
    .loading {
        text-align: center;
        padding: 2rem;
        color: #1976D2;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load clothing data with caching."""
    try:
        return load_clothing_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def encode_image_to_base64(image_file):
    """Convert uploaded image to base64."""
    image_bytes = image_file.read()
    image_file.seek(0)  # Reset file pointer
    return base64.b64encode(image_bytes).decode('utf-8')

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">👔 RetailNext00</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header" style="text-align: center;">AI-Powered Fashion Matching System</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading fashion database..."):
        styles_df = load_data()
    
    if styles_df is None:
        st.error("Failed to load fashion database. Please check your connection.")
        return
    
    # Introduction
    st.markdown("""
    <div class="info-message">
        <strong>🚀 Welcome!</strong> Upload a clothing image and get AI-powered outfit recommendations 
        using OpenAI's GPT-5 Vision and semantic search.
    </div>
    """, unsafe_allow_html=True)
    
    # Main Interface
    st.markdown('<h2 class="sub-header">📤 Upload Your Image</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a clothing image",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload a clear image of clothing to analyze"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption="Your Image", width=300)
        
        with col2:
            st.markdown("""
            <div class="info-message">
                <strong>Image Ready!</strong> Click the button below to analyze this image and get 
                AI-powered fashion recommendations.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Analyze & Find Matches", type="primary"):
                with st.spinner("Analyzing image with AI..."):
                    try:
                        # Encode image
                        encoded_image = encode_image_to_base64(uploaded_file)
                        
                        # Get unique categories for analysis
                        unique_subcategories = styles_df['articleType'].unique()
                        
                        # Analyze the image
                        analysis = analyze_image(encoded_image, unique_subcategories)
                        image_analysis = json.loads(analysis)
                        
                        st.markdown('<h3 class="sub-header">🔍 AI Analysis Results</h3>', unsafe_allow_html=True)
                        
                        # Display analysis results
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Category", image_analysis['category'])
                        with col2:
                            st.metric("Gender", image_analysis['gender'])
                        with col3:
                            st.metric("Items Found", len(image_analysis['items']))
                        
                        # Show detected items
                        st.markdown("**Detected Items:**")
                        for item in image_analysis['items']:
                            st.markdown(f"• {item}")
                        
                        # Find matching items
                        with st.spinner("Finding matching items..."):
                            # Filter data by gender and different category
                            filtered_items = styles_df.loc[styles_df['gender'].isin([image_analysis['gender'], 'Unisex'])]
                            filtered_items = filtered_items[filtered_items['articleType'] != image_analysis['category']]
                            
                            # Find matches
                            matching_items = find_matching_items_with_rag(filtered_items, image_analysis['items'])
                            
                            st.markdown('<h3 class="sub-header">🎯 Recommended Matches</h3>', unsafe_allow_html=True)
                            
                            # Display matches in a grid
                            cols = st.columns(3)
                            for i, item in enumerate(matching_items[:6]):  # Show top 6 matches
                                with cols[i % 3]:
                                    st.markdown(f"""
                                    <div class="result-card">
                                        <strong>{item['productDisplayName']}</strong><br>
                                        <small>Category: {item['articleType']}</small><br>
                                        <small>Color: {item['baseColour']}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="success-message">
                            <strong>✅ Analysis Complete!</strong> The AI has analyzed your image and found 
                            compatible clothing items. Each recommendation is based on semantic similarity 
                            and style compatibility.
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {e}")
                        st.info("Please try with a different image or check your OpenAI API key.")
    
    # Demo Information
    st.markdown('<h2 class="sub-header">🧪 System Status</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>✅ Working Features</h3>
        <ul>
            <li>🖼️ Image upload and processing</li>
            <li>🤖 GPT-5 Vision analysis</li>
            <li>🔍 Semantic search with embeddings</li>
            <li>📊 Fashion database integration</li>
            <li>🎨 Material Design interface</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with ❤️ using Streamlit, OpenAI GPT-5, and Material Design principles
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
