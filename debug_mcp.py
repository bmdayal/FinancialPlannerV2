"""
MCP Troubleshooting & Debugging Guide

This module provides diagnostic tools to identify and fix MCP issues
"""
import sys
import os
import requests
from datetime import datetime
from pathlib import Path

# Load .env file from web_app directory
web_app_dir = Path(__file__).parent / 'web_app'
env_file = web_app_dir / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp_servers'))

def check_api_keys():
    """Verify all API keys are configured"""
    print("\n" + "="*80)
    print("  API KEY CONFIGURATION CHECK")
    print("="*80 + "\n")
    
    keys = {
        'OPENAI_API_KEY': ('OpenAI', 'Required for agents'),
        'MARKET_DATA_API_KEY': ('Alpha Vantage', 'Optional - market data disabled if missing'),
        'FRED_API_KEY': ('Federal Reserve', 'Optional - economic data disabled if missing'),
        'MORTGAGE_API_KEY': ('Mortgage Rates', 'Optional - uses FRED by default'),
    }
    
    for env_var, (service, note) in keys.items():
        value = os.getenv(env_var, '')
        status = "✓" if value else "✗"
        masked = f"{value[:10]}...{value[-4:]}" if value else "[NOT SET]"
        print(f"{status} {env_var:<25} | {service:<20} | {masked:<20} | {note}")
    
    print()


def check_alpha_vantage_api():
    """Test Alpha Vantage API connectivity and rate limits"""
    print("\n" + "="*80)
    print("  ALPHA VANTAGE API TEST")
    print("="*80 + "\n")
    
    api_key = os.getenv('MARKET_DATA_API_KEY', '')
    if not api_key:
        print("✗ MARKET_DATA_API_KEY not set")
        print("  To get a free API key:")
        print("  1. Visit: https://www.alphavantage.co/api/")
        print("  2. Sign up for free tier")
        print("  3. Add to .env: MARKET_DATA_API_KEY=your_key_here")
        print()
        return
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}\n")
    
    # Test 1: Basic connectivity
    print("Test 1: Basic Connectivity")
    print("  Fetching AAPL quote...")
    try:
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': 'AAPL',
            'apikey': api_key
        }
        response = requests.get('https://www.alphavantage.co/query', 
                               params=params, 
                               timeout=10)
        
        print(f"  Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            
            # Check for rate limit error
            if 'Note' in data:
                print(f"  ⚠️  RATE LIMIT HIT: {data['Note']}")
                print("  Solution: Wait 60 seconds before next call")
                print("  Reason: Free tier limited to 5 calls/minute")
                print()
                return
            
            # Check for API key error
            if 'Error Message' in data:
                print(f"  ✗ API ERROR: {data['Error Message']}")
                print()
                return
            
            # Check for quote data
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                print(f"  ✓ Quote data received")
                print(f"    Symbol: {quote.get('01. symbol')}")
                print(f"    Price: ${quote.get('05. price')}")
                print(f"    Volume: {quote.get('06. volume'):,}")
            else:
                print(f"  ⚠️  NO QUOTE DATA")
                print(f"  Response: {data}")
                print()
                print("Possible causes:")
                print("  1. API Rate Limited (5 calls/min limit)")
                print("  2. Symbol not found on NYSE/NASDAQ")
                print("  3. API Key invalid or disabled")
                return
            
            print()
        else:
            print(f"  ✗ HTTP Error: {response.status_code}")
            print()
            return
    
    except requests.Timeout:
        print("  ✗ Request timed out (10 seconds)")
        print("  Check your internet connection")
        print()
        return
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        print()
        return
    
    # Test 2: Alternative symbols
    print("Test 2: Test Multiple Symbols (check for throttling)")
    test_symbols = ['SPY', 'QQQ', 'DIA']
    for symbol in test_symbols:
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': api_key
            }
            response = requests.get('https://www.alphavantage.co/query', 
                                   params=params, 
                                   timeout=10)
            
            data = response.json()
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                print(f"  ✓ {symbol}: ${quote.get('05. price')}")
            elif 'Note' in data:
                print(f"  ⚠️  {symbol}: RATE LIMITED")
            else:
                print(f"  ⚠️  {symbol}: No quote data")
        except Exception as e:
            print(f"  ✗ {symbol}: {str(e)}")
    
    print()


def check_fred_api():
    """Test FRED API connectivity"""
    print("\n" + "="*80)
    print("  FEDERAL RESERVE (FRED) API TEST")
    print("="*80 + "\n")
    
    api_key = os.getenv('FRED_API_KEY', '')
    if not api_key:
        print("✗ FRED_API_KEY not set")
        print("  To get a free API key:")
        print("  1. Visit: https://fred.stlouisfed.org/docs/api/")
        print("  2. Sign up for free account")
        print("  3. Add to .env: FRED_API_KEY=your_key_here")
        print()
        return
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}\n")
    
    # Test: Get inflation data
    print("Test: Fetching Inflation Rate (CPIAUCSL)")
    try:
        params = {
            'series_id': 'CPIAUCSL',
            'api_key': api_key,
            'sort_order': 'desc',
            'limit': 1
        }
        response = requests.get('https://api.stlouisfed.org/fred/series/observations',
                               params=params,
                               timeout=10)
        
        print(f"  Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            observations = data.get('observations', [])
            if observations:
                obs = observations[0]
                print(f"  ✓ Data received")
                print(f"    Date: {obs.get('date')}")
                print(f"    CPI Value: {obs.get('value')}")
            else:
                print(f"  ⚠️  No observations returned")
                print(f"  Response: {data}")
        else:
            print(f"  ✗ HTTP Error: {response.status_code}")
            print(f"  Response: {data}")
    
    except requests.Timeout:
        print("  ✗ Request timed out")
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
    
    print()


def check_mcp_client():
    """Test MCP Client initialization"""
    print("\n" + "="*80)
    print("  MCP CLIENT INITIALIZATION TEST")
    print("="*80 + "\n")
    
    try:
        from mcp_client import MCPClientManager
        
        print("Initializing MCPClientManager...")
        mcp = MCPClientManager()
        
        print("✓ MCPClientManager initialized successfully\n")
        
        # Check tools registry
        total_tools = sum(len(tools) for tools in mcp.tools_registry.values())
        print(f"Tools registered: {total_tools}")
        for category, tools in mcp.tools_registry.items():
            print(f"  - {category}: {len(tools)} tools")
        
        print()
    
    except Exception as e:
        print(f"✗ Failed to initialize MCPClientManager")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print()


def check_rate_limiting():
    """Explain Alpha Vantage rate limiting"""
    print("\n" + "="*80)
    print("  ALPHA VANTAGE RATE LIMITING")
    print("="*80 + "\n")
    
    print("FREE TIER LIMITS:")
    print("  ✓ 5 API requests per minute")
    print("  ✓ 100 API requests per day")
    print("  ✓ Calls are subject to burst limits")
    print()
    print("WHEN YOU SEE 'No Quote Data':")
    print("  1. You've exceeded 5 calls/minute")
    print("  2. Solution: Wait 60 seconds before trying again")
    print()
    print("HOW TO AVOID:")
    print("  ✓ Add delays between requests: time.sleep(13)  # 13 seconds = safe margin")
    print("  ✓ Use caching (5-minute TTL implemented in MCP)")
    print("  ✓ Upgrade to premium plan for higher limits")
    print("  ✓ Stagger requests across multiple symbols")
    print()


def main():
    """Run all diagnostics"""
    print("\n" + "=" * 80)
    print("  MCP DIAGNOSTIC SUITE".center(80))
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
    print("=" * 80)
    
    check_api_keys()
    check_mcp_client()
    check_alpha_vantage_api()
    check_fred_api()
    check_rate_limiting()
    
    print("\n" + "=" * 80)
    print("  DIAGNOSTICS COMPLETE".center(80))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
