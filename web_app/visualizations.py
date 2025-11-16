"""
Visualization module for Financial Planning Web Application
"""
from typing import Dict, Any, Optional, List
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


def create_retirement_projection_chart(user_info: Dict[str, Any]) -> str:
    """Create retirement savings projection chart - returns JSON for Plotly"""
    current_age = user_info.get('age', 30)
    retirement_age = user_info.get('retirement_age', 65)
    current_savings = user_info.get('savings', 0)
    annual_income = user_info.get('annual_income', 0)

    # Project savings with different contribution rates
    ages = list(range(current_age, 86))

    # Scenario 1: Current savings only (no additional contributions)
    no_contrib = []
    # Scenario 2: Conservative (5% of income)
    conservative = []
    # Scenario 3: Moderate (10% of income)
    moderate = []
    # Scenario 4: Aggressive (15% of income)
    aggressive = []

    for i, age in enumerate(ages):
        years_elapsed = i
        growth_rate = 0.07  # 7% annual return

        # No contributions
        no_contrib.append(current_savings * ((1 + growth_rate) ** years_elapsed))

        # With contributions (future value of annuity formula)
        if age < retirement_age:
            conservative_contrib = annual_income * 0.05
            moderate_contrib = annual_income * 0.10
            aggressive_contrib = annual_income * 0.15

            fv_contrib_c = conservative_contrib * (((1 + growth_rate) ** years_elapsed - 1) / growth_rate)
            fv_contrib_m = moderate_contrib * (((1 + growth_rate) ** years_elapsed - 1) / growth_rate)
            fv_contrib_a = aggressive_contrib * (((1 + growth_rate) ** years_elapsed - 1) / growth_rate)

            conservative.append(current_savings * ((1 + growth_rate) ** years_elapsed) + fv_contrib_c)
            moderate.append(current_savings * ((1 + growth_rate) ** years_elapsed) + fv_contrib_m)
            aggressive.append(current_savings * ((1 + growth_rate) ** years_elapsed) + fv_contrib_a)
        else:
            # After retirement, start drawing down
            withdrawal_rate = 0.04
            years_in_retirement = age - retirement_age

            conservative.append(max(0, conservative[-1] * ((1 + growth_rate - withdrawal_rate) ** 1)))
            moderate.append(max(0, moderate[-1] * ((1 + growth_rate - withdrawal_rate) ** 1)))
            aggressive.append(max(0, aggressive[-1] * ((1 + growth_rate - withdrawal_rate) ** 1)))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=ages, y=no_contrib, name='No Additional Savings',
                             line=dict(color='red', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=ages, y=conservative, name='Conservative (5% savings)',
                             line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=ages, y=moderate, name='Moderate (10% savings)',
                             line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=ages, y=aggressive, name='Aggressive (15% savings)',
                             line=dict(color='green', width=2)))

    # Add retirement age line
    fig.add_vline(x=retirement_age, line_dash="dot", line_color="gray",
                  annotation_text="Retirement Age", annotation_position="top")

    fig.update_layout(
        title='Retirement Savings Projection',
        xaxis_title='Age',
        yaxis_title='Portfolio Value ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        yaxis=dict(tickformat='$,.0f')
    )

    return fig.to_json()


def create_asset_allocation_pie(user_info: Dict[str, Any]) -> str:
    """Create asset allocation pie chart - returns JSON for Plotly"""
    age = user_info.get('age', 30)
    risk_tolerance = user_info.get('risk_tolerance', 'moderate')
    total_assets = user_info.get('total_assets', user_info.get('savings', 0))

    # Calculate allocation
    base_stock_pct = 100 - age

    if risk_tolerance.lower() == "aggressive":
        stock_pct = min(90, base_stock_pct + 10)
    elif risk_tolerance.lower() == "conservative":
        stock_pct = max(20, base_stock_pct - 20)
    else:
        stock_pct = base_stock_pct

    bond_pct = 100 - stock_pct

    # Further breakdown
    allocations = {
        'US Stocks': stock_pct * 0.6,
        'International Stocks': stock_pct * 0.3,
        'Emerging Markets': stock_pct * 0.1,
        'Bonds': bond_pct * 0.7,
        'Cash/Money Market': bond_pct * 0.3
    }

    values = [total_assets * (pct / 100) for pct in allocations.values()]

    fig = go.Figure(data=[go.Pie(
        labels=list(allocations.keys()),
        values=values,
        hole=.3,
        marker=dict(colors=['#2E86AB', '#A23B72', '#F18F01', '#06A77D', '#D4AF37'])
    )])

    fig.update_layout(
        title=f'Recommended Asset Allocation ({risk_tolerance.title()} Profile)',
        annotations=[dict(text=f'${total_assets:,.0f}', x=0.5, y=0.5, font_size=20, showarrow=False)],
        height=500
    )

    return fig.to_json()


def create_insurance_coverage_chart(user_info: Dict[str, Any]) -> str:
    """Create insurance coverage comparison chart - returns JSON for Plotly"""
    annual_income = user_info.get('annual_income', 0)
    num_dependents = user_info.get('num_dependents', 0)
    debts = user_info.get('debts', 0)
    savings = user_info.get('savings', 0)

    # Calculate recommended coverage
    base_coverage = (annual_income * 10) + debts - savings
    dependent_factor = 1 + (num_dependents * 0.2)
    recommended_coverage = base_coverage * dependent_factor

    # Different insurance types
    insurance_types = ['Life Insurance', 'Disability Insurance', 'Critical Illness', 'Long-term Care']
    recommended = [
        recommended_coverage,
        annual_income * 5,  # Disability
        annual_income * 3,  # Critical illness
        300000  # Long-term care average
    ]

    current = [
        recommended_coverage * 0.4,  # Assume underinsured
        annual_income * 2,
        0,
        0
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Current Coverage',
        x=insurance_types,
        y=current,
        marker_color='lightcoral'
    ))

    fig.add_trace(go.Bar(
        name='Recommended Coverage',
        x=insurance_types,
        y=recommended,
        marker_color='lightseagreen'
    ))

    fig.update_layout(
        title='Insurance Coverage Analysis',
        xaxis_title='Insurance Type',
        yaxis_title='Coverage Amount ($)',
        barmode='group',
        template='plotly_white',
        height=500,
        yaxis=dict(tickformat='$,.0f')
    )

    return fig.to_json()


def create_education_funding_chart(user_info: Dict[str, Any]) -> Optional[str]:
    """Create education funding progress chart - returns JSON for Plotly"""
    num_children = user_info.get('num_children', 0)
    children_ages = user_info.get('children_ages', [])

    if num_children == 0 or not children_ages:
        return None

    cost_per_year = 30000
    inflation_rate = 0.05

    children_data = []
    for i, age in enumerate(children_ages):
        years_until_college = max(0, 18 - age)
        future_cost = cost_per_year * ((1 + inflation_rate) ** years_until_college)
        total_needed = future_cost * 4

        # Assume some savings already (30% of needed)
        current_savings = total_needed * 0.3

        children_data.append({
            'child': f'Child {i+1} (Age {age})',
            'needed': total_needed,
            'saved': current_savings,
            'gap': total_needed - current_savings,
            'years': years_until_college
        })

    fig = go.Figure()

    children_labels = [c['child'] for c in children_data]

    fig.add_trace(go.Bar(
        name='Amount Saved',
        x=children_labels,
        y=[c['saved'] for c in children_data],
        marker_color='mediumseagreen'
    ))

    fig.add_trace(go.Bar(
        name='Funding Gap',
        x=children_labels,
        y=[c['gap'] for c in children_data],
        marker_color='tomato'
    ))

    fig.update_layout(
        title='Education Funding Status',
        xaxis_title='Child',
        yaxis_title='Amount ($)',
        barmode='stack',
        template='plotly_white',
        height=500,
        yaxis=dict(tickformat='$,.0f')
    )

    return fig.to_json()


def create_net_worth_projection(user_info: Dict[str, Any]) -> str:
    """Create net worth projection over time - returns JSON for Plotly"""
    current_age = user_info.get('age', 30)
    annual_income = user_info.get('annual_income', 0)
    current_savings = user_info.get('savings', 0)
    debts = user_info.get('debts', 0)
    retirement_age = user_info.get('retirement_age', 65)

    ages = list(range(current_age, retirement_age + 30))

    assets = []
    liabilities = []
    net_worth = []

    annual_savings = annual_income * 0.15
    debt_payment = debts * 0.1 if debts > 0 else 0

    current_asset = current_savings
    current_debt = debts

    for i, age in enumerate(ages):
        growth_rate = 0.07

        if age < retirement_age:
            # Accumulation phase
            current_asset = current_asset * (1 + growth_rate) + annual_savings
            current_debt = max(0, current_debt - debt_payment)
        else:
            # Retirement phase
            current_asset = current_asset * (1 + growth_rate) - (annual_income * 0.8 * 0.04)
            current_debt = 0

        assets.append(current_asset)
        liabilities.append(current_debt)
        net_worth.append(current_asset - current_debt)

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(
        x=ages, y=assets, name='Assets',
        fill='tonexty',
        line=dict(color='green', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=ages, y=liabilities, name='Liabilities',
        fill='tozeroy',
        line=dict(color='red', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=ages, y=net_worth, name='Net Worth',
        line=dict(color='blue', width=3, dash='dash')
    ))

    fig.add_vline(x=retirement_age, line_dash="dot", line_color="gray",
                  annotation_text="Retirement", annotation_position="top")

    fig.update_layout(
        title='Net Worth Projection Over Time',
        xaxis_title='Age',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        yaxis=dict(tickformat='$,.0f')
    )

    return fig.to_json()


def create_monthly_budget_breakdown(user_info: Dict[str, Any]) -> str:
    """Create monthly budget breakdown - returns JSON for Plotly"""
    annual_income = user_info.get('annual_income', 0)
    monthly_income = annual_income / 12

    # 50/30/20 rule with adjustments
    categories = {
        'Housing': monthly_income * 0.28,
        'Transportation': monthly_income * 0.15,
        'Food': monthly_income * 0.12,
        'Utilities': monthly_income * 0.08,
        'Insurance': monthly_income * 0.07,
        'Savings/Investments': monthly_income * 0.15,
        'Entertainment': monthly_income * 0.08,
        'Personal Care': monthly_income * 0.04,
        'Other': monthly_income * 0.03
    }

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
              '#6C5CE7', '#FDCB6E', '#E17055', '#A29BFE']

    fig = go.Figure(data=[go.Bar(
        y=list(categories.keys()),
        x=list(categories.values()),
        orientation='h',
        marker=dict(color=colors),
        text=[f'${v:,.0f}' for v in categories.values()],
        textposition='auto',
    )])

    fig.update_layout(
        title=f'Recommended Monthly Budget (Total: ${monthly_income:,.0f})',
        xaxis_title='Monthly Amount ($)',
        yaxis_title='Category',
        template='plotly_white',
        height=500,
        showlegend=False,
        xaxis=dict(tickformat='$,.0f')
    )

    return fig.to_json()


def get_visualizations(user_info: Dict[str, Any], selected_plans: List[str]) -> Dict[str, str]:
    """Get all relevant visualizations based on selected plans"""
    visualizations = {}

    # Net Worth Projection (always show)
    visualizations['net_worth'] = create_net_worth_projection(user_info)

    # Retirement Planning visualizations
    if "Retirement Planning" in selected_plans:
        visualizations['retirement'] = create_retirement_projection_chart(user_info)

    # Wealth Management visualizations
    if "Personal Wealth Management" in selected_plans or "Retirement Planning" in selected_plans:
        visualizations['allocation'] = create_asset_allocation_pie(user_info)
        visualizations['budget'] = create_monthly_budget_breakdown(user_info)

    # Insurance Planning visualizations
    if "Insurance Planning" in selected_plans:
        visualizations['insurance'] = create_insurance_coverage_chart(user_info)

    # Estate Planning visualizations
    if "Estate Planning" in selected_plans:
        num_children = user_info.get('num_children', 0)
        if num_children > 0:
            edu_viz = create_education_funding_chart(user_info)
            if edu_viz:
                visualizations['education'] = edu_viz

    return visualizations
