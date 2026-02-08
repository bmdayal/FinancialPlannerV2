"""
Mortgage Rates & Interest Rates MCP Server
Provides current mortgage rates, loan calculations, and federal rate data
External API: Federal Reserve API + Mortgage Rates APIs
"""
import os
import json
import requests
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import logging

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [MCP:MortgageRates] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MortgageRatesMCP:
    """Mortgage Rates and Interest Rates MCP Server"""
    
    def __init__(self, fred_api_key: Optional[str] = None, mortgage_api_key: Optional[str] = None):
        """
        Initialize Mortgage Rates MCP
        
        Args:
            fred_api_key: Federal Reserve Economic Data API key
            mortgage_api_key: Mortgage rates API key (if using external service)
        """
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY', '')
        self.mortgage_api_key = mortgage_api_key or os.getenv('MORTGAGE_API_KEY', '')
        self.fred_base_url = 'https://api.stlouisfed.org/fred'
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour for interest rates
        
        logger.info("MortgageRatesMCP initialized")
        if not self.fred_api_key:
            logger.warning("No FRED API key found - interest rate functions may fail")
        
    def get_current_mortgage_rates(self) -> Dict[str, Any]:
        """
        Get current mortgage rates for different terms
        
        Returns:
            Dictionary with 15-year and 30-year mortgage rates
        """
        logger.info("Getting current mortgage rates from FRED API")
        try:
            rates = {
                '15_year': self._get_fred_rate('MORTGAGE15US'),
                '30_year': self._get_fred_rate('MORTGAGE30US'),
                'jumbo': self._get_fred_rate('MMNRNJ'),  # Jumbo mortgage rate
                'fha': self._get_fred_rate('MMNRNRNJ')   # FHA mortgage rate
            }
            
            # Filter out None values
            rates = {k: v for k, v in rates.items() if v is not None}
            
            logger.info(f"✓ Mortgage rates fetched: {rates}")
            return {
                'rates': rates,
                'timestamp': datetime.now().isoformat(),
                'source': 'Federal Reserve (FRED)'
            }
        except Exception as e:
            logger.error(f"Error fetching mortgage rates: {str(e)}", exc_info=True)
            return {"error": str(e)}
    
    def _get_fred_rate(self, series_id: str) -> Optional[float]:
        """
        Get the latest rate from FRED API
        
        Args:
            series_id: FRED series identifier
            
        Returns:
            Latest rate value or None
        """
        try:
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'sort_order': 'desc',
                'limit': 1
            }
            logger.debug(f"Fetching FRED series: {series_id}")
            response = requests.get(
                f'{self.fred_base_url}/series/observations',
                params=params,
                timeout=10
            )
            logger.debug(f"FRED API response status: {response.status_code}")
            data = response.json()
            
            if data.get('observations') and len(data['observations']) > 0:
                rate_value = float(data['observations'][0]['value'])
                logger.debug(f"✓ {series_id} = {rate_value}%")
                return rate_value
            logger.warning(f"No observations returned for {series_id}")
            return None
        except Exception as e:
            logger.warning(f"Could not fetch {series_id}: {str(e)}")
            return None
    
    def calculate_mortgage_payment(self, principal: float, annual_rate: float, 
                                   years: int) -> Dict[str, Any]:
        """
        Calculate monthly mortgage payment
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate (as percentage, e.g., 7.5)
            years: Loan term in years
            
        Returns:
            Monthly payment and amortization details
        """
        try:
            monthly_rate = annual_rate / 100 / 12
            num_payments = years * 12
            
            if monthly_rate == 0:
                monthly_payment = principal / num_payments
            else:
                monthly_payment = principal * (
                    monthly_rate * (1 + monthly_rate) ** num_payments
                ) / ((1 + monthly_rate) ** num_payments - 1)
            
            total_paid = monthly_payment * num_payments
            total_interest = total_paid - principal
            
            # Generate first few months of amortization schedule
            amortization = []
            remaining_balance = principal
            
            for month in range(1, min(13, num_payments + 1)):
                interest_payment = remaining_balance * monthly_rate
                principal_payment = monthly_payment - interest_payment
                remaining_balance -= principal_payment
                
                amortization.append({
                    'month': month,
                    'payment': round(monthly_payment, 2),
                    'principal': round(principal_payment, 2),
                    'interest': round(interest_payment, 2),
                    'balance': round(max(0, remaining_balance), 2)
                })
            
            return {
                'loan_amount': principal,
                'annual_rate': annual_rate,
                'loan_term_years': years,
                'monthly_payment': round(monthly_payment, 2),
                'total_paid': round(total_paid, 2),
                'total_interest': round(total_interest, 2),
                'interest_to_principal_ratio': round(total_interest / principal, 2),
                'amortization_schedule_sample': amortization
            }
        except Exception as e:
            logger.error(f"Error calculating mortgage payment: {str(e)}")
            return {"error": str(e)}
    
    def get_federal_funds_rate(self) -> Dict[str, Any]:
        """
        Get current Federal Funds Rate
        
        Returns:
            Federal funds effective rate
        """
        try:
            rate = self._get_fred_rate('FEDFUNDS')
            
            return {
                'federal_funds_rate': rate,
                'description': 'Federal Funds Effective Rate (%)',
                'timestamp': datetime.now().isoformat(),
                'source': 'Federal Reserve (FRED)'
            }
        except Exception as e:
            logger.error(f"Error fetching Federal Funds Rate: {str(e)}")
            return {"error": str(e)}
    
    def get_prime_rate(self) -> Dict[str, Any]:
        """
        Get current Prime Rate
        
        Returns:
            Prime lending rate
        """
        try:
            rate = self._get_fred_rate('DPRIME')
            
            return {
                'prime_rate': rate,
                'description': 'Bank Prime Loan Rate (%)',
                'timestamp': datetime.now().isoformat(),
                'source': 'Federal Reserve (FRED)'
            }
        except Exception as e:
            logger.error(f"Error fetching Prime Rate: {str(e)}")
            return {"error": str(e)}
    
    def project_rate_scenarios(self, current_rate: float, 
                              scenarios: str = 'standard') -> Dict[str, Any]:
        """
        Generate rate scenario projections
        
        Args:
            current_rate: Current mortgage rate
            scenarios: 'conservative', 'standard', or 'aggressive'
            
        Returns:
            Projected rates for next 12-24 months
        """
        try:
            adjustments = {
                'conservative': [0, 0.25, 0.5, 0.5, 0.75],
                'standard': [0, 0.5, 0.75, 1.0, 1.25],
                'aggressive': [0, 0.75, 1.25, 1.5, 2.0]
            }
            
            scenario_adjustments = adjustments.get(scenarios, adjustments['standard'])
            
            projections = []
            for i, adjustment in enumerate(scenario_adjustments):
                month = i * 3
                projected_rate = current_rate + adjustment
                projections.append({
                    'month': month,
                    'projected_rate': round(projected_rate, 2),
                    'rate_change': round(adjustment, 2)
                })
            
            return {
                'scenario': scenarios,
                'base_rate': current_rate,
                'projections': projections,
                'disclaimer': 'These are hypothetical scenarios for planning purposes only'
            }
        except Exception as e:
            logger.error(f"Error projecting rate scenarios: {str(e)}")
            return {"error": str(e)}
    
    def compare_mortgage_options(self, home_price: float, down_payment_percent: float,
                                rates_to_compare: Optional[list] = None) -> Dict[str, Any]:
        """
        Compare mortgage payment across different rates and terms
        
        Args:
            home_price: Home purchase price
            down_payment_percent: Down payment percentage
            rates_to_compare: List of rates to compare (if None, uses current rates)
            
        Returns:
            Comparison of payment amounts across scenarios
        """
        try:
            principal = home_price * (1 - down_payment_percent / 100)
            
            if rates_to_compare is None:
                current_rates = self.get_current_mortgage_rates()
                rates_to_compare = [
                    current_rates.get('rates', {}).get('30_year', 7.5),
                    current_rates.get('rates', {}).get('15_year', 7.0)
                ]
            
            comparisons = []
            for annual_rate in rates_to_compare:
                payment_30 = self.calculate_mortgage_payment(principal, annual_rate, 30)
                payment_15 = self.calculate_mortgage_payment(principal, annual_rate, 15)
                
                comparisons.append({
                    'rate': annual_rate,
                    'term_30_years': {
                        'monthly_payment': payment_30.get('monthly_payment'),
                        'total_interest': payment_30.get('total_interest')
                    },
                    'term_15_years': {
                        'monthly_payment': payment_15.get('monthly_payment'),
                        'total_interest': payment_15.get('total_interest')
                    }
                })
            
            return {
                'home_price': home_price,
                'down_payment_amount': home_price * down_payment_percent / 100,
                'loan_amount': principal,
                'comparisons': comparisons
            }
        except Exception as e:
            logger.error(f"Error comparing mortgage options: {str(e)}")
            return {"error": str(e)}


# For running as a standalone service
if __name__ == "__main__":
    mcp = MortgageRatesMCP()
    
    print("Current Mortgage Rates:")
    print(json.dumps(mcp.get_current_mortgage_rates(), indent=2))
    
    print("\nMortgage Payment Calculation (30-year at 7.5%):")
    print(json.dumps(mcp.calculate_mortgage_payment(300000, 7.5, 30), indent=2))
    
    print("\nFederal Funds Rate:")
    print(json.dumps(mcp.get_federal_funds_rate(), indent=2))
    
    print("\nRate Scenario Projections:")
    print(json.dumps(mcp.project_rate_scenarios(7.5, 'standard'), indent=2))
    
    print("\nMortgage Comparison:")
    print(json.dumps(mcp.compare_mortgage_options(500000, 20), indent=2))
