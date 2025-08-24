"""
embed_samples_load.py
Loads and verifies the clothing catalog from CSV for embedding and matching.
"""

# 3P Imports
import pandas as pd

styles_filepath = "data/sample_clothes/sample_styles.csv"
styles_df = pd.read_csv(styles_filepath, on_bad_lines='skip')
print(styles_df.head())
print("Opened dataset successfully. Dataset has {} items of clothing.".format(len(styles_df)))
