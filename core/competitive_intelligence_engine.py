"""
Competitive Intelligence Engine
Automated competitor tracking, market analysis, and strategic recommendations
Provides real-time competitive insights and strategic positioning analysis
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class CompetitorTier(Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    SUBSTITUTE = "substitute"
    EMERGING = "emerging"

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CompetitiveAdvantage(Enum):
    PRODUCT = "product"
    PRICING = "pricing"
    BRAND = "brand"
    DISTRIBUTION = "distribution"
    TECHNOLOGY = "technology"
    CUSTOMER_SERVICE = "customer_service"

@dataclass
class Competitor:
    """Individual competitor profile"""
    competitor_id: str
    name: str
    tier: CompetitorTier
    threat_level: ThreatLevel
    
    # Company information
    founded_year: int
    headquarters: str
    employee_count: int
    funding_raised: float
    valuation: Optional[float] = None
    
    # Business model
    business_model: str
    revenue_model: str
    target_market: List[str] = field(default_factory=list)
    
    # Product information
    key_products: List[str] = field(default_factory=list)
    key_features: List[str] = field(default_factory=list)
    pricing_model: str = ""
    pricing_tiers: Dict[str, float] = field(default_factory=dict)
    
    # Market position
    market_share: float = 0.0
    customer_count: Optional[int] = None
    revenue_estimate: Optional[float] = None
    growth_rate: Optional[float] = None
    
    # Strengths and weaknesses
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    competitive_advantages: List[CompetitiveAdvantage] = field(default_factory=list)
    
    # Recent activities
    recent_funding: List[Dict[str, Any]] = field(default_factory=list)
    recent_product_launches: List[Dict[str, Any]] = field(default_factory=list)
    recent_partnerships: List[Dict[str, Any]] = field(default_factory=list)
    recent_hires: List[Dict[str, Any]] = field(default_factory=list)
    
    # Monitoring data
    website_traffic: Dict[str, int] = field(default_factory=dict)
    social_media_metrics: Dict[str, int] = field(default_factory=dict)
    news_mentions: List[Dict[str, Any]] = field(default_factory=list)
    
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class MarketAnalysis:
    """Market landscape analysis"""
    analysis_id: str
    market_segment: str
    analysis_date: str
    
    # Market size and growth
    total_addressable_market: float
    serviceable_addressable_market: float
    market_growth_rate: float
    
    # Market structure
    market_concentration: str  # "fragmented", "consolidated", "oligopoly"
    barriers_to_entry: str     # "low", "medium", "high"
    switching_costs: str       # "low", "medium", "high"
    
    # Competitive dynamics
    competitive_intensity: str  # "low", "medium", "high", "fierce"
    price_competition: str     # "low", "medium", "high"
    innovation_rate: str       # "slow", "moderate", "rapid"
    
    # Market trends
    key_trends: List[str] = field(default_factory=list)
    emerging_technologies: List[str] = field(default_factory=list)
    regulatory_changes: List[str] = field(default_factory=list)
    
    # Opportunity analysis
    market_gaps: List[str] = field(default_factory=list)
    underserved_segments: List[str] = field(default_factory=list)
    growth_opportunities: List[str] = field(default_factory=list)

@dataclass
class CompetitivePositioning:
    """Competitive positioning analysis"""
    positioning_id: str
    our_company: str
    
    # Positioning map
    positioning_dimensions: List[str] = field(default_factory=list)
    our_position: Dict[str, float] = field(default_factory=dict)
    competitor_positions: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Differentiation analysis
    unique_value_propositions: List[str] = field(default_factory=list)
    competitive_moats: List[str] = field(default_factory=list)
    differentiation_opportunities: List[str] = field(default_factory=list)
    
    # Strategic recommendations
    positioning_recommendations: List[str] = field(default_factory=list)
    competitive_responses: List[str] = field(default_factory=list)

class CompetitiveIntelligenceEngine:
    """
    Comprehensive competitive intelligence system that provides:
    - Automated competitor tracking and monitoring
    - Market landscape analysis
    - Competitive positioning insights
    - Strategic recommendations
    - Threat assessment and early warning
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.competitors: Dict[str, Competitor] = {}
        self.market_analyses: Dict[str, MarketAnalysis] = {}
        self.positioning_analyses: Dict[str, CompetitivePositioning] = {}
        
        # Monitoring configuration
        self.monitoring_keywords: List[str] = []
        self.alert_thresholds: Dict[str, float] = {}
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample competitive data"""
        
        # Sample competitors
        sample_competitors = [
            Competitor(
                competitor_id="comp_001",
                name="DataFlow Pro",
                tier=CompetitorTier.DIRECT,
                threat_level=ThreatLevel.HIGH,
                founded_year=2019,
                headquarters="San Francisco, CA",
                employee_count=150,
                funding_raised=25000000,
                valuation=100000000,
                business_model="SaaS",
                revenue_model="Subscription",
                target_market=["Enterprise", "Mid-market"],
                key_products=["Business Intelligence Platform", "Analytics Dashboard", "Reporting Suite"],
                key_features=["Real-time analytics", "Custom dashboards", "API integrations"],
                pricing_model="Tiered subscription",
                pricing_tiers={"Starter": 99, "Professional": 299, "Enterprise": 999},
                market_share=0.15,
                customer_count=2500,
                revenue_estimate=15000000,
                growth_rate=0.25,
                strengths=["Strong brand recognition", "Comprehensive feature set", "Enterprise sales team"],
                weaknesses=["High pricing", "Complex setup", "Limited customization"],
                competitive_advantages=[CompetitiveAdvantage.BRAND, CompetitiveAdvantage.PRODUCT],
                recent_funding=[
                    {"date": "2025-06-15", "amount": 15000000, "round": "Series B", "lead": "Accel Partners"}
                ],
                recent_product_launches=[
                    {"date": "2025-08-01", "product": "AI Insights", "description": "Machine learning-powered business insights"}
                ],
                website_traffic={"monthly_visitors": 125000, "organic_traffic": 85000},
                social_media_metrics={"linkedin_followers": 15000, "twitter_followers": 8500}
            ),
            Competitor(
                competitor_id="comp_002",
                name="InsightHub",
                tier=CompetitorTier.DIRECT,
                threat_level=ThreatLevel.MEDIUM,
                founded_year=2020,
                headquarters="Austin, TX",
                employee_count=75,
                funding_raised=8000000,
                business_model="SaaS",
                revenue_model="Freemium",
                target_market=["SMB", "Mid-market"],
                key_products=["Analytics Platform", "Data Visualization", "Business Reports"],
                key_features=["Drag-and-drop interface", "Pre-built templates", "Mobile app"],
                pricing_model="Freemium with paid tiers",
                pricing_tiers={"Free": 0, "Pro": 49, "Business": 149},
                market_share=0.08,
                customer_count=5000,
                revenue_estimate=3000000,
                growth_rate=0.40,
                strengths=["User-friendly interface", "Competitive pricing", "Fast implementation"],
                weaknesses=["Limited enterprise features", "Smaller team", "Less brand recognition"],
                competitive_advantages=[CompetitiveAdvantage.PRICING, CompetitiveAdvantage.CUSTOMER_SERVICE],
                recent_product_launches=[
                    {"date": "2025-07-15", "product": "Mobile Analytics", "description": "Native mobile app for iOS and Android"}
                ],
                website_traffic={"monthly_visitors": 65000, "organic_traffic": 45000},
                social_media_metrics={"linkedin_followers": 5000, "twitter_followers": 3200}
            ),
            Competitor(
                competitor_id="comp_003",
                name="TechCorp Analytics",
                tier=CompetitorTier.INDIRECT,
                threat_level=ThreatLevel.CRITICAL,
                founded_year=2015,
                headquarters="Seattle, WA",
                employee_count=500,
                funding_raised=100000000,
                valuation=1000000000,
                business_model="Enterprise Software",
                revenue_model="License + Support",
                target_market=["Large Enterprise"],
                key_products=["Enterprise Analytics Suite", "Data Warehouse", "BI Tools"],
                key_features=["Enterprise-grade security", "Scalable architecture", "Advanced analytics"],
                pricing_model="Custom enterprise pricing",
                pricing_tiers={"Enterprise": 50000},  # Annual license
                market_share=0.25,
                customer_count=500,
                revenue_estimate=75000000,
                growth_rate=0.15,
                strengths=["Market leader", "Enterprise relationships", "Comprehensive platform"],
                weaknesses=["High cost", "Complex implementation", "Slow innovation"],
                competitive_advantages=[CompetitiveAdvantage.BRAND, CompetitiveAdvantage.DISTRIBUTION],
                recent_partnerships=[
                    {"date": "2025-05-20", "partner": "Microsoft", "description": "Azure integration partnership"}
                ],
                website_traffic={"monthly_visitors": 250000, "organic_traffic": 180000},
                social_media_metrics={"linkedin_followers": 50000, "twitter_followers": 25000}
            )
        ]
        
        for competitor in sample_competitors:
            self.competitors[competitor.competitor_id] = competitor
    
    async def analyze_competitive_landscape(self, blueprint: CompanyBlueprint) -> Dict[str, Any]:
        """Analyze the complete competitive landscape"""
        
        try:
            logger.info(f"Analyzing competitive landscape for {blueprint.name}")
            
            # Market analysis
            market_analysis = await self._analyze_market_structure(blueprint)
            
            # Competitor analysis
            competitor_analysis = await self._analyze_competitors()
            
            # Positioning analysis
            positioning_analysis = await self._analyze_competitive_positioning(blueprint)
            
            # Threat assessment
            threat_assessment = await self._assess_competitive_threats()
            
            # Strategic recommendations
            strategic_recommendations = await self._generate_strategic_recommendations(blueprint)
            
            landscape_analysis = {
                "analysis_id": f"landscape_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "company_name": blueprint.name,
                "analysis_date": datetime.now(timezone.utc).isoformat(),
                "market_analysis": asdict(market_analysis),
                "competitor_analysis": competitor_analysis,
                "positioning_analysis": asdict(positioning_analysis),
                "threat_assessment": threat_assessment,
                "strategic_recommendations": strategic_recommendations,
                "executive_summary": await self._generate_executive_summary(
                    market_analysis, competitor_analysis, positioning_analysis, threat_assessment
                )
            }
            
            logger.info("Competitive landscape analysis completed")
            return landscape_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze competitive landscape: {e}")
            raise
    
    async def _analyze_market_structure(self, blueprint: CompanyBlueprint) -> MarketAnalysis:
        """Analyze market structure and dynamics"""
        
        market_analysis = MarketAnalysis(
            analysis_id=f"market_{datetime.now().strftime('%H%M%S')}",
            market_segment=blueprint.target_market.primary_segment,
            analysis_date=datetime.now(timezone.utc).isoformat(),
            total_addressable_market=50000000000,  # $50B
            serviceable_addressable_market=5000000000,  # $5B
            market_growth_rate=0.25,  # 25% annual growth
            market_concentration="fragmented",
            barriers_to_entry="medium",
            switching_costs="medium",
            competitive_intensity="high",
            price_competition="medium",
            innovation_rate="rapid",
            key_trends=[
                "AI and machine learning integration",
                "Real-time analytics demand",
                "Self-service BI adoption",
                "Cloud-first architecture",
                "Mobile-first user experience",
                "Data democratization"
            ],
            emerging_technologies=[
                "Natural language processing for queries",
                "Automated insight generation",
                "Augmented analytics",
                "Edge computing for real-time processing",
                "Blockchain for data integrity"
            ],
            regulatory_changes=[
                "GDPR and data privacy regulations",
                "Industry-specific compliance requirements",
                "Cross-border data transfer restrictions"
            ],
            market_gaps=[
                "SMB-focused solutions with enterprise features",
                "Industry-specific vertical solutions",
                "No-code/low-code analytics platforms",
                "Real-time collaborative analytics"
            ],
            underserved_segments=[
                "Small businesses with limited technical resources",
                "Non-profit organizations",
                "Emerging market companies",
                "Industry-specific niches"
            ],
            growth_opportunities=[
                "International expansion",
                "Vertical market specialization",
                "API-first platform approach",
                "Embedded analytics solutions"
            ]
        )
        
        self.market_analyses[market_analysis.analysis_id] = market_analysis
        return market_analysis
    
    async def _analyze_competitors(self) -> Dict[str, Any]:
        """Analyze competitor landscape and dynamics"""
        
        # Competitor segmentation
        direct_competitors = [c for c in self.competitors.values() if c.tier == CompetitorTier.DIRECT]
        indirect_competitors = [c for c in self.competitors.values() if c.tier == CompetitorTier.INDIRECT]
        emerging_competitors = [c for c in self.competitors.values() if c.tier == CompetitorTier.EMERGING]
        
        # Market share analysis
        total_market_share = sum(c.market_share for c in self.competitors.values())
        market_leader = max(self.competitors.values(), key=lambda x: x.market_share)
        
        # Funding analysis
        total_funding = sum(c.funding_raised for c in self.competitors.values())
        avg_funding = total_funding / len(self.competitors) if self.competitors else 0
        
        # Growth analysis
        high_growth_competitors = [c for c in self.competitors.values() if c.growth_rate and c.growth_rate > 0.3]
        
        # Threat analysis
        high_threat_competitors = [c for c in self.competitors.values() if c.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]
        
        competitor_analysis = {
            "total_competitors": len(self.competitors),
            "competitor_segmentation": {
                "direct": len(direct_competitors),
                "indirect": len(indirect_competitors),
                "emerging": len(emerging_competitors)
            },
            "market_concentration": {
                "total_tracked_market_share": round(total_market_share, 3),
                "market_leader": {
                    "name": market_leader.name,
                    "market_share": market_leader.market_share
                },
                "top_3_competitors": [
                    {"name": c.name, "market_share": c.market_share}
                    for c in sorted(self.competitors.values(), key=lambda x: x.market_share, reverse=True)[:3]
                ]
            },
            "funding_landscape": {
                "total_funding": total_funding,
                "average_funding": round(avg_funding, 0),
                "most_funded": max(self.competitors.values(), key=lambda x: x.funding_raised).name,
                "recent_funding_activity": len([c for c in self.competitors.values() if c.recent_funding])
            },
            "growth_dynamics": {
                "high_growth_competitors": len(high_growth_competitors),
                "average_growth_rate": round(statistics.mean([c.growth_rate for c in self.competitors.values() if c.growth_rate]), 3),
                "fastest_growing": max([c for c in self.competitors.values() if c.growth_rate], key=lambda x: x.growth_rate).name if high_growth_competitors else None
            },
            "threat_assessment": {
                "high_threat_competitors": len(high_threat_competitors),
                "critical_threats": [c.name for c in self.competitors.values() if c.threat_level == ThreatLevel.CRITICAL],
                "emerging_threats": [c.name for c in self.competitors.values() if c.tier == CompetitorTier.EMERGING and c.threat_level in [ThreatLevel.MEDIUM, ThreatLevel.HIGH]]
            },
            "competitive_advantages_distribution": await self._analyze_competitive_advantages(),
            "recent_market_activity": await self._analyze_recent_activity()
        }
        
        return competitor_analysis
    
    async def _analyze_competitive_advantages(self) -> Dict[str, int]:
        """Analyze distribution of competitive advantages"""
        
        advantage_counts = {}
        for advantage in CompetitiveAdvantage:
            count = sum(1 for c in self.competitors.values() if advantage in c.competitive_advantages)
            advantage_counts[advantage.value] = count
        
        return advantage_counts
    
    async def _analyze_recent_activity(self) -> Dict[str, Any]:
        """Analyze recent competitive activity"""
        
        recent_activity = {
            "funding_rounds": [],
            "product_launches": [],
            "partnerships": [],
            "key_hires": []
        }
        
        for competitor in self.competitors.values():
            # Recent funding
            for funding in competitor.recent_funding:
                recent_activity["funding_rounds"].append({
                    "competitor": competitor.name,
                    "date": funding["date"],
                    "amount": funding["amount"],
                    "round": funding["round"]
                })
            
            # Recent product launches
            for launch in competitor.recent_product_launches:
                recent_activity["product_launches"].append({
                    "competitor": competitor.name,
                    "date": launch["date"],
                    "product": launch["product"],
                    "description": launch["description"]
                })
            
            # Recent partnerships
            for partnership in competitor.recent_partnerships:
                recent_activity["partnerships"].append({
                    "competitor": competitor.name,
                    "date": partnership["date"],
                    "partner": partnership["partner"],
                    "description": partnership["description"]
                })
        
        # Sort by date (most recent first)
        for activity_type in recent_activity:
            recent_activity[activity_type] = sorted(
                recent_activity[activity_type],
                key=lambda x: x["date"],
                reverse=True
            )[:5]  # Top 5 most recent
        
        return recent_activity
    
    async def _analyze_competitive_positioning(self, blueprint: CompanyBlueprint) -> CompetitivePositioning:
        """Analyze competitive positioning"""
        
        positioning = CompetitivePositioning(
            positioning_id=f"positioning_{datetime.now().strftime('%H%M%S')}",
            our_company=blueprint.name,
            positioning_dimensions=["Price", "Features", "Ease of Use", "Enterprise Focus", "Innovation"],
            our_position={
                "Price": 7.0,  # 1-10 scale (10 = premium pricing)
                "Features": 8.5,
                "Ease of Use": 9.0,
                "Enterprise Focus": 6.0,
                "Innovation": 9.5
            }
        )
        
        # Competitor positions
        for competitor in self.competitors.values():
            if competitor.tier == CompetitorTier.DIRECT:
                if competitor.name == "DataFlow Pro":
                    positioning.competitor_positions[competitor.name] = {
                        "Price": 9.0,
                        "Features": 9.5,
                        "Ease of Use": 6.0,
                        "Enterprise Focus": 9.0,
                        "Innovation": 7.0
                    }
                elif competitor.name == "InsightHub":
                    positioning.competitor_positions[competitor.name] = {
                        "Price": 3.0,
                        "Features": 6.0,
                        "Ease of Use": 9.5,
                        "Enterprise Focus": 4.0,
                        "Innovation": 8.0
                    }
        
        # Unique value propositions
        positioning.unique_value_propositions = [
            "AI-powered insights with human-friendly explanations",
            "Real-time collaborative analytics",
            "No-code/low-code interface for business users",
            "Industry-specific templates and benchmarks",
            "Embedded analytics API for product teams"
        ]
        
        # Competitive moats
        positioning.competitive_moats = [
            "Proprietary AI algorithms for business forecasting",
            "Strong network effects from collaborative features",
            "Extensive integration ecosystem",
            "Industry-specific domain expertise",
            "Superior user experience and design"
        ]
        
        # Differentiation opportunities
        positioning.differentiation_opportunities = [
            "Focus on SMB market with enterprise-grade features",
            "Vertical specialization in underserved industries",
            "Mobile-first analytics experience",
            "Real-time collaborative decision making",
            "AI-powered automated insights and recommendations"
        ]
        
        # Strategic recommendations
        positioning.positioning_recommendations = [
            "Position as the 'intelligent analytics platform for modern businesses'",
            "Emphasize ease of use and rapid time-to-value",
            "Target the gap between simple tools and complex enterprise solutions",
            "Build thought leadership around AI-powered business intelligence",
            "Focus on customer success stories and ROI demonstrations"
        ]
        
        # Competitive responses
        positioning.competitive_responses = [
            "Respond to pricing pressure with value-based selling",
            "Counter feature comparisons with superior user experience",
            "Address enterprise concerns with security and compliance certifications",
            "Differentiate through industry-specific solutions",
            "Leverage AI capabilities as key differentiator"
        ]
        
        self.positioning_analyses[positioning.positioning_id] = positioning
        return positioning
    
    async def _assess_competitive_threats(self) -> Dict[str, Any]:
        """Assess competitive threats and risks"""
        
        threat_assessment = {
            "immediate_threats": [],
            "emerging_threats": [],
            "market_risks": [],
            "strategic_risks": [],
            "mitigation_strategies": []
        }
        
        # Immediate threats
        for competitor in self.competitors.values():
            if competitor.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                threat_assessment["immediate_threats"].append({
                    "competitor": competitor.name,
                    "threat_level": competitor.threat_level.value,
                    "key_concerns": [
                        f"Market share: {competitor.market_share*100:.1f}%",
                        f"Growth rate: {competitor.growth_rate*100:.1f}%" if competitor.growth_rate else "Unknown growth",
                        f"Funding: ${competitor.funding_raised:,.0f}",
                        f"Strengths: {', '.join(competitor.strengths[:2])}"
                    ],
                    "recent_activity": len(competitor.recent_funding + competitor.recent_product_launches)
                })
        
        # Emerging threats
        emerging_threats = [
            {
                "threat": "New AI-powered entrants",
                "description": "Well-funded startups with advanced AI capabilities",
                "probability": "medium",
                "impact": "high",
                "timeline": "6-12 months"
            },
            {
                "threat": "Big Tech expansion",
                "description": "Google, Microsoft, or Amazon entering the market",
                "probability": "high",
                "impact": "critical",
                "timeline": "12-18 months"
            },
            {
                "threat": "Open source alternatives",
                "description": "Mature open source BI tools gaining enterprise adoption",
                "probability": "medium",
                "impact": "medium",
                "timeline": "18-24 months"
            }
        ]
        threat_assessment["emerging_threats"] = emerging_threats
        
        # Market risks
        threat_assessment["market_risks"] = [
            "Economic downturn reducing enterprise software spending",
            "Increased price competition from well-funded competitors",
            "Market consolidation through M&A activity",
            "Regulatory changes affecting data analytics",
            "Technology disruption from new paradigms"
        ]
        
        # Strategic risks
        threat_assessment["strategic_risks"] = [
            "Customer concentration risk with large competitors",
            "Talent acquisition competition in AI/ML space",
            "Technology scalability challenges",
            "Intellectual property risks",
            "Partnership dependencies"
        ]
        
        # Mitigation strategies
        threat_assessment["mitigation_strategies"] = [
            "Build strong customer relationships and switching costs",
            "Invest heavily in product differentiation and innovation",
            "Secure strategic partnerships and distribution channels",
            "Maintain strong financial position for competitive responses",
            "Focus on underserved market segments",
            "Build proprietary data and network effects"
        ]
        
        return threat_assessment
    
    async def _generate_strategic_recommendations(self, blueprint: CompanyBlueprint) -> List[str]:
        """Generate strategic recommendations based on competitive analysis"""
        
        recommendations = [
            "🎯 POSITIONING: Focus on 'AI-powered analytics for modern businesses' positioning to differentiate from traditional BI tools",
            "🚀 PRODUCT: Accelerate AI feature development to maintain technology leadership advantage",
            "💰 PRICING: Implement value-based pricing strategy to compete on ROI rather than price",
            "🎪 MARKET: Target underserved SMB segment with enterprise-grade features at accessible pricing",
            "🤝 PARTNERSHIPS: Build strategic partnerships with complementary platforms to expand distribution",
            "📊 CUSTOMER SUCCESS: Invest heavily in customer success to build switching costs and reduce churn",
            "🔒 MOATS: Develop proprietary data assets and network effects to create competitive moats",
            "⚡ SPEED: Maintain rapid innovation cycle to stay ahead of larger, slower competitors",
            "🌍 EXPANSION: Consider international expansion to markets with less competitive pressure",
            "💡 THOUGHT LEADERSHIP: Build thought leadership around AI-powered business intelligence"
        ]
        
        return recommendations
    
    async def _generate_executive_summary(
        self,
        market_analysis: MarketAnalysis,
        competitor_analysis: Dict[str, Any],
        positioning_analysis: CompetitivePositioning,
        threat_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate executive summary of competitive intelligence"""
        
        executive_summary = {
            "market_overview": {
                "market_size": f"${market_analysis.total_addressable_market/1000000000:.1f}B TAM",
                "growth_rate": f"{market_analysis.market_growth_rate*100:.0f}% annual growth",
                "market_structure": market_analysis.market_concentration,
                "competitive_intensity": market_analysis.competitive_intensity
            },
            "competitive_landscape": {
                "total_competitors_tracked": competitor_analysis["total_competitors"],
                "direct_competitors": competitor_analysis["competitor_segmentation"]["direct"],
                "market_leader": competitor_analysis["market_concentration"]["market_leader"]["name"],
                "high_threat_competitors": len(threat_assessment["immediate_threats"])
            },
            "our_position": {
                "key_differentiators": positioning_analysis.unique_value_propositions[:3],
                "competitive_advantages": positioning_analysis.competitive_moats[:3],
                "positioning_strength": "Strong in Innovation and Ease of Use"
            },
            "key_threats": [threat["competitor"] for threat in threat_assessment["immediate_threats"][:3]],
            "key_opportunities": market_analysis.growth_opportunities[:3],
            "strategic_priorities": [
                "Accelerate AI feature development",
                "Build customer success and retention",
                "Expand into underserved market segments",
                "Develop strategic partnerships"
            ]
        }
        
        return executive_summary
    
    async def get_competitive_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive competitive intelligence dashboard data"""
        
        try:
            # Competitor overview
            competitor_overview = {
                "total_competitors": len(self.competitors),
                "direct_competitors": len([c for c in self.competitors.values() if c.tier == CompetitorTier.DIRECT]),
                "high_threat_competitors": len([c for c in self.competitors.values() if c.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]),
                "recent_activity_count": sum(len(c.recent_funding + c.recent_product_launches + c.recent_partnerships) for c in self.competitors.values())
            }
            
            # Top competitors
            top_competitors = sorted(
                self.competitors.values(),
                key=lambda x: (x.threat_level == ThreatLevel.CRITICAL, x.threat_level == ThreatLevel.HIGH, x.market_share),
                reverse=True
            )[:5]
            
            # Market insights
            latest_market_analysis = max(self.market_analyses.values(), key=lambda x: x.analysis_id) if self.market_analyses else None
            
            # Recent competitive activity
            recent_activity = []
            for competitor in self.competitors.values():
                for funding in competitor.recent_funding:
                    recent_activity.append({
                        "type": "funding",
                        "competitor": competitor.name,
                        "date": funding["date"],
                        "description": f"Raised ${funding['amount']:,.0f} in {funding['round']}"
                    })
                for launch in competitor.recent_product_launches:
                    recent_activity.append({
                        "type": "product",
                        "competitor": competitor.name,
                        "date": launch["date"],
                        "description": f"Launched {launch['product']}"
                    })
            
            # Sort by date and take top 10
            recent_activity = sorted(recent_activity, key=lambda x: x["date"], reverse=True)[:10]
            
            dashboard_data = {
                "competitor_overview": competitor_overview,
                "top_competitors": [
                    {
                        "name": c.name,
                        "tier": c.tier.value,
                        "threat_level": c.threat_level.value,
                        "market_share": c.market_share,
                        "funding_raised": c.funding_raised,
                        "strengths": c.strengths[:2],
                        "recent_activity_count": len(c.recent_funding + c.recent_product_launches)
                    }
                    for c in top_competitors
                ],
                "market_insights": {
                    "market_size": latest_market_analysis.total_addressable_market if latest_market_analysis else 0,
                    "growth_rate": latest_market_analysis.market_growth_rate if latest_market_analysis else 0,
                    "key_trends": latest_market_analysis.key_trends[:5] if latest_market_analysis else [],
                    "market_gaps": latest_market_analysis.market_gaps[:3] if latest_market_analysis else []
                },
                "recent_activity": recent_activity,
                "threat_alerts": [
                    {
                        "competitor": c.name,
                        "threat_level": c.threat_level.value,
                        "alert": f"High growth rate: {c.growth_rate*100:.0f}%" if c.growth_rate and c.growth_rate > 0.3 else f"Large funding: ${c.funding_raised:,.0f}"
                    }
                    for c in self.competitors.values()
                    if c.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
                ][:5],
                "strategic_recommendations": await self._generate_dashboard_recommendations()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get competitive dashboard data: {e}")
            raise
    
    async def _generate_dashboard_recommendations(self) -> List[str]:
        """Generate dashboard-specific recommendations"""
        
        return [
            "🎯 Monitor DataFlow Pro's AI feature development - direct threat to our positioning",
            "⚡ Accelerate mobile app development - InsightHub gaining traction with mobile-first approach",
            "💰 Prepare competitive response to potential price war from well-funded competitors",
            "🤝 Explore strategic partnerships to counter TechCorp's distribution advantages",
            "🚀 Focus on customer success to build switching costs against competitive pressure"
        ]

# Global competitive intelligence engine
competitive_intelligence = CompetitiveIntelligenceEngine()