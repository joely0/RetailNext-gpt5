# Standard Library Imports
import ast
import base64
import json
import os

# 3P Imports
import pandas as pd
from IPython.display import Image, display, HTML

# Local Application Imports
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from analysis import analyze_image
from guardrails import check_match
from search_similar_items import find_matching_items_with_rag

# Load the dataset with embeddings from GCP Cloud Storage

def encode_image_from_url(image_url):
    """Download image from URL and encode to base64."""
    import requests
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        encoded_image = base64.b64encode(response.content)
        return encoded_image.decode("utf-8")
    except Exception as e:
        print(f"❌ Error downloading image from {image_url}: {e}")
        return None

def encode_image_to_base64(image_path):
    """Legacy function for local files."""
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode("utf-8")
from data_loader import load_clothing_data
styles_df = load_clothing_data()





## Test Prompt including sample images

# Set the path to the images and select a test image
# Try local images first, then fall back to URLs
base_image_url = "https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/sample_clothes/sample_images/"
local_image_path = "data/sample_clothes/sample_images/"
test_images = ["2133.jpg", "7143.jpg", "4226.jpg"]

# Try to use local image first
reference_image_path = local_image_path + test_images[0]
if os.path.exists(reference_image_path):
    print(f"📁 Using local image: {reference_image_path}")
    encoded_image = encode_image_to_base64(reference_image_path)
else:
    print(f"🌐 Using remote image: {base_image_url + test_images[0]}")
    reference_image_url = base_image_url + test_images[0]
    encoded_image = encode_image_from_url(reference_image_url)

# Select the unique subcategories from the DataFrame
unique_subcategories = styles_df['articleType'].unique()

# Analyze the image and return the results
analysis = analyze_image(encoded_image, unique_subcategories)
image_analysis = json.loads(analysis)

# Display the image and the analysis results
if 'reference_image_url' in locals():
    print(f"🖼️  Sample image URL: {reference_image_url}")
else:
    print(f"🖼️  Sample image path: {reference_image_path}")
print(image_analysis)

## Break this out into own file TODO match_from_image
# Extract the relevant features from the analysis
item_descs = image_analysis['items']
item_category = image_analysis['category']
item_gender = image_analysis['gender']


# Filter data such that we only look through the items of the same gender (or unisex) and different category
filtered_items = styles_df.loc[styles_df['gender'].isin([item_gender, 'Unisex'])]
filtered_items = filtered_items[filtered_items['articleType'] != item_category]
print(str(len(filtered_items)) + " Remaining Items")

# Find the most similar items based on the input item descriptions
matching_items = find_matching_items_with_rag(filtered_items, item_descs)

# Display the matching items (this will display 2 items for each description in the image analysis)
html = ""
paths = []
for i, item in enumerate(matching_items):
    item_id = item['id']
        
    # Path to the image file - try local first, then remote
    local_image_path = f"data/sample_clothes/sample_images/{item_id}.jpg"
    if os.path.exists(local_image_path):
        image_path = local_image_path
        html += f"<img src=\"{local_image_path}\" style=\"display:inline;margin:1px;max-width:200px\"/>"
    else:
        image_url = f"{base_image_url}{item_id}.jpg"
        image_path = image_url
        html += f"<img src=\"{image_url}\" style=\"display:inline;margin:1px;max-width:200px\"/>"
    paths.append(image_path)

# Print the matching item description as a reminder of what we are looking for
print(item_descs)

# Display the image
display(HTML(html))


# Select the unique paths for the generated images
paths = list(set(paths))

for path in paths:
    # Handle both local files and URLs
    if path.startswith("http"):
        # Remote URL
        suggested_image = encode_image_from_url(path)
    elif os.path.exists(path):
        # Local file
        suggested_image = encode_image_to_base64(path)
    else:
        print(f"⚠️ File not found, skipping: {path}")
        continue
    
    # Check if the items match
    match = json.loads(check_match(encoded_image, suggested_image))
    
    # Display the image and the analysis results
    if match["answer"] == 'yes':
        # Use HTML display for URLs instead of local file display
        display(HTML(f'<img src="{path}" style="max-width:300px;margin:10px;border:2px solid green;"/>'))
        print("The items match!")
        print(match["reason"])