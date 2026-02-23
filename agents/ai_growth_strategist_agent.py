"""
AI Growth Strategist Agent
Strategic growth planning, market analysis, and expansion optimization
Provides data-driven growth strategies and competitive intelligence
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from core.enhanced_base_agent import EnhancedBaseAgent
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

@dataclass
class GrowthStrategy:
    """Growth strategy analysis and recommendations"""
    strategy_id: str
    strategy_name: str
    strategy_type: str  # market_expansion, product_development, customer_acquisition
    
    # Strategy details
    target_market: str
    growth_potential: float  # 0-10
    implementation_complexity: float  # 0-10
    resource_requirements: Dict[str, Any]
    
    # Projections
    projected_revenue_impact: float
    projected_timeline: int  # months
    success_probability: float  # 0-1
    
    # Analysis
    strengths: List[str]
    challenges: List[str]
    key_metrics: List[str]
    milestones: List[Dict[str, Any]]
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class MarketAnalysis:
    """Market analysis and competitive intelligence"""
    analysis_id: str
    market_segment: str
    analysis_date: str
    
    # Market metrics
    market_size: float
    growth_rate: float
    competition_level: str  # low, medium, high
    
    # Opportunities and threats
    opportunities: List[str]
    threats: List[str]
    market_trends: List[str]
    
    # Competitive landscape
    key_competitors: List[Dict[str, Any]]
    competitive_advantages: List[str]
    market_positioning: str
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AIGrowthStrategistAgent(EnhancedBaseAgent):
    """
    AI Growth Strategist Agent that provides:
    - Strategic growth planning and analysis
    - Market opportunity identification
    - Competitive intelligence and positioning
    - Growth experiment design and optimization
    - Revenue forecasting and modeling
    - Expansion strategy development
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ai_growth_strategist",
            name="AI Growth Strategist",
            description="Strategic growth planning and market analysis automation",
            capabilities=[
                "growth_strategy_development",
                "market_analysis",
                "competitive_intelligence",
                "revenue_optimization",
                "expansion_planning",
                "growth_experimentation"
            ]
        )
        
        # Growth strategies and market analyses
        self.growth_strategies: Dict[str, GrowthStrategy] = {}
        self.market_analyses: Dict[str, MarketAnalysis] = {}
        
        # Growth frameworks and methodologies
        self.growth_frameworks = {
            "pirate_metrics": {
                "name": "AARRR (Pirate Metrics)",
                "stages": ["Acquisition", "Activation", "Retention", "Referral", "Revenue"],
                "focus": "Customer lifecycle optimization"
            },
            "north_star": {
                "name": "North Star Framework",
                "components": ["North Star Metric", "Input Metrics", "Contextual Metrics"],
                "focus": "Single metric alignment"
            },
            "ice_scoring": {
                "name": "ICE Scoring",
                "criteria": ["Impact", "Confidence", "Ease"],
                "focus": "Growth experiment prioritization"
            }
        }
        
        # Market data and benchmarks
        self._initialize_market_data()
    
    def _initialize_market_data(self):
        """Initialize market data and competitive intelligence"""
        
        # Sample market segments
        self.market_segments = {
            "saas_b2b": {
                "size": 250000000000,  # $250B
                "growth_rate": 0.18,
                "competition": "high",
                "key_trends": [
                    "AI/ML integration",
                    "Remote work solutions",
                    "API-first architecture",
                    "No-code/low-code platforms"
                ]
            },
            "fintech": {
                "size": 180000000000,  # $180B
                "growth_rate": 0.25,
                "competition": "high",
                "key_trends": [
                    "Digital banking",
                    "Cryptocurrency adoption",
                    "Embedded finance",
                    "RegTech solutions"
                ]
            },
            "healthtech": {
                "size": 120000000000,  # $120B
                "growth_rate": 0.22,
                "competition": "medium",
                "key_trends": [
                    "Telemedicine",
                    "AI diagnostics",
                    "Wearable health tech",
                    "Mental health platforms"
                ]
            }
        }
        
        # Competitive landscape
        self.competitive_landscape = {
            "direct_competitors": [
                {
                    "name": "Competitor A",
                    "market_share": 0.15,
                    "strengths": ["Brand recognition", "Enterprise sales"],
                    "weaknesses": ["Legacy technology", "Slow innovation"]
                },
                {
                    "name": "Competitor B", 
                    "market_share": 0.12,
                    "strengths": ["Product features", "Customer support"],
                    "weaknesses": ["Limited integrations", "High pricing"]
                }
            ],
            "indirect_competitors": [
                {
                    "name": "Alternative Solution C",
                    "threat_level": "medium",
                    "differentiation": "Different approach to same problem"
                }
            ]
        }
    
    async def develop_growth_strategy(self, strategy_type: str, target_market: str, 
                                   current_metrics: Dict[str, Any]) -> GrowthStrategy:
        """Develop comprehensive growth strategy based on type and market"""
        
        try:
            logger.info(f"Developing growth strategy: {strategy_type} for {target_market}")
            
            strategy_id = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze market opportunity
            market_data = self.market_segments.get(target_market, {})
            
            # Calculate growth potential
            growth_potential = self._calculate_growth_potential(strategy_type, target_market, current_metrics)
            
            # Assess implementation complexity
            complexity = self._assess_implementation_complexity(strategy_type, current_metrics)
            
            # Generate strategy recommendations
            strategy_details = await self._generate_strategy_details(strategy_type, target_market, current_metrics)
            
            # Create growth strategy
            strategy = GrowthStrategy(
                strategy_id=strategy_id,
                strategy_name=strategy_details["name"],
                strategy_type=strategy_type,
                target_market=target_market,
                growth_potential=growth_potential,
                implementation_complexity=complexity,
                resource_requirements=strategy_details["resources"],
                projected_revenue_impact=strategy_details["revenue_impact"],
                projected_timeline=strategy_details["timeline"],
                success_probability=strategy_details["success_probability"],
                strengths=strategy_details["strengths"],
                challenges=strategy_details["challenges"],
                key_metrics=strategy_details["key_metrics"],
                milestones=strategy_details["milestones"]
            )
            
            # Store strategy
            self.growth_strategies[strategy_id] = strategy
            
            logger.info(f"Growth strategy developed: {strategy.strategy_name}")
            return strategy
            
        except Exception as e:
            logger.error(f"Failed to develop growth strategy: {e}")
            raise
    
    def _calculate_growth_potential(self, strategy_type: str, target_market: str, 
                                  current_metrics: Dict[str, Any]) -> float:
        """Calculate growth potential score (0-10)"""
        
        base_score = 5.0
        
        # Market size factor
        market_data = self.market_segments.get(target_market, {})
        if market_data.get("size", 0) > 100000000000:  # >$100B market
            base_score += 1.5
        elif market_data.get("size", 0) > 10000000000:  # >$10B market
            base_score += 1.0
        
        # Market growth rate factor
        growth_rate = market_data.get("growth_rate", 0)
        if growth_rate > 0.2:  # >20% growth
            base_score += 1.5
        elif growth_rate > 0.1:  # >10% growth
            base_score += 1.0
        
        # Competition level factor
        competition = market_data.get("competition", "medium")
        if competition == "low":
            base_score += 1.0
        elif competition == "high":
            base_score -= 0.5
        
        # Strategy type factor
        if strategy_type == "market_expansion":
            base_score += 0.5  # Generally lower risk
        elif strategy_type == "product_development":
            base_score += 1.0  # High potential if executed well
        
        # Current performance factor
        current_revenue = current_metrics.get("monthly_revenue", 0)
        if current_revenue > 100000:  # Strong foundation
            base_score += 0.5
        
        return min(base_score, 10.0)
    
    def _assess_implementation_complexity(self, strategy_type: str, 
                                        current_metrics: Dict[str, Any]) -> float:
        """Assess implementation complexity (0-10, higher = more complex)"""
        
        base_complexity = 5.0
        
        # Strategy type complexity
        complexity_map = {
            "customer_acquisition": 3.0,
            "market_expansion": 6.0,
            "product_development": 8.0,
            "vertical_expansion": 7.0,
            "geographic_expansion": 9.0
        }
        
        base_complexity = complexity_map.get(strategy_type, 5.0)
        
        # Resource availability factor
        team_size = current_metrics.get("team_size", 10)
        if team_size < 5:
            base_complexity += 1.0
        elif team_size > 20:
            base_complexity -= 0.5
        
        # Current revenue factor (more resources = lower complexity)
        current_revenue = current_metrics.get("monthly_revenue", 0)
        if current_revenue < 50000:
            base_complexity += 1.0
        elif current_revenue > 500000:
            base_complexity -= 1.0
        
        return min(base_complexity, 10.0)
    
    async def _generate_strategy_details(self, strategy_type: str, target_market: str, 
                                       current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed strategy recommendations"""
        
        if strategy_type == "customer_acquisition":
            return {
                "name": "Customer Acquisition Optimization",
                "resources": {
                    "budget": 50000,
                    "team_members": 3,
                    "timeline": "3-6 months",
                    "tools": ["Marketing automation", "Analytics platform", "CRM system"]
                },
                "revenue_impact": current_metrics.get("monthly_revenue", 100000) * 0.3,
                "timeline": 4,
                "success_probability": 0.75,
                "strengths": [
                    "Leverages existing product-market fit",
                    "Scalable through digital channels",
                    "Measurable ROI and quick feedback loops"
                ],
                "challenges": [
                    "Increasing customer acquisition costs",
                    "Market saturation in some channels",
                    "Need for continuous optimization"
                ],
                "key_metrics": [
                    "Customer Acquisition Cost (CAC)",
                    "Lifetime Value (LTV)",
                    "Conversion rates by channel",
                    "Monthly Recurring Revenue (MRR)"
                ],
                "milestones": [
                    {"month": 1, "goal": "Channel analysis and strategy finalization"},
                    {"month": 2, "goal": "Campaign launch and initial optimization"},
                    {"month": 3, "goal": "Performance evaluation and scaling"},
                    {"month": 4, "goal": "Full implementation and ROI assessment"}
                ]
            }
        
        elif strategy_type == "market_expansion":
            return {
                "name": "Adjacent Market Expansion",
                "resources": {
                    "budget": 150000,
                    "team_members": 5,
                    "timeline": "6-12 months",
                    "tools": ["Market research", "Product adaptation", "Sales enablement"]
                },
                "revenue_impact": current_metrics.get("monthly_revenue", 100000) * 0.5,
                "timeline": 8,
                "success_probability": 0.65,
                "strengths": [
                    "Leverages existing capabilities",
                    "Diversifies revenue streams",
                    "Potential for significant growth"
                ],
                "challenges": [
                    "Market education requirements",
                    "Different customer needs and behaviors",
                    "Competitive landscape variations"
                ],
                "key_metrics": [
                    "Market penetration rate",
                    "Revenue from new market",
                    "Customer acquisition in new segment",
                    "Product-market fit indicators"
                ],
                "milestones": [
                    {"month": 2, "goal": "Market research and validation"},
                    {"month": 4, "goal": "Product/service adaptation"},
                    {"month": 6, "goal": "Pilot launch and testing"},
                    {"month": 8, "goal": "Full market entry and scaling"}
                ]
            }
        
        elif strategy_type == "product_development":
            return {
                "name": "New Product Development",
                "resources": {
                    "budget": 300000,
                    "team_members": 8,
                    "timeline": "9-18 months",
                    "tools": ["Development platform", "User research", "Testing infrastructure"]
                },
                "revenue_impact": current_metrics.get("monthly_revenue", 100000) * 0.8,
                "timeline": 12,
                "success_probability": 0.55,
                "strengths": [
                    "Addresses unmet customer needs",
                    "Potential for market leadership",
                    "Higher margins on innovative products"
                ],
                "challenges": [
                    "High development costs and risks",
                    "Uncertain market reception",
                    "Long time to market and ROI"
                ],
                "key_metrics": [
                    "Product development milestones",
                    "User adoption and engagement",
                    "Revenue per new product",
                    "Market share in new category"
                ],
                "milestones": [
                    {"month": 3, "goal": "Product specification and design"},
                    {"month": 6, "goal": "MVP development and testing"},
                    {"month": 9, "goal": "Beta launch and user feedback"},
                    {"month": 12, "goal": "Full product launch and marketing"}
                ]
            }
        
        else:
            # Default strategy template
            return {
                "name": f"{strategy_type.replace('_', ' ').title()} Strategy",
                "resources": {"budget": 100000, "team_members": 4, "timeline": "6 months"},
                "revenue_impact": current_metrics.get("monthly_revenue", 100000) * 0.4,
                "timeline": 6,
                "success_probability": 0.7,
                "strengths": ["Strategic opportunity", "Market potential"],
                "challenges": ["Implementation complexity", "Resource requirements"],
                "key_metrics": ["Revenue growth", "Market share", "Customer satisfaction"],
                "milestones": [
                    {"month": 2, "goal": "Strategy implementation"},
                    {"month": 4, "goal": "Initial results evaluation"},
                    {"month": 6, "goal": "Full strategy execution"}
                ]
            }
    
    async def analyze_market_opportunity(self, market_segment: str) -> MarketAnalysis:
        """Analyze market opportunity and competitive landscape"""
        
        try:
            logger.info(f"Analyzing market opportunity: {market_segment}")
            
            analysis_id = f"market_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get market data
            market_data = self.market_segments.get(market_segment, {})
            
            # Analyze competitive landscape
            competitive_analysis = self._analyze_competitive_landscape(market_segment)
            
            # Identify opportunities and threats
            opportunities, threats = self._identify_market_dynamics(market_segment, market_data)
            
            # Create market analysis
            analysis = MarketAnalysis(
                analysis_id=analysis_id,
                market_segment=market_segment,
                analysis_date=datetime.now(timezone.utc).isoformat(),
                market_size=market_data.get("size", 0),
                growth_rate=market_data.get("growth_rate", 0),
                competition_level=market_data.get("competition", "medium"),
                opportunities=opportunities,
                threats=threats,
                market_trends=market_data.get("key_trends", []),
                key_competitors=competitive_analysis["competitors"],
                competitive_advantages=competitive_analysis["advantages"],
                market_positioning=competitive_analysis["positioning"]
            )
            
            # Store analysis
            self.market_analyses[analysis_id] = analysis
            
            logger.info(f"Market analysis completed: {market_segment}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze market opportunity: {e}")
            raise
    
    def _analyze_competitive_landscape(self, market_segment: str) -> Dict[str, Any]:
        """Analyze competitive landscape for market segment"""
        
        # Get relevant competitors
        competitors = []
        for competitor in self.competitive_landscape["direct_competitors"]:
            competitors.append({
                "name": competitor["name"],
                "market_share": competitor["market_share"],
                "strengths": competitor["strengths"],
                "weaknesses": competitor["weaknesses"],
                "threat_level": "high" if competitor["market_share"] > 0.1 else "medium"
            })
        
        # Identify competitive advantages
        advantages = [
            "Innovative technology stack",
            "Superior user experience",
            "Faster time to market",
            "Better customer support",
            "More flexible pricing"
        ]
        
        # Determine market positioning
        positioning = "Challenger with differentiated offering"
        
        return {
            "competitors": competitors,
            "advantages": advantages,
            "positioning": positioning
        }
    
    def _identify_market_dynamics(self, market_segment: str, 
                                market_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Identify market opportunities and threats"""
        
        opportunities = []
        threats = []
        
        # Growth rate opportunities
        if market_data.get("growth_rate", 0) > 0.15:
            opportunities.append("High market growth rate creates expansion opportunities")
        
        # Market size opportunities
        if market_data.get("size", 0) > 50000000000:  # >$50B
            opportunities.append("Large addressable market with significant revenue potential")
        
        # Technology trends
        trends = market_data.get("key_trends", [])
        if "AI/ML integration" in trends:
            opportunities.append("AI/ML trend creates product differentiation opportunities")
        if "Remote work solutions" in trends:
            opportunities.append("Remote work trend drives demand for digital solutions")
        
        # Competition threats
        competition_level = market_data.get("competition", "medium")
        if competition_level == "high":
            threats.append("Intense competition may pressure margins and market share")
        
        # Market maturity threats
        if market_data.get("growth_rate", 0) < 0.05:
            threats.append("Slow market growth limits expansion opportunities")
        
        # Regulatory threats
        if market_segment in ["fintech", "healthtech"]:
            threats.append("Regulatory changes may impact market dynamics")
        
        return opportunities, threats
    
    async def optimize_growth_experiments(self, experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize growth experiments using ICE scoring framework"""
        
        try:
            logger.info("Optimizing growth experiments")
            
            scored_experiments = []
            
            for experiment in experiments:
                # Calculate ICE score
                impact = experiment.get("impact", 5)  # 1-10
                confidence = experiment.get("confidence", 5)  # 1-10
                ease = experiment.get("ease", 5)  # 1-10
                
                ice_score = (impact + confidence + ease) / 3
                
                scored_experiment = {
                    **experiment,
                    "ice_score": round(ice_score, 2),
                    "priority": self._determine_priority(ice_score),
                    "recommended_timeline": self._recommend_timeline(impact, ease),
                    "resource_allocation": self._recommend_resources(impact, ease)
                }
                
                scored_experiments.append(scored_experiment)
            
            # Sort by ICE score
            scored_experiments.sort(key=lambda x: x["ice_score"], reverse=True)
            
            # Generate optimization recommendations
            optimization_result = {
                "total_experiments": len(experiments),
                "prioritized_experiments": scored_experiments,
                "high_priority_count": len([e for e in scored_experiments if e["priority"] == "high"]),
                "recommendations": self._generate_experiment_recommendations(scored_experiments),
                "resource_plan": self._create_resource_plan(scored_experiments[:5]),  # Top 5
                "success_metrics": [
                    "Experiment completion rate",
                    "Statistical significance achieved",
                    "Positive impact on key metrics",
                    "Learning velocity"
                ]
            }
            
            logger.info("Growth experiment optimization completed")
            return optimization_result
            
        except Exception as e:
            logger.error(f"Failed to optimize growth experiments: {e}")
            raise
    
    def _determine_priority(self, ice_score: float) -> str:
        """Determine experiment priority based on ICE score"""
        if ice_score >= 8.0:
            return "high"
        elif ice_score >= 6.0:
            return "medium"
        else:
            return "low"
    
    def _recommend_timeline(self, impact: int, ease: int) -> str:
        """Recommend timeline based on impact and ease"""
        if ease >= 8:
            return "1-2 weeks"
        elif ease >= 6:
            return "2-4 weeks"
        elif impact >= 8:
            return "4-8 weeks"
        else:
            return "8-12 weeks"
    
    def _recommend_resources(self, impact: int, ease: int) -> Dict[str, Any]:
        """Recommend resource allocation"""
        if impact >= 8 and ease >= 6:
            return {"team_size": 3, "budget": 10000, "priority": "high"}
        elif impact >= 6:
            return {"team_size": 2, "budget": 5000, "priority": "medium"}
        else:
            return {"team_size": 1, "budget": 2000, "priority": "low"}
    
    def _generate_experiment_recommendations(self, experiments: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations for experiment portfolio"""
        
        recommendations = []
        
        high_priority = [e for e in experiments if e["priority"] == "high"]
        if len(high_priority) > 5:
            recommendations.append("Focus on top 5 high-priority experiments to avoid resource dilution")
        
        quick_wins = [e for e in experiments if e["recommended_timeline"] == "1-2 weeks"]
        if quick_wins:
            recommendations.append(f"Prioritize {len(quick_wins)} quick-win experiments for immediate impact")
        
        high_impact = [e for e in experiments if e.get("impact", 0) >= 8]
        if high_impact:
            recommendations.append(f"Allocate additional resources to {len(high_impact)} high-impact experiments")
        
        return recommendations
    
    def _create_resource_plan(self, top_experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create resource allocation plan for top experiments"""
        
        total_budget = sum(e["resource_allocation"]["budget"] for e in top_experiments)
        total_team_size = sum(e["resource_allocation"]["team_size"] for e in top_experiments)
        
        return {
            "total_budget_required": total_budget,
            "total_team_members": total_team_size,
            "timeline": "4-8 weeks for full portfolio",
            "resource_distribution": [
                {
                    "experiment": exp["name"],
                    "budget": exp["resource_allocation"]["budget"],
                    "team_size": exp["resource_allocation"]["team_size"],
                    "timeline": exp["recommended_timeline"]
                }
                for exp in top_experiments
            ]
        }
    
    async def get_growth_insights(self) -> Dict[str, Any]:
        """Get comprehensive growth insights and recommendations"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Analyze growth strategies
            active_strategies = [s for s in self.growth_strategies.values()]
            recent_analyses = [a for a in self.market_analyses.values() 
                             if (current_time - datetime.fromisoformat(a.created_at.replace('Z', '+00:00'))).days <= 30]
            
            # Calculate growth metrics
            avg_growth_potential = sum(s.growth_potential for s in active_strategies) / max(len(active_strategies), 1)
            avg_success_probability = sum(s.success_probability for s in active_strategies) / max(len(active_strategies), 1)
            
            growth_insights = {
                "growth_health_score": 0.0,
                "strategy_portfolio": {
                    "total_strategies": len(active_strategies),
                    "average_growth_potential": round(avg_growth_potential, 1),
                    "average_success_probability": round(avg_success_probability * 100, 1),
                    "high_potential_strategies": len([s for s in active_strategies if s.growth_potential >= 7.0])
                },
                "market_intelligence": {
                    "markets_analyzed": len(recent_analyses),
                    "total_addressable_market": sum(a.market_size for a in recent_analyses),
                    "average_market_growth": round(sum(a.growth_rate for a in recent_analyses) / max(len(recent_analyses), 1) * 100, 1)
                },
                "key_insights": [],
                "strategic_recommendations": [],
                "growth_opportunities": [],
                "risk_factors": []
            }
            
            # Calculate growth health score
            strategy_score = min(avg_growth_potential / 10 * 40, 40)
            execution_score = min(avg_success_probability * 30, 30)
            market_score = min(len(recent_analyses) / 3 * 30, 30)  # 3 markets analyzed = full score
            
            growth_insights["growth_health_score"] = round(strategy_score + execution_score + market_score, 1)
            
            # Generate key insights
            if avg_growth_potential >= 7.0:
                growth_insights["key_insights"].append("🚀 High-potential growth strategies identified")
                growth_insights["strategic_recommendations"].append("Accelerate execution of high-potential strategies")
            
            if avg_success_probability >= 0.7:
                growth_insights["key_insights"].append("💪 Strong confidence in strategy execution")
            else:
                growth_insights["key_insights"].append("⚠️ Strategy execution confidence needs improvement")
                growth_insights["strategic_recommendations"].append("Reduce strategy complexity and improve execution capabilities")
            
            # Market opportunities
            for analysis in recent_analyses:
                if analysis.growth_rate > 0.15:
                    growth_insights["growth_opportunities"].append(f"{analysis.market_segment} market growing at {analysis.growth_rate*100:.1f}%")
            
            # Risk factors
            high_complexity_strategies = [s for s in active_strategies if s.implementation_complexity >= 7.0]
            if high_complexity_strategies:
                growth_insights["risk_factors"].append(f"{len(high_complexity_strategies)} strategies have high implementation complexity")
            
            # Strategic recommendations
            if growth_insights["growth_health_score"] >= 80:
                growth_insights["strategic_recommendations"].extend([
                    "Growth strategy portfolio is strong - focus on execution",
                    "Consider expanding into additional high-growth markets",
                    "Develop advanced growth experimentation capabilities"
                ])
            elif growth_insights["growth_health_score"] >= 60:
                growth_insights["strategic_recommendations"].extend([
                    "Strengthen growth strategy development process",
                    "Improve market analysis and competitive intelligence",
                    "Focus on higher-probability growth initiatives"
                ])
            else:
                growth_insights["strategic_recommendations"].extend([
                    "Conduct comprehensive growth strategy review",
                    "Invest in market research and competitive analysis",
                    "Simplify growth initiatives for better execution"
                ])
            
            return growth_insights
            
        except Exception as e:
            logger.error(f"Failed to get growth insights: {e}")
            raise

# Global AI growth strategist agent
ai_growth_strategist = AIGrowthStrategistAgent()