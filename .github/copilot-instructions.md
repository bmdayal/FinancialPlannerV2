# Copilot Instructions for FinancialPlannerV2

## Project Overview

**FinancialPlannerV2** is an agentic AI financial planning system powered by LangChain, OpenAI GPT-4, and Flask. It uses specialized AI agents to create personalized financial plans across multiple life goals (retirement, homeownership, education, insurance, estate planning, etc.).

### Architecture: Three-Tier System

1. **Web App Layer** (`web_app/`): Flask REST API + HTML/JS frontend
2. **Agent Layer** (`web_app/agents.py`): LangChain agents with tool orchestration
3. **MCP Servers** (`mcp_servers/`): External API integrations for real-time market/economic data

## Critical Workflows

### Running the Application

```powershell
cd web_app
python app.py
# Launches Flask server at http://localhost:5000
# Requires: OPENAI_API_KEY in .env
```

### MCP Servers (Model Context Protocol)

The three specialized MCP servers provide real-time financial data:

- **`market_data_mcp.py`**: Stock prices, market indices via Alpha Vantage/IEX Cloud API
- **`mortgage_rates_mcp.py`**: Mortgage rates via FRED API (Federal Reserve)
- **`economic_data_mcp.py`**: Inflation, unemployment, GDP via FRED API
- **`mcp_client.py`**: Unified MCPClientManager that routes tool calls to appropriate servers

**Key Pattern**: All MCP servers follow this design:
```python
class [XyzMCP]:
    def __init__(self, api_key):
        self.api_key = api_key
        logger.info("Server initialized")
    
    def tool_method(self, params):
        # Call external API, cache results for 5 min
        return {"result": data, "success": True}
```

Tools registered in `MCPClientManager._build_tools_registry()` and exposed to agents via `@tool` decorator wrappers in `agents.py`.

## Code Organization Patterns

### Agent Tool Definition Pattern

In `agents.py`, all MCP-backed tools follow this structure:

```python
@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price for investment analysis."""
    logger.debug(f"[AGENT] Calling MCP tool: get_stock_price(symbol={symbol})")
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_stock_price', symbol=symbol)
    return json.dumps(result.get('result', result))
```

**Why this pattern**: Graceful degradation if MCP servers unavailable; consistent logging for debugging.

### Financial Planning Agent States

Agents use LangChain's `StateGraph` with `TypedDict` for state management. State includes:
- User messages and AI responses
- Accumulated planning data
- Tool outputs
- Conversation history

See `class AgentState(TypedDict)` in agents.py for full schema.

### Configuration Management

`config.py` uses environment variables with safe defaults:
- `OPENAI_API_KEY` (required)
- `MARKET_DATA_API_KEY` + `MARKET_DATA_PROVIDER` (optional, defaults to 'alpha_vantage')
- `FRED_API_KEY` (optional, for inflation/rate data)
- `ENABLE_MCP_SERVERS` (controls fallback behavior)

Environment configs: `DevelopmentConfig`, `ProductionConfig`, `TestingConfig` inherit from base `Config`.

## Data Flows & Integration Points

### User Request Flow

1. Frontend (index.html) → POST `/api/plan` with user inputs
2. `app.py` handler creates `AgentState` and invokes `OrchestratorAgent`
3. OrchestratorAgent routes to domain-specific agents (RetirementAgent, etc.)
4. Agents call tools (`@tool` decorators) → MCP server methods
5. MCP servers hit external APIs (Alpha Vantage, FRED, IEX Cloud)
6. Results cached for 5 minutes, returned to agent for reasoning
7. Agent generates plan, stored in Flask session
8. Plan exported as PDF/DOCX via `reportlab`/`python-docx`

### Tool Call Chain Example

```
get_stock_price("AAPL")
  → agents.py wrapper calls mcp_client.call_tool()
    → MCPClientManager routes to market_data.get_stock_price()
      → Alpha Vantage API (with cache check)
        → Returns {price, change, %, high, low, etc.}
      → Cached for 300 sec
    → JSON serialized back to LangChain agent
```

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

All MCP components have DEBUG-level logging enabled:
```bash
# Monitor startup and tool calls
python app.py 2>&1 | findstr "MCP\|AGENT\|ERROR"

# Verify MCP client initialization
python -c "from mcp_servers.mcp_client import get_mcp_client; get_mcp_client()"
```

Look for:
- `[MCP:MarketData] - Fetching stock price from Alpha Vantage`
- `[AGENT] Calling MCP tool: get_stock_price`
- API key status messages during initialization

## Testing Notes

- **Unit Tests**: `test_setup.py` validates dependency installation
- **Integration**: Start with simple agent requests before testing MCP tools
- **MCP Fallback**: Agents continue without MCP data if servers unavailable (graceful degradation)

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

