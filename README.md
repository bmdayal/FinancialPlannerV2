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
4. **Configure External APIs (Optional)**: Set up MCP servers for real-time market and economic data (see section below)
5. **Install**: `pip install -r requirements.txt`
6. **Run**: `python app.py`
7. **Open**: http://localhost:5000

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

### 🌐 **External API Integration (MCP Servers)**
- **Real-Time Market Data** - Live stock prices and portfolio performance tracking
- **Current Interest Rates** - Mortgage rates, Federal Funds Rate, Prime Rate
- **Economic Indicators** - Inflation rates, unemployment, GDP data
- **Accurate Projections** - Retirement expenses adjusted for actual inflation
- **Market Context** - Make decisions based on current market conditions

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

### Optional: Configure MCP Servers for Real-Time Market & Economic Data

The application includes integrated MCP (Model Context Protocol) servers that connect to external APIs for real-time financial data. This enables more accurate financial planning with current market conditions and economic indicators.

#### Step 1: Copy Environment Template
```powershell
# From the project root directory
copy .env.example .env
```

#### Step 2: Configure Market Data API (Choose One)

**Option A: Alpha Vantage (Recommended for beginners)**
1. Get free API key: https://www.alphavantage.co/
2. Add to `.env`:
   ```env
   MARKET_DATA_API_KEY=your_alpha_vantage_api_key_here
   MARKET_DATA_PROVIDER=alpha_vantage
   ```
3. Free tier includes: Stock prices, market indices, portfolio analysis
4. Limitations: 5 API calls per minute, 500 requests per day

**Option B: IEX Cloud (More robust)**
1. Get free account: https://iexcloud.io/
2. Add to `.env`:
   ```env
   MARKET_DATA_API_KEY=your_iex_cloud_token_here
   MARKET_DATA_PROVIDER=iex_cloud
   ```
3. Free tier includes: Real-time prices, intraday data
4. Limitations: 100 messages per second, 10 million messages per month

#### Step 3: Configure Economic Data API (Required for inflation/rate data)

Get free API key from Federal Reserve Economic Data (FRED):
1. Visit: https://fred.stlouisfed.org/docs/api/
2. Register for free account
3. Add to `.env`:
   ```env
   FRED_API_KEY=your_fred_api_key_here
   ```

This provides:
- **Inflation Rate**: Consumer Price Index (CPI) data
- **Interest Rates**: Federal Funds Rate, Mortgage Rates (15yr, 30yr, Jumbo, FHA)
- **Unemployment**: Current unemployment statistics
- **GDP Growth**: Economic growth data
- **Economic Dashboard**: Comprehensive economic indicators

#### Step 4: (Optional) Mortgage Rates API

For specialized mortgage rate data beyond FRED:
```env
MORTGAGE_API_KEY=your_mortgage_api_key_here
```

#### Step 5: Configure MCP Settings

Fine-tune MCP behavior in `.env`:
```env
ENABLE_MCP_SERVERS=true              # Enable/disable MCP functionality
MCP_CACHE_ENABLED=true               # Cache API responses
MCP_CACHE_TIMEOUT=300                # Cache duration (seconds)
```

#### What MCPs Enable

With MCPs configured, the financial planning agents gain access to:

**Market Data Tools**
- `get_stock_price()` - Real-time stock prices and market data
- `get_portfolio_performance()` - Current portfolio value and gains/losses
- `get_market_indices()` - S&P 500, Nasdaq, Dow Jones data
- `search_stocks()` - Find stocks by keywords

**Interest Rate Tools**
- `get_current_mortgage_rates()` - Current mortgage rates by type
- `calculate_mortgage_payment()` - Accurate payment calculations
- `get_federal_funds_rate()` - Current Fed rate
- `project_rate_scenarios()` - Future rate projections

**Economic Data Tools**
- `get_inflation_rate()` - Current inflation metrics
- `get_unemployment_rate()` - Employment statistics
- `get_economic_dashboard()` - Comprehensive economic overview
- `project_retirement_inflation()` - Adjust projections for inflation
- `compare_inflation_scenarios()` - Low/moderate/high inflation analysis

#### Troubleshooting MCP Setup

**"MCP client not available" message**
- Ensure `anthropic>=0.29.0` is installed: `pip install -r requirements.txt`
- Check that all API keys in `.env` are filled in correctly
- Verify internet connection for API calls

**API Rate Limits**
- Alpha Vantage: Wait between requests, spread out multiple queries
- FRED: Very generous limits, rarely hit (120 requests per minute)
- Use caching to reduce API calls: `MCP_CACHE_ENABLED=true`

**Missing Rates/Data**
- Some indicators only update monthly (e.g., unemployment, inflation)
- Check FRED website for latest available data: https://fred.stlouisfed.org/
- Application will gracefully fall back to default values if APIs unavailable

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

### MCP Integration Architecture
```
Financial Agents → MCP Client Manager → External APIs
                        ↓
        ┌───────────┬────────────┬──────────────┐
        ↓           ↓            ↓              ↓
    Market Data  Interest Rates  Inflation   Economic
    (Alpha V)    (FRED API)      (FRED)      Data
```

### System Components
- **Flask Web Server**: Handles HTTP requests and responses
- **LangChain Framework**: Manages AI agent orchestration
- **OpenAI Integration**: Powers natural language processing
- **Session Management**: Maintains conversation state
- **Export Engine**: Generates professional documents
- **MCP Servers**: Provide real-time market and economic data
  - Market Data MCP: Stock prices, indices, portfolio analysis
  - Mortgage Rates MCP: Interest rates, loan calculations
  - Economic Data MCP: Inflation, unemployment, GDP metrics

## 📁 Project Structure

```
FinancialPlannerV2/
├── web_app/                    # Main Flask application
│   ├── app.py                  # Flask application entry point
│   ├── agents.py               # AI agent definitions & tools
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── static/                # CSS, JS, assets
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript files
│   ├── templates/             # HTML templates
│   └── flask_session/         # Session data
├── mcp_servers/                # MCP Server implementations
│   ├── market_data_mcp.py      # Stock prices & market data
│   ├── mortgage_rates_mcp.py   # Interest rates & mortgage calculations
│   ├── economic_data_mcp.py    # Inflation, unemployment, GDP data
│   ├── mcp_client.py           # Unified MCP client manager
│   ├── __init__.py             # Package initialization
│   └── mcp_utils.py            # Helper utilities (optional)
├── .env.example                # Environment template with MCP setup
├── .gitignore
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

### MCP Servers & External APIs
- **Anthropic MCP SDK** - Model Context Protocol implementation
- **Alpha Vantage API** - Real-time stock prices and market data
- **Federal Reserve FRED API** - Economic indicators, interest rates, inflation
- **IEX Cloud** - Alternative market data provider

### Frontend
- **HTML5** - Structure and semantics
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Plotly.js** - Data visualizations

### Infrastructure
- **Flask-Session** - Session management
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation
- **Requests** - HTTP client for API calls
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