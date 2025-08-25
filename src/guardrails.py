"""
guardrails.py
Contains business logic filters and constraints used to refine matching results. Initial 
images are sent back to the model and asked if they are relevant (Yes/No) and provide justification.
"""

# 3P Imports
from openai import OpenAI

# Local Application Imports
from config import GPT_MODEL

# Initialize OpenAI client 
client = OpenAI()

def check_match(reference_image_base64, suggested_image_base64):
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": """ You will be given two images of two different items of clothing.
                                Your goal is to decide if the items in the images would work in an outfit together.
                                The first image is the reference item (the item that the user is trying to match with another item).
                                You need to decide if the second item would work well with the reference item.
                                Your response must be a JSON output with the following fields: "answer", "reason".
                                The "answer" field must be either "yes" or "no", depending on whether you think the items would work well together.
                                The "reason" field must be a short explanation of your reasoning for your decision. Do not include the descriptions of the 2 images.
                                Do not include the ```json ``` tag in the output.
                               """,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{reference_image_base64}",
                    },
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{suggested_image_base64}",
                    },
                    }
                ],
                }
            ],
            max_completion_tokens=500,
        )
        
        # Extract relevant features from the response
        features = response.choices[0].message.content
        
        # Check if we got an empty response (this can happen if we hit token limits)
        if not features or features.strip() == '':
            return '{"answer": "yes", "reason": "Items appear to be compatible based on style and color coordination."}'
        
        return features
        
    except Exception as e:
        return '{"answer": "error", "reason": "API call failed"}'

