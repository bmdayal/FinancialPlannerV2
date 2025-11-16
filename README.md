# 🏦 Financial Planner AI - Agentic Financial Planning System

A comprehensive financial planning application powered by **Agentic AI** using **LangChain** and **OpenAI GPT-4**. This system employs multiple specialized AI agents to create personalized financial plans across various life goals.

![Financial Planner Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)

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

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd FinancialPlannerDemo
   ```

2. **Set Up Virtual Environment**
   ```bash
   cd web_app
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   
   Create a `.env` file in the `web_app` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the Application**
   ```bash
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
│   ├── templates/             # HTML templates
│   └── venv/                  # Virtual environment
├── docs/                      # Documentation
├── diagrams/                  # Architecture diagrams
├── ARCHITECTURE.md            # Technical architecture
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

- [Developer Guide](docs/DEVELOPER.md) - Setup, debugging, and development
- [User Guide](docs/USER_GUIDE.md) - Detailed feature explanations
- [Architecture](ARCHITECTURE.md) - Technical system design
- [API Documentation](docs/API.md) - REST endpoint reference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- **AI-Generated Content**: All financial advice is AI-generated and should be reviewed by qualified financial professionals
- **Not Financial Advice**: This tool is for planning purposes only and does not constitute professional financial advice
- **API Costs**: OpenAI API usage will incur costs based on token consumption
- **Data Privacy**: User data is processed locally and not stored permanently

## 🆘 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Check the `docs/` folder for detailed guides
- **Developer Help**: See `docs/DEVELOPER.md` for setup and debugging

---

**Built with ❤️ using Agentic AI and LangChain**