# Financial Planner Web Application

A comprehensive web application for financial planning powered by AI agents using LangChain and OpenAI.

## Features

- 🎯 **Multi-Agent Planning System**: Choose from four specialized planning areas:
  - Retirement Planning
  - Insurance Planning
  - Estate Planning
  - Personal Wealth Management

- 📊 **Interactive Visualizations**: Dynamic charts using Plotly showing:
  - Retirement savings projections
  - Asset allocation recommendations
  - Insurance coverage analysis
  - Education funding status
  - Net worth projections
  - Monthly budget breakdowns

- 💬 **AI-Powered Chat Interface**: Ask follow-up questions about your plan with context-aware responses

- 📥 **Export Functionality**: Download your financial plan as JSON

## Project Structure

```
web_app/
├── app.py                 # Flask application entry point
├── agents.py             # AI agents and orchestration logic
├── config.py             # Configuration management
├── visualizations.py     # Chart generation functions
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
│
├── templates/
│   └── index.html        # Main HTML template
│
└── static/
    ├── css/
    │   └── style.css     # Application styling
    └── js/
        └── app.js        # Frontend JavaScript
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd web_app
pip install -r requirements.txt
```

### 2. Configure Environment

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
APP_PORT=5000
APP_HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### 1. Select Planning Options
- Check the planning services you need (you can select multiple)
- Form sections will dynamically appear based on your selections

### 2. Provide Your Information
- Enter basic financial information (age, income, savings)
- Fill in additional details based on selected planning areas
- Click "Generate My Financial Plan"

### 3. Review Your Plan
- Executive summary with integrated recommendations
- Individual planning summaries for each selected area
- Interactive charts and visualizations
- Key recommendations and action items

### 4. Ask Follow-Up Questions
- Use the chat interface to ask questions about your plan
- The AI advisor has full context of your financial situation
- Get personalized clarifications and additional insights

### 5. Export Your Plan
- Download your complete financial plan as a JSON file
- Include with professional financial advisor consultations

## Planning Modules

### Retirement Planning
- Calculate retirement fund needs based on age and expenses
- Project savings with multiple contribution scenarios
- Asset allocation recommendations by risk tolerance
- Withdrawal rate planning

### Insurance Planning
- Life insurance coverage recommendations (10x income rule)
- Adjustment for dependents and debt levels
- Disability insurance guidelines
- Long-term care planning
- Liability insurance considerations

### Estate Planning
- Estate tax calculations (federal exemption basis)
- Education funding needs for children
- Recommendations for wills and trusts
- Beneficiary designation guidance
- Tax minimization strategies

### Wealth Management
- Personalized asset allocation strategies
- Risk-adjusted investment recommendations
- Diversification guidelines
- Portfolio rebalancing schedule
- Cash flow management

## AI Agents

The application uses specialized AI agents that work together:

- **RetirementAgent**: Specializes in retirement planning calculations and projections
- **InsuranceAgent**: Analyzes insurance needs and coverage recommendations
- **EstateAgent**: Plans for wealth transfer and education funding
- **WealthAgent**: Creates comprehensive wealth management strategies
- **OrchestratorAgent**: Coordinates between agents and creates integrated executive summary

Each agent uses specialized tools for financial calculations:
- `calculate_retirement_needs`: Calculates future retirement fund requirements
- `calculate_life_insurance`: Determines optimal insurance coverage
- `calculate_education_fund`: Projects education funding needs
- `calculate_estate_tax`: Estimates potential estate tax liability
- `calculate_wealth_allocation`: Recommends asset allocation

## API Endpoints

### GET `/api/plans`
Get list of available planning options

**Response:**
```json
[
  {
    "id": "retirement",
    "name": "Retirement Planning",
    "description": "...",
    "icon": "🏖️"
  }
]
```

### POST `/api/planning/start`
Start a new planning session

**Request:**
```json
{
  "selected_plans": ["retirement", "insurance"],
  "user_info": {
    "age": 45,
    "annual_income": 100000,
    "savings": 250000,
    "retirement_age": 65,
    "risk_tolerance": "moderate"
  }
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "plan_summaries": {...},
  "visualizations": {...},
  "status": "success"
}
```

### GET `/api/planning/<session_id>`
Retrieve planning results for a session

### POST `/api/chat/<session_id>`
Send a message to the AI advisor

**Request:**
```json
{
  "message": "What if I retire at 62 instead?"
}
```

**Response:**
```json
{
  "message": "Based on your profile...",
  "status": "success"
}
```

### GET `/api/export/<session_id>`
Export the financial plan as JSON

## Technology Stack

- **Backend**: Flask 3.0
- **AI/LLM**: LangChain, OpenAI GPT-4o-mini
- **Agent Framework**: LangGraph
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Plotly.js
- **Session Management**: Flask-Session
- **CORS**: Flask-CORS

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `APP_PORT` | Server port | 5000 |
| `APP_HOST` | Server host | 0.0.0.0 |
| `SECRET_KEY` | Flask secret key | dev-key |

### Configuration Modes

The application supports three configuration modes:
- **development**: Debug mode enabled, suitable for local development
- **production**: Debug mode disabled, optimized for deployment
- **testing**: Test configuration with mock API key

## Security Considerations

⚠️ **Important**: 
- Never commit `.env` file with real API keys to version control
- Use strong secret keys in production
- Implement rate limiting for chat endpoints in production
- Consider adding authentication for production deployment
- Validate all user inputs on the backend

## Performance Notes

- Sessions are stored in-memory; for production, implement persistent session storage (database)
- Large numbers of concurrent users may require load balancing
- Consider caching frequently accessed visualizations
- API calls to OpenAI may incur costs based on token usage

## Troubleshooting

### "OPENAI_API_KEY not set" error
- Ensure `.env` file exists in the `web_app` directory
- Verify the API key is correctly set and starts with `sk-`

### Charts not displaying
- Ensure Plotly.js CDN is accessible
- Check browser console for JavaScript errors
- Verify visualization data is being generated

### Chat not working
- Ensure a planning session has been generated
- Check that OPENAI_API_KEY is valid
- Monitor server logs for API errors

### Slow response times
- OpenAI API calls can take 10-30 seconds
- Consider showing more explicit loading indicators for long operations
- Monitor token usage for efficiency

## Future Enhancements

- [ ] PDF export functionality
- [ ] Database persistence for sessions
- [ ] User authentication and saved profiles
- [ ] Scenario comparison (what-if analysis)
- [ ] Integration with financial data providers
- [ ] Mobile app version
- [ ] Advanced tax optimization strategies
- [ ] Real-time market data integration
- [ ] Professional advisor collaboration features

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in browser console and server logs
3. Verify all environment variables are correctly set
4. Ensure all dependencies are installed with correct versions

---

**Note**: This application demonstrates AI agent orchestration for financial planning. For actual financial planning, always consult with qualified financial advisors.
