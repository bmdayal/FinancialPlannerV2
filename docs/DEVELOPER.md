# 🔧 Developer Guide - Financial Planner AI

Comprehensive development, debugging, and deployment guide for the Financial Planner AI application.

## 📋 Table of Contents

- [Development Setup](#-development-setup)
- [Architecture Overview](#-architecture-overview)
- [Debugging Guide](#-debugging-guide)
- [Code Structure](#-code-structure)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

## 🚀 Development Setup

### Prerequisites

```bash
# Required software
Python 3.8+
Git
VS Code (recommended)
Postman (for API testing)
```

### Environment Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd FinancialPlannerDemo/web_app
   ```

2. **Create Virtual Environment**
   ```bash
   # Create venv
   python -m venv venv
   
   # Activate (Windows)
   .\venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   
   # Verify activation
   which python  # Should show venv path
   ```

3. **Install Dependencies**
   ```bash
   # Install all requirements
   pip install -r requirements.txt
   
   # Verify critical packages
   python -c "import flask, langchain, openai; print('All packages installed successfully')"
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_key_here" > .env
   echo "FLASK_ENV=development" >> .env
   echo "DEBUG=True" >> .env
   ```

### Development Workflow

```bash
# 1. Start development server
python app.py

# 2. Access application
# Browser: http://localhost:5000
# API: http://localhost:5000/api/

# 3. Development tools
# Debug mode: Flask reloads automatically
# Logs: Check console output
# API testing: Use Postman or curl
```

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   AI Agents     │
│   (HTML/CSS/JS) │◄──►│   (app.py)      │◄──►│   (agents.py)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LangChain     │
                       │   Framework     │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   OpenAI GPT-4  │
                       │   Language Model│
                       └─────────────────┘
```

### Key Components

#### 1. Flask Application (`app.py`)
- **Route Handlers**: HTTP endpoint management
- **Session Management**: User state persistence
- **Export System**: PDF/DOCX generation
- **Error Handling**: Graceful error responses

#### 2. AI Agents (`agents.py`)
- **Specialized Agents**: Domain-specific financial planning
- **LangChain Integration**: Prompt management and conversation flow
- **Context Management**: Maintaining conversation history

#### 3. Frontend (`static/`, `templates/`)
- **Responsive UI**: Cross-device compatibility
- **Real-time Updates**: AJAX communication with backend
- **Document Export**: Client-side download management

## 🐛 Debugging Guide

### Common Issues and Solutions

#### 1. Flask Server Won't Start

**Problem**: `ModuleNotFoundError: No module named 'flask'`

```bash
# Solution: Verify virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Check if Flask is installed
pip list | findstr flask  # Windows
pip list | grep flask     # macOS/Linux

# Reinstall if needed
pip install flask
```

#### 2. OpenAI API Errors

**Problem**: `openai.error.AuthenticationError: Invalid API key`

```bash
# Check .env file exists
ls -la .env  # Should show .env file

# Verify API key format
cat .env | grep OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-...

# Test API key
python -c "import openai; openai.api_key='your_key'; print('API key valid')"
```

#### 3. PDF/DOCX Export Issues

**Problem**: `ImportError: cannot import name 'colors' from 'reportlab'`

```bash
# Reinstall document libraries
pip uninstall reportlab python-docx
pip install reportlab==4.4.4 python-docx==1.2.0

# Verify installation
python -c "from reportlab.lib.colors import HexColor; from docx import Document; print('Export libraries OK')"
```

### Debug Mode Configuration

```python
# In app.py - Enable detailed debugging
app.config['DEBUG'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
```

### Debugging Techniques

#### 1. Print Debugging
```python
# Add debug prints in app.py
print(f"DEBUG: Session data: {session_data}")
print(f"DEBUG: User input: {request.json}")
print(f"DEBUG: API response: {response}")
```

#### 2. Browser Developer Tools
```javascript
// Console debugging in app.js
console.log('User data:', userData);
console.log('API response:', response);
console.error('Error occurred:', error);
```

#### 3. Network Debugging
```bash
# Monitor API calls
curl -X POST http://localhost:5000/api/planning/start \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "income": 50000}'
```

## 📂 Code Structure

### File Organization

```
web_app/
├── app.py                 # Main Flask application
├── agents.py              # AI agent definitions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── static/
│   ├── css/
│   │   └── style.css      # Application styling
│   └── js/
│       └── app.js         # Frontend logic
├── templates/
│   └── index.html         # Main HTML template
└── venv/                  # Virtual environment
```

### Key Functions

#### `app.py` - Main Routes
```python
@app.route('/')                           # Home page
@app.route('/api/plans')                  # Available plans
@app.route('/api/planning/start')         # Start planning
@app.route('/api/chat/<session_id>')      # Chat interface
@app.route('/api/export/<session_id>/pdf') # PDF export
@app.route('/api/export/<session_id>/docx') # DOCX export
```

#### `agents.py` - AI Functions
```python
def create_financial_agents()             # Initialize agents
def get_retirement_plan()                 # Retirement planning
def get_homeownership_plan()              # Home buying plan
def get_education_plan()                  # Education savings
# ... other specialized agents
```

## 🔌 API Reference

### Authentication
No authentication required for development. API key handled server-side.

### Endpoints

#### GET `/api/plans`
Get available financial planning modules.

**Response:**
```json
{
  "plans": [
    "Retirement Planning",
    "Homeownership",
    "Education Savings",
    "Emergency Fund",
    "Investment Portfolio",
    "Debt Management"
  ]
}
```

#### POST `/api/planning/start`
Start a new planning session.

**Request:**
```json
{
  "age": 30,
  "annual_income": 75000,
  "savings": 25000,
  "selected_plans": ["Retirement Planning", "Homeownership"]
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "success",
  "plans": {
    "Retirement Planning": "detailed plan...",
    "Homeownership": "detailed plan..."
  }
}
```

#### POST `/api/chat/<session_id>`
Send chat message to AI.

**Request:**
```json
{
  "message": "How much should I save for retirement?"
}
```

**Response:**
```json
{
  "message": "Based on your profile...",
  "status": "success"
}
```

## 🧪 Testing

### Manual Testing Checklist

#### Frontend Tests
- [ ] Page loads correctly
- [ ] Form validation works
- [ ] Loading animations display
- [ ] Error messages show properly
- [ ] Responsive design on mobile

#### Backend Tests
- [ ] API endpoints respond correctly
- [ ] Session management works
- [ ] AI agents generate plans
- [ ] PDF export functions
- [ ] DOCX export functions

#### Integration Tests
```bash
# Test full workflow
curl -X POST http://localhost:5000/api/planning/start \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "annual_income": 75000,
    "savings": 25000,
    "selected_plans": ["Retirement Planning"]
  }'

# Test chat
curl -X POST http://localhost:5000/api/chat/SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about my retirement plan"}'

# Test export
curl -X GET http://localhost:5000/api/export/SESSION_ID/pdf
```

### Automated Testing Setup

```python
# test_app.py - Basic test structure
import unittest
import json
from app import app

class FinancialPlannerTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_plans_api(self):
        response = self.app.get('/api/plans')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('plans', data)

if __name__ == '__main__':
    unittest.main()
```

## 🚀 Deployment

### Development Deployment
```bash
# Run development server
python app.py
# Access at http://localhost:5000
```

### Production Deployment

#### Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Environment Variables for Production
```bash
export FLASK_ENV=production
export DEBUG=False
export OPENAI_API_KEY=your_production_key
export SECRET_KEY=your_secret_key
```

## 🔧 Troubleshooting

### Performance Issues

#### Slow AI Responses
```python
# Monitor API response times
import time
start_time = time.time()
response = llm.invoke(messages)
print(f"AI response time: {time.time() - start_time:.2f}s")
```

#### Memory Usage
```python
# Monitor memory in app.py
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

### Common Error Patterns

#### 1. Session Timeout
```python
# Check session data exists
if session_id not in planning_sessions:
    return jsonify({'error': 'Session expired'}), 404
```

#### 2. API Rate Limits
```python
# Handle OpenAI rate limits
try:
    response = llm.invoke(messages)
except openai.error.RateLimitError:
    return jsonify({'error': 'API rate limit exceeded'}), 429
```

#### 3. Export Generation Failures
```python
# Robust export error handling
try:
    doc.build(content)
except Exception as e:
    app.logger.error(f"PDF generation failed: {str(e)}")
    return jsonify({'error': 'Export failed'}), 500
```

### Development Tips

1. **Use Virtual Environment**: Always activate venv before development
2. **Monitor Logs**: Keep Flask console output visible
3. **Test Incrementally**: Test changes immediately after making them
4. **Use Browser DevTools**: Monitor network requests and console errors
5. **Version Control**: Commit frequently with descriptive messages

### Getting Help

- **Flask Documentation**: https://flask.palletsprojects.com/
- **LangChain Docs**: https://python.langchain.com/
- **OpenAI API Docs**: https://platform.openai.com/docs
- **ReportLab Guide**: https://www.reportlab.com/docs/

---

**Need additional help?** Check the main README.md or create an issue on GitHub.