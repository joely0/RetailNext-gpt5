#!/usr/bin/env python3
"""
run_streamlit.py
Simple launcher for the Streamlit app
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit app."""
    
    # Get the streamlit app directory
    streamlit_dir = Path(__file__).parent / "streamlit_app"
    
    if not streamlit_dir.exists():
        print("❌ Streamlit app directory not found!")
        return
    
    # Change to streamlit directory and run
    os.chdir(streamlit_dir)
    
    print("🚀 Starting RetailNext00 Streamlit App...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port", "8501"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()
