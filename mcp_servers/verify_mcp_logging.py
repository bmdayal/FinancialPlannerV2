"""
MCP Debug Logging Verification Script
Quick test to verify debug logging is working
Run from: c:\source\FinancialPlannerV2\mcp_servers
python verify_mcp_logging.py
"""

import sys
import os

# Load environment
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'web_app', '.env'))

print("\n" + "=" * 80)
print("MCP DEBUG LOGGING VERIFICATION")
print("=" * 80 + "\n")

print("📋 Checking Debug Logging in MCP Servers...\n")

# Test 1: Check imports and logging
print("Test 1: Checking imports and logging configuration...")
try:
    import logging
    from mcp_client import get_mcp_client
    
    print("✓ Logging module imported")
    print("✓ MCP Client imported")
    print("✓ Initializing MCP Client...\n")
    
    client = get_mcp_client()
    print("\n✓ MCP Client successfully initialized!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 2: Verify tools are available
print("\nTest 2: Checking available MCP tools...")
try:
    tools = client.get_tools_summary()
    total_tools = sum(len(t) for t in tools.values())
    
    print(f"✓ Tools Summary:")
    for category, tool_list in tools.items():
        print(f"  - {category}: {len(tool_list)} tools")
    print(f"\n✓ Total tools available: {total_tools}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 3: Test a tool call with logging
print("\nTest 3: Testing tool call (should show logging)...")
print("-" * 80)
try:
    print("\nCalling: get_inflation_rate()")
    result = client.call_tool('get_inflation_rate')
    
    if result['success']:
        print("\n✓ Tool call successful!")
        data = result.get('result', {})
        if 'inflation_rate_yoy' in data:
            print(f"✓ Real inflation data received: {data['inflation_rate_yoy']}%")
        else:
            print("⚠️ No inflation data in response (API may not have data)")
    else:
        print(f"✗ Tool call failed: {result.get('error')}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 4: Check for logging in console
print("\n" + "-" * 80)
print("\nTest 4: Debug Logging Check")
print("-" * 80)
print("""
✓ If you saw logs above with these features, logging is working:

  1. [MCP:Client] - INFO - INITIALIZING MCP CLIENT MANAGER
  2. ✓ Market Data MCP initialized
  3. ✓ Mortgage Rates MCP initialized
  4. ✓ Economic Data MCP initialized
  5. ✓ Tools registry built
  6. [TOOL CALL] Calling 'get_inflation_rate'
  7. Fetching FRED data...
  8. ✓ Successfully completed
  
Look for these indicators:
  - ✓ checkmarks = Success
  - ⚠️ = Warnings
  - 🔴 = Errors
  - [MCP:ModuleName] = Module identifier
  - Timestamps on each log
""")

# Summary
print("\n" + "=" * 80)
print("✅ VERIFICATION COMPLETE")
print("=" * 80)
print("""
If you saw:
  ✓ All initialization messages
  ✓ Tool call logs
  ✓ API response logs
  ✓ Success indicators

Then debug logging is working correctly! 🎉

Next Steps:
  1. Run: python app.py (from web_app directory)
  2. Watch console for MCP logs
  3. Create a financial plan
  4. See [TOOL CALL] logs in real-time
  5. Check for ✓ success indicators

For detailed logging information, see:
  - MCP_DEBUG_QUICK_REF.txt
  - MCP_DEBUG_GUIDE.md
  - MCP_DEBUG_IMPLEMENTATION_COMPLETE.md
""")
print("=" * 80 + "\n")
