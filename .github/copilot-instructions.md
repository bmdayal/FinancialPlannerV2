# Copilot Instructions for FinancialPlannerV2

## Project Overview

**FinancialPlannerV2** is an agentic AI financial planning system powered by LangChain, OpenAI GPT-4o-mini, and Flask. It uses specialized AI agents to create personalized financial plans across multiple life goals (retirement, homeownership, education, insurance, estate planning, etc.).

### Architecture: Three-Tier System

1. **Web App Layer** (`web_app/`): Flask REST API + HTML/JS frontend
2. **Agent Layer** (`web_app/agents.py`): LangChain agents with tool orchestration (StateGraph-based)
3. **MCP Servers** (`mcp_servers/`): External API integrations for real-time market/economic data

## Critical Workflows

### Running the Application

```powershell
cd web_app
python app.py
# Launches Flask server at http://localhost:5000
# Requires: OPENAI_API_KEY in .env (and optional MARKET_DATA_API_KEY, FRED_API_KEY)
```

See `web_app/QUICKSTART.md` for detailed setup instructions including environment configuration.

### MCP Servers (Model Context Protocol)

Three specialized MCP servers provide real-time financial data via external APIs with 5-minute result caching:

- **`market_data_mcp.py`**: Stock prices, market indices (Alpha Vantage API, default; IEX Cloud optional)
- **`mortgage_rates_mcp.py`**: Mortgage rates, federal funds rate, prime rate (FRED API)
- **`economic_data_mcp.py`**: Inflation, unemployment, GDP, scenario projections (FRED API)
- **`mcp_client.py`**: `MCPClientManager` singleton that routes tool calls to appropriate servers

**Key Pattern**: All MCP servers follow consistent design:
```python
class [XyzMCP]:
    def __init__(self, api_key):
        self.api_key = api_key
        logger.info("Server initialized")
    
    def tool_method(self, params):
        # Check cache, call external API, cache for 300 sec
        return {"result": data, "success": True}
```

Tools registered in `MCPClientManager._build_tools_registry()` (15 total tools) and exposed to agents via `@tool` decorator wrappers in `agents.py`.

## Code Organization Patterns

### Agent Tool Definition Pattern

In `agents.py`, all MCP-backed tools follow this structure with graceful degradation:

```python
@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price and market data for investment analysis."""
    logger.debug(f"[AGENT] Calling MCP tool: get_stock_price(symbol={symbol})")
    if mcp_client is None:
        logger.error("MCP client not available for get_stock_price")
        return "MCP client not available"  # Agents continue planning without live data
    result = mcp_client.call_tool('get_stock_price', symbol=symbol)
    logger.debug(f"[AGENT] get_stock_price result: {result}")
    return json.dumps(result.get('result', result))
```

**Why this pattern**: 
- Graceful degradation if MCP servers unavailable (agents still work without live data)
- Consistent logging for debugging via logger.debug() calls
- JSON serialization ensures LangChain receives proper tool output
- All tools follow identical structure for predictability

### Agent State Management

Agents use LangChain's `StateGraph` pattern with `TypedDict` for state. Example from `AgentState`:
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_input: str
    planning_data: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
```

Messages field uses `operator.add` to accumulate conversation history automatically. All agents inherit this state pattern for consistency.

### Configuration Management

`config.py` uses environment variables with defaults for all deployment scenarios:

**Required**:
- `OPENAI_API_KEY` - OpenAI API key (no default; app won't start without it)

**Optional** (with graceful fallback):
- `MARKET_DATA_API_KEY` + `MARKET_DATA_PROVIDER` ('alpha_vantage' default; 'iex_cloud' supported)
- `FRED_API_KEY` - Federal Reserve economic data (fallback to cached/hardcoded values)
- `FLASK_ENV` - 'development'/'production'/'testing' (development default)
- `ENABLE_MCP_SERVERS` - 'true'/'false' (true default; agents work if false but without live data)

Three config classes inherit from base `Config`:
- `DevelopmentConfig`: DEBUG=True, filesystem session storage
- `ProductionConfig`: DEBUG=False, hardened defaults
- `TestingConfig`: Mock API keys, TESTING=True

## Data Flows & Integration Points

### User Request Flow (Complete End-to-End)

1. **Frontend Capture**: User fills form in `templates/index.html`, hits "Create Plan"
2. **API Route**: JavaScript calls `POST /api/plan` with JSON body containing user profile
3. **Session Creation**: `app.py` creates unique session ID, initializes `AgentState` TypedDict
4. **Agent Invocation**: `OrchestratorAgent.invoke()` starts with user input (StateGraph entry point)
5. **Tool Availability Check**: Agent checks available tools via `get_tools()` method
6. **Tool Execution**: When agent calls tool (e.g., `get_stock_price("AAPL")`):
   - `@tool` wrapper in `agents.py` checks if `mcp_client` is not None
   - Calls `mcp_client.call_tool('get_stock_price', symbol='AAPL')`
   - MCPClientManager routes to `market_data.get_stock_price()`
   - Alpha Vantage API returns real-time data (with 5-min cache check first)
   - Result JSON-serialized back to agent for reasoning
7. **Agent Response**: Agent synthesizes tools outputs with reasoning, returns structured plan
8. **Session Storage**: Plan saved in `planning_sessions[session_id]` for export
9. **PDF/DOCX Export**: User downloads via `POST /api/export-plan` (uses reportlab/python-docx)

**Graceful Degradation**: If MCP client is None or API fails, tool returns error string; agent recognizes this and continues planning with fallback logic.

### Tool Call Chain Example

```
User requests "Show me AAPL stock analysis"
  ↓
Agent calls get_stock_price("AAPL")
  ↓
agents.py wrapper:
  - Logs: [AGENT] Calling MCP tool: get_stock_price(symbol=AAPL)
  - Calls: mcp_client.call_tool('get_stock_price', symbol='AAPL')
  ↓
MCPClientManager.call_tool():
  - Logs: [TOOL CALL] Calling 'get_stock_price' with args: {'symbol': 'AAPL'}
  - Routes to: market_data.get_stock_price('AAPL')
  ↓
MarketDataMCP.get_stock_price():
  - Checks 5-min cache first (if enabled in config)
  - Logs: [MCP:MarketData] - Fetching stock price from Alpha Vantage for AAPL
  - Calls Alpha Vantage API
  - Returns: {"price": 150.23, "change": +2.45, "percent": +1.65, ...}
  ↓
Back to agent as: json.dumps({"price": 150.23, ...})
  - Agent receives clean JSON, uses in analysis
```

**Key Insight**: Tool failures never block agent execution—graceful fallback ensures agents always return usable plans even if APIs are down.

## Key External Dependencies

- **LangChain 0.1.10**: Agent framework, tool definitions, state graphs
- **OpenAI API**: GPT-4o-mini for reasoning (configured in `config.py`)
- **Alpha Vantage / IEX Cloud**: Market data (configurable, Alpha Vantage default)
- **FRED API**: Federal Reserve economic indicators
- **Flask 3.0**: REST API server
- **Plotly**: Charts in visualizations module
- **reportlab / python-docx**: PDF/DOCX export

## Common Modifications

### Adding a New Financial Planning Agent

1. Create agent class in `agents.py` inheriting from base agent pattern
2. Register in `OrchestratorAgent._route_to_specialized_agent()`
3. Add new tools via `@tool` decorators calling MCP servers if needed
4. Add planning route in `app.py` (e.g., `/api/plan/education`)

### Adding a New MCP Tool

1. Implement method in appropriate MCP server (market_data_mcp.py, etc.)
2. Register in `MCPClientManager._build_tools_registry()`
3. Create wrapper `@tool` in `agents.py`
4. Add to agent tool list in agent initialization

### Debugging MCP Issues

All MCP components have DEBUG-level logging enabled. Check these patterns:

**Startup Verification** (when running `python app.py`):
```
[MCP:Client] - INFO - ================================================================================
[MCP:Client] - INFO - INITIALIZING MCP CLIENT MANAGER
[MCP:MarketData] - INFO - MarketDataMCP initialized with provider: alpha_vantage
[MCP:Client] - INFO - ✓ Market Data MCP initialized
[MCP:MortgageRates] - INFO - MortgageRatesMCP initialized
[MCP:Client] - INFO - ✓ Tools registry built with 15 total tools
```

**Tool Call Success**:
```
[MCP:Client] - INFO - [TOOL CALL] Calling 'get_stock_price' with args: {'symbol': 'AAPL'}
[MCP:MarketData] - DEBUG - get_stock_price called with symbol: AAPL
[MCP:MarketData] - INFO - ✓ Successfully fetched AAPL: $150.23
[MCP:Client] - INFO - ✓ Tool 'get_stock_price' executed successfully
```

**Common Issues**:
- Missing `OPENAI_API_KEY`: App won't start; check `.env` in `web_app/`
- Missing `MARKET_DATA_API_KEY`: Market tools return error, agent continues with fallback
- MCP initialization failure: Check log for "MCP client not available"; agent gracefully degrades
- Rate limiting (429 error): Built-in 5-min caching should help; wait then retry

## Testing & Deployment

### Unit Tests
- `test_setup.py`: Validates dependency installation and basic module imports
- Run with: `python test_setup.py` (checks Flask, LangChain, MCP servers import correctly)

### Integration Testing
- Start with simple agent requests before testing MCP tools
- Test without API keys first: agents function with fallback logic
- Then add API keys (MARKET_DATA_API_KEY, FRED_API_KEY) and retest to verify MCP integration

### MCP Fallback Mode
- Agents continue planning without MCP data if servers unavailable (graceful degradation)
- When `ENABLE_MCP_SERVERS=false` or APIs are down, tools return error strings instead of data
- Agent reasoning pipeline adapts; final plans remain actionable

## Critical Troubleshooting

### "Module not found" errors
**Problem**: `ImportError` when starting app.py  
**Solution**: Ensure `web_app/` is current directory and `.venv` is activated. Virtual env must have all packages from `requirements.txt` installed.

### MCP client returns None
**Problem**: All MCP tools return "MCP client not available"  
**Solution**: Check MCP initialization in startup logs. If `[MCP:Client]` banner missing, verify:
- All MCP server files exist in `mcp_servers/`
- No syntax errors: `python -m py_compile mcp_servers/*.py`
- Environment variables for APIs aren't breaking initialization (graceful degradation happens if APIs not configured)

### Agent produces vague recommendations
**Problem**: Plan lacks specifics about rates, inflation, etc.  
**Solution**: Agent is working without live MCP data. Add API keys:
- `MARKET_DATA_API_KEY` from Alpha Vantage or IEX Cloud
- `FRED_API_KEY` from Federal Reserve (https://fred.stlouisfed.org/docs/api/)
- Restart app; agent now has real data for specific recommendations

### Flask session errors
**Problem**: Session files not persisting between requests  
**Solution**: Check `SESSION_TYPE = 'filesystem'` in `config.py`. Session storage uses `flask_session/` directory. Ensure directory exists and is writable: `ls -la web_app/flask_session/`

## File Map of Essentials

| File | Purpose |
|------|---------|
| `app.py` | Flask routes, session mgmt, PDF/DOCX export |
| `agents.py` | LangChain agents, tool definitions, MCP wrappers |
| `config.py` | Environment-based configuration |
| `mcp_client.py` | MCPClientManager unifying all MCP servers |
| `market_data_mcp.py` | Stock/index data via Alpha Vantage or IEX |
| `mortgage_rates_mcp.py` | Mortgage & interest rates via FRED |
| `economic_data_mcp.py` | Inflation, unemployment, GDP via FRED |
| `visualizations.py` | Plotly chart generation for projections |

