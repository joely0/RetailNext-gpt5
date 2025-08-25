"""
RetailNext00 GPT-5 Fashion Matching System - Streamlit App
A modern, Material Design-inspired web interface for AI-powered fashion recommendations.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

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
        font-size: 3rem;
        font-weight: 300;
        color: #1976D2;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Roboto', sans-serif;
    }
    
    .sub-header {
        font-size: 1.5rem;
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
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">�� RetailNext00</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header" style="text-align: center;">AI-Powered Fashion Matching System</p>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="info-message">
        <strong>🚀 Welcome!</strong> This AI-powered system analyzes clothing images and suggests 
        compatible outfit combinations using OpenAI's GPT-5 Vision and semantic search.
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<h2 class="sub-header">✨ Key Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Image Analysis</h3>
            <p>Uses GPT-5 Vision to identify clothing items and styles in uploaded images.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Matching</h3>
            <p>Finds compatible clothing items using AI-powered semantic search and embeddings.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Style Validation</h3>
            <p>AI-powered compatibility checking with detailed reasoning for each recommendation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Interface
    st.markdown('<h2 class="sub-header">📱 Try It Out</h2>', unsafe_allow_html=True)
    
    # Image Upload Section
    st.markdown("""
    <div class="upload-area">
        <h3>📤 Upload a Clothing Image</h3>
        <p>Upload an image of clothing to get AI-powered style recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload a clear image of clothing to analyze"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        st.markdown('<h3 class="sub-header">🖼️ Uploaded Image</h3>', unsafe_allow_html=True)
        
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
            
            if st.button("🚀 Analyze Image & Find Matches", type="primary"):
                st.markdown("""
                <div class="success-message">
                    <strong>Coming Soon!</strong> The AI analysis functionality will be integrated here.
                    For now, you can test the core system using the demo script.
                </div>
                """, unsafe_allow_html=True)
    
    # Demo Information
    st.markdown('<h2 class="sub-header">🧪 Test the System</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔧 Current Status</h3>
        <p>The core AI functionality is working perfectly! You can test it by running:</p>
        <code>python scripts/run_demo.py</code>
        <br><br>
        <strong>What's Working:</strong>
        <ul>
            <li>✅ GCP Cloud Storage integration</li>
            <li>✅ AI image analysis with GPT-5</li>
            <li>✅ Semantic search and matching</li>
            <li>✅ Professional Streamlit interface</li>
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
