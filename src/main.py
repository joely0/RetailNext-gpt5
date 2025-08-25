"""
main.py
Entry point for the Outfit Assistant demo. Generates a caption from an input image using GPT-4o mini
and retrieves similar items from a pre-embedded catalog using semantic search.
"""

# Standard Library Imports
import ast
import concurrent
import json
from typing import List

# 3P imports
import numpy as np
import pandas as pd
import tiktoken
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt
from IPython.display import Image, display, HTML
from openai import OpenAI

# Local Application Imports
from config import GPT_MODEL, EMBEDDING_MODEL

# Initialize OpenAI client - Need to add API key
client = OpenAI()