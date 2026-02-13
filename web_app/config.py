"""
Configuration module for Financial Planner Web Application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    OPENAI_TEMPERATURE = 0.7
    
    # Application
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    
    # Session
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # MCP Server Configuration
    # Market Data API (Alpha Vantage or IEX Cloud)
    MARKET_DATA_API_KEY = os.getenv('MARKET_DATA_API_KEY', '')
    MARKET_DATA_PROVIDER = os.getenv('MARKET_DATA_PROVIDER', 'yfinance')  # 'yfinance', 'alpha_vantage', or 'iex_cloud'
    
    # Federal Reserve Economic Data (FRED) API
    FRED_API_KEY = os.getenv('FRED_API_KEY', '')
    
    # Mortgage Rates API (optional, if using external service)
    MORTGAGE_API_KEY = os.getenv('MORTGAGE_API_KEY', '')
    
    # MCP Settings
    ENABLE_MCP_SERVERS = os.getenv('ENABLE_MCP_SERVERS', 'true').lower() == 'true'
    MCP_CACHE_ENABLED = os.getenv('MCP_CACHE_ENABLED', 'true').lower() == 'true'
    MCP_CACHE_TIMEOUT = int(os.getenv('MCP_CACHE_TIMEOUT', '300'))  # 5 minutes default

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    OPENAI_API_KEY = 'test-key'
    MARKET_DATA_API_KEY = 'test-key'
    FRED_API_KEY = 'test-key'

# Get config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
