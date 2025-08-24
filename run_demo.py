# Standard Library Imports
import ast
import base64
import json
import os

# 3P Imports
import pandas as pd
from IPython.display import Image, display, HTML

# Local Application Imports
from analysis import analyze_image
from utils.guardrails import check_match
from match.search_similar_items import find_matching_items_with_rag

# Load the dataset with embeddings
styles_df = pd.read_csv("data/sample_clothes/sample_styles_with_embeddings.csv", on_bad_lines="skip")
print(styles_df.columns)


# Convert the 'embeddings' column from string to list of floats
styles_df["embeddings"] = styles_df["embeddings"].apply(ast.literal_eval)


def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode('utf-8')

## Test Prompt including sample images

# Set the path to the images and select a test image
image_path = "../openai-cookbook/examples/data/sample_clothes/sample_images/"
test_images = ["2133.jpg", "7143.jpg", "4226.jpg"]

# Encode the test image to base64
reference_image = image_path + test_images[0]
encoded_image = encode_image_to_base64(reference_image)

## WRAP IN OWN FUNCTION TODO run_image_analysis etc

# Encode the test image to base64
reference_image = image_path + test_images[0]
encoded_image = encode_image_to_base64(reference_image)

# Select the unique subcategories from the DataFrame
unique_subcategories = styles_df['articleType'].unique()

# Analyze the image and return the results
analysis = analyze_image(encoded_image, unique_subcategories)
image_analysis = json.loads(analysis)

# Display the image and the analysis results
display(Image(filename=reference_image))
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
        
    # Path to the image file
    image_path = f'../openai-cookbook/examples/data/sample_clothes/sample_images/{item_id}.jpg'
    paths.append(image_path)
    html += f'<img src="{image_path}" style="display:inline;margin:1px"/>'

# Print the matching item description as a reminder of what we are looking for
print(item_descs)

# Display the image
display(HTML(html))


# Select the unique paths for the generated images
paths = list(set(paths))

for path in paths:
    # Run a check to see if file exists
    if not os.path.exists(path):
        print(f"⚠️ Image not found, skipping: {path}")
        continue
    # Encode the test image to base64
    suggested_image = encode_image_to_base64(path)
    
    # Check if the items match
    match = json.loads(check_match(encoded_image, suggested_image))
    
    # Display the image and the analysis results
    if match["answer"] == 'yes':
        display(Image(filename=path))
        print("The items match!")
        print(match["reason"])