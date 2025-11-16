# Financial Planner AI - Example Notebook

This notebook demonstrates the Financial Planner AI system. 

## Setup Instructions

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set OpenAI API Key**:
```python
import os
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
```

3. **Run the Application**:
```bash
python app.py
```

4. **Access Interface**:
Navigate to `http://localhost:5000` in your browser.

## Features

- **Multi-Agent AI System**: Specialized agents for different financial planning areas
- **Interactive Chat**: Context-aware conversations with AI advisors
- **Professional Export**: PDF and DOCX document generation
- **Responsive Design**: Works on all devices
- **Real-time Processing**: Live updates and progress indicators

## Usage Example

```python
# Example user profile
user_profile = {
    "age": 32,
    "annual_income": 85000,
    "savings": 45000,
    "selected_plans": ["Retirement Planning", "Homeownership"]
}

# The system automatically routes to appropriate AI agents
# and generates comprehensive financial recommendations
```

## Security Note

**Never commit API keys to version control.** Always use environment variables or `.env` files that are excluded from git.

For detailed documentation, see:
- [User Guide](USER_GUIDE.md)
- [Developer Guide](DEVELOPER.md)
- [API Documentation](API.md)