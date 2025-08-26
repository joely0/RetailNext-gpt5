"""
analysis.py
This module defines the `analyze_image` function, which uses OpenAI's GPT-5 mini 
API to analyze a clothing image and return structured fashion metadata. It provides
an example input and output prompt (one shot example). The output (JSON format) includes a predefined structure
including, items, category, gender 
"""

# 3P Imports
from openai import OpenAI

# Local Application Imports
from config import GPT_MODEL

# Initialize OpenAI client
client = OpenAI()

# Includes example of expected output, to future clarify expected output. 

def analyze_image(image_base64, subcategories):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Given an image of an item of clothing, analyze the item and generate a JSON output with the following fields: "items", "category", and "gender".

                           ANALYSIS TASK:
                           - Identify what clothing item is in the uploaded image
                           - Determine the category from this list: {subcategories}
                           - Determine the gender from this list: [Men, Women, Boys, Girls, Unisex]

                           RECOMMENDATION TASK:
                           - Generate exactly 3 complementary clothing items that would complete an outfit with the uploaded item
                           - Each recommended item should include style, color, and gender
                           - These are suggestions for what would go well together, not items detected in the image

                           OUTPUT FORMAT:
                           {{
                             "items": ["Item 1 description", "Item 2 description", "Item 3 description"],
                             "category": "Category of uploaded item",
                             "gender": "Gender of uploaded item"
                           }}

                           Example Input: An image of a black leather jacket
                           Example Output: {{"items": ["Fitted White Women's T-shirt", "White Canvas Sneakers", "Women's Black Skinny Jeans"], "category": "Jackets", "gender": "Women"}}

                           Do not include the ```json ``` tag in the output.
                           """,
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                },
                }
            ],
            }
        ]
    )
    # Extract relevant features from the response
    features = response.choices[0].message.content
    return features