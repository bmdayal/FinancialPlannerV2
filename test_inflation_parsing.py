"""
Quick test to verify MCP inflation data is retrieved and parsed correctly
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_root, '.env'))

# Add mcp_servers to path
sys.path.insert(0, os.path.join(project_root, 'mcp_servers'))

from economic_data_mcp import EconomicDataMCP
import json

def test_inflation_retrieval():
    """Test that inflation data can be retrieved and parsed"""
    print("\n" + "="*80)
    print("Testing MCP Inflation Data Retrieval and Parsing")
    print("="*80)
    
    # Initialize MCP
    print("\n1. Initializing Economic Data MCP...")
    mcp = EconomicDataMCP()
    
    # Get inflation data
    print("\n2. Retrieving inflation rate...")
    result = mcp.get_inflation_rate()
    print(f"   Raw result: {result}")
    
    # Parse the result
    print("\n3. Parsing inflation data...")
    try:
        if isinstance(result, dict):
            inflation_data = result
        else:
            inflation_data = json.loads(result)
        
        inflation_rate = inflation_data.get('rate', None)
        
        if inflation_rate is not None:
            print(f"   ✓ Successfully parsed inflation rate: {inflation_rate}%")
            
            # Convert to decimal for calculation
            inflation_decimal = inflation_rate / 100
            print(f"   ✓ As decimal for calculations: {inflation_decimal}")
            
            # Test calculation
            print("\n4. Testing inflation-adjusted calculation...")
            current_income = 100000
            years = 30
            future_income = current_income * ((1 + inflation_decimal) ** years)
            print(f"   Current income: ${current_income:,.2f}")
            print(f"   Inflation rate: {inflation_rate}%")
            print(f"   Years: {years}")
            print(f"   Future income (inflation-adjusted): ${future_income:,.2f}")
            print(f"   ✓ Calculation successful!")
            
            return True
        else:
            print(f"   ✗ Could not find 'rate' in result: {inflation_data}")
            return False
            
    except Exception as e:
        print(f"   ✗ Parsing failed: {e}")
        print(f"   Result type: {type(result)}")
        return False

if __name__ == "__main__":
    success = test_inflation_retrieval()
    
    print("\n" + "="*80)
    if success:
        print("✓ MCP INFLATION DATA READY FOR USE IN AGENTS")
    else:
        print("✗ ISSUE WITH MCP INFLATION DATA - CHECK LOGS ABOVE")
    print("="*80 + "\n")
    
    sys.exit(0 if success else 1)
