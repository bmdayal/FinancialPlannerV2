# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**Critical working-directory constraint**: `app.py` uses relative imports and expects `templates/`/`static/` in the current directory. Always run from `web_app/`:

```powershell
# From project root
.venv\Scripts\Activate.ps1
cd web_app
python app.py        # http://localhost:5000
# or
python start.py      # includes env/dependency checks
```

Running from the wrong directory causes `ModuleNotFoundError` or template 404s.

## Testing & Diagnostics

```powershell
# Syntax check
python -m py_compile web_app/agents.py mcp_servers/*.py

# Dependency / import validation
python web_app/test_setup.py

# MCP integration (all 16 tools) — run from project root
python test_mcp_tools.py

# MCP diagnostics (API keys, connectivity, rate limits) — run from web_app/
cd web_app && python ../debug_mcp.py

# Single tool smoke test (from project root)
python -c "
import sys, os; sys.path.insert(0, 'mcp_servers'); os.chdir('web_app')
from dotenv import load_dotenv; load_dotenv()
from mcp_client import MCPClientManager
import json
print(json.dumps(MCPClientManager().call_tool('get_stock_price', symbol='AAPL'), indent=2))
"
```

## Architecture

3-tier agentic pipeline:

```
User (templates/index.html)
  → Flask API (app.py)                      # routes, export (PDF/DOCX)
    → OrchestratorAgent (agents.py)         # routes by plan name
      → 6 Specialized Agents (agents.py)    # Retirement, Insurance, Estate,
        → @tool wrappers (agents.py)        #   Wealth, Education, Tax
          → MCPClientManager (mcp_client.py)
            → MCP servers (mcp_servers/)    # market_data, mortgage_rates,
              → External APIs               #   economic_data (FRED, yfinance,
                                            #   Alpha Vantage)
```

**Core design principle**: Graceful degradation everywhere. If `mcp_client` is None or an API fails, agents fall back to hardcoded assumptions (e.g., 3% inflation) rather than crashing.

**LLM invocation pattern per agent**: 2 calls per agent (`(2 × N) + 1` total for N agents):
1. Tool selection — LLM with bound tools decides which tools to call
2. Synthesis — LLM takes tool results and generates the plan narrative
3. Executive summary — OrchestratorAgent combines all plans (1 call, always)

If tool selection returns no `tool_calls`, fallback mode executes tools directly and skips the synthesis LLM call.

## Code Patterns — Follow Exactly

### @tool wrapper (agents.py)

Every MCP-backed tool must follow this pattern:

```python
@tool
def get_stock_price(symbol: str) -> str:
    """Docstring used as tool description by LangChain."""
    logger.debug(f"[AGENT] Calling MCP tool: get_stock_price(symbol={symbol})")
    if mcp_client is None:
        return "MCP client not available"
    result = mcp_client.call_tool('get_stock_price', symbol=symbol)
    logger.debug(f"[AGENT] get_stock_price result: {result}")
    return json.dumps(result.get('result', result))
```

- Always return `json.dumps(...)`, never a raw dict — LangChain requires string return values
- Always guard with `if mcp_client is None`
- Tool names must match exactly between `MCPClientManager._build_tools_registry()` and the `@tool` function name

### AgentState mutation rules

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]  # never mutate directly
    user_info: Dict[str, Any]
    selected_plans: List[str]
    plan_summaries: Dict[str, str]
    mcp_data: Dict[str, Any]   # frontend reads this to show which tools ran
    next_agent: str
```

- Never push to `messages` manually — `operator.add` accumulates automatically
- Always populate `mcp_data[plan_name]["tools"]` with `{"name": tool_name, "args": args, "result": result}` — the frontend displays this

### Adding a new agent

1. Create class in `agents.py` with `__init__(self, llm)` + `process(self, state) -> AgentState`
2. Add to `OrchestratorAgent._route_to_specialized_agent()` plan-name mapping
3. Add `@tool` wrappers following the pattern above
4. Register new MCP tools in `MCPClientManager._build_tools_registry()` first
5. Add plan to `/api/plans` endpoint in `app.py`

**Never modify `AgentState` without updating all 6 agent classes** — they all depend on the same shape.

## Configuration

`web_app/.env` (copy from `.env.example` or run `python setup.py`):

```env
OPENAI_API_KEY=sk-...          # required — app crashes without it
MARKET_DATA_API_KEY=...         # optional — falls back gracefully
MARKET_DATA_PROVIDER=yfinance   # yfinance (free/unlimited, best for dev)
                                # alpha_vantage (25 calls/day free, $20/mo unlimited)
                                # iex_cloud (100/mo free)
FRED_API_KEY=...                # optional — economic data (inflation, GDP, unemployment)
FLASK_ENV=development
APP_PORT=5000                   # change if port in use
ENABLE_MCP_SERVERS=true
MCP_CACHE_TIMEOUT=300           # 5-min cache prevents rate limiting
```

Config classes in `config.py`: `DevelopmentConfig`, `ProductionConfig`, `TestingConfig` — selected via `FLASK_ENV`.

## Known Issues

- **Alpha Vantage free tier**: 25 calls/day; returns `200 OK` with empty data when exhausted. Switch to `MARKET_DATA_PROVIDER=yfinance` for development.
- **FRED API**: Occasionally returns malformed JSON — needs `try/except` in `economic_data_mcp.py`.
- **Two venvs**: `.venv/` at project root is the primary; `web_app/venv/` may exist but activate `.venv` from root.

## Log Prefixes for Debugging

| Prefix | Source |
|---|---|
| `[MCP:Client]` | mcp_client.py — routing and registry |
| `[MCP:MarketData]` | market_data_mcp.py |
| `[MCP:Economic]` | economic_data_mcp.py |
| `[AGENT]` | agents.py tool calls |

All components default to DEBUG level. A `✓` in MCP logs indicates a successful API call.
