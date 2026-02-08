"""
Market Data MCP Server
Provides real-time stock prices, market data, and portfolio analysis
External API: Alpha Vantage or IEX Cloud
"""
import os
import json
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import logging

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [MCP:MarketData] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MarketDataMCP:
    """Market Data MCP Server for stock prices and market indices"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "alpha_vantage"):
        """
        Initialize Market Data MCP
        
        Args:
            api_key: API key for the market data provider
            provider: "alpha_vantage" or "iex_cloud"
        """
        self.api_key = api_key or os.getenv('MARKET_DATA_API_KEY', '')
        self.provider = provider
        self.base_urls = {
            'alpha_vantage': 'https://www.alphavantage.co/query',
            'iex_cloud': 'https://cloud.iexapis.com/stable'
        }
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
        logger.info(f"MarketDataMCP initialized with provider: {self.provider}")
        if not self.api_key:
            logger.warning(f"No API key found for {self.provider} - some functions may fail")
        
    def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current stock price and market data
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            Dictionary with price, change, and market data
        """
        try:
            if self.provider == 'alpha_vantage':
                return self._get_stock_price_av(symbol)
            elif self.provider == 'iex_cloud':
                return self._get_stock_price_iex(symbol)
        except Exception as e:
            logger.error(f"Error fetching stock price for {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def _get_stock_price_av(self, symbol: str) -> Dict[str, Any]:
        """Get stock price from Alpha Vantage"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_urls['alpha_vantage'], params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            result = {
                'symbol': symbol,
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': float(quote.get('10. change percent', '0').rstrip('%')),
                'volume': int(quote.get('06. volume', 0)),
                'timestamp': datetime.now().isoformat()
            }
            logger.info(f"[TOOL CALL] get_stock_price('{symbol}') -> ${result['price']}")
            return result
        logger.warning(f"No quote data for {symbol}")
        return {"error": "Symbol not found or API limit reached", "symbol": symbol}
    
    def _get_stock_price_iex(self, symbol: str) -> Dict[str, Any]:
        """Get stock price from IEX Cloud"""
        url = f"{self.base_urls['iex_cloud']}/stock/{symbol}/quote"
        params = {'token': self.api_key}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'latestPrice' in data:
            return {
                'symbol': symbol,
                'price': data.get('latestPrice', 0),
                'change': data.get('change', 0),
                'change_percent': data.get('changePercent', 0) * 100,
                'volume': data.get('latestVolume', 0),
                'market_cap': data.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
            }
        return {"error": "Symbol not found", "symbol": symbol}
    
    def get_portfolio_performance(self, holdings: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Calculate portfolio performance based on current prices
        
        Args:
            holdings: List of dicts with 'symbol', 'quantity', 'purchase_price'
            
        Returns:
            Portfolio performance metrics
        """
        try:
            total_cost = 0
            total_value = 0
            positions = []
            
            for holding in holdings:
                symbol = holding.get('symbol')
                quantity = holding.get('quantity', 0)
                purchase_price = holding.get('purchase_price', 0)
                
                cost = quantity * purchase_price
                total_cost += cost
                
                # Get current price
                price_data = self.get_stock_price(symbol)
                current_price = price_data.get('price', purchase_price)
                current_value = quantity * current_price
                total_value += current_value
                
                positions.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'current_price': current_price,
                    'cost_basis': cost,
                    'current_value': current_value,
                    'gain_loss': current_value - cost,
                    'gain_loss_percent': ((current_value - cost) / cost * 100) if cost > 0 else 0
                })
            
            total_gain_loss = total_value - total_cost
            
            return {
                'total_cost_basis': total_cost,
                'total_current_value': total_value,
                'total_gain_loss': total_gain_loss,
                'total_gain_loss_percent': (total_gain_loss / total_cost * 100) if total_cost > 0 else 0,
                'positions': positions,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calculating portfolio performance: {str(e)}")
            return {"error": str(e)}
    
    def get_market_indices(self) -> Dict[str, Any]:
        """
        Get major market indices data (S&P 500, Nasdaq, Dow Jones)
        
        Returns:
            Dictionary with major indices data
        """
        try:
            indices = ['SPY', 'QQQ', 'DIA']  # Proxies for S&P 500, Nasdaq, Dow
            index_names = {'SPY': 'S&P 500', 'QQQ': 'Nasdaq-100', 'DIA': 'Dow Jones'}
            
            results = {}
            for symbol in indices:
                price_data = self.get_stock_price(symbol)
                if 'error' not in price_data:
                    results[index_names.get(symbol, symbol)] = {
                        'symbol': symbol,
                        'price': price_data.get('price'),
                        'change': price_data.get('change'),
                        'change_percent': price_data.get('change_percent')
                    }
            
            return {
                'indices': results,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching market indices: {str(e)}")
            return {"error": str(e)}
    
    def search_stocks(self, keywords: str) -> Dict[str, Any]:
        """
        Search for stocks by keywords or sector
        
        Args:
            keywords: Search terms (company name, sector, etc.)
            
        Returns:
            List of matching stocks
        """
        try:
            if self.provider == 'alpha_vantage':
                params = {
                    'function': 'SYMBOL_SEARCH',
                    'keywords': keywords,
                    'apikey': self.api_key
                }
                response = requests.get(self.base_urls['alpha_vantage'], params=params, timeout=10)
                data = response.json()
                
                return {
                    'results': data.get('bestMatches', []),
                    'count': len(data.get('bestMatches', []))
                }
            else:
                return {"error": "Search not available with current provider"}
        except Exception as e:
            logger.error(f"Error searching stocks: {str(e)}")
            return {"error": str(e)}


# For running as a standalone service
if __name__ == "__main__":
    mcp = MarketDataMCP()
    
    # Test calls
    print("Stock Price Test:")
    print(json.dumps(mcp.get_stock_price('AAPL'), indent=2))
    
    print("\nMarket Indices Test:")
    print(json.dumps(mcp.get_market_indices(), indent=2))
    
    print("\nPortfolio Performance Test:")
    holdings = [
        {'symbol': 'AAPL', 'quantity': 10, 'purchase_price': 150},
        {'symbol': 'MSFT', 'quantity': 5, 'purchase_price': 300}
    ]
    print(json.dumps(mcp.get_portfolio_performance(holdings), indent=2))
