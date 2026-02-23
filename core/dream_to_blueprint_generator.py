"""
Dream to Blueprint Generator
Transforms founder dreams into actionable business plans using LLM and MBA frameworks
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

from core.llm_integration import LLMManager, LLMMessage, LLMProvider
from core.mba_business_frameworks import MBABusinessFrameworks, BusinessStage, RevenueModel
from core.company_blueprint_dataclass import CompanyBlueprint, TargetMarket

logger = logging.getLogger(__name__)

@dataclass
class FounderDream:
    """Structured representation of founder's dream/vision"""
    raw_dream: str
    industry_hint: Optional[str] = None
    target_market_hint: Optional[str] = None
    revenue_goal: Optional[float] = None
    timeline_months: Optional[int] = None
    budget_available: Optional[float] = None
    founder_background: Optional[str] = None

@dataclass
class BusinessOpportunityAssessment:
    """Comprehensive business opportunity assessment"""
    opportunity_score: float
    market_size: float
    competition_level: str
    revenue_potential: float
    risk_level: str
    recommended_next_steps: List[str]
    funding_requirements: float
    time_to_revenue: int  # months

class DreamToBlueprintGenerator:
    """
    Transforms founder dreams into actionable business blueprints using:
    - LLM for intelligent parsing and analysis
    - MBA frameworks for structured business planning
    - Y Combinator principles for rapid validation
    - Revenue-focused recommendations
    """
    
    def __init__(self, llm_manager: Optional[LLMManager] = None):
        self.llm_manager = llm_manager or LLMManager()
        self.mba_frameworks = MBABusinessFrameworks()
        
        # Revenue-focused prompts based on YC and top accelerator principles
        self.system_prompts = {
            "dream_parser": """You are a world-class business strategist trained at Harvard Business School, Stanford GSB, and Y Combinator. 
Your expertise includes analyzing founder visions and transforming them into structured business opportunities.

Parse the founder's dream and extract:
1. Core business idea and value proposition
2. Target market and customer segments  
3. Revenue model and monetization strategy
4. Competitive landscape and differentiation
5. Resource requirements and timeline
6. Risk assessment and mitigation strategies

Focus on REVENUE GENERATION and MINIMAL VIABLE PRODUCT approach. 
Think like Paul Graham, Reid Hoffman, and Marc Andreessen.

Respond in JSON format with structured business analysis.""",

            "market_analyzer": """You are a top-tier market research analyst with expertise from McKinsey, BCG, and Bain.
Analyze the business opportunity using proven frameworks:

1. TAM/SAM/SOM analysis (Total/Serviceable/Obtainable Market)
2. Porter's Five Forces competitive analysis
3. Customer development and segmentation
4. Revenue model validation
5. Go-to-market strategy recommendations

Focus on FASTEST PATH TO REVENUE with MINIMAL RESOURCES.
Provide actionable insights for immediate execution.""",

            "financial_modeler": """You are a financial modeling expert from Wharton and Goldman Sachs.
Create realistic financial projections focusing on:

1. Unit economics (CAC, LTV, payback period)
2. Revenue projections (conservative, realistic, optimistic)
3. Cost structure and burn rate
4. Funding requirements and runway
5. Break-even analysis
6. Key financial metrics and KPIs

Prioritize CASH FLOW POSITIVE operations and SUSTAINABLE GROWTH.
Model for 24-month timeline with monthly granularity.""",

            "mvp_strategist": """You are a product strategy expert from Y Combinator and 500 Startups.
Design the Minimum Viable Product (MVP) strategy:

1. Core features vs nice-to-have features
2. Build vs buy vs partner decisions
3. Technology stack recommendations
4. Development timeline and milestones
5. Validation experiments and metrics
6. Launch strategy and early customer acquisition

Focus on SPEED TO MARKET and CUSTOMER VALIDATION.
Recommend the leanest approach to prove product-market fit."""
        }
    
    async def transform_dream_to_blueprint(self, founder_dream: FounderDream) -> CompanyBlueprint:
        """
        Main method: Transform founder's dream into actionable business blueprint
        """
        try:
            logger.info(f"Transforming dream to blueprint: {founder_dream.raw_dream[:100]}...")
            
            # Step 1: Parse and structure the dream using LLM
            structured_analysis = await self._parse_dream_with_llm(founder_dream)
            
            # Step 2: Conduct MBA-framework business analysis
            business_analysis = await self._conduct_business_analysis(structured_analysis)
            
            # Step 3: Generate financial projections
            financial_projections = await self._generate_financial_projections(structured_analysis)
            
            # Step 4: Create MVP strategy
            mvp_strategy = await self._create_mvp_strategy(structured_analysis)
            
            # Step 5: Assess overall opportunity
            opportunity_assessment = self._assess_business_opportunity(
                structured_analysis, business_analysis, financial_projections
            )
            
            # Step 6: Generate actionable blueprint
            blueprint = self._create_company_blueprint(
                founder_dream, structured_analysis, business_analysis, 
                financial_projections, mvp_strategy, opportunity_assessment
            )
            
            logger.info(f"Successfully generated blueprint for: {blueprint.name}")
            return blueprint
            
        except Exception as e:
            logger.error(f"Failed to transform dream to blueprint: {e}")
            raise
    
    async def _parse_dream_with_llm(self, founder_dream: FounderDream) -> Dict[str, Any]:
        """Parse founder's dream using LLM with business strategy expertise"""
        
        messages = [
            LLMMessage(role="system", content=self.system_prompts["dream_parser"]),
            LLMMessage(role="user", content=f"""
Analyze this founder's dream and business idea:

FOUNDER'S DREAM: {founder_dream.raw_dream}

ADDITIONAL CONTEXT:
- Industry hint: {founder_dream.industry_hint or 'Not specified'}
- Target market hint: {founder_dream.target_market_hint or 'Not specified'}
- Revenue goal: ${founder_dream.revenue_goal or 'Not specified'}
- Timeline: {founder_dream.timeline_months or 'Not specified'} months
- Available budget: ${founder_dream.budget_available or 'Not specified'}
- Founder background: {founder_dream.founder_background or 'Not specified'}

Provide structured analysis in JSON format focusing on:
1. Business idea clarity and viability
2. Market opportunity and size
3. Revenue model recommendations
4. Competitive differentiation
5. Resource requirements
6. Risk assessment
7. Recommended next steps

Focus on FASTEST PATH TO REVENUE with MINIMAL RESOURCES.
""")
        ]
        
        try:
            response = await self.llm_manager.generate_response(messages)
            
            # Parse JSON response
            analysis = json.loads(response.content)
            analysis["llm_confidence"] = response.confidence
            analysis["analysis_timestamp"] = datetime.now(timezone.utc).isoformat()
            
            return analysis
            
        except json.JSONDecodeError:
            logger.warning("LLM response was not valid JSON, using fallback analysis")
            return self._fallback_dream_analysis(founder_dream)
        except Exception as e:
            logger.error(f"LLM dream parsing failed: {e}")
            return self._fallback_dream_analysis(founder_dream)
    
    async def _conduct_business_analysis(self, structured_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive business analysis using MBA frameworks"""
        
        business_idea = structured_analysis.get("business_idea", "")
        industry = structured_analysis.get("industry", "saas")
        target_market = structured_analysis.get("target_market", "small_businesses")
        
        # Use MBA frameworks for comprehensive analysis
        mba_analysis = self.mba_frameworks.analyze_business_opportunity(
            business_idea, industry, target_market
        )
        
        # Enhance with LLM-powered market analysis
        market_analysis = await self._llm_market_analysis(business_idea, industry)
        
        # Combine MBA frameworks with LLM insights
        combined_analysis = {
            **mba_analysis,
            "llm_market_insights": market_analysis,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return combined_analysis
    
    async def _llm_market_analysis(self, business_idea: str, industry: str) -> Dict[str, Any]:
        """Enhanced market analysis using LLM"""
        
        messages = [
            LLMMessage(role="system", content=self.system_prompts["market_analyzer"]),
            LLMMessage(role="user", content=f"""
Conduct comprehensive market analysis for:

BUSINESS IDEA: {business_idea}
INDUSTRY: {industry}

Provide analysis covering:
1. Market size and growth potential
2. Competitive landscape and key players
3. Customer segments and pain points
4. Market trends and opportunities
5. Barriers to entry and risks
6. Go-to-market strategy recommendations

Focus on actionable insights for RAPID MARKET ENTRY and REVENUE GENERATION.
Respond in JSON format.
""")
        ]
        
        try:
            response = await self.llm_manager.generate_response(messages)
            return json.loads(response.content)
        except Exception as e:
            logger.error(f"LLM market analysis failed: {e}")
            return {"error": "Market analysis unavailable", "fallback": True}
    
    async def _generate_financial_projections(self, structured_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed financial projections using LLM and MBA frameworks"""
        
        business_idea = structured_analysis.get("business_idea", "")
        revenue_model = structured_analysis.get("revenue_model", "subscription")
        target_market = structured_analysis.get("target_market", "")
        
        messages = [
            LLMMessage(role="system", content=self.system_prompts["financial_modeler"]),
            LLMMessage(role="user", content=f"""
Create detailed financial projections for:

BUSINESS IDEA: {business_idea}
REVENUE MODEL: {revenue_model}
TARGET MARKET: {target_market}

Generate 24-month financial model including:
1. Monthly revenue projections (conservative, realistic, optimistic scenarios)
2. Unit economics (CAC, LTV, payback period, churn rate)
3. Cost structure breakdown
4. Cash flow analysis
5. Funding requirements and runway
6. Break-even analysis
7. Key financial KPIs

Focus on REALISTIC projections that lead to PROFITABILITY.
Respond in JSON format with monthly granularity.
""")
        ]
        
        try:
            response = await self.llm_manager.generate_response(messages)
            llm_projections = json.loads(response.content)
            
            # Enhance with MBA framework financial modeling
            mba_projections = self.mba_frameworks._wharton_financial_modeling(business_idea, "saas")
            
            # Combine LLM and MBA projections
            combined_projections = {
                "llm_projections": llm_projections,
                "mba_projections": asdict(mba_projections),
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            return combined_projections
            
        except Exception as e:
            logger.error(f"Financial projections failed: {e}")
            # Fallback to MBA framework only
            mba_projections = self.mba_frameworks._wharton_financial_modeling(business_idea, "saas")
            return {"mba_projections": asdict(mba_projections), "fallback": True}
    
    async def _create_mvp_strategy(self, structured_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create MVP strategy using Y Combinator principles"""
        
        business_idea = structured_analysis.get("business_idea", "")
        
        messages = [
            LLMMessage(role="system", content=self.system_prompts["mvp_strategist"]),
            LLMMessage(role="user", content=f"""
Design MVP strategy for:

BUSINESS IDEA: {business_idea}

Create comprehensive MVP plan including:
1. Core features (must-have for launch)
2. Nice-to-have features (post-launch)
3. Technology stack recommendations
4. Development timeline and milestones
5. Validation experiments and success metrics
6. Launch strategy and early customer acquisition
7. Resource requirements (team, budget, time)

Focus on SPEED TO MARKET and CUSTOMER VALIDATION.
Follow Y Combinator's "build something people want" philosophy.
Respond in JSON format.
""")
        ]
        
        try:
            response = await self.llm_manager.generate_response(messages)
            llm_mvp = json.loads(response.content)
            
            # Enhance with MBA framework MVP recommendations
            mba_mvp = self.mba_frameworks._ycombinator_mvp_framework(business_idea)
            
            # Combine strategies
            combined_mvp = {
                "llm_strategy": llm_mvp,
                "mba_strategy": mba_mvp,
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            return combined_mvp
            
        except Exception as e:
            logger.error(f"MVP strategy creation failed: {e}")
            # Fallback to MBA framework only
            mba_mvp = self.mba_frameworks._ycombinator_mvp_framework(business_idea)
            return {"mba_strategy": mba_mvp, "fallback": True}
    
    def _assess_business_opportunity(self, structured_analysis: Dict[str, Any], 
                                   business_analysis: Dict[str, Any],
                                   financial_projections: Dict[str, Any]) -> BusinessOpportunityAssessment:
        """Assess overall business opportunity and provide recommendations"""
        
        # Calculate opportunity score from MBA frameworks
        opportunity_score = business_analysis.get("opportunity_score", 50)
        
        # Extract key metrics
        market_analysis = business_analysis.get("market_analysis")
        financial = financial_projections.get("mba_projections", {})
        
        market_size = market_analysis.serviceable_obtainable_market if market_analysis else 10000000
        revenue_potential = financial.get("revenue_projections", {}).get("month_12", 100000)
        funding_requirements = financial.get("funding_requirements", 500000)
        
        # Determine competition level
        competitors = business_analysis.get("market_analysis")
        competition_level = "medium"  # Default
        if competitors and len(competitors.competitive_landscape) > 5:
            competition_level = "high"
        elif competitors and len(competitors.competitive_landscape) < 3:
            competition_level = "low"
        
        # Determine risk level
        risk_level = "medium"  # Default
        if opportunity_score > 75:
            risk_level = "low"
        elif opportunity_score < 40:
            risk_level = "high"
        
        # Generate recommendations
        recommendations = self._generate_opportunity_recommendations(
            opportunity_score, market_size, competition_level, risk_level
        )
        
        return BusinessOpportunityAssessment(
            opportunity_score=opportunity_score,
            market_size=market_size,
            competition_level=competition_level,
            revenue_potential=revenue_potential,
            risk_level=risk_level,
            recommended_next_steps=recommendations,
            funding_requirements=funding_requirements,
            time_to_revenue=6  # Default 6 months
        )
    
    def _generate_opportunity_recommendations(self, opportunity_score: float, 
                                            market_size: float, competition_level: str,
                                            risk_level: str) -> List[str]:
        """Generate specific recommendations based on opportunity assessment"""
        
        recommendations = []
        
        if opportunity_score > 75:
            recommendations.extend([
                "🚀 HIGH OPPORTUNITY: Proceed with full development",
                "💰 Secure seed funding immediately",
                "👥 Build core team and advisory board",
                "📈 Focus on rapid customer acquisition"
            ])
        elif opportunity_score > 50:
            recommendations.extend([
                "✅ MODERATE OPPORTUNITY: Validate with MVP",
                "🔍 Conduct customer interviews and market research",
                "💡 Refine value proposition and pricing",
                "🎯 Focus on specific customer segment"
            ])
        else:
            recommendations.extend([
                "⚠️ LOW OPPORTUNITY: Pivot or iterate significantly",
                "🔄 Reconsider business model and target market",
                "📊 Conduct extensive market validation",
                "💭 Explore alternative approaches"
            ])
        
        if market_size > 100000000:  # $100M+ market
            recommendations.append("🎯 Large market opportunity - scale aggressively")
        elif market_size < 10000000:  # <$10M market
            recommendations.append("📏 Small market - focus on niche dominance")
        
        if competition_level == "high":
            recommendations.append("⚔️ High competition - differentiate strongly")
        elif competition_level == "low":
            recommendations.append("🏃‍♂️ Low competition - move fast to establish market position")
        
        if risk_level == "high":
            recommendations.append("🛡️ High risk - implement strong risk mitigation strategies")
        
        return recommendations
    
    def _create_company_blueprint(self, founder_dream: FounderDream,
                                structured_analysis: Dict[str, Any],
                                business_analysis: Dict[str, Any],
                                financial_projections: Dict[str, Any],
                                mvp_strategy: Dict[str, Any],
                                opportunity_assessment: BusinessOpportunityAssessment) -> CompanyBlueprint:
        """Create final company blueprint combining all analyses"""
        
        # Extract core information
        business_name = structured_analysis.get("business_name", "New Venture")
        industry = structured_analysis.get("industry", "Technology")
        vision = structured_analysis.get("vision", founder_dream.raw_dream)
        mission = structured_analysis.get("mission", "Creating value for customers")
        
        # Create target market
        target_market = TargetMarket(
            primary_segment=structured_analysis.get("target_market", "Small businesses"),
            demographics=structured_analysis.get("demographics", ["Age 25-45", "Tech-savvy"]),
            psychographics=structured_analysis.get("psychographics", ["Innovation-focused", "Growth-oriented"]),
            size_estimate=int(opportunity_assessment.market_size),
            pain_points=structured_analysis.get("pain_points", ["Efficiency", "Cost reduction"])
        )
        
        # Extract key features from MVP strategy
        mvp_features = mvp_strategy.get("mba_strategy", {}).get("core_features", [])
        if not mvp_features:
            mvp_features = mvp_strategy.get("llm_strategy", {}).get("core_features", [])
        
        # Create comprehensive blueprint
        blueprint = CompanyBlueprint(
            name=business_name,
            industry=industry,
            vision=vision,
            mission=mission,
            target_market=target_market,
            key_features=mvp_features or ["Core functionality", "User dashboard", "Analytics"],
            
            # Enhanced fields for comprehensive business planning
            business_model=structured_analysis.get("revenue_model", "subscription"),
            value_proposition=structured_analysis.get("value_proposition", "Solving customer problems efficiently"),
            competitive_advantages=structured_analysis.get("competitive_advantages", ["Innovation", "Speed"]),
            revenue_projections=financial_projections.get("mba_projections", {}).get("revenue_projections", {}),
            funding_requirements=opportunity_assessment.funding_requirements,
            team_requirements=mvp_strategy.get("mba_strategy", {}).get("resource_requirements", {}),
            
            # Opportunity assessment
            opportunity_score=opportunity_assessment.opportunity_score,
            risk_level=opportunity_assessment.risk_level,
            recommended_next_steps=opportunity_assessment.recommended_next_steps,
            time_to_revenue_months=opportunity_assessment.time_to_revenue,
            
            # Metadata
            created_at=datetime.now(timezone.utc).isoformat(),
            founder_dream=founder_dream.raw_dream,
            analysis_confidence=structured_analysis.get("llm_confidence", 0.8)
        )
        
        return blueprint
    
    def _fallback_dream_analysis(self, founder_dream: FounderDream) -> Dict[str, Any]:
        """Fallback analysis when LLM is unavailable"""
        
        return {
            "business_idea": founder_dream.raw_dream,
            "business_name": "New Venture",
            "industry": founder_dream.industry_hint or "technology",
            "target_market": founder_dream.target_market_hint or "small_businesses",
            "revenue_model": "subscription",
            "vision": founder_dream.raw_dream,
            "mission": "Creating value for customers",
            "value_proposition": "Solving important problems",
            "competitive_advantages": ["Innovation", "Customer focus"],
            "pain_points": ["Efficiency", "Cost reduction"],
            "demographics": ["Business owners", "Professionals"],
            "psychographics": ["Growth-oriented", "Tech-savvy"],
            "llm_confidence": 0.5,
            "fallback": True,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global dream to blueprint generator
dream_generator = DreamToBlueprintGenerator()