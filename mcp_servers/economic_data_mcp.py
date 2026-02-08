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
    
    def __init__(self, fred_api_key: str = None):
        """
        Initialize Economic Data MCP with FRED API
        
        Args:
            fred_api_key: Federal Reserve Economic Data API key
        """
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY')
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.cache = {}
        self.cache_timeout = 86400  # 1 day for economic data
        logger.info(f"EconomicDataMCP initialized with FRED API key: {'***' + self.fred_api_key[-4:] if self.fred_api_key else 'None'}")
    
    def _get_fred_data(self, series_id: str, limit: int = 1) -> Optional[Dict[str, Any]]:
        """
        Fetch data from FRED API
        
        Args:
            series_id: FRED series identifier
            limit: Number of recent observations to fetch
            
        Returns:
            Dict with observation data or None on error
        """
        if not self.fred_api_key:
            logger.error("FRED API key not configured")
            return None
            
        try:
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': limit
            }
            
            logger.debug(f"Fetching FRED series: {series_id}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'observations' in data and len(data['observations']) > 0:
                logger.debug(f"✓ FRED data retrieved for {series_id}")
                return data
            else:
                logger.warning(f"No observations found for series {series_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"FRED API request failed for {series_id}: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse FRED response for {series_id}: {str(e)}")
            return None
    
    def get_inflation_rate(self) -> Dict[str, Any]:
        """
        Get current inflation rate (CPI year-over-year) from FRED
        Series: CPIAUCSL (Consumer Price Index for All Urban Consumers)
        """
        try:
            # Get last 13 months to calculate year-over-year change
            data = self._get_fred_data('CPIAUCSL', limit=13)
            
            if data and 'observations' in data:
                observations = data['observations']
                if len(observations) >= 2:
                    current = float(observations[0]['value'])
                    year_ago = float(observations[-1]['value'])
                    inflation_rate = ((current - year_ago) / year_ago) * 100
                    
                    result = {
                        'rate': round(inflation_rate, 2),
                        'inflation_rate_yoy': round(inflation_rate, 2),
                        'current_cpi': round(current, 2),
                        'cpi_year_ago': round(year_ago, 2),
                        'date': observations[0]['date'],
                        'unit': 'Percentage (%)',
                        'source': 'Federal Reserve (FRED)',
                        'success': True,
                        'description': 'Consumer Price Index year-over-year change'
                    }
                    logger.info(f"[TOOL CALL] get_inflation_rate() -> {inflation_rate:.2f}% (FRED)")
                    return result
            
            # Fallback if FRED data unavailable
            logger.warning("FRED data unavailable, using fallback inflation estimate")
            return {
                'rate': 3.2,
                'inflation_rate_yoy': 3.2,
                'date': str(datetime.now().date()),
                'unit': 'Percentage (%)',
                'source': 'Fallback estimate',
                'success': True,
                'description': 'Inflation estimate (FRED unavailable)',
                'note': 'Using 3.2% fallback - FRED API may be down'
            }
            
        except Exception as e:
            logger.error(f"Error in get_inflation_rate: {str(e)}")
            return {"error": str(e), "success": False}
    
    def get_unemployment_rate(self) -> Dict[str, Any]:
        """
        Get current unemployment rate from FRED
        Series: UNRATE (Unemployment Rate)
        """
        try:
            data = self._get_fred_data('UNRATE', limit=2)
            
            if data and 'observations' in data:
                observations = data['observations']
                if len(observations) >= 1:
                    current = float(observations[0]['value'])
                    previous = float(observations[1]['value']) if len(observations) > 1 else current
                    change = current - previous
                    
                    result = {
                        'rate': round(current, 2),
                        'unemployment_rate': round(current, 2),
                        'previous_rate': round(previous, 2),
                        'rate_change': round(change, 2),
                        'date': observations[0]['date'],
                        'unit': 'Percentage (%)',
                        'source': 'Federal Reserve (FRED)',
                        'success': True,
                        'description': 'Civilian Unemployment Rate'
                    }
                    logger.info(f"[TOOL CALL] get_unemployment_rate() -> {current:.2f}% (FRED)")
                    return result
            
            return {"error": "No unemployment data available", "success": False}
            
        except Exception as e:
            logger.error(f"Error fetching unemployment rate: {str(e)}")
            return {"error": str(e), "success": False}
    
    def get_gdp_growth(self) -> Dict[str, Any]:
        """
        Get current GDP growth rate from FRED
        Series: GDP (Gross Domestic Product)
        """
        try:
            data = self._get_fred_data('GDP', limit=5)  # Get last 5 quarters
            
            if data and 'observations' in data:
                observations = data['observations']
                if len(observations) >= 2:
                    current = float(observations[0]['value'])
                    previous = float(observations[-1]['value'])
                    growth = ((current - previous) / previous) * 100
                    
                    result = {
                        'rate': round(growth, 2),
                        'gdp': round(current, 2),
                        'previous_gdp': round(previous, 2),
                        'gdp_growth_percent': round(growth, 2),
                        'date': observations[0]['date'],
                        'unit': 'Percentage (%)',
                        'source': 'Federal Reserve (FRED)',
                        'success': True,
                        'description': 'Real Gross Domestic Product year-over-year change'
                    }
                    logger.info(f"[TOOL CALL] get_gdp_growth() -> {growth:.2f}% (FRED)")
                    return result
            
            return {"error": "No GDP data available", "success": False}
            
        except Exception as e:
            logger.error(f"Error fetching GDP growth: {str(e)}")
            return {"error": str(e), "success": False}
    
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
