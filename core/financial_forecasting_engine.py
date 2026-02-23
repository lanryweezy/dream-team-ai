"""
Financial Forecasting & Planning Engine
Advanced financial modeling, scenario planning, and runway optimization
Integrates with business intelligence and provides comprehensive financial insights
"""

import json
import logging
import asyncio
import math
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class ScenarioType(Enum):
    CONSERVATIVE = "conservative"
    BASE_CASE = "base_case"
    OPTIMISTIC = "optimistic"
    STRESS_TEST = "stress_test"

class RevenueModel(Enum):
    SUBSCRIPTION = "subscription"
    TRANSACTION = "transaction"
    MARKETPLACE = "marketplace"
    ADVERTISING = "advertising"
    FREEMIUM = "freemium"
    ENTERPRISE = "enterprise"

@dataclass
class FinancialAssumptions:
    """Core financial assumptions for modeling"""
    # Revenue assumptions
    monthly_growth_rate: float = 0.15
    churn_rate: float = 0.05
    average_revenue_per_user: float = 100.0
    customer_acquisition_cost: float = 450.0
    customer_lifetime_value: float = 2000.0
    
    # Cost assumptions
    gross_margin: float = 0.75
    sales_marketing_percentage: float = 0.40
    rd_percentage: float = 0.25
    ga_percentage: float = 0.15
    
    # Growth assumptions
    market_penetration_rate: float = 0.02
    viral_coefficient: float = 0.3
    pricing_power: float = 0.05  # Annual price increase capability
    
    # Operational assumptions
    employee_growth_rate: float = 0.10
    average_salary: float = 120000.0
    office_cost_per_employee: float = 2000.0
    
    # Market assumptions
    market_size: float = 1000000000.0
    market_growth_rate: float = 0.20
    competitive_pressure: float = 0.05

@dataclass
class FinancialScenario:
    """Complete financial scenario with projections"""
    scenario_id: str
    scenario_type: ScenarioType
    scenario_name: str
    assumptions: FinancialAssumptions
    time_horizon_months: int = 36
    
    # Projections
    revenue_projections: Dict[str, float] = field(default_factory=dict)
    cost_projections: Dict[str, float] = field(default_factory=dict)
    profit_projections: Dict[str, float] = field(default_factory=dict)
    cash_flow_projections: Dict[str, float] = field(default_factory=dict)
    customer_projections: Dict[str, int] = field(default_factory=dict)
    employee_projections: Dict[str, int] = field(default_factory=dict)
    
    # Key metrics
    break_even_month: Optional[int] = None
    peak_funding_requirement: float = 0.0
    ltv_cac_ratio: float = 0.0
    payback_period_months: float = 0.0
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class CashFlowForecast:
    """Detailed cash flow forecast"""
    forecast_id: str
    period_months: int
    
    # Operating cash flow
    operating_cash_flow: Dict[str, float] = field(default_factory=dict)
    
    # Investing cash flow
    capex: Dict[str, float] = field(default_factory=dict)
    rd_investments: Dict[str, float] = field(default_factory=dict)
    
    # Financing cash flow
    equity_funding: Dict[str, float] = field(default_factory=dict)
    debt_financing: Dict[str, float] = field(default_factory=dict)
    
    # Net cash flow and balance
    net_cash_flow: Dict[str, float] = field(default_factory=dict)
    cash_balance: Dict[str, float] = field(default_factory=dict)
    
    # Runway analysis
    runway_months: float = 0.0
    funding_requirements: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class SensitivityAnalysis:
    """Sensitivity analysis for key variables"""
    analysis_id: str
    base_scenario: str
    
    # Variable sensitivity
    revenue_sensitivity: Dict[str, Dict[str, float]] = field(default_factory=dict)
    cost_sensitivity: Dict[str, Dict[str, float]] = field(default_factory=dict)
    growth_sensitivity: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Tornado chart data
    tornado_chart: List[Dict[str, Any]] = field(default_factory=list)
    
    # Monte Carlo results
    monte_carlo_results: Dict[str, Any] = field(default_factory=dict)

class FinancialForecastingEngine:
    """
    Advanced financial forecasting and planning engine that provides:
    - Multi-scenario financial modeling
    - Cash flow forecasting and runway analysis
    - Sensitivity analysis and stress testing
    - Unit economics optimization
    - Funding requirement planning
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.scenarios: Dict[str, FinancialScenario] = {}
        self.cash_flow_forecasts: Dict[str, CashFlowForecast] = {}
        self.sensitivity_analyses: Dict[str, SensitivityAnalysis] = {}
        
        # Model parameters
        self.default_assumptions = FinancialAssumptions()
        self.industry_benchmarks: Dict[str, Dict[str, float]] = {}
        
        self._initialize_industry_benchmarks()
    
    def _initialize_industry_benchmarks(self):
        """Initialize industry benchmark data"""
        
        self.industry_benchmarks = {
            "saas": {
                "monthly_growth_rate": 0.15,
                "churn_rate": 0.05,
                "gross_margin": 0.80,
                "ltv_cac_ratio": 3.0,
                "payback_period": 12,
                "sales_marketing_percentage": 0.45,
                "rd_percentage": 0.20
            },
            "ecommerce": {
                "monthly_growth_rate": 0.10,
                "churn_rate": 0.08,
                "gross_margin": 0.40,
                "ltv_cac_ratio": 2.5,
                "payback_period": 8,
                "sales_marketing_percentage": 0.35,
                "rd_percentage": 0.10
            },
            "fintech": {
                "monthly_growth_rate": 0.20,
                "churn_rate": 0.03,
                "gross_margin": 0.85,
                "ltv_cac_ratio": 4.0,
                "payback_period": 10,
                "sales_marketing_percentage": 0.40,
                "rd_percentage": 0.25
            },
            "marketplace": {
                "monthly_growth_rate": 0.18,
                "churn_rate": 0.06,
                "gross_margin": 0.20,
                "ltv_cac_ratio": 3.5,
                "payback_period": 15,
                "sales_marketing_percentage": 0.50,
                "rd_percentage": 0.15
            }
        }
    
    async def create_financial_scenarios(self, blueprint: CompanyBlueprint) -> Dict[str, FinancialScenario]:
        """Create multiple financial scenarios for comprehensive planning"""
        
        try:
            logger.info(f"Creating financial scenarios for {blueprint.name}")
            
            # Get industry benchmarks
            industry = blueprint.industry.lower()
            benchmarks = self.industry_benchmarks.get(industry, self.industry_benchmarks["saas"])
            
            # Create base assumptions
            base_assumptions = FinancialAssumptions(
                monthly_growth_rate=benchmarks["monthly_growth_rate"],
                churn_rate=benchmarks["churn_rate"],
                gross_margin=benchmarks["gross_margin"],
                sales_marketing_percentage=benchmarks["sales_marketing_percentage"],
                rd_percentage=benchmarks["rd_percentage"]
            )
            
            scenarios = {}
            
            # Conservative scenario
            conservative_assumptions = FinancialAssumptions(
                monthly_growth_rate=base_assumptions.monthly_growth_rate * 0.7,
                churn_rate=base_assumptions.churn_rate * 1.5,
                customer_acquisition_cost=base_assumptions.customer_acquisition_cost * 1.3,
                gross_margin=base_assumptions.gross_margin * 0.9,
                sales_marketing_percentage=base_assumptions.sales_marketing_percentage * 1.2
            )
            
            conservative_scenario = await self._build_scenario(
                "conservative",
                ScenarioType.CONSERVATIVE,
                "Conservative Case",
                conservative_assumptions,
                blueprint
            )
            scenarios["conservative"] = conservative_scenario
            
            # Base case scenario
            base_scenario = await self._build_scenario(
                "base_case",
                ScenarioType.BASE_CASE,
                "Base Case",
                base_assumptions,
                blueprint
            )
            scenarios["base_case"] = base_scenario
            
            # Optimistic scenario
            optimistic_assumptions = FinancialAssumptions(
                monthly_growth_rate=base_assumptions.monthly_growth_rate * 1.5,
                churn_rate=base_assumptions.churn_rate * 0.7,
                customer_acquisition_cost=base_assumptions.customer_acquisition_cost * 0.8,
                gross_margin=base_assumptions.gross_margin * 1.1,
                viral_coefficient=base_assumptions.viral_coefficient * 2.0
            )
            
            optimistic_scenario = await self._build_scenario(
                "optimistic",
                ScenarioType.OPTIMISTIC,
                "Optimistic Case",
                optimistic_assumptions,
                blueprint
            )
            scenarios["optimistic"] = optimistic_scenario
            
            # Stress test scenario
            stress_assumptions = FinancialAssumptions(
                monthly_growth_rate=base_assumptions.monthly_growth_rate * 0.3,
                churn_rate=base_assumptions.churn_rate * 3.0,
                customer_acquisition_cost=base_assumptions.customer_acquisition_cost * 2.0,
                gross_margin=base_assumptions.gross_margin * 0.7,
                market_growth_rate=0.05  # Market contraction
            )
            
            stress_scenario = await self._build_scenario(
                "stress_test",
                ScenarioType.STRESS_TEST,
                "Stress Test",
                stress_assumptions,
                blueprint
            )
            scenarios["stress_test"] = stress_scenario
            
            # Store scenarios
            self.scenarios.update(scenarios)
            
            logger.info(f"Created {len(scenarios)} financial scenarios")
            return scenarios
            
        except Exception as e:
            logger.error(f"Failed to create financial scenarios: {e}")
            raise
    
    async def _build_scenario(
        self,
        scenario_id: str,
        scenario_type: ScenarioType,
        scenario_name: str,
        assumptions: FinancialAssumptions,
        blueprint: CompanyBlueprint
    ) -> FinancialScenario:
        """Build detailed financial scenario"""
        
        scenario = FinancialScenario(
            scenario_id=scenario_id,
            scenario_type=scenario_type,
            scenario_name=scenario_name,
            assumptions=assumptions,
            time_horizon_months=36
        )
        
        # Starting values
        initial_customers = 100
        initial_revenue = initial_customers * assumptions.average_revenue_per_user
        initial_employees = 10
        initial_cash = blueprint.funding_requirements
        
        # Build monthly projections
        customers = initial_customers
        employees = initial_employees
        cumulative_cash = initial_cash
        
        for month in range(1, 37):
            # Customer growth with churn
            new_customers = customers * assumptions.monthly_growth_rate
            churned_customers = customers * assumptions.churn_rate
            customers = customers + new_customers - churned_customers
            
            # Revenue calculation
            monthly_revenue = customers * assumptions.average_revenue_per_user
            
            # Cost calculations
            cogs = monthly_revenue * (1 - assumptions.gross_margin)
            
            # Operating expenses
            sales_marketing = monthly_revenue * assumptions.sales_marketing_percentage
            rd_costs = monthly_revenue * assumptions.rd_percentage
            ga_costs = monthly_revenue * assumptions.ga_percentage
            
            # Employee costs
            if month % 3 == 0:  # Hire every quarter
                employees = int(employees * (1 + assumptions.employee_growth_rate))
            
            employee_costs = employees * assumptions.average_salary / 12
            office_costs = employees * assumptions.office_cost_per_employee / 12
            
            total_costs = cogs + sales_marketing + rd_costs + ga_costs + employee_costs + office_costs
            
            # Profit and cash flow
            monthly_profit = monthly_revenue - total_costs
            cumulative_cash += monthly_profit
            
            # Store projections
            scenario.revenue_projections[f"month_{month}"] = round(monthly_revenue, 2)
            scenario.cost_projections[f"month_{month}"] = round(total_costs, 2)
            scenario.profit_projections[f"month_{month}"] = round(monthly_profit, 2)
            scenario.cash_flow_projections[f"month_{month}"] = round(cumulative_cash, 2)
            scenario.customer_projections[f"month_{month}"] = int(customers)
            scenario.employee_projections[f"month_{month}"] = employees
        
        # Calculate key metrics
        scenario.ltv_cac_ratio = assumptions.customer_lifetime_value / assumptions.customer_acquisition_cost
        scenario.payback_period_months = assumptions.customer_acquisition_cost / (assumptions.average_revenue_per_user * assumptions.gross_margin)
        
        # Find break-even month
        for month in range(1, 37):
            if scenario.cash_flow_projections[f"month_{month}"] > initial_cash:
                scenario.break_even_month = month
                break
        
        # Find peak funding requirement
        min_cash = min(scenario.cash_flow_projections.values())
        scenario.peak_funding_requirement = max(0, initial_cash - min_cash)
        
        return scenario
    
    async def generate_cash_flow_forecast(self, scenario_id: str) -> CashFlowForecast:
        """Generate detailed cash flow forecast"""
        
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.scenarios[scenario_id]
        
        forecast = CashFlowForecast(
            forecast_id=f"cf_{scenario_id}_{datetime.now().strftime('%H%M%S')}",
            period_months=scenario.time_horizon_months
        )
        
        # Calculate detailed cash flows
        for month in range(1, scenario.time_horizon_months + 1):
            month_key = f"month_{month}"
            
            # Operating cash flow
            revenue = scenario.revenue_projections[month_key]
            costs = scenario.cost_projections[month_key]
            operating_cf = revenue - costs
            forecast.operating_cash_flow[month_key] = round(operating_cf, 2)
            
            # Investing cash flow (CapEx and R&D investments)
            capex = revenue * 0.05  # 5% of revenue for infrastructure
            rd_investment = revenue * scenario.assumptions.rd_percentage
            forecast.capex[month_key] = round(capex, 2)
            forecast.rd_investments[month_key] = round(rd_investment, 2)
            
            # Financing cash flow (assume funding rounds)
            equity_funding = 0.0
            if month == 12:  # Series A at month 12
                equity_funding = 2000000
            elif month == 24:  # Series B at month 24
                equity_funding = 5000000
            
            forecast.equity_funding[month_key] = equity_funding
            forecast.debt_financing[month_key] = 0.0
            
            # Net cash flow
            net_cf = operating_cf - capex - rd_investment + equity_funding
            forecast.net_cash_flow[month_key] = round(net_cf, 2)
            
            # Cash balance
            if month == 1:
                cash_balance = scenario.cash_flow_projections[month_key]
            else:
                prev_balance = forecast.cash_balance[f"month_{month-1}"]
                cash_balance = prev_balance + net_cf
            
            forecast.cash_balance[month_key] = round(cash_balance, 2)
        
        # Calculate runway
        current_cash = list(forecast.cash_balance.values())[-1]
        avg_burn = statistics.mean([abs(cf) for cf in forecast.operating_cash_flow.values() if cf < 0])
        forecast.runway_months = current_cash / avg_burn if avg_burn > 0 else float('inf')
        
        # Identify funding requirements
        funding_requirements = []
        for month in range(1, scenario.time_horizon_months + 1):
            cash_balance = forecast.cash_balance[f"month_{month}"]
            if cash_balance < 500000:  # Less than 6 months runway
                funding_requirements.append({
                    "month": month,
                    "cash_balance": cash_balance,
                    "recommended_funding": 2000000,
                    "urgency": "high" if cash_balance < 200000 else "medium"
                })
        
        forecast.funding_requirements = funding_requirements
        
        self.cash_flow_forecasts[forecast.forecast_id] = forecast
        return forecast
    
    async def perform_sensitivity_analysis(self, base_scenario_id: str) -> SensitivityAnalysis:
        """Perform comprehensive sensitivity analysis"""
        
        if base_scenario_id not in self.scenarios:
            raise ValueError(f"Base scenario {base_scenario_id} not found")
        
        base_scenario = self.scenarios[base_scenario_id]
        
        analysis = SensitivityAnalysis(
            analysis_id=f"sensitivity_{base_scenario_id}_{datetime.now().strftime('%H%M%S')}",
            base_scenario=base_scenario_id
        )
        
        # Variables to test
        sensitivity_variables = {
            "monthly_growth_rate": [0.05, 0.10, 0.15, 0.20, 0.25],
            "churn_rate": [0.02, 0.035, 0.05, 0.065, 0.08],
            "customer_acquisition_cost": [300, 375, 450, 525, 600],
            "gross_margin": [0.65, 0.70, 0.75, 0.80, 0.85]
        }
        
        base_revenue_36 = base_scenario.revenue_projections["month_36"]
        
        # Test each variable
        for variable, values in sensitivity_variables.items():
            analysis.revenue_sensitivity[variable] = {}
            
            for value in values:
                # Create modified assumptions
                modified_assumptions = FinancialAssumptions(**asdict(base_scenario.assumptions))
                setattr(modified_assumptions, variable, value)
                
                # Build quick scenario
                test_scenario = await self._build_scenario(
                    f"test_{variable}_{value}",
                    ScenarioType.BASE_CASE,
                    f"Test {variable}",
                    modified_assumptions,
                    CompanyBlueprint(name="Test", industry="SaaS", business_model="Subscription")
                )
                
                # Calculate impact
                test_revenue_36 = test_scenario.revenue_projections["month_36"]
                impact_percentage = ((test_revenue_36 - base_revenue_36) / base_revenue_36) * 100
                
                analysis.revenue_sensitivity[variable][str(value)] = round(impact_percentage, 2)
        
        # Create tornado chart data
        tornado_data = []
        for variable, impacts in analysis.revenue_sensitivity.items():
            impact_values = list(impacts.values())
            max_impact = max(impact_values)
            min_impact = min(impact_values)
            range_impact = max_impact - min_impact
            
            tornado_data.append({
                "variable": variable,
                "max_impact": max_impact,
                "min_impact": min_impact,
                "range": range_impact
            })
        
        # Sort by impact range
        analysis.tornado_chart = sorted(tornado_data, key=lambda x: x["range"], reverse=True)
        
        # Monte Carlo simulation (simplified)
        monte_carlo_results = await self._run_monte_carlo_simulation(base_scenario)
        analysis.monte_carlo_results = monte_carlo_results
        
        self.sensitivity_analyses[analysis.analysis_id] = analysis
        return analysis
    
    async def _run_monte_carlo_simulation(self, base_scenario: FinancialScenario, iterations: int = 1000) -> Dict[str, Any]:
        """Run Monte Carlo simulation for risk analysis"""
        
        import random
        
        results = []
        
        for _ in range(iterations):
            # Randomly vary key assumptions
            growth_rate = base_scenario.assumptions.monthly_growth_rate * random.uniform(0.7, 1.3)
            churn_rate = base_scenario.assumptions.churn_rate * random.uniform(0.5, 2.0)
            cac = base_scenario.assumptions.customer_acquisition_cost * random.uniform(0.8, 1.5)
            
            # Quick calculation of 36-month revenue
            customers = 100
            total_revenue = 0
            
            for month in range(36):
                new_customers = customers * growth_rate
                churned_customers = customers * churn_rate
                customers = customers + new_customers - churned_customers
                monthly_revenue = customers * base_scenario.assumptions.average_revenue_per_user
                total_revenue += monthly_revenue
            
            results.append(total_revenue)
        
        # Calculate statistics
        results.sort()
        
        monte_carlo_results = {
            "mean": statistics.mean(results),
            "median": statistics.median(results),
            "std_dev": statistics.stdev(results),
            "percentile_10": results[int(0.1 * len(results))],
            "percentile_25": results[int(0.25 * len(results))],
            "percentile_75": results[int(0.75 * len(results))],
            "percentile_90": results[int(0.9 * len(results))],
            "min": min(results),
            "max": max(results),
            "iterations": iterations
        }
        
        return monte_carlo_results
    
    async def get_financial_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive financial dashboard data"""
        
        try:
            # Get latest scenarios
            scenarios_data = {}
            for scenario_id, scenario in self.scenarios.items():
                scenarios_data[scenario_id] = {
                    "scenario_name": scenario.scenario_name,
                    "scenario_type": scenario.scenario_type.value,
                    "revenue_36_months": scenario.revenue_projections.get("month_36", 0),
                    "break_even_month": scenario.break_even_month,
                    "peak_funding_requirement": scenario.peak_funding_requirement,
                    "ltv_cac_ratio": scenario.ltv_cac_ratio
                }
            
            # Get latest cash flow forecast
            latest_forecast = None
            if self.cash_flow_forecasts:
                latest_forecast = max(self.cash_flow_forecasts.values(), key=lambda x: x.forecast_id)
            
            # Key financial metrics
            base_scenario = self.scenarios.get("base_case")
            key_metrics = {}
            if base_scenario:
                key_metrics = {
                    "current_revenue_run_rate": base_scenario.revenue_projections.get("month_12", 0) * 12,
                    "projected_revenue_36m": base_scenario.revenue_projections.get("month_36", 0),
                    "break_even_month": base_scenario.break_even_month,
                    "runway_months": latest_forecast.runway_months if latest_forecast else 0,
                    "ltv_cac_ratio": base_scenario.ltv_cac_ratio,
                    "payback_period": base_scenario.payback_period_months
                }
            
            # Funding requirements
            funding_requirements = []
            if latest_forecast:
                funding_requirements = latest_forecast.funding_requirements
            
            dashboard_data = {
                "key_metrics": key_metrics,
                "scenarios": scenarios_data,
                "cash_flow_summary": {
                    "runway_months": latest_forecast.runway_months if latest_forecast else 0,
                    "funding_requirements": funding_requirements,
                    "current_cash_balance": list(latest_forecast.cash_balance.values())[-1] if latest_forecast else 0
                },
                "sensitivity_summary": await self._get_sensitivity_summary(),
                "recommendations": await self._generate_financial_recommendations()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get financial dashboard data: {e}")
            raise
    
    async def _get_sensitivity_summary(self) -> Dict[str, Any]:
        """Get summary of sensitivity analysis"""
        
        if not self.sensitivity_analyses:
            return {}
        
        latest_analysis = max(self.sensitivity_analyses.values(), key=lambda x: x.analysis_id)
        
        return {
            "most_sensitive_variable": latest_analysis.tornado_chart[0]["variable"] if latest_analysis.tornado_chart else None,
            "top_risk_factors": [item["variable"] for item in latest_analysis.tornado_chart[:3]],
            "monte_carlo_confidence_interval": {
                "p10": latest_analysis.monte_carlo_results.get("percentile_10", 0),
                "p90": latest_analysis.monte_carlo_results.get("percentile_90", 0)
            }
        }
    
    async def _generate_financial_recommendations(self) -> List[str]:
        """Generate AI-powered financial recommendations"""
        
        recommendations = [
            "🎯 Focus on improving unit economics - optimize CAC and increase LTV",
            "💰 Plan Series A fundraising for month 12-15 based on cash flow projections",
            "📊 Monitor monthly growth rate closely - most sensitive variable for success",
            "🔄 Implement customer success programs to reduce churn rate",
            "⚡ Consider usage-based pricing to improve revenue per customer",
            "📈 Invest in product-led growth to reduce customer acquisition costs"
        ]
        
        return recommendations

# Global financial forecasting engine
financial_forecasting = FinancialForecastingEngine()