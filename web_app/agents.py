"""
Financial Planning Agents Module
Extracted from PlanSummary-AgenticAI.ipynb
"""
import json
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import operator


# ============================================================================
# FINANCIAL PLANNING TOOLS
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

    return f"""Retirement Calculation:
- Years until retirement: {years_to_retirement}
- Years in retirement: {years_in_retirement}
- Future annual expenses (adjusted for inflation): ${future_annual_expenses:,.2f}
- Total retirement fund needed: ${total_needed:,.2f}
- Recommended monthly savings: ${(total_needed / (years_to_retirement * 12)):,.2f}"""

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

    return f"""Education Fund Calculation:
{chr(10).join(details)}
- Total education fund needed: ${total_needed:,.2f}
- Recommended monthly savings: ${(total_needed / (max([18 - age for age in children_ages if age < 18] + [1]) * 12)):,.2f}"""

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


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(TypedDict):
    """State for agent graph"""
    messages: Annotated[Sequence[HumanMessage | AIMessage | SystemMessage], operator.add]
    user_info: Dict[str, Any]
    selected_plans: List[str]
    plan_summaries: Dict[str, str]
    next_agent: str


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

class RetirementAgent:
    """Retirement Planning Specialist Agent"""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_retirement_needs, calculate_wealth_allocation]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are a Retirement Planning Specialist. Analyze the user's information and create a comprehensive retirement plan.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Retirement Age: {user_info.get('retirement_age', 'Not provided')}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Current Savings: ${user_info.get('savings', 0):,.2f}
- Risk Tolerance: {user_info.get('risk_tolerance', 'moderate')}

Use the available tools to calculate retirement needs and recommend asset allocation.
Provide a detailed retirement plan summary."""

        tools_to_use = self.tools
        llm_with_tools = self.llm.bind_tools(tools_to_use)

        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        # Execute tool calls if any
        tool_results = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # Find and execute the tool
                for tool in tools_to_use:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(result)

            # Create final summary with tool results
            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive retirement planning summary with specific recommendations."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            summary = response.content

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

Use the life insurance calculation tool and provide comprehensive insurance recommendations
including life, health, disability, and liability insurance."""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = calculate_life_insurance.invoke(tool_call["args"])
                tool_results.append(result)

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive insurance planning summary covering life, health, disability, and liability insurance."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            summary = response.content

        state["plan_summaries"]["Insurance Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Insurance Planning Complete"))

        return state


class EstateAgent:
    """Estate Planning Specialist Agent"""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_estate_tax, calculate_education_fund]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are an Estate Planning Specialist. Create a comprehensive estate plan.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Total Assets: ${user_info.get('total_assets', user_info.get('savings', 0)):,.2f}
- Number of Children: {user_info.get('num_children', 0)}
- Children Ages: {user_info.get('children_ages', [])}

Use the available tools to calculate estate taxes and education funding needs.
Provide recommendations for wills, trusts, beneficiaries, and legacy planning."""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                for tool in self.tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_call["args"])
                        tool_results.append(result)

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive estate planning summary including wills, trusts, beneficiary designations,
education funding, and tax minimization strategies."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            summary = response.content

        state["plan_summaries"]["Estate Planning"] = summary
        state["messages"].append(AIMessage(content="✓ Estate Planning Complete"))

        return state


class WealthAgent:
    """Personal Wealth Management Specialist Agent"""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = [calculate_wealth_allocation]

    def process(self, state: AgentState) -> AgentState:
        user_info = state["user_info"]

        prompt = f"""You are a Personal Wealth Management Specialist. Create a comprehensive wealth management strategy.

User Information:
- Age: {user_info.get('age', 'Not provided')}
- Annual Income: ${user_info.get('annual_income', 0):,.2f}
- Total Assets: ${user_info.get('total_assets', user_info.get('savings', 0)):,.2f}
- Risk Tolerance: {user_info.get('risk_tolerance', 'moderate')}

Use the asset allocation tool and provide recommendations for:
- Investment strategy
- Tax optimization
- Cash flow management
- Diversification
- Regular portfolio review schedule"""

        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])

        tool_results = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = calculate_wealth_allocation.invoke(tool_call["args"])
                tool_results.append(result)

            summary_prompt = f"""Based on these calculations:
{chr(10).join(tool_results)}

Create a comprehensive wealth management summary including investment strategy, tax optimization,
diversification recommendations, and monitoring schedule."""

            final_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            summary = final_response.content
        else:
            summary = response.content

        state["plan_summaries"]["Personal Wealth Management"] = summary
        state["messages"].append(AIMessage(content="✓ Wealth Management Planning Complete"))

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

        # Generate integrated summary
        state = self.create_integrated_summary(state)

        return state

    def create_integrated_summary(self, state: AgentState) -> AgentState:
        """Create an integrated summary of all plans"""
        summaries = state["plan_summaries"]
        user_info = state["user_info"]

        prompt = f"""You are a Senior Financial Advisor. Create an integrated Executive Summary
that combines all the individual plan summaries into a cohesive financial plan.

User Profile:
{json.dumps(user_info, indent=2)}

Individual Plan Summaries:
{chr(10).join([f"### {plan}:{chr(10)}{summary}{chr(10)}" for plan, summary in summaries.items()])}

Create an Executive Summary that:
1. Provides an overview of the client's financial situation
2. Highlights key recommendations from each planning area
3. Identifies synergies and priorities across plans
4. Provides a clear action plan with timeline
5. Notes any areas requiring immediate attention"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        state["plan_summaries"]["Executive Summary"] = response.content

        return state
