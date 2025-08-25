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

# Custom CSS for Pitch Deck-Inspired Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.4rem;
        font-weight: 400;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.01em;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.01em;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin: 1.5rem 0;
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
    }
    
    .success-message {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10B981;
        font-weight: 500;
    }
    
    .info-message {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        color: #1E40AF;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3B82F6;
        font-weight: 500;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        margin: 0.75rem 0;
        border: 1px solid #E5E7EB;
        transition: all 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .loading {
        text-align: center;
        padding: 3rem;
        color: #667eea;
        font-weight: 500;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #6B7280;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid #E5E7EB;
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
    st.markdown('<p class="sub-header">AI-Powered Fashion Matching System</p>', unsafe_allow_html=True)
    
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
    st.markdown('<h2 class="section-header">📷 Upload Your Image</h2>', unsafe_allow_html=True)
    
    # Upload area with better styling
    st.markdown("""
    <div class="upload-area">
        <h3 style="font-size: 1.5rem; font-weight: 600; color: #1F2937; margin-bottom: 1rem;">📷 Choose a Clothing Image</h3>
        <p style="font-size: 1.1rem; color: #6B7280; margin: 0;">Upload a clear image of clothing to get AI-powered style recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a clothing image to analyze",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload a clear image of clothing to get AI-powered recommendations"
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
                        
                        st.markdown('<h3 class="section-header">🔍 AI Analysis Results</h3>', unsafe_allow_html=True)
                        
                        # Display analysis results with custom styling
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{image_analysis['category']}</div>
                                <div class="metric-label">Category</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{image_analysis['gender']}</div>
                                <div class="metric-label">Gender</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{len(image_analysis['items'])}</div>
                                <div class="metric-label">Items Found</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
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
                            
                            st.markdown('<h3 class="section-header">🎯 Recommended Matches</h3>', unsafe_allow_html=True)
                            
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
    
    # Footer
    st.markdown("""
    <div class="footer">
        Built with ❤️ using Streamlit, OpenAI GPT-5, and modern design principles
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
