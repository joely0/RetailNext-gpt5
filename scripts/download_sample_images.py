"""
download_sample_images.py
Download sample clothing images for local testing
"""

import os
import requests
from pathlib import Path

def download_sample_images():
    """Download sample images from OpenAI's repository"""
    
    # Create data directory if it doesn't exist
    data_dir = Path("data/sample_clothes/sample_images")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample image IDs from the dataset
    # These are the IDs that appear in the sample_styles.csv
    sample_image_ids = [
        "2133", "7143", "4226", "45534", "45535", "45536", "45537", "45538",
        "45539", "45540", "45541", "45542", "45543", "45544", "45545"
    ]
    
    print("🔄 Downloading sample images...")
    
    # Try different possible URLs for the images
    base_urls = [
        "https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/sample_clothes/sample_images/",
        "https://github.com/openai/openai-cookbook/raw/main/examples/data/sample_clothes/sample_images/"
    ]
    
    downloaded_count = 0
    
    for image_id in sample_image_ids:
        image_filename = f"{image_id}.jpg"
        local_path = data_dir / image_filename
        
        # Skip if already downloaded
        if local_path.exists():
            print(f"✅ {image_filename} already exists")
            downloaded_count += 1
            continue
        
        # Try to download from different URLs
        downloaded = False
        for base_url in base_urls:
            try:
                url = base_url + image_filename
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Downloaded {image_filename}")
                    downloaded_count += 1
                    downloaded = True
                    break
                else:
                    print(f"❌ Failed to download {image_filename} from {url} (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"❌ Error downloading {image_filename} from {url}: {e}")
                continue
        
        if not downloaded:
            print(f"⚠️  Could not download {image_filename} from any source")
    
    print(f"\n🎉 Downloaded {downloaded_count} images to {data_dir}")
    return downloaded_count > 0

if __name__ == "__main__":
    download_sample_images()
