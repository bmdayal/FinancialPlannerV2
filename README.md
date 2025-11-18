# 🏦 Financial Planner AI - Agentic Financial Planning System

![Financial Planner Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)

A comprehensive financial planning application powered by **Agentic AI** using **LangChain** and **OpenAI GPT-4**. This system employs multiple specialized AI agents to create personalized financial plans across various life goals.

## 🚀 Quick Start

1. **Get OpenAI API Key**: Visit https://platform.openai.com/api-keys
2. **Navigate to app**: `cd web_app`
3. **Set API key**: Create `.env` file with `OPENAI_API_KEY=your-key-here`
4. **Install**: `pip install -r requirements.txt`
5. **Run**: `python app.py`
6. **Open**: http://localhost:5000

## 🌟 Key Features

### 🤖 **Agentic AI System**
- **Multiple Specialized Agents**: Each financial goal handled by dedicated AI agents
- **LangChain Integration**: Advanced prompt engineering and conversation management
- **Context-Aware Planning**: AI maintains conversation history and user context
- **Intelligent Recommendations**: Data-driven insights based on user profile

### 📊 **Financial Planning Modules**
- **Retirement Planning** - 401k optimization, pension planning, retirement income strategies
- **Homeownership** - Down payment planning, mortgage analysis, property investment
- **Education Savings** - 529 plans, education cost projections, funding strategies
- **Emergency Fund** - Risk assessment, liquidity planning, emergency preparedness
- **Investment Portfolio** - Asset allocation, risk tolerance, diversification strategies
- **Debt Management** - Payment strategies, consolidation analysis, debt elimination plans

### 💼 **Professional Export System**
- **PDF Reports** - Professionally formatted documents with visual hierarchy
- **Word Documents** - Editable DOCX files with rich formatting and tables
- **Financial Data Highlighting** - Automatic formatting of currency, percentages, and key metrics
- **Client-Ready Output** - Professional styling suitable for client presentations

### 🎨 **Modern Web Interface**
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Real-Time Chat** - Interactive conversation with AI agents
- **Loading Animations** - Visual feedback during AI processing
- **Progress Indicators** - Step-by-step planning guidance
- **Interactive Visualizations** - Charts and graphs for financial projections

## 🚀 Detailed Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bmdayal/FinancialPlannerV2.git
   cd FinancialPlannerDemo
   ```

2. **Set Up Virtual Environment**
   ```powershell
   cd web_app
   python -m venv venv
   
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   .\venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   
   Create a `.env` file in the `web_app` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the Application**
   ```powershell
   python app.py
   ```

6. **Access the Application**
   
   Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### Getting Started
1. **Enter Personal Information**
   - Age, annual income, current savings
   - Financial goals and timeline

2. **Select Planning Modules**
   - Choose from retirement, homeownership, education, etc.
   - Multiple selections supported

3. **AI-Powered Planning**
   - AI agents analyze your profile
   - Generate comprehensive financial strategies
   - Provide actionable recommendations

4. **Interactive Chat**
   - Ask questions about your plan
   - Get clarifications and additional insights
   - Context-aware responses

5. **Export Professional Reports**
   - Download as PDF or Word document
   - Share with financial advisors
   - Print for offline review

### Advanced Features
- **Multi-Goal Planning**: Coordinate multiple financial objectives
- **Scenario Analysis**: Compare different planning approaches
- **Progress Tracking**: Monitor goal achievement over time
- **Regular Updates**: Refresh plans as circumstances change

## 🏗️ Architecture Overview

### Agentic AI System
```
User Input → LangChain Router → Specialized Agents → Response Synthesis
     ↓              ↓                    ↓                  ↓
Context Management → Prompt Engineering → OpenAI GPT-4 → Formatted Output
```

### System Components
- **Flask Web Server**: Handles HTTP requests and responses
- **LangChain Framework**: Manages AI agent orchestration
- **OpenAI Integration**: Powers natural language processing
- **Session Management**: Maintains conversation state
- **Export Engine**: Generates professional documents

## 📁 Project Structure

```
FinancialPlannerDemo/
├── web_app/                    # Main application
│   ├── app.py                  # Flask application
│   ├── agents.py               # AI agent definitions
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── static/                # CSS, JS, assets
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript files
│   ├── templates/             # HTML templates
│   └── flask_session/         # Session data
├── flask_session/             # Session storage
└── README.md                  # This file
```

## 🔧 Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.1.2** - Web framework
- **LangChain** - AI agent framework
- **OpenAI GPT-4** - Language model
- **ReportLab** - PDF generation
- **python-docx** - Word document creation

### Frontend
- **HTML5** - Structure and semantics
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Plotly.js** - Data visualizations

### Infrastructure
- **Flask-Session** - Session management
- **NumPy** - Numerical computations
- **JSON** - Data exchange format

## 📚 Documentation

For detailed information about the application:
- Check the code comments in `web_app/` for implementation details
- Review `web_app/QUICKSTART.md` for additional setup instructions
- Explore the Flask application structure in the `web_app/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch:
   ```powershell
   git checkout -b feature/amazing-feature
   ```
3. Make your changes
4. Commit your changes:
   ```powershell
   git commit -m "Add amazing feature"
   ```
5. Push to the branch:
   ```powershell
   git push origin feature/amazing-feature
   ```
6. Submit a pull request

## 📄 License

This project is open source. Please check with the repository owner for specific licensing terms.

## ⚠️ Important Notes

- **AI-Generated Content**: All financial advice is AI-generated and should be reviewed by qualified financial professionals
- **Not Financial Advice**: This tool is for planning purposes only and does not constitute professional financial advice
- **API Costs**: OpenAI API usage will incur costs based on token consumption
- **Data Privacy**: User data is processed locally and not stored permanently

## 🆘 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Code Documentation**: Check inline comments and docstrings in the source code
- **Setup Help**: Review the installation steps above or check `web_app/QUICKSTART.md`

---

**Built with ❤️ using Agentic AI and LangChain**