# Test Environment Setup
import os
import sys

# Set a dummy OpenAI API key for testing (won't make actual API calls)
os.environ['OPENAI_API_KEY'] = 'sk-test-dummy-key-for-testing-only'

# Test imports
try:
    import flask
    print("✓ Flask imported successfully")
    
    import langchain
    print("✓ LangChain imported successfully")
    
    import openai
    print("✓ OpenAI imported successfully")
    
    from reportlab.lib.colors import HexColor, black, white
    print("✓ ReportLab imported successfully")
    
    from docx import Document
    print("✓ python-docx imported successfully")
    
    # Try importing the main app
    from app import app
    print("✓ Flask app imported successfully")
    
    print("\n🎉 All dependencies working! App should run successfully.")
    print("\nTo start the app:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Run: python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"❌ Error type: {type(e)}")
    import traceback
    traceback.print_exc()