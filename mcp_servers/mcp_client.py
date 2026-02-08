"""
MCP Client Integration Module
Unified interface for accessing all MCP servers and tools
"""
import os
import json
from typing import Optional, Dict, Any, List
import logging
from market_data_mcp import MarketDataMCP
from mortgage_rates_mcp import MortgageRatesMCP
from economic_data_mcp import EconomicDataMCP

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [MCP:Client] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class MCPClientManager:
    """Unified client for managing all MCP servers"""
    
    def __init__(self):
        """Initialize all MCP servers"""
        logger.info("=" * 80)
        logger.info("INITIALIZING MCP CLIENT MANAGER")
        logger.info("=" * 80)
        
        self.market_data = MarketDataMCP(
            api_key=os.getenv('MARKET_DATA_API_KEY'),
            provider=os.getenv('MARKET_DATA_PROVIDER', 'alpha_vantage')
        )
        logger.info(f"✓ Market Data MCP initialized (Provider: {os.getenv('MARKET_DATA_PROVIDER', 'alpha_vantage')})")
        
        self.mortgage_rates = MortgageRatesMCP(
            fred_api_key=os.getenv('FRED_API_KEY'),
            mortgage_api_key=os.getenv('MORTGAGE_API_KEY')
        )
        logger.info("✓ Mortgage Rates MCP initialized")
        
        self.economic_data = EconomicDataMCP(
            fred_api_key=os.getenv('FRED_API_KEY')
        )
        logger.info("✓ Economic Data MCP initialized")
        
        self.tools_registry = self._build_tools_registry()
        logger.info(f"✓ Tools registry built with {sum(len(tools) for tools in self.tools_registry.values())} total tools")
        logger.info("=" * 80)
    
    def _build_tools_registry(self) -> Dict[str, Any]:
        """Build registry of all available MCP tools"""
        return {
            'market': {
                'get_stock_price': self.market_data.get_stock_price,
                'get_portfolio_performance': self.market_data.get_portfolio_performance,
                'get_market_indices': self.market_data.get_market_indices,
                'search_stocks': self.market_data.search_stocks,
            },
            'mortgage': {
                'get_current_mortgage_rates': self.mortgage_rates.get_current_mortgage_rates,
                'calculate_mortgage_payment': self.mortgage_rates.calculate_mortgage_payment,
                'get_federal_funds_rate': self.mortgage_rates.get_federal_funds_rate,
                'get_prime_rate': self.mortgage_rates.get_prime_rate,
                'project_rate_scenarios': self.mortgage_rates.project_rate_scenarios,
                'compare_mortgage_options': self.mortgage_rates.compare_mortgage_options,
            },
            'economic': {
                'get_inflation_rate': self.economic_data.get_inflation_rate,
                'get_unemployment_rate': self.economic_data.get_unemployment_rate,
                'get_gdp_growth': self.economic_data.get_gdp_growth,
                'project_retirement_inflation': self.economic_data.project_retirement_inflation,
                'get_economic_dashboard': self.economic_data.get_economic_dashboard,
                'compare_inflation_scenarios': self.economic_data.compare_inflation_scenarios,
            }
        }
    
    def get_tools_for_agents(self) -> List[Dict[str, Any]]:
        """
        Get all tools in LangChain-compatible format
        
        Returns:
            List of tool definitions for LangChain agents
        """
        tools = []
        
        # Market Data Tools
        tools.extend([
            {
                'name': 'get_stock_price',
                'description': 'Get current stock price and market data for a given ticker symbol',
                'category': 'market',
                'function': self.market_data.get_stock_price
            },
            {
                'name': 'get_portfolio_performance',
                'description': 'Calculate portfolio performance based on current market prices',
                'category': 'market',
                'function': self.market_data.get_portfolio_performance
            },
            {
                'name': 'get_market_indices',
                'description': 'Get major market indices (S&P 500, Nasdaq, Dow Jones) data',
                'category': 'market',
                'function': self.market_data.get_market_indices
            },
            {
                'name': 'search_stocks',
                'description': 'Search for stocks by company name, symbol, or sector',
                'category': 'market',
                'function': self.market_data.search_stocks
            },
        ])
        
        # Mortgage & Interest Rate Tools
        tools.extend([
            {
                'name': 'get_current_mortgage_rates',
                'description': 'Get current mortgage rates for 15-year, 30-year, jumbo, and FHA loans',
                'category': 'mortgage',
                'function': self.mortgage_rates.get_current_mortgage_rates
            },
            {
                'name': 'calculate_mortgage_payment',
                'description': 'Calculate monthly mortgage payment and amortization schedule',
                'category': 'mortgage',
                'function': self.mortgage_rates.calculate_mortgage_payment
            },
            {
                'name': 'get_federal_funds_rate',
                'description': 'Get current Federal Reserve Funds Rate',
                'category': 'mortgage',
                'function': self.mortgage_rates.get_federal_funds_rate
            },
            {
                'name': 'get_prime_rate',
                'description': 'Get current Bank Prime Lending Rate',
                'category': 'mortgage',
                'function': self.mortgage_rates.get_prime_rate
            },
            {
                'name': 'project_rate_scenarios',
                'description': 'Project mortgage rate scenarios for conservative, standard, or aggressive outlook',
                'category': 'mortgage',
                'function': self.mortgage_rates.project_rate_scenarios
            },
            {
                'name': 'compare_mortgage_options',
                'description': 'Compare mortgage payments across different rates and terms',
                'category': 'mortgage',
                'function': self.mortgage_rates.compare_mortgage_options
            },
        ])
        
        # Economic Data Tools
        tools.extend([
            {
                'name': 'get_inflation_rate',
                'description': 'Get current inflation rate based on Consumer Price Index',
                'category': 'economic',
                'function': self.economic_data.get_inflation_rate
            },
            {
                'name': 'get_unemployment_rate',
                'description': 'Get current unemployment rate',
                'category': 'economic',
                'function': self.economic_data.get_unemployment_rate
            },
            {
                'name': 'get_gdp_growth',
                'description': 'Get current GDP growth data',
                'category': 'economic',
                'function': self.economic_data.get_gdp_growth
            },
            {
                'name': 'project_retirement_inflation',
                'description': 'Project retirement expenses accounting for inflation',
                'category': 'economic',
                'function': self.economic_data.project_retirement_inflation
            },
            {
                'name': 'get_economic_dashboard',
                'description': 'Get comprehensive dashboard of key economic indicators',
                'category': 'economic',
                'function': self.economic_data.get_economic_dashboard
            },
            {
                'name': 'compare_inflation_scenarios',
                'description': 'Compare retirement expenses under different inflation scenarios',
                'category': 'economic',
                'function': self.economic_data.compare_inflation_scenarios
            },
        ])
        
        return tools
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool by name with provided arguments
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Result from the tool
        """
        logger.info(f"[TOOL CALL] Calling '{tool_name}' with args: {kwargs}")
        
        for category, tools in self.tools_registry.items():
            if tool_name in tools:
                try:
                    logger.debug(f"Found tool '{tool_name}' in category '{category}'")
                    result = tools[tool_name](**kwargs)
                    
                    # Check if result contains an error
                    if isinstance(result, dict) and 'error' in result:
                        logger.warning(f"✗ Tool '{tool_name}' returned error: {result['error']}")
                    else:
                        logger.info(f"✓ Tool '{tool_name}' executed successfully")
                    
                    return {
                        'success': True,
                        'tool': tool_name,
                        'category': category,
                        'result': result
                    }
                except TypeError as e:
                    logger.error(f"✗ Invalid arguments for tool '{tool_name}': {str(e)}", exc_info=True)
                    return {
                        'success': False,
                        'tool': tool_name,
                        'error': f'Invalid arguments: {str(e)}'
                    }
                except Exception as e:
                    logger.error(f"✗ Exception in tool '{tool_name}': {str(e)}", exc_info=True)
                    return {
                        'success': False,
                        'tool': tool_name,
                        'error': str(e)
                    }
        
        logger.error(f"✗ Tool '{tool_name}' not found in registry")
        return {
            'success': False,
            'tool': tool_name,
            'error': f'Tool "{tool_name}" not found'
        }
    
    def get_tools_summary(self) -> Dict[str, List[str]]:
        """Get summary of all available tools by category"""
        summary = {}
        for category, tools in self.tools_registry.items():
            summary[category] = list(tools.keys())
        return summary


# Singleton instance
_mcp_client = None


def get_mcp_client() -> MCPClientManager:
    """Get or create the MCP client singleton"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClientManager()
    return _mcp_client


# For testing
if __name__ == "__main__":
    client = MCPClientManager()
    
    print("MCP Tools Registry:")
    print(json.dumps(client.get_tools_summary(), indent=2))
    
    print("\n\nTesting Market Data Tool:")
    result = client.call_tool('get_stock_price', symbol='AAPL')
    print(json.dumps(result, indent=2))
    
    print("\n\nTesting Mortgage Rates Tool:")
    result = client.call_tool('get_current_mortgage_rates')
    print(json.dumps(result, indent=2))
    
    print("\n\nTesting Economic Data Tool:")
    result = client.call_tool('get_inflation_rate')
    print(json.dumps(result, indent=2))
