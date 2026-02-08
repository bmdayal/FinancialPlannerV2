#!/usr/bin/env python
"""
MCP Tools Test Suite
Validates all MCP server functions independently without agent overhead
"""
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add mcp_servers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../mcp_servers'))

from mcp_client import MCPClientManager

def print_header(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_result(tool_name, result, status="✓"):
    print(f"{status} {tool_name}")
    print(f"  Result: {json.dumps(result, indent=2)[:200]}...")
    print()

def test_market_data_tools():
    print_header("MARKET DATA MCP TOOLS")
    mcp = MCPClientManager()
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

if __name__ == "__main__":
    test_market_data_tools()
    # Add other test functions here if needed
