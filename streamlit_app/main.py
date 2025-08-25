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

# Custom CSS matching RetailNext website design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles - Sophisticated website design */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        min-height: 100vh;
    }
    
    /* Header section - Dark, sophisticated */
    .header-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 3rem 0;
        margin: -2rem -2rem 3rem -2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="%23374151" stroke-width="0.5" opacity="0.3"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.1;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-image {
        max-width: 220px;
        height: auto;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .sub-header {
        font-size: 1.3rem;
        font-weight: 400;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
        text-align: center;
    }
    
    .content-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .upload-area {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        margin: 2rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .upload-area:hover {
        border-color: rgba(255, 255, 255, 0.5);
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }
    
    .success-message {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    .info-message {
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    
    .result-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-1px);
    }
    
    .loading {
        text-align: center;
        padding: 3rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(147, 51, 234, 0.2) 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Custom button styling - Modern and sophisticated */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding: 3rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Clean, minimal styling for file uploader */
    .stFileUploader > div {
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Streamlit sidebar cleanup */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
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
    
    # Header with Logo - Clean and minimal
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    
    # Display the logo - try white logo first, then fallback
    white_logo_path = "../data/website/Retailnextlogo-white-new.png"
    logo_path = "../data/RetailNextlogo.png"
    
    if os.path.exists(white_logo_path):
        st.image(white_logo_path, width=200)
    elif os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        # Fallback if logo not found
        st.markdown('<h1 class="main-header">RetailNext00</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="sub-header">AI-Powered Fashion Matching System</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Upload area with clean styling
    st.markdown("""
    <div class="upload-area">
        <h3 style="font-size: 1.3rem; font-weight: 600; color: #ffffff; margin-bottom: 0.5rem;">Upload a Clothing Image</h3>
        <p style="font-size: 1rem; color: #94a3b8; margin: 0;">Get AI-powered style recommendations for your outfit</p>
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
                            try:
                                # Filter data by gender and different category
                                filtered_items = styles_df.loc[styles_df['gender'].isin([image_analysis['gender'], 'Unisex'])]
                                filtered_items = filtered_items[filtered_items['articleType'] != image_analysis['category']]
                                
                                # Debug info
                                st.info(f"Found {len(filtered_items)} items to search through")
                                
                                # Find matches
                                matching_items = find_matching_items_with_rag(filtered_items, image_analysis['items'])
                                
                                # Debug info
                                st.info(f"AI found {len(matching_items) if matching_items else 0} matching items")
                                
                            except Exception as search_error:
                                st.error(f"Error during search: {search_error}")
                                matching_items = []
                            
                            st.markdown('<h3 class="section-header">🎯 Recommended Matches</h3>', unsafe_allow_html=True)
                            
                            # Display matches in a grid
                            if matching_items and len(matching_items) > 0:
                                cols = st.columns(3)
                                for i, item in enumerate(matching_items[:6]):  # Show top 6 matches
                                    with cols[i % 3]:
                                        try:
                                            # Get product details
                                            product_id = item.get('id', 'Unknown')
                                            product_name = item.get('productDisplayName', 'Product Name Not Available')
                                            category = item.get('articleType', 'Category Not Available')
                                            color = item.get('baseColour', 'Color Not Available')
                                            
                                            # Try to display the product image
                                            image_path = f"../data/sample_clothes/sample_images/{product_id}.jpg"
                                            try:
                                                st.image(image_path, caption=f"ID: {product_id}", use_container_width=True)
                                            except:
                                                # If image not found, show a placeholder
                                                st.markdown("""
                                                <div style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 8px;">
                                                    📷<br>Image Not Available
                                                </div>
                                                """, unsafe_allow_html=True)
                                            
                                            # Display product information
                                            st.markdown(f"""
                                            <div class="result-card">
                                                <strong>{product_name}</strong><br>
                                                <small>Category: {category}</small><br>
                                                <small>Color: {color}</small>
                                            </div>
                                            """, unsafe_allow_html=True)
                                        except Exception as item_error:
                                            st.markdown(f"""
                                            <div class="result-card">
                                                <strong>Product {i+1}</strong><br>
                                                <small>Error: {str(item_error)}</small>
                                            </div>
                                            """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="info-message">
                                    <strong>No matches found</strong> for the uploaded image. 
                                    Try uploading a different clothing item.
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
