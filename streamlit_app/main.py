"""
RetailNext - AI Fashion Recommendation System
Modern Streamlit interface using the RetailNext UX skin
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

# Import the UX skin
from ui_skin import mount_ui, render_navbar, render_footer, hero, section, cards, steps

# Mount the UI skin
mount_ui(title="RetailNext — AI Outfit Assistant", favicon="🛍️")

def main():
    # Render the navbar (without navigation links)
    render_navbar(links=[], cta=None)
    
    # Hero section
    hero(
        title="Turn product images into personalised outfit ideas.",
        subtitle="A retail solution that analyses clothing images, embeds style descriptors, searches a vector database, and suggests matching items",
        eyebrow="AI Outfit Assistant"
    )
    
    # Main functionality section
    
    # File uploader in a card
    st.markdown("<div class='rnx-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the clothing item you want to match"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display the uploaded image
        st.markdown("<div class='rnx-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Uploaded Image</h3>", unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        # Display image in a smaller, contained box
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(image, width=300, caption="Your uploaded image")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Convert image to base64 for analysis
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Custom styled Streamlit button with purple gradient
        st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(135deg, #7c5cff, #8b5cf6) !important;
            color: white !important;
            border-radius: 999px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,.35) !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 40px rgba(0,0,0,.45) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Analyze & Find Matches", type="primary"):
            with st.spinner("Analyzing your image with GPT-5..."):
                try:
                    # Analyze the image
                    analysis = analyze_image(img_str, ["Tshirts", "Kurtas", "Casual Shoes", "Shorts", "Trousers", "Sports Shoes", "Track Pants", "Flip Flops", "Jeans", "Sandals", "Night suits", "Formal Shoes", "Jackets", "Sweatshirts", "Tracksuits", "Rain Trousers", "Free Gifts", "Sweaters", "Lounge Pants", "Basketballs", "Waistcoat", "Lounge Shorts", "Ties"])
                    
                    # Parse the analysis
                    try:
                        analysis_data = json.loads(analysis)
                        st.success("✅ Image analysis complete!")
                        
                        # Display what was detected in the uploaded image using the new result box
                        from ui_skin import result_box
                        
                        # Create fields for the result box
                        fields = {}
                        if 'category' in analysis_data:
                            fields['Item Category'] = analysis_data['category']
                        if 'gender' in analysis_data:
                            fields['Target Gender'] = analysis_data['gender']
                        
                        # Get AI style recommendations
                        matches = analysis_data.get('items', [])
                        
                        # Display everything in one beautiful result box
                        result_box(
                            title="Item Analysis Results",
                            fields=fields,
                            matches=matches
                        )
                        
                        # Find matching items from catalog
                        section("Finding Similar Items", "Searching our catalog for items that match the AI recommendations...")
                        
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
                            section("Catalog Matches Found", f"Found {len(matches)} items in our catalog that match the AI recommendations!")
                            
                            # Display matches in cards
                            match_cards = []
                            for i, match in enumerate(matches[:5]):
                                card_content = f"""
                                <div class='rnx-card'>
                                    <h3>{match.get('productDisplayName', 'Unknown Item')}</h3>
                                    <p class='rnx-muted'>
                                        <strong>Category:</strong> {match.get('articleType', 'N/A')}<br/>
                                        <strong>Gender:</strong> {match.get('gender', 'N/A')}<br/>
                                        <strong>Color:</strong> {match.get('baseColour', 'N/A')}<br/>
                                        <strong>Season:</strong> {match.get('season', 'N/A')}<br/>
                                        <strong>Usage:</strong> {match.get('usage', 'N/A')}
                                    </p>
                                </div>
                                """
                                match_cards.append(("Match " + str(i+1), card_content))
                            
                            # Display matches in columns
                            cols = st.columns(min(3, len(match_cards)))
                            for i, (title, content) in enumerate(match_cards):
                                with cols[i % len(cols)]:
                                    st.markdown(content, unsafe_allow_html=True)
                                    
                                    # Show product image if available
                                    try:
                                        # Get the corresponding match data for this card
                                        current_match = matches[i]
                                        image_filename = f"{current_match.get('id', 'unknown')}.jpg"
                                        image_path = f"data/sample_clothes/sample_images/{image_filename}"
                                        
                                        if os.path.exists(image_path):
                                            st.image(image_path, caption=f"ID: {current_match.get('id', 'N/A')}", width=210)
                                        else:
                                            st.markdown("""
                                            <div style="
                                                width: 100%; 
                                                height: 150px; 
                                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                                border-radius: 10px;
                                                display: flex;
                                                align-items: center;
                                                justify-content: center;
                                                color: white;
                                                font-size: 24px;
                                            ">
                                                👔
                                            </div>
                                            """, unsafe_allow_html=True)
                                    except Exception as e:
                                        st.error(f"Error loading image: {e}")
                                    
                                    # Guardrails compatibility check
                                    st.markdown("<div class='rnx-card'>", unsafe_allow_html=True)
                                    st.markdown("<h4>Compatibility Analysis</h4>", unsafe_allow_html=True)
                                    try:
                                        if 'img_str' in locals():
                                            from guardrails import check_match
                                            
                                            # Get the suggested item image as base64
                                            with open(image_path, "rb") as img_file:
                                                suggested_img_base64 = base64.b64encode(img_file.read()).decode()
                                            
                                            # Run the compatibility check
                                            compatibility_result = check_match(img_str, suggested_img_base64)
                                            
                                            try:
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
                                    st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.warning("❌ No matching items found. Try uploading a different image.")
                            
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Error parsing analysis response: {e}")
                        st.info(f"Raw response: {analysis}")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                    st.info("Please try again with a different image.")
    
    # How it works section
    section("How It Works", "Our AI-powered system analyzes your clothing and finds perfect matches in three simple steps:", anchor="how")
    steps([
        "<strong>Upload your item</strong><br/><span class='rnx-muted'>Provide a clear image of the clothing you want to match.</span>",
        "<strong>AI analysis</strong><br/><span class='rnx-muted'>GPT-5 analyzes style, color, and category attributes.</span>",
        "<strong>Smart matching</strong><br/><span class='rnx-muted'>Our system finds complementary items using semantic search.</span>",
        "<strong>Get recommendations</strong><br/><span class='rnx-muted'>Receive curated outfit suggestions with compatibility validation.</span>",
    ])
    
    # Features section
    section("Key Features", "What makes RetailNext special:", anchor="features")
    cards([
        ("AI Image Analysis", "GPT-5 Vision analyzes clothing images to understand style, color, and category."),
        ("Semantic Search", "Find similar items using OpenAI embeddings and vector similarity."),
        ("Smart Filtering", "Get complementary items from different categories for complete outfits."),
        ("AI Validation", "Guardrails system validates outfit compatibility with detailed reasoning."),
    ], columns=2)
    
    # Technical details section
    section("Technical Details", "Built with cutting-edge AI technology:", anchor="tech")
    cards([
        ("GPT-5 Vision", "Latest OpenAI model for advanced image understanding."),
        ("Text Embeddings", "text-embedding-3-large for semantic similarity search."),
        ("Vector Database", "Fast cosine similarity search over product catalog."),
        ("AI Guardrails", "Intelligent compatibility validation system."),
    ], columns=2)
    
    # Render the footer
    render_footer()

if __name__ == "__main__":
    main()
