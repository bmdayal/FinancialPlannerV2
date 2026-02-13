#!/usr/bin/env python
"""
MCP Tools Test Suite
Validates all MCP server functions independently without agent overhead
"""
import sys
import os
import json
from datetime import datetime

# Add mcp_servers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp_servers'))

from mcp_client import MCPClientManager

def print_header(title):
    """Print formatted test section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_result(tool_name, result, status="✓"):
    """Print formatted test result"""
    print(f"{status} {tool_name}")
    print(f"  Result: {json.dumps(result, indent=2)[:200]}...")
    print()

def test_market_data_tools():
    """Test all market data MCP tools"""
    print_header("MARKET DATA MCP TOOLS")
    
    mcp = MCPClientManager()
    
    # Test 1: Get Stock Price (Individual Stock)
    print("Test 1: Get Stock Price for AAPL")
    result = mcp.call_tool('get_stock_price', symbol='AAPL')
    print(f"Success: {result['success']}")
    if result['success']:
        price_data = result['result']
        symbol = price_data.get('symbol')
        price = price_data.get('price')
        change = price_data.get('change')
        change_percent = price_data.get('change_percent')
        volume = price_data.get('volume')
        print(f"  Symbol: {symbol if symbol is not None else 'N/A'}")
        print(f"  Price: ${price if price is not None else 'N/A'}")
        print(f"  Change: {change if change is not None else 'N/A'} ({change_percent if change_percent is not None else 'N/A'}%)")
        print(f"  Volume: {volume:,}" if volume is not None else "  Volume: N/A")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Removed tests for get_market_indices and search_stocks (only yfinance-based tests remain)
    
    # Test 4: Portfolio Performance
    print("Test 4: Calculate Portfolio Performance")
    holdings = [
        {'symbol': 'AAPL', 'quantity': 10, 'purchase_price': 150},
        {'symbol': 'MSFT', 'quantity': 5, 'purchase_price': 300}
    ]
    result = mcp.call_tool('get_portfolio_performance', holdings=holdings)
    print(f"Success: {result['success']}")
    if result['success']:
        perf = result['result']
        print(f"  Total Cost Basis: ${perf.get('total_cost_basis'):,.2f}")
        print(f"  Current Value: ${perf.get('total_current_value'):,.2f}")
        print(f"  Gain/Loss: ${perf.get('total_gain_loss'):,.2f} ({perf.get('total_gain_loss_percent'):.2f}%)")
    else:
        print(f"  Error: {result.get('error')}")
    print()


def test_mortgage_rates_tools():
    """Test all mortgage rates MCP tools"""
    print_header("MORTGAGE RATES MCP TOOLS")
    
    mcp = MCPClientManager()
    
    # Test 1: Get Current Mortgage Rates
    print("Test 1: Get Current Mortgage Rates")
    result = mcp.call_tool('get_current_mortgage_rates')
    print(f"Success: {result['success']}")
    if result['success']:
        rates = result['result'].get('rates', {})
        for rate_type, rate_value in rates.items():
            print(f"  {rate_type}: {rate_value}%")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 2: Calculate Mortgage Payment
    print("Test 2: Calculate Mortgage Payment")
    print("  Principal: $300,000")
    print("  Annual Rate: 7.5%")
    print("  Years: 30")
    result = mcp.call_tool('calculate_mortgage_payment', 
                          principal=300000, 
                          annual_rate=7.5, 
                          years=30)
    print(f"Success: {result['success']}")
    if result['success']:
        payment = result['result']
        print(f"  Monthly Payment: ${payment.get('monthly_payment', 0):,.2f}")
        print(f"  Total Paid: ${payment.get('total_paid', 0):,.2f}")
        print(f"  Total Interest: ${payment.get('total_interest', 0):,.2f}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 3: Get Federal Funds Rate
    print("Test 3: Get Federal Funds Rate")
    result = mcp.call_tool('get_federal_funds_rate')
    print(f"Success: {result['success']}")
    if result['success']:
        rate = result['result']
        print(f"  Rate: {rate.get('rate')}%")
        print(f"  Source: {rate.get('source')}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 4: Get Prime Rate
    print("Test 4: Get Prime Rate")
    result = mcp.call_tool('get_prime_rate')
    print(f"Success: {result['success']}")
    if result['success']:
        rate = result['result']
        print(f"  Rate: {rate.get('rate')}%")
    else:
        print(f"  Error: {result.get('error')}")
    print()


def test_economic_data_tools():
    """Test all economic data MCP tools"""
    print_header("ECONOMIC DATA MCP TOOLS")
    
    mcp = MCPClientManager()
    
    # Test 1: Get Inflation Rate
    print("Test 1: Get Inflation Rate")
    result = mcp.call_tool('get_inflation_rate')
    print(f"Success: {result['success']}")
    if result['success']:
        inflation = result['result']
        print(f"  Year-over-Year: {inflation.get('inflation_rate_yoy')}%")
        print(f"  Current CPI: {inflation.get('current_cpi')}")
        print(f"  Date: {inflation.get('date')}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 2: Get Unemployment Rate
    print("Test 2: Get Unemployment Rate")
    result = mcp.call_tool('get_unemployment_rate')
    print(f"Success: {result['success']}")
    if result['success']:
        unemployment = result['result']
        print(f"  Rate: {unemployment.get('unemployment_rate')}%")
        print(f"  Date: {unemployment.get('date')}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 3: Get GDP Growth
    print("Test 3: Get GDP Growth")
    result = mcp.call_tool('get_gdp_growth')
    print(f"Success: {result['success']}")
    if result['success']:
        gdp = result['result']
        print(f"  Growth Rate: {gdp.get('gdp_growth')}%")
        print(f"  Date: {gdp.get('date')}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 4: Project Retirement Inflation
    print("Test 4: Project Retirement Inflation")
    print("  Current Annual Expense: $50,000")
    print("  Years to Retirement: 20")
    result = mcp.call_tool('project_retirement_inflation',
                          current_annual_expense=50000,
                          years_to_retirement=20)
    print(f"Success: {result['success']}")
    if result['success']:
        projection = result['result']
        print(f"  Projected Annual Expense: ${projection.get('projected_annual_expense', 0):,.2f}")
        print(f"  Total 20-Year Cost: ${projection.get('total_20_year_cost', 0):,.2f}")
    else:
        print(f"  Error: {result.get('error')}")
    print()
    
    # Test 5: Get Economic Dashboard
    print("Test 5: Get Economic Dashboard (All Indicators)")
    result = mcp.call_tool('get_economic_dashboard')
    print(f"Success: {result['success']}")
    if result['success']:
        dashboard = result['result']
        print(f"  Inflation: {dashboard.get('inflation_rate')}%")
        print(f"  Unemployment: {dashboard.get('unemployment_rate')}%")
        print(f"  GDP Growth: {dashboard.get('gdp_growth')}%")
        print(f"  Federal Funds Rate: {dashboard.get('federal_funds_rate')}%")
    else:
        print(f"  Error: {result.get('error')}")
    print()


def test_error_handling():
    """Test error handling and edge cases"""
    print_header("ERROR HANDLING & EDGE CASES")
    
    mcp = MCPClientManager()
    
    # Test 1: Invalid Stock Symbol
    print("Test 1: Invalid Stock Symbol (INVALID123)")
    result = mcp.call_tool('get_stock_price', symbol='INVALID123')
    print(f"Success: {result['success']}")
    print(f"Error: {result.get('error')}")
    print()
    
    # Test 2: Invalid Tool Name
    print("Test 2: Invalid Tool Name (nonexistent_tool)")
    result = mcp.call_tool('nonexistent_tool')
    print(f"Success: {result['success']}")
    print(f"Error: {result.get('error')}")
    print()
    
    # Test 3: Missing Required Arguments
    print("Test 3: Missing Required Arguments (get_stock_price with no symbol)")
    result = mcp.call_tool('get_stock_price')
    print(f"Success: {result['success']}")
    print(f"Error: {result.get('error')}")
    print()
    
    # Test 4: Invalid Argument Types
    print("Test 4: Invalid Argument Types (mortgage_payment with string principal)")
    result = mcp.call_tool('calculate_mortgage_payment',
                          principal='not_a_number',
                          annual_rate=7.5,
                          years=30)
    print(f"Success: {result['success']}")
    print(f"Error: {result.get('error')}")
    print()


def main():
    """Run all test suites"""
    print("\n")
    print("=" * 80)
    print("  MCP TOOLS COMPREHENSIVE TEST SUITE".center(80))
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
    print("=" * 80)
    
    try:
        test_market_data_tools()
        test_mortgage_rates_tools()
        test_economic_data_tools()
        test_error_handling()
        
        print("\n")
        print("=" * 80)
        print("  ALL TESTS COMPLETED".center(80))
        print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
        print("=" * 80)
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
