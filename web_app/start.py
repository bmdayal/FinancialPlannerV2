#!/usr/bin/env python3
"""
Stable startup script for Financial Planner AI
This script ensures proper environment setup and error handling
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔧 Checking environment setup...")
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Make sure you're in the web_app directory.")
        return False
    
    # Check if virtual environment is activated
    if "venv" not in sys.executable:
        print("⚠️  Warning: Virtual environment may not be activated.")
        print("   Please run: .\\venv\\Scripts\\Activate.ps1 (Windows) or source venv/bin/activate (Linux/Mac)")
    
    # Check for OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("   Please set your OpenAI API key:")
        print("   Windows: $env:OPENAI_API_KEY='your-key-here'")
        print("   Linux/Mac: export OPENAI_API_KEY='your-key-here'")
        print("   Or create a .env file with: OPENAI_API_KEY=your-key-here")
        return False
    elif api_key.startswith('sk-'):
        print("✓ OpenAI API key found")
    else:
        print("⚠️  Warning: OpenAI API key format may be incorrect")
    
    return True

def test_imports():
    """Test all required imports"""
    print("📦 Testing imports...")
    
    try:
        import flask
        import langchain
        import openai
        import reportlab
        import docx
        import numpy
        print("✓ All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please install dependencies: pip install -r requirements.txt")
        return False

def start_app():
    """Start the Flask application with proper error handling"""
    print("🚀 Starting Financial Planner AI...")
    
    try:
        from app import app
        print("✓ Flask app loaded successfully")
        
        print("\n" + "="*60)
        print("🏦 Financial Planner AI - Agentic AI System")
        print("="*60)
        print("🌐 Starting server on http://localhost:5000")
        print("📖 Documentation: See docs/ folder")
        print("🔧 Developer Guide: docs/DEVELOPER.md")
        print("👤 User Guide: docs/USER_GUIDE.md")
        print("="*60)
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("\n🔍 Troubleshooting steps:")
        print("1. Check that all dependencies are installed")
        print("2. Verify OpenAI API key is set correctly")
        print("3. Ensure you're in the web_app directory")
        print("4. Check the logs above for specific error details")
        return False

def main():
    """Main function with comprehensive error handling"""
    print("🏦 Financial Planner AI - Startup Script")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return 1
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install dependencies.")
        return 1
    
    # Start the application
    try:
        start_app()
        return 0
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user. Goodbye!")
        return 0
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())