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
        
        # Anchor point for the Analyze & Find Matches button
        st.markdown('<div id="analyze-button"></div>', unsafe_allow_html=True)
        

        
        if st.button("🔍 Analyze & Find Matches", type="primary"):
            with st.spinner("Analyzing your image with GPT-5..."):
                try:
                    # Analyze the image
                    analysis = analyze_image(img_str, ["Tshirts", "Kurtas", "Casual Shoes", "Shorts", "Trousers", "Sports Shoes", "Track Pants", "Flip Flops", "Jeans", "Sandals", "Night suits", "Formal Shoes", "Jackets", "Sweatshirts", "Tracksuits", "Rain Trousers", "Free Gifts", "Sweaters", "Lounge Pants", "Basketballs", "Waistcoat", "Lounge Shorts", "Ties"])
                    
                    # Parse the analysis
                    try:
                        analysis_data = json.loads(analysis)
                        st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #7c5cff, #8b5cf6);
                            color: white;
                            padding: 12px 20px;
                            border-radius: 12px;
                            text-align: center;
                            font-weight: 600;
                            margin: 20px 0;
                            box-shadow: 0 8px 25px rgba(124, 92, 255, 0.3);
                        ">
                            Image analysis complete!
                        </div>
                        """, unsafe_allow_html=True)
                        
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
                        from ui_skin import _inject_result_box_css
                        _inject_result_box_css()
                        st.markdown("""
                        <div class="rnx-result-box">
                          <h3>Finding Similar Items</h3>
                          <p class="rnx-kv">Searching our catalog for items that match the AI recommendations...</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
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
                            st.markdown(f"""
                            <div class="rnx-result-box">
                              <h3>Catalog Matches Found</h3>
                              <p class="rnx-kv">Found {len(matches)} items in our catalog that match</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display matches in cards
                            match_cards = []
                            for i, match in enumerate(matches[:5]):
                                card_content = f"""
                                <div class='rnx-card'>
                                    <h3 style="background: linear-gradient(135deg, #7c5cff, #5eead4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; font-size: 18px; margin-bottom: 12px;">{match.get('productDisplayName', 'Unknown Item')}</h3>
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
                                        image_path = f"../data/sample_clothes/sample_images/{image_filename}"
                                        
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
                                    
                                    # Guardrails compatibility check - only show compatible items
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
                                                
                                                # Only display this item if it's compatible
                                                if compatibility_data.get('answer') == 'yes':
                                                    st.markdown("<div class='rnx-card'>", unsafe_allow_html=True)
                                                    
                                                    # Show compatibility analysis
                                                    st.markdown(f"""
                                                    <div style="
                                                        background: #5eead4;
                                                        color: #0b0b10;
                                                        padding: 12px 16px;
                                                        border-radius: 12px;
                                                        margin: 8px 0;
                                                        box-shadow: 0 4px 15px rgba(94, 234, 212, 0.3);
                                                        width: 100%;
                                                        max-width: 280px;
                                                    ">
                                                        {compatibility_data.get('reason', 'These items work well together!')}
                                                    </div>
                                                    """, unsafe_allow_html=True)
                                                    
                                                    # Action buttons for compatible items
                                                    st.markdown("""
                                                    <div style="display: flex; gap: 12px; margin-top: 16px; justify-content: center; width: 100%; max-width: 280px; margin-left: 0;">
                                                        <a href="#" style="
                                                            display: inline-block;
                                                            background: linear-gradient(135deg, #7c5cff, #8b5cf6);
                                                            color: white;
                                                            padding: 10px 20px;
                                                            border-radius: 999px;
                                                            text-decoration: none;
                                                            box-shadow: 0 10px 30px rgba(0,0,0,.35);
                                                            font-weight: 600;
                                                            font-size: 14px;
                                                        ">
                                                            Find in Store
                                                        </a>
                                                        <a href="#" style="
                                                            display: inline-block;
                                                            background: linear-gradient(135deg, #5eead4, #06b6d4);
                                                            color: white;
                                                            padding: 10px 20px;
                                                            border-radius: 999px;
                                                            text-decoration: none;
                                                            box-shadow: 0 10px 30px rgba(0,0,0,.35);
                                                            font-weight: 600;
                                                            font-size: 14px;
                                                        ">
                                                            Buy Now
                                                        </a>
                                                    </div>
                                                    """, unsafe_allow_html=True)
                                                    
                                                    st.markdown("</div>", unsafe_allow_html=True)
                                                # If not compatible, don't show anything - item is effectively hidden
                                            except:
                                                # If compatibility check fails, don't show the item
                                                pass
                                        else:
                                            st.info("ℹ️ Upload an image to see compatibility analysis")
                                    except Exception as e:
                                        # If there's an error, don't show the item
                                        pass
                        else:
                            st.warning("❌ No matching items found. Try uploading a different image.")
                            
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Error parsing analysis response: {e}")
                        st.info(f"Raw response: {analysis}")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                    st.info("Please try again with a different image.")
    
    # Add spacing between compatibility section and How It Works
    st.markdown("<div style='margin: 60px 0;'></div>", unsafe_allow_html=True)
    
    # How it works section
    st.markdown("<h2 style='font-size:clamp(24px,3vw,34px); margin:0 0 16px; color: #5eead4;'>How It Works</h2>", unsafe_allow_html=True)
    st.markdown("<p class='rnx-muted' style='max-width:740px; margin-bottom: 20px;'>Get outfit recommendations in four simple steps:</p>", unsafe_allow_html=True)
    
    # Simple numbered steps
    st.markdown("### 1. Upload your item")
    st.markdown("Upload a clear image of the clothing you want to match.")
    
    st.markdown("### 2. AI analysis")
    st.markdown("Our AI analyzes style, color, and category details.")
    
    st.markdown("### 3. Smart matching")
    st.markdown("We find complementary items from our catalog.")
    
    st.markdown("### 4. Get recommendations")
    st.markdown("Receive outfit suggestions with compatibility notes.")
    

    
    # Render the footer
    render_footer()

if __name__ == "__main__":
    main()
