"""
Financial Planning Agents Module
Extracted from PlanSummary-AgenticAI.ipynb
"""
import json
import logging
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import operator
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Add mcp_servers to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers'))

# Import MCP Client
try:
    from mcp_client import get_mcp_client
    mcp_client = get_mcp_client()
    logger.info("✓ MCP Client successfully initialized in agents module")
except ImportError as e:
    logger.warning(f"Failed to import MCP Client: {e}")
    mcp_client = None
except Exception as e:
    logger.error(f"Error initializing MCP Client: {e}", exc_info=True)
    mcp_client = None


# ============================================================================
# MCP-BASED TOOLS (Real-time Market & Economic Data)
# ============================================================================

@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price and market data for investment analysis."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_stock_price', symbol=symbol)
    return json.dumps(result.get('result', result))

@tool
def get_portfolio_performance(holdings: List[Dict[str, float]]) -> str:
    """Calculate portfolio performance based on current market prices."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_portfolio_performance', holdings=holdings)
    return json.dumps(result.get('result', result))

@tool
def get_market_indices() -> str:
    """Get major market indices (S&P 500, Nasdaq, Dow Jones) data for portfolio context."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_market_indices')
    return json.dumps(result.get('result', result))

@tool
def get_current_mortgage_rates() -> str:
    """Get current mortgage rates for 15-year, 30-year, jumbo, and FHA loans."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_current_mortgage_rates')
    return json.dumps(result.get('result', result))

@tool
def calculate_mortgage_payment(principal: float, annual_rate: float, years: int) -> str:
    """Calculate monthly mortgage payment with amortization schedule."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('calculate_mortgage_payment', principal=principal, annual_rate=annual_rate, years=years)
    return json.dumps(result.get('result', result))

@tool
def get_inflation_rate() -> str:
    """Get current inflation rate based on Consumer Price Index for expense projections."""
    if mcp_client is None:
        logger.error("MCP client not available for get_inflation_rate")
        return "MCP client not available"
    result = mcp_client.call_tool('get_inflation_rate')
    return json.dumps(result.get('result', result))

@tool
def project_retirement_inflation(current_annual_expense: float, years_to_retirement: int) -> str:
    """Project retirement expenses accounting for current inflation rates."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('project_retirement_inflation', current_annual_expense=current_annual_expense, years_to_retirement=years_to_retirement)
    return json.dumps(result.get('result', result))

@tool
def get_federal_funds_rate() -> str:
    """Get current Federal Reserve Funds Rate for interest rate analysis."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_federal_funds_rate')
    return json.dumps(result.get('result', result))

@tool
def get_economic_dashboard() -> str:
    """Get comprehensive dashboard of key economic indicators for planning context."""
    if mcp_client is None:
        logger.error("MCP client not available")
        return "MCP client not available"
    result = mcp_client.call_tool('get_economic_dashboard')
    return json.dumps(result.get('result', result))


# ============================================================================
# TRADITIONAL FINANCIAL PLANNING TOOLS
# ============================================================================

@tool
def calculate_retirement_needs(current_age: int, retirement_age: int,
                               annual_expenses: float, life_expectancy: int = 85) -> str:
    """Calculate estimated retirement fund needed based on age and expenses."""
    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    # Simple calculation with 3% inflation
    inflation_rate = 0.03
    future_annual_expenses = annual_expenses * ((1 + inflation_rate) ** years_to_retirement)
    total_needed = future_annual_expenses * years_in_retirement

    # Guard against division by zero
    monthly_savings = 0 if years_to_retirement <= 0 else total_needed / (years_to_retirement * 12)

    return f"""Retirement Calculation:
- Years until retirement: {years_to_retirement}
- Years in retirement: {years_in_retirement}
- Future annual expenses (adjusted for inflation): ${future_annual_expenses:,.2f}
- Total retirement fund needed: ${total_needed:,.2f}
- Recommended monthly savings: ${monthly_savings:,.2f}"""

@tool
def calculate_life_insurance(annual_income: float, num_dependents: int,
                            outstanding_debts: float, savings: float) -> str:
    """Calculate recommended life insurance coverage."""
    # Rule of thumb: 10x annual income + debts - savings
    base_coverage = (annual_income * 10) + outstanding_debts - savings
    dependent_factor = 1 + (num_dependents * 0.2)
    recommended_coverage = base_coverage * dependent_factor

    return f"""Life Insurance Recommendation:
- Base coverage needed: ${base_coverage:,.2f}
- Adjustment for {num_dependents} dependent(s): {dependent_factor}x
- Recommended coverage: ${recommended_coverage:,.2f}
- Estimated monthly premium (term life): ${(recommended_coverage * 0.0005 / 12):,.2f}"""

@tool
def calculate_education_fund(num_children: int, children_ages: List[int],
                             cost_per_year: float = 30000) -> str:
    """Calculate education fund needed for children."""
    total_needed = 0
    details = []

    for i, age in enumerate(children_ages):
        years_until_college = max(0, 18 - age)
        years_in_college = 4

        # Inflation adjusted cost
        inflation_rate = 0.05
        future_cost = cost_per_year * ((1 + inflation_rate) ** years_until_college)
        child_total = future_cost * years_in_college
        total_needed += child_total

        details.append(f"Child {i+1} (age {age}): ${child_total:,.2f} needed in {years_until_college} years")

    # Guard against division by zero
    months_until_college = max([18 - age for age in children_ages if age < 18] + [1]) * 12
    monthly_savings = 0 if months_until_college <= 0 else total_needed / months_until_college

    return f"""Education Fund Calculation:
{chr(10).join(details)}
- Total education fund needed: ${total_needed:,.2f}
- Recommended monthly savings: ${monthly_savings:,.2f}"""

@tool
def calculate_estate_tax(total_assets: float, state: str = "Federal") -> str:
    """Estimate potential estate taxes."""
    federal_exemption = 13610000  # 2024 exemption
    taxable_estate = max(0, total_assets - federal_exemption)
    estimated_tax = taxable_estate * 0.40  # Top federal rate

    return f"""Estate Tax Estimation:
- Total assets: ${total_assets:,.2f}
- Federal exemption: ${federal_exemption:,.2f}
- Taxable estate: ${taxable_estate:,.2f}
- Estimated federal estate tax: ${estimated_tax:,.2f}
- Recommendation: {'Estate planning strategies recommended' if taxable_estate > 0 else 'Below exemption threshold'}"""

@tool
def calculate_wealth_allocation(total_assets: float, age: int, risk_tolerance: str = "moderate") -> str:
    """Recommend asset allocation based on age and risk tolerance."""
    # Age-based stock allocation
    base_stock_pct = 100 - age

    # Adjust for risk tolerance
    if risk_tolerance.lower() == "aggressive":
        stock_pct = min(90, base_stock_pct + 10)
    elif risk_tolerance.lower() == "conservative":
        stock_pct = max(20, base_stock_pct - 20)
    else:
        stock_pct = base_stock_pct

    bond_pct = 100 - stock_pct

    stock_amount = total_assets * (stock_pct / 100)
    bond_amount = total_assets * (bond_pct / 100)

    return f"""Asset Allocation Recommendation:
- Risk Profile: {risk_tolerance.title()}
- Stocks/Equity: {stock_pct}% (${stock_amount:,.2f})
- Bonds/Fixed Income: {bond_pct}% (${bond_amount:,.2f})
- Rebalance: Quarterly or when allocation drifts 5%+"""

@tool
def calculate_529_plan(num_children: int, children_ages: List[int], 
                      annual_contribution: float = 0, state: str = "National") -> str:
    """Calculate 529 education savings plan projections and benefits."""
    total_needed = 0
    total_savings = 0
    details = []
    
    for i, age in enumerate(children_ages):
        years_until_college = max(0, 18 - age)
        
        # Future college cost (assuming 5% annual increase)
        current_cost = 35000  # Average annual college cost
        future_cost = current_cost * ((1.05) ** years_until_college)
        four_year_total = future_cost * 4
        total_needed += four_year_total
        
        # 529 savings projection (assuming 6% annual return)
        if years_until_college > 0:
            monthly_contribution = annual_contribution / 12 / num_children
            future_value = monthly_contribution * (((1 + 0.06/12) ** (years_until_college * 12) - 1) / (0.06/12))
            total_savings += future_value
            
            details.append(f"Child {i+1} (age {age}): ${four_year_total:,.0f} needed, ${future_value:,.0f} projected savings")
        else:
            details.append(f"Child {i+1} (age {age}): Currently in college - ${four_year_total:,.0f} needed")
    
    shortfall = max(0, total_needed - total_savings)
    
    return f"""529 Education Savings Analysis:
{chr(10).join(details)}
- Total education costs projected: ${total_needed:,.0f}
- Projected 529 savings: ${total_savings:,.0f}
- Funding gap: ${shortfall:,.0f}
- Tax benefits: State deduction varies by state
- Recommended: {'Increase contributions' if shortfall > 0 else 'On track for funding'}"""

@tool
def calculate_tax_optimization(annual_income: float, filing_status: str = "married", 
                              retirement_contributions: float = 0, charitable_giving: float = 0) -> str:
    """Calculate tax optimization strategies and potential savings."""
    # 2024 tax brackets (simplified)
    if filing_status.lower() == "married":
        standard_deduction = 29200
        brackets = [(22275, 0.10), (89450, 0.12), (190750, 0.22), (364200, 0.24), (462500, 0.32), (693750, 0.35)]
    else:
        standard_deduction = 14600
        brackets = [(11000, 0.10), (44725, 0.12), (95375, 0.22), (182050, 0.24), (231250, 0.32), (578125, 0.35)]
    
    # Calculate current tax
    taxable_income = max(0, annual_income - standard_deduction - retirement_contributions)
    current_tax = 0
    remaining_income = taxable_income
    
    for bracket_max, rate in brackets:
        if remaining_income > 0:
            taxable_at_bracket = min(remaining_income, bracket_max)
            current_tax += taxable_at_bracket * rate
            remaining_income -= taxable_at_bracket
    
    # Tax optimization strategies
    max_401k = 23000  # 2024 limit
    max_ira = 7000    # 2024 limit
    additional_retirement = max_401k - retirement_contributions
    
    # Calculate tax savings from additional contributions
    marginal_rate = 0.22  # Approximate marginal rate for middle income
    retirement_tax_savings = min(additional_retirement, annual_income * 0.15) * marginal_rate
    charitable_tax_savings = charitable_giving * marginal_rate if charitable_giving > standard_deduction else 0
    
    return f"""Tax Optimization Analysis:
- Current taxable income: ${taxable_income:,.0f}
- Estimated current tax: ${current_tax:,.0f}
- Marginal tax rate: {marginal_rate:.0%}

Optimization Opportunities:
- Additional 401(k) contributions: ${additional_retirement:,.0f} (saves ${retirement_tax_savings:,.0f})
- IRA contribution potential: ${max_ira:,.0f} (saves ${max_ira * marginal_rate:,.0f})
- Charitable giving tax benefit: ${charitable_tax_savings:,.0f}
- HSA max contribution: $4,300 (saves ${4300 * marginal_rate:,.0f})

Recommended: Maximize pre-tax retirement contributions and consider tax-loss harvesting"""

@tool
def analyze_scholarship_opportunities(student_age: int, gpa: float = 0.0, 
                                    family_income: float = 0, activities: str = "") -> str:
    """Analyze scholarship opportunities and financial aid eligibility."""
    opportunities = []
    
    # Merit-based scholarships
    if gpa >= 3.8:
        opportunities.append("High academic achievement scholarships (up to $20,000/year)")
    elif gpa >= 3.5:
        opportunities.append("Academic merit scholarships (up to $10,000/year)")
    elif gpa >= 3.0:
        opportunities.append("Merit-based awards (up to $5,000/year)")
    
    # Need-based aid
    if family_income < 60000:
        opportunities.append("Maximum Pell Grant eligibility (~$7,400/year)")
        opportunities.append("State need-based grants")
    elif family_income < 100000:
        opportunities.append("Partial need-based aid eligibility")
    
    # Activity-based
    if "sports" in activities.lower():
        opportunities.append("Athletic scholarships (varies by sport and division)")
    if "music" in activities.lower() or "art" in activities.lower():
        opportunities.append("Arts and performance scholarships")
    if "volunteer" in activities.lower() or "community" in activities.lower():
        opportunities.append("Community service scholarships")
    
    # Other opportunities
    opportunities.extend([
        "Local community foundation scholarships",
        "Professional association scholarships",
        "Employer tuition assistance programs"
    ])
    
    return f"""Scholarship and Financial Aid Analysis:
Student Profile: Age {student_age}, GPA {gpa:.1f}, Family Income ${family_income:,.0f}

Eligible Opportunities:
{chr(10).join([f'- {opp}' for opp in opportunities])}

Next Steps:
- Complete FAFSA for need-based aid
- Research school-specific scholarships
- Apply to external scholarship databases
- Consider community college transfer option
- Explore work-study programs"""


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(TypedDict):
    """State for agent graph"""
    messages: Annotated[Sequence[HumanMessage | AIMessage | SystemMessage], operator.add]
    user_info: Dict[str, Any]
    selected_plans: List[str]
    plan_summaries: Dict[str, str]
    mcp_data: Dict[str, Any]  # Track MCP tool calls and results for display
    next_agent: str


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

class RetirementAgent:
    """Retirement Planning Specialist Agent
    
    Designs and monitors retirement portfolios, projecting future needs and adapting strategies 
    for a secure and comfortable post-work future. It considers factors like Social Security 
    optimization, required minimum distributions, and sustainable withdrawal rates.
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_retirement_needs, calculate_wealth_allocation, 
                     project_retirement_inflation, get_inflation_rate, get_market_indices]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are a Retirement Planning Specialist who designs and monitors retirement portfolios, 
projecting future needs and adapting strategies for a secure and comfortable post-work future. 
You consider factors like Social Security optimization, required minimum distributions, and sustainable withdrawal rates.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Retirement Age: {user_info.get('retirement_age', 'Not provided')}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Current Savings: ${user_info.get('savings', 0):,.2f}
- Risk Tolerance: {user_info.get('risk_tolerance', 'moderate')}

IMPORTANT: You MUST use ALL available tools to provide comprehensive retirement planning with real market data:

1. Call get_inflation_rate - Get CURRENT inflation rate for accurate projections
2. Call get_market_indices - Get current S&P 500, Nasdaq, Dow Jones performance
3. Call project_retirement_inflation with current expense estimates and inflation data
4. Call calculate_retirement_needs with current age, retirement age, and estimated annual expenses
5. Call calculate_wealth_allocation with total assets, current age, and risk tolerance

After using ALL these tools, provide a detailed retirement plan summary including:
- Current market conditions and inflation context
- Retirement fund needed calculations based on inflation
- Social Security optimization strategies  
- Required minimum distribution planning
- Sustainable withdrawal rate recommendations
- Asset allocation aligned with current market conditions"""

        tools_to_use = self.tools
        llm_with_tools = self.llm.bind_tools(tools_to_use)

        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        # Execute tool calls if any
        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Retirement Planning")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                print(f"  → Executing: {tool_name}({list(tool_args.keys())})")

                # Find and execute the tool
                for tool in tools_to_use:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(result)
                        mcp_tools_used.append({"name": tool_name, "args": tool_args, "result": result})
                        print(f"  ✓ {tool_name} completed")

            # Create final summary with tool results
            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive retirement planning summary with specific recommendations."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            print(f"\n⚠ LLM did not invoke tools for Retirement Planning, calling directly")
            # Call ONLY MCP data sources - no calculation logic
            print(f"  → Fetching MCP data sources...")
            
            # Economic Data MCP
            inflation_result = get_inflation_rate.invoke({})
            mcp_tools_used.append({"name": "get_inflation_rate", "source": "Economic Data MCP", "args": {}, "result": inflation_result})
            print(f"  ✓ get_inflation_rate (Economic Data MCP) completed")
            
            # Market Data MCP
            market_result = get_market_indices.invoke({})
            mcp_tools_used.append({"name": "get_market_indices", "source": "Market Data MCP", "args": {}, "result": market_result})
            print(f"  ✓ get_market_indices (Market Data MCP) completed")
            
            # Create simple summary from MCP data only
            summary = "MCP Data Sources Retrieved: Market indices and inflation data fetched successfully for workshop demonstration."

        # Track MCP tools used for this plan
        if "Retirement Planning" not in state["mcp_data"]:
            state["mcp_data"]["Retirement Planning"] = {"tools": []}
        state["mcp_data"]["Retirement Planning"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Retirement Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Retirement Planning Complete"))

        return state


class InsuranceAgent:
    """Insurance Planning Specialist Agent"""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_life_insurance]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are an Insurance Planning Specialist. Analyze the user's situation and recommend appropriate insurance coverage.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Number of Dependents: {user_info.get('num_dependents', 0)}
- Current Savings: ${user_info.get('savings', 0):,.2f}
- Outstanding Debts: ${user_info.get('debts', 0):,.2f}

IMPORTANT: You MUST use the life insurance calculation tool to determine appropriate coverage amounts.

Call calculate_life_insurance with the client's income, dependents, and debts to calculate:
- Required life insurance coverage amount
- Recommended term length based on dependents

After using this tool, provide comprehensive insurance recommendations covering:
- Life insurance type and amount (term vs permanent)
- Health insurance coverage assessment
- Disability insurance needs
- Liability insurance requirements
- Overall insurance strategy aligned with financial plan"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Insurance Planning")
            for tool_call in response.tool_calls:
                tool_args = tool_call["args"]
                result = calculate_life_insurance.invoke(tool_args)
                tool_results.append(result)
                mcp_tools_used.append({"name": "calculate_life_insurance", "args": tool_args, "result": result})
                print(f"  ✓ calculate_life_insurance completed")

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive insurance planning summary covering life, health, disability, and liability insurance."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            print(f"\n⚠ LLM did not invoke tools for Insurance Planning, calling directly")
            # Call tool directly
            annual_income = user_info.get('annual_income', 0)
            num_dependents = user_info.get('num_dependents', 0)
            outstanding_debts = user_info.get('debts', 0)
            savings = user_info.get('savings', 0)
            
            insurance_args = {
                "annual_income": annual_income,
                "num_dependents": num_dependents,
                "outstanding_debts": outstanding_debts,
                "savings": savings
            }
            insurance_result = calculate_life_insurance.invoke(insurance_args)
            tool_results.append(insurance_result)
            mcp_tools_used.append({"name": "calculate_life_insurance", "args": insurance_args, "result": insurance_result})
            print(f"  ✓ calculate_life_insurance completed")
            
            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive insurance planning summary covering life, health, disability, and liability insurance."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content

        # Track MCP tools used for this plan
        if "Insurance Planning" not in state["mcp_data"]:
            state["mcp_data"]["Insurance Planning"] = {"tools": []}
        state["mcp_data"]["Insurance Planning"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Insurance Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Insurance Planning Complete"))

        return state


class EstateAgent:
    """Estate Planning Specialist Agent
    
    Assists in organizing assets, wills, and trusts to ensure seamless transfer of wealth and 
    fulfillment of client wishes. This includes legacy planning and ensuring beneficiaries are 
    properly set up.
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_estate_tax, calculate_education_fund]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are an Estate Planning Specialist who assists in organizing assets, wills, 
and trusts to ensure seamless transfer of wealth and fulfillment of client wishes. You focus on 
legacy planning and ensuring beneficiaries are properly set up.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Total Assets: ${user_info.get('total_assets', user_info.get('savings', 0)):,.2f}
- Number of Children: {user_info.get('num_children', 0)}
- Children Ages: {user_info.get('children_ages', [])}

IMPORTANT: You MUST use the available tools to provide accurate calculations:

1. Call calculate_estate_tax with the client's total assets to determine potential estate tax liability
2. If there are children, call calculate_education_fund to plan for education expenses

After calling these tools, provide comprehensive recommendations for:
- Wills and trust structures
- Beneficiary designations
- Legacy planning strategies
- Estate tax minimization
- Seamless wealth transfer mechanisms"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Estate Planning")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                for tool in self.tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(result)
                        mcp_tools_used.append({"name": tool_name, "args": tool_args, "result": result})
                        print(f"  ✓ {tool_name} completed")
        else:
            print(f"\n⚠ LLM did not invoke tools for Estate Planning, calling directly")
            # Call tools directly
            total_assets = user_info.get('total_assets', user_info.get('savings', 0))
            if total_assets > 0:
                estate_tax_args = {"total_assets": total_assets}
                estate_tax_result = calculate_estate_tax.invoke(estate_tax_args)
                tool_results.append(estate_tax_result)
                mcp_tools_used.append({"name": "calculate_estate_tax", "args": estate_tax_args, "result": estate_tax_result})
                print(f"  ✓ calculate_estate_tax completed")
            
            num_children = user_info.get('num_children', 0)
            children_ages = user_info.get('children_ages', [])
            if num_children > 0 and children_ages:
                education_args = {"num_children": num_children, "children_ages": children_ages}
                education_result = calculate_education_fund.invoke(education_args)
                tool_results.append(education_result)
                mcp_tools_used.append({"name": "calculate_education_fund", "args": education_args, "result": education_result})
                print(f"  ✓ calculate_education_fund completed")

        summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive estate planning summary including wills, trusts, beneficiary designations,
education funding, and tax minimization strategies."""

        final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
        summary = final_response.content

        # Track MCP tools used for this plan
        if "Estate Planning" not in state["mcp_data"]:
            state["mcp_data"]["Estate Planning"] = {"tools": []}
        state["mcp_data"]["Estate Planning"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Estate Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Estate Planning Complete"))

        return state


class WealthAgent:
    """Personal Wealth Management Specialist Agent
    
    Manages investments, tracks financial goals, and provides personalized advice for growing wealth. 
    It adapts to market changes in real-time, adjusting strategies based on current conditions and 
    the client's risk tolerance.
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_wealth_allocation, get_market_indices, get_portfolio_performance, get_stock_price]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are a Personal Wealth Management Specialist who manages investments, tracks 
financial goals, and provides personalized advice for growing wealth. You adapt to market changes 
in real-time, adjusting strategies based on current conditions and the client's risk tolerance.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Total Assets: ${user_info.get('total_assets', user_info.get('savings', 0)):,.2f}
- Risk Tolerance: {user_info.get('risk_tolerance', 'moderate')}

IMPORTANT: You MUST use the available tools to provide accurate wealth management advice:

1. Call calculate_wealth_allocation with total assets, age, and risk tolerance
2. Call get_market_indices to assess current market conditions
3. Call get_portfolio_performance to evaluate current portfolio health
4. Call get_stock_price for specific investment examples if applicable

After using these tools, provide comprehensive recommendations for:
- Personalized investment strategy aligned with risk tolerance
- Real-time portfolio adjustments based on market conditions
- Financial goal tracking and progress monitoring
- Tax optimization strategies
- Cash flow management and diversification
- Regular portfolio review and rebalancing schedule"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Personal Wealth Management")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                result = calculate_wealth_allocation.invoke(tool_args)
                tool_results.append(result)
                mcp_tools_used.append({"name": tool_name, "args": tool_args, "result": result})
                print(f"  ✓ {tool_name} completed")

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive wealth management summary including investment strategy, tax optimization,
diversification recommendations, and monitoring schedule."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            print(f"\n⚠ LLM did not invoke tools for Personal Wealth Management, calling directly")
            # Call ONLY MCP data sources - no calculation logic
            print(f"  → Fetching MCP data sources...")
            
            # Market Data MCP
            market_result = get_market_indices.invoke({})
            mcp_tools_used.append({"name": "get_market_indices", "source": "Market Data MCP", "args": {}, "result": market_result})
            print(f"  ✓ get_market_indices (Market Data MCP) completed")
            
            # Create simple summary from MCP data only
            summary = "MCP Data Sources Retrieved: Market indices data fetched successfully for workshop demonstration."

        # Track MCP tools used for this plan
        if "Personal Wealth Management" not in state["mcp_data"]:
            state["mcp_data"]["Personal Wealth Management"] = {"tools": []}
        state["mcp_data"]["Personal Wealth Management"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Personal Wealth Management"] = summary
        state["messages"].append(AIMessage(content="✓ Wealth Management Planning Complete"))

        return state


class EducationAgent:
    """Education Planning Specialist Agent
    
    Helps clients plan and save for educational expenses. It explores options for tuition funding, 
    researches scholarships, and develops loan strategies based on individual needs and timelines. 
    Whether it's 529 plans or other education savings vehicles, this agent knows the options.
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_education_fund, calculate_529_plan, analyze_scholarship_opportunities, project_retirement_inflation]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are an Education Planning Specialist who helps clients plan and save for 
educational expenses. You explore options for tuition funding, research scholarships, and develop 
loan strategies based on individual needs and timelines. You're an expert in 529 plans and other 
education savings vehicles.

User Information:
- Number of Children: {user_info.get('num_children', 0)}
- Children Ages: {user_info.get('children_ages', [])}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Current Education Savings: ${user_info.get('education_savings', 0):,.2f}
- Annual Education Contribution: ${user_info.get('annual_education_contribution', 0):,.2f}

IMPORTANT: You MUST use the available tools to provide accurate education planning:

1. Call calculate_education_fund with number of children and their ages to determine funding needs
2. Call calculate_529_plan to show tax-advantaged saving strategies
3. Call analyze_scholarship_opportunities to identify funding sources
4. Call project_retirement_inflation to understand cost escalation over time

After using these tools, provide comprehensive education planning recommendations including:
- Total education funding needs by child
- 529 plan strategy and contribution recommendations
- Scholarship opportunities and research guidance
- Loan optimization approaches
- Timeline-based funding strategy"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Education Planning")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                for tool in self.tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(result)
                        mcp_tools_used.append({"name": tool_name, "args": tool_args, "result": result})
                        print(f"  ✓ {tool_name} completed")

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive education planning summary including 529 plan strategies, 
scholarship opportunities, loan optimization, and timeline-based funding approaches."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            print(f"\n⚠ LLM did not invoke tools for Education Planning, calling directly")
            # Call key tool directly
            num_children = user_info.get('num_children', 0)
            children_ages = user_info.get('children_ages', [])
            
            if num_children > 0 and children_ages:
                education_args = {
                    "num_children": num_children,
                    "children_ages": children_ages
                }
                education_result = calculate_education_fund.invoke(education_args)
                tool_results.append(education_result)
                mcp_tools_used.append({"name": "calculate_education_fund", "args": education_args, "result": education_result})
                print(f"  ✓ calculate_education_fund completed")
            
            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive education planning summary including 529 plan strategies, 
scholarship opportunities, loan optimization, and timeline-based funding approaches."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content

        # Track MCP tools used for this plan
        if "Education Planning" not in state["mcp_data"]:
            state["mcp_data"]["Education Planning"] = {"tools": []}
        state["mcp_data"]["Education Planning"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Education Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Education Planning Complete"))

        return state


class TaxAgent:
    """Tax Planning Specialist Agent
    
    Optimizes tax strategies, identifies deductions, and assists with compliance to minimize 
    liabilities and maximize savings year-round. This is particularly valuable because tax 
    implications touch almost every financial decision. This agent ensures we're making 
    tax-efficient choices across the entire financial plan.
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_tax_optimization, get_inflation_rate, get_federal_funds_rate]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are a Tax Planning Specialist who optimizes tax strategies, identifies 
deductions, and assists with compliance to minimize liabilities and maximize savings year-round. 
Tax implications touch almost every financial decision, so you ensure tax-efficient choices 
across the entire financial plan.

User Information:
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Filing Status: {user_info.get('filing_status', 'married')}
- Current Retirement Contributions: ${user_info.get('retirement_contributions', 0):,.2f}
- Charitable Giving: ${user_info.get('charitable_giving', 0):,.2f}
- Other Deductions: ${user_info.get('other_deductions', 0):,.2f}

IMPORTANT: You MUST use the available tools to provide accurate tax planning:

1. Call calculate_tax_optimization with income and deductions to identify tax savings opportunities
2. Call get_inflation_rate to understand impact on tax brackets and deductions
3. Call get_federal_funds_rate to assess interest rate implications for tax strategy

After using these tools, provide comprehensive tax planning strategies including:
- Deduction optimization and maximization
- Retirement contribution strategies (401k, IRA, backdoor conversions)
- Tax-loss harvesting opportunities
- Estimated quarterly tax planning
- Year-round tax-efficient decision making"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        mcp_tools_used = []  # Track tools for display
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\n✓ LLM invoked {len(response.tool_calls)} tools for Tax Planning")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                result = calculate_tax_optimization.invoke(tool_args)
                tool_results.append(result)
                mcp_tools_used.append({"name": tool_name, "args": tool_args, "result": result})
                print(f"  ✓ {tool_name} completed")

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive tax planning summary including optimization strategies, 
deduction identification, compliance assistance, and year-round tax-efficient decision making."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            print(f"\n⚠ LLM did not invoke tools for Tax Planning, calling directly")
            # Call key tool directly
            annual_income = user_info.get('annual_income', 0)
            retirement_contributions = user_info.get('retirement_contributions', 0)
            charitable_giving = user_info.get('charitable_giving', 0)
            
            tax_args = {
                "annual_income": annual_income,
                "retirement_contributions": retirement_contributions,
                "charitable_giving": charitable_giving
            }
            tax_result = calculate_tax_optimization.invoke(tax_args)
            tool_results.append(tax_result)
            mcp_tools_used.append({"name": "calculate_tax_optimization", "args": tax_args, "result": tax_result})
            print(f"  ✓ calculate_tax_optimization completed")
            
            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive tax planning summary including optimization strategies, 
deduction identification, compliance assistance, and year-round tax-efficient decision making."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content

        # Track MCP tools used for this plan
        if "Tax Planning" not in state["mcp_data"]:
            state["mcp_data"]["Tax Planning"] = {"tools": []}
        state["mcp_data"]["Tax Planning"]["tools"] = mcp_tools_used

        state["plan_summaries"]["Tax Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Tax Planning Complete"))

        return state


# ============================================================================
# ORCHESTRATOR AGENT
# ============================================================================

class OrchestratorAgent:
    """Orchestrator that routes to appropriate agents"""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.retirement_agent = RetirementAgent(llm)
        self.insurance_agent = InsuranceAgent(llm)
        self.estate_agent = EstateAgent(llm)
        self.wealth_agent = WealthAgent(llm)
        self.education_agent = EducationAgent(llm)
        self.tax_agent = TaxAgent(llm)

    def route(self, state: AgentState) -> AgentState:
        """Route to appropriate agents based on selected plans"""
        selected = state["selected_plans"]

        if "Retirement Planning" in selected and "Retirement Planning" not in state["plan_summaries"]:
            state = self.retirement_agent.process(state)

        if "Insurance Planning" in selected and "Insurance Planning" not in state["plan_summaries"]:
            state = self.insurance_agent.process(state)

        if "Estate Planning" in selected and "Estate Planning" not in state["plan_summaries"]:
            state = self.estate_agent.process(state)

        if "Personal Wealth Management" in selected and "Personal Wealth Management" not in state["plan_summaries"]:
            state = self.wealth_agent.process(state)

        if "Education Planning" in selected and "Education Planning" not in state["plan_summaries"]:
            state = self.education_agent.process(state)

        if "Tax Planning" in selected and "Tax Planning" not in state["plan_summaries"]:
            state = self.tax_agent.process(state)

        # Generate integrated summary
        state = self.create_integrated_summary(state)

        return state

    def create_integrated_summary(self, state: AgentState) -> AgentState:
        """Create an integrated summary of all plans"""
        summaries = state["plan_summaries"]
        user_info = state["user_info"]

        prompt = f"""You are a Senior Financial Advisor. Create an integrated Executive Summary
that combines all the individual plan summaries into a cohesive financial plan.

Each of our specialized agents brings expert knowledge to the table - just like you'd have different 
advisors in a traditional wealth management firm. The difference is that our AI agents can work 
simultaneously, share information instantly, and provide recommendations in minutes rather than weeks.

User Profile:
{json.dumps(user_info, indent=2)}

Individual Plan Summaries:
{chr(10).join([f"### {plan}:{chr(10)}{summary}{chr(10)}" for plan, summary in summaries.items()])}

Create an Executive Summary that:
1. Provides an overview of the client's financial situation
2. Highlights key recommendations from each planning area
3. Identifies synergies and priorities across plans (especially tax implications that touch every decision)
4. Provides a clear action plan with timeline
5. Notes any areas requiring immediate attention
6. Emphasizes how our specialized agents work together for comprehensive planning"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        state["plan_summaries"]["Executive Summary"] = response.content

        return state
