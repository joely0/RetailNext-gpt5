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
from data_loader import load_clothing_data

# Page configuration
st.set_page_config(
    page_title="RetailNext Clothing Matchmaker",
    page_icon="data/website/favicon.ico",
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
    st.markdown('<h1 class="main-header">RetailNext Clothing Matchmaker</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    **Upload an image of a clothing item to get AI-powered fashion recommendations!**
    
    Our system uses GPT-5 to analyze your clothing and find perfectly matching items from our catalog.
    """)
    
    # File uploader
    st.subheader("📸 Upload Your Clothing Item")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the clothing item you want to match"
    )
    
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
                        
                        # Display what was detected in the uploaded image
                        st.subheader("🔍 Item Analysis:")
                        if 'category' in analysis_data:
                            st.write(f"**Item Category:** {analysis_data['category']}")
                        if 'gender' in analysis_data:
                            st.write(f"**Target Gender:** {analysis_data['gender']}")
                        
                        # Display AI style recommendations
                        if 'items' in analysis_data:
                            st.subheader("💡 AI Style Recommendations:")
                            st.info("Based on your uploaded item, here are 3 complementary pieces that would complete the outfit:")
                            for i, item in enumerate(analysis_data['items'], 1):
                                st.write(f"{i}. {item}")
                        
                        # Find matching items from catalog
                        st.subheader("🔍 Finding Similar Items in Our Catalog...")
                        st.info("Searching our catalog for items that match the AI style recommendations...")
                        
                        # Load clothing data
                        try:
                            df_items = load_clothing_data()
                            
                            # Extract item descriptions from AI analysis for search
                            item_descriptions = analysis_data.get('items', [])
                            
                            # Find matching items
                            matches = find_matching_items_with_rag(df_items, item_descriptions)
                        except Exception as e:
                            st.error(f"❌ Error loading catalog data: {e}")
                            matches = []
                        
                        if matches and len(matches) > 0:
                            st.subheader("🎉 Catalog Matches Found:")
                            st.success(f"Found {len(matches)} items in our catalog that match the AI recommendations!")
                            
                            for i, match in enumerate(matches[:5]):
                                with st.expander(f"Match {i+1}: {match.get('productDisplayName', 'Unknown Item')}", expanded=True):
                                    col1, col2 = st.columns([1, 2])
                                    
                                    with col1:
                                        # Display the actual product image from the sample_images folder
                                        try:
                                            # Construct image path based on catalog item ID
                                            image_filename = f"{match.get('id', 'unknown')}.jpg"
                                            image_path = f"data/sample_clothes/sample_images/{image_filename}"
                                            
                                            # Check if image file exists
                                            if os.path.exists(image_path):
                                                st.image(image_path, width=150, caption=f"ID: {match.get('id', 'N/A')}")
                                            else:
                                                # Fallback to placeholder if image doesn't exist
                                                st.markdown("""
                                                <div style="
                                                    width: 150px; 
                                                    height: 150px; 
                                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                                    border-radius: 10px;
                                                    display: flex;
                                                    align-items: center;
                                                    justify-content: center;
                                                    color: white;
                                                    font-size: 48px;
                                                    margin: 0 auto;
                                                ">
                                                    👔
                                                </div>
                                                """, unsafe_allow_html=True)
                                                st.caption(f"Image not found: {image_filename}")
                                        except Exception as e:
                                            st.error(f"Error loading image: {e}")
                                    
                                    with col2:
                                        st.write(f"**Product Name:** {match.get('productDisplayName', 'N/A')}")
                                        st.write(f"**Category:** {match.get('articleType', 'N/A')}")
                                        st.write(f"**Gender:** {match.get('gender', 'N/A')}")
                                        st.write(f"**Color:** {match.get('baseColour', 'N/A')}")
                                        st.write(f"**Season:** {match.get('season', 'N/A')}")
                                        st.write(f"**Usage:** {match.get('usage', 'N/A')}")
                                        
                                        # Show why this item was recommended
                                        if 'similarity_score' in match:
                                            st.write(f"**Match Score:** {match.get('similarity_score', 'N/A'):.3f}")
                                            st.info(f"🎯 **Recommended because:** This item has similar style, color, and category characteristics to your uploaded image")
                                        elif 'score' in match:
                                            st.write(f"**Match Score:** {match.get('score', 'N/A'):.3f}")
                                            st.info(f"🎯 **Recommended because:** This item has similar style, color, and category characteristics to your uploaded image")

                                        
                                        # Guardrails check
                                        st.write("**Why This is a Good Match:**")
                                        try:
                                            # Run compatibility validation if we have the uploaded image
                                            if 'img_str' in locals():
                                                from guardrails import check_match
                                                
                                                # Get the suggested item image as base64
                                                with open(image_path, "rb") as img_file:
                                                    suggested_img_base64 = base64.b64encode(img_file.read()).decode()
                                                
                                                # Run the compatibility check
                                                compatibility_result = check_match(img_str, suggested_img_base64)
                                                
                                                try:
                                                    # Parse the JSON response - import json at the top level
                                                    compatibility_data = json.loads(compatibility_result)
                                                    
                                                    if compatibility_data.get('answer') == 'yes':
                                                        st.success(f"✅ **Compatible!** {compatibility_data.get('reason', 'These items work well together!')}")
                                                    else:
                                                        st.warning(f"⚠️ **Limited compatibility:** {compatibility_data.get('reason', 'Consider alternatives')}")
                                                except:
                                                    st.info(f"ℹ️ {compatibility_result}")
                                            else:
                                                st.info("ℹ️ Upload an image to see compatibility analysis")
                                        except Exception as e:
                                            st.info(f"ℹ️ Compatibility analysis: {str(e)}")
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
        **RetailNext Clothing Matchmaker**
        
        - 🧠 **Analyze clothing images** with GPT-5
        - 🔍 **Find similar items** using semantic search
        - ✅ **Validate compatibility** with AI guardrails
        - 🎯 **Provide personalized recommendations**
        

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
