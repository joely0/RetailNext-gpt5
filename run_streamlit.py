#!/usr/bin/env python3
"""
Launcher script for RetailNext Fashion Recommender Streamlit app.
Run this from the project root directory.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app."""
    print("🚀 Launching RetailNext Fashion Recommender...")
    print("📍 Make sure you're in the project root directory")
    print("🔑 Ensure your OPENAI_API_KEY is set")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app/main.py"):
        print("❌ Error: streamlit_app/main.py not found!")
        print("   Please run this script from the project root directory")
        sys.exit(1)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app/main.py",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
