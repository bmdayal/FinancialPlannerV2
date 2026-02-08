#!/usr/bin/env python
"""
MCP Debugging Tool
Checks API keys, provider config, and MCP server status
"""
import sys
import os
import requests
from datetime import datetime
from pathlib import Path

# Load .env file from project root
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../mcp_servers'))

from mcp_client import MCPClientManager

# ...existing code...
