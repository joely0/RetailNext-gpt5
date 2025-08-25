"""
test_streamlit.py
Simple test to verify Streamlit app functionality
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test if all required modules can be imported."""
    try:
        from analysis import analyze_image
        print("✅ analysis module imported")
        
        from data_loader import load_clothing_data
        print("✅ data_loader module imported")
        
        from search_similar_items import find_matching_items_with_rag
        print("✅ search_similar_items module imported")
        
        from guardrails import check_match
        print("✅ guardrails module imported")
        
        import streamlit as st
        print("✅ streamlit imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_loading():
    """Test if data can be loaded."""
    try:
        from data_loader import load_clothing_data
        data = load_clothing_data()
        print(f"✅ Data loaded successfully: {len(data)} items")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Streamlit App Components...\n")
    
    imports_ok = test_imports()
    data_ok = test_data_loading()
    
    if imports_ok and data_ok:
        print("\n🎉 All tests passed! Streamlit app should work correctly.")
        print("\nTo run the app:")
        print("cd streamlit_app")
        print("streamlit run main.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
