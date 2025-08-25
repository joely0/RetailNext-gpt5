"""
test_setup.py
Simple test script to verify OpenAI API key and basic functionality
"""

import os
import sys
from openai import OpenAI

def test_openai_connection():
    """Test if OpenAI API key is working"""
    try:
        # Initialize OpenAI client
        client = OpenAI()
        
        # Make a simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Hello! API is working!' and nothing else."}
            ],
            max_tokens=10
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        print("\nTo fix this:")
        print("1. Make sure you have an OpenAI API key")
        print("2. Set it as an environment variable: export OPENAI_API_KEY='your-key-here'")
        print("3. Or create a .env file with: OPENAI_API_KEY=your-key-here")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'pandas',
        'openai', 
        'tiktoken',
        'tenacity',
        'requests'  # This is missing from requirements.txt
    ]
    
    print("\n🔍 Testing package imports...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            return False
    return True

def main():
    """Run all tests"""
    print("🚀 Testing RetailNext00 Setup...\n")
    
    # Test imports first
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Some packages are missing. Please install them:")
        print("pip install requests")  # Add missing dependency
        return
    
    # Test OpenAI connection
    api_ok = test_openai_connection()
    
    if api_ok:
        print("\n🎉 All tests passed! Your setup is ready to go.")
    else:
        print("\n⚠️  Please fix the API key issue before proceeding.")

if __name__ == "__main__":
    main()
