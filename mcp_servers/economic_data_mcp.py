"""
Economic Data MCP Server
Provides inflation, unemployment, GDP data and economic projections
External API: Federal Reserve Economic Data (FRED) API
"""
import os
import json
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [MCP:EconomicData] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class EconomicDataMCP:
    """Economic Data MCP Server for inflation, employment, and growth metrics"""
    
    def __init__(self, fred_api_key: Optional[str] = None):
        """
        Initialize Economic Data MCP
        
        Args:
            fred_api_key: Federal Reserve Economic Data API key
        """
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY', '')
        self.fred_base_url = 'https://api.stlouisfed.org/fred'
        self.cache = {}
        self.cache_timeout = 86400  # 1 day for economic data
        
        logger.info("EconomicDataMCP initialized")
        if not self.fred_api_key:
            logger.warning("No FRED API key found - economic data functions may fail")
        
    def _get_fred_data(self, series_id: str, limit: int = 1) -> List[Dict[str, Any]]:
        """
        Get data from FRED API
        
        Args:
            series_id: FRED series identifier
            limit: Number of observations to retrieve
            
        Returns:
            List of observations with dates and values
        """
        try:
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'sort_order': 'desc',
                'limit': limit,
                'output_type': 'json' 
            }
            response = requests.get(
                f'{self.fred_base_url}/series/observations',
                params=params,
                timeout=10
            )
            data = response.json()
            return data.get('observations', [])
        except Exception as e:
            logger.warning(f"Could not fetch {series_id}: {str(e)}")
            return []
    
    def get_inflation_rate(self) -> Dict[str, Any]:
        """
        Get current inflation rate (CPI year-over-year)
        
        Returns:
            Dictionary with current inflation data
        """
        try:
            # CPIAUCSL = Consumer Price Index for All Urban Consumers
            observations = self._get_fred_data('CPIAUCSL', limit=13)
            
            if len(observations) >= 2:
                current = float(observations[0]['value'])
                previous_year = float(observations[12]['value'])
                
                yoy_inflation = ((current - previous_year) / previous_year) * 100
                
                result = {
                    'inflation_rate_yoy': round(yoy_inflation, 2),
                    'current_cpi': round(current, 2),
                    'cpi_month_ago': round(observations[1]['value'], 2) if len(observations) > 1 else None,
                    'cpi_year_ago': round(previous_year, 2),
                    'date': observations[0]['date'],
                    'unit': 'Percentage (%)',
                    'source': 'Federal Reserve (FRED)',
                    'description': 'Consumer Price Index year-over-year change'
                }
                logger.info(f"[TOOL CALL] get_inflation_rate() -> {yoy_inflation:.2f}%")
                return result
            
            return {"error": "Insufficient data"}
        except Exception as e:
            logger.error(f"Error fetching inflation rate: {str(e)}")
            return {"error": str(e)}
    
    def get_unemployment_rate(self) -> Dict[str, Any]:
        """
        Get current unemployment rate
        
        Returns:
            Dictionary with current unemployment statistics
        """
        try:
            # UNRATE = Civilian Unemployment Rate
            observations = self._get_fred_data('UNRATE', limit=2)
            
            if observations:
                current = float(observations[0]['value'])
                previous = float(observations[1]['value']) if len(observations) > 1 else current
                change = current - previous
                
                return {
                    'unemployment_rate': round(current, 2),
                    'previous_rate': round(previous, 2),
                    'rate_change': round(change, 2),
                    'date': observations[0]['date'],
                    'unit': 'Percentage (%)',
                    'source': 'Federal Reserve (FRED)',
                    'description': 'Civilian Unemployment Rate'
                }
            
            return {"error": "No data available"}
        except Exception as e:
            logger.error(f"Error fetching unemployment rate: {str(e)}")
            return {"error": str(e)}
    
    def get_gdp_growth(self) -> Dict[str, Any]:
        """
        Get current GDP growth rate
        
        Returns:
            Dictionary with GDP growth data
        """
        try:
            # A191RA1Q225SBEA = Real Gross Domestic Product
            observations = self._get_fred_data('A191RA1Q225SBEA', limit=2)
            
            if observations:
                return {
                    'gdp': float(observations[0]['value']),
                    'previous_gdp': float(observations[1]['value']) if len(observations) > 1 else None,
                    'date': observations[0]['date'],
                    'unit': 'Billions of Dollars (Real)',
                    'source': 'Federal Reserve (FRED)',
                    'description': 'Real Gross Domestic Product, Quarterly'
                }
            
            return {"error": "No data available"}
        except Exception as e:
            logger.error(f"Error fetching GDP growth: {str(e)}")
            return {"error": str(e)}
    
    def project_retirement_inflation(self, current_annual_expense: float, 
                                   years_to_retirement: int,
                                   inflation_rate: Optional[float] = None) -> Dict[str, Any]:
        """
        Project retirement expenses accounting for inflation
        
        Args:
            current_annual_expense: Current annual expenses
            years_to_retirement: Years until retirement
            inflation_rate: Expected annual inflation rate (if None, uses historical avg)
            
        Returns:
            Inflation-adjusted retirement expense projection
        """
        try:
            if inflation_rate is None:
                # Use historical average inflation of 3%
                inflation_data = self.get_inflation_rate()
                inflation_rate = inflation_data.get('inflation_rate_yoy', 3.0) / 100
            else:
                inflation_rate = inflation_rate / 100
            
            projections = []
            future_expense = current_annual_expense
            
            for year in range(years_to_retirement + 1):
                projections.append({
                    'year': year,
                    'annual_expense': round(future_expense, 2),
                    'increase_from_current': round(future_expense - current_annual_expense, 2)
                })
                future_expense *= (1 + inflation_rate)
            
            return {
                'current_annual_expense': current_annual_expense,
                'years_to_retirement': years_to_retirement,
                'inflation_rate_applied': round(inflation_rate * 100, 2),
                'projected_annual_expense_at_retirement': round(future_expense, 2),
                'total_increase': round(future_expense - current_annual_expense, 2),
                'percent_increase': round(((future_expense - current_annual_expense) / current_annual_expense) * 100, 2),
                'projections': projections
            }
        except Exception as e:
            logger.error(f"Error projecting retirement inflation: {str(e)}")
            return {"error": str(e)}
    
    def get_economic_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive economic dashboard with key indicators
        
        Returns:
            Dictionary with multiple economic indicators
        """
        try:
            return {
                'inflation': self.get_inflation_rate(),
                'unemployment': self.get_unemployment_rate(),
                'gdp': self.get_gdp_growth(),
                'federal_funds_rate': self._get_federal_funds_rate(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating economic dashboard: {str(e)}")
            return {"error": str(e)}
    
    def _get_federal_funds_rate(self) -> Dict[str, Any]:
        """
        Get current Federal Funds Rate
        
        Returns:
            Federal funds effective rate
        """
        try:
            observations = self._get_fred_data('FEDFUNDS', limit=1)
            
            if observations:
                return {
                    'federal_funds_rate': round(float(observations[0]['value']), 2),
                    'date': observations[0]['date'],
                    'unit': 'Percentage (%)'
                }
            return {}
        except Exception as e:
            logger.warning(f"Could not fetch Federal Funds Rate: {str(e)}")
            return {}
    
    def compare_inflation_scenarios(self, starting_expense: float,
                                   years: int) -> Dict[str, Any]:
        """
        Compare retirement expenses under different inflation scenarios
        
        Args:
            starting_expense: Current annual expense
            years: Number of years to project
            
        Returns:
            Comparison of low, moderate, and high inflation scenarios
        """
        try:
            scenarios = {
                'low': 2.0,      # 2% inflation
                'moderate': 3.0,  # 3% inflation
                'high': 5.0       # 5% inflation
            }
            
            results = {}
            for scenario_name, inflation_rate in scenarios.items():
                projection = self.project_retirement_inflation(
                    starting_expense, years, inflation_rate
                )
                results[scenario_name] = {
                    'inflation_rate': inflation_rate,
                    'final_expense': projection.get('projected_annual_expense_at_retirement'),
                    'total_increase_percent': projection.get('percent_increase')
                }
            
            return {
                'starting_expense': starting_expense,
                'projection_years': years,
                'scenarios': results
            }
        except Exception as e:
            logger.error(f"Error comparing inflation scenarios: {str(e)}")
            return {"error": str(e)}


# For running as a standalone service
if __name__ == "__main__":
    mcp = EconomicDataMCP()
    
    print("Inflation Rate:")
    print(json.dumps(mcp.get_inflation_rate(), indent=2))
    
    print("\nUnemployment Rate:")
    print(json.dumps(mcp.get_unemployment_rate(), indent=2))
    
    print("\nGDP Growth:")
    print(json.dumps(mcp.get_gdp_growth(), indent=2))
    
    print("\nRetirement Inflation Projection (30 years, $80,000/year):")
    print(json.dumps(mcp.project_retirement_inflation(80000, 30), indent=2))
    
    print("\nInflation Scenarios Comparison:")
    print(json.dumps(mcp.compare_inflation_scenarios(80000, 30), indent=2))
    
    print("\nEconomic Dashboard:")
    print(json.dumps(mcp.get_economic_dashboard(), indent=2))
