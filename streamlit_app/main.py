"""
RetailNext00 - AI Fashion Recommendation System
Simple Streamlit interface for the working recommendation engine
"""

import streamlit as st
import os
import sys
import json
import base64
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Import our core modules
from analysis import analyze_image
from search_similar_items import find_matching_items_with_rag
from guardrails import check_match

# Page configuration
st.set_page_config(
    page_title="RetailNext Fashion Recommender",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .results-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">👔 RetailNext Fashion Recommender</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    **Upload an image of a clothing item to get AI-powered fashion recommendations!**
    
    Our system uses GPT-5 to analyze your clothing and find perfectly matching items from our catalog.
    """)
    
    # File uploader
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📸 Upload Your Clothing Item")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of the clothing item you want to match"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Convert image to base64 for analysis
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        if st.button("🔍 Analyze & Find Matches", type="primary"):
            with st.spinner("Analyzing your image with GPT-5..."):
                try:
                    # Analyze the image
                    analysis = analyze_image(img_str, ["Tshirts", "Kurtas", "Casual Shoes", "Shorts", "Trousers", "Sports Shoes", "Track Pants", "Flip Flops", "Jeans", "Sandals", "Night suits", "Formal Shoes", "Jackets", "Sweatshirts", "Tracksuits", "Rain Trousers", "Free Gifts", "Sweaters", "Lounge Pants", "Basketballs", "Waistcoat", "Lounge Shorts", "Ties"])
                    
                    # Parse the analysis
                    try:
                        analysis_data = json.loads(analysis)
                        st.success("✅ Image analysis complete!")
                        
                        # Display detected items
                        if 'items' in analysis_data:
                            st.subheader("🎯 Detected Items:")
                            for item in analysis_data['items']:
                                st.write(f"• {item}")
                        
                        if 'category' in analysis_data:
                            st.write(f"**Category:** {analysis_data['category']}")
                        if 'gender' in analysis_data:
                            st.write(f"**Gender:** {analysis_data['gender']}")
                        
                        # Find matching items
                        st.subheader("🔍 Searching for Similar Items...")
                        matches = find_matching_items_with_rag(analysis, top_k=5)
                        
                        if matches and len(matches) > 0:
                            st.subheader("🎉 Recommended Matches:")
                            
                            for i, match in enumerate(matches[:5]):
                                with st.expander(f"Match {i+1}: {match['title']}", expanded=True):
                                    col1, col2 = st.columns([1, 2])
                                    
                                    with col1:
                                        if 'image_url' in match:
                                            st.image(match['image_url'], width=150)
                                        else:
                                            st.write("🖼️ Image not available")
                                    
                                    with col2:
                                        st.write(f"**Title:** {match['title']}")
                                        st.write(f"**Category:** {match['category']}")
                                        st.write(f"**Gender:** {match['gender']}")
                                        if 'price' in match:
                                            st.write(f"**Price:** ${match['price']}")
                                        
                                        # Guardrails check
                                        st.write("**Compatibility Check:**")
                                        try:
                                            guardrail_result = check_match(img_str, match.get('image_base64', ''))
                                            guardrail_data = json.loads(guardrail_result)
                                            
                                            if guardrail_data.get('answer') == 'yes':
                                                st.success(f"✅ {guardrail_data.get('reason', 'Items are compatible!')}")
                                            else:
                                                st.warning(f"⚠️ {guardrail_data.get('reason', 'Items may not be compatible.')}")
                                        except Exception as e:
                                            st.info("ℹ️ Compatibility check not available")
                        else:
                            st.warning("❌ No matching items found. Try uploading a different image.")
                            
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Error parsing analysis response: {e}")
                        st.info(f"Raw response: {analysis}")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                    st.info("Please try again with a different image.")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About This System")
        st.markdown("""
        **RetailNext Fashion Recommender** uses advanced AI to:
        
        - 🧠 **Analyze clothing images** with GPT-5
        - 🔍 **Find similar items** using semantic search
        - ✅ **Validate compatibility** with AI guardrails
        - 🎯 **Provide personalized recommendations**
        
        **Perfect for:**
        - Fashion retailers
        - Personal styling
        - Outfit coordination
        """)
        
        st.header("🔧 Technical Details")
        st.markdown("""
        - **AI Model:** GPT-5 (OpenAI)
        - **Embeddings:** text-embedding-3-large
        - **Search:** Cosine similarity
        - **Validation:** AI-powered guardrails
        """)

if __name__ == "__main__":
    main()
