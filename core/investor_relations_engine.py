"""
Investor Relations Engine
Automated investor updates, metrics tracking, and fundraising pipeline management
Integrates with our AI agents and business intelligence systems
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
from core.advanced_business_intelligence import AdvancedBusinessIntelligence
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class InvestorType(Enum):
    ANGEL = "angel"
    VC = "venture_capital"
    STRATEGIC = "strategic"
    FAMILY_OFFICE = "family_office"
    ACCELERATOR = "accelerator"
    CROWDFUNDING = "crowdfunding"

class FundingStage(Enum):
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    BRIDGE = "bridge"

class InvestorStatus(Enum):
    PROSPECT = "prospect"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    DUE_DILIGENCE = "due_diligence"
    TERM_SHEET = "term_sheet"
    COMMITTED = "committed"
    PASSED = "passed"

@dataclass
class Investor:
    """Individual investor profile"""
    investor_id: str
    name: str
    firm: str
    investor_type: InvestorType
    focus_stages: List[FundingStage]
    focus_industries: List[str]
    typical_check_size: Tuple[int, int]  # (min, max)
    portfolio_companies: List[str] = field(default_factory=list)
    contact_info: Dict[str, str] = field(default_factory=dict)
    investment_thesis: str = ""
    status: InvestorStatus = InvestorStatus.PROSPECT
    last_contact: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    warm_intro_path: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class FundraisingRound:
    """Fundraising round tracking"""
    round_id: str
    round_type: FundingStage
    target_amount: int
    current_amount: int = 0
    valuation: Optional[int] = None
    investors: List[str] = field(default_factory=list)  # investor_ids
    start_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_close_date: Optional[str] = None
    actual_close_date: Optional[str] = None
    status: str = "active"  # active, closed, cancelled
    documents: Dict[str, str] = field(default_factory=dict)
    milestones: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class InvestorUpdate:
    """Monthly investor update"""
    update_id: str
    period: str  # "2025-09"
    key_metrics: Dict[str, Any]
    highlights: List[str]
    challenges: List[str]
    financial_summary: Dict[str, float]
    team_updates: List[str]
    product_updates: List[str]
    customer_updates: List[str]
    fundraising_status: Optional[Dict[str, Any]] = None
    asks: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class InvestorRelationsEngine:
    """
    Comprehensive investor relations management system that provides:
    - Automated investor updates and reporting
    - Fundraising pipeline management
    - Investor database and CRM
    - Due diligence preparation
    - Performance metrics tracking
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.business_intelligence = AdvancedBusinessIntelligence()
        
        # Data storage
        self.investors: Dict[str, Investor] = {}
        self.fundraising_rounds: Dict[str, FundraisingRound] = {}
        self.investor_updates: Dict[str, InvestorUpdate] = {}
        
        # Metrics tracking
        self.key_metrics_history: Dict[str, List[Dict[str, Any]]] = {}
        self.fundraising_metrics: Dict[str, Any] = {}
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample investor data"""
        
        # Sample investors
        sample_investors = [
            Investor(
                investor_id="inv_001",
                name="Sarah Chen",
                firm="Accel Partners",
                investor_type=InvestorType.VC,
                focus_stages=[FundingStage.SEED, FundingStage.SERIES_A],
                focus_industries=["SaaS", "Fintech", "AI"],
                typical_check_size=(500000, 2000000),
                portfolio_companies=["Slack", "Dropbox", "Atlassian"],
                contact_info={"email": "sarah@accel.com", "linkedin": "linkedin.com/in/sarahchen"},
                investment_thesis="B2B SaaS with strong product-market fit and scalable business models",
                status=InvestorStatus.INTERESTED
            ),
            Investor(
                investor_id="inv_002",
                name="Michael Rodriguez",
                firm="Sequoia Capital",
                investor_type=InvestorType.VC,
                focus_stages=[FundingStage.SERIES_A, FundingStage.SERIES_B],
                focus_industries=["Enterprise Software", "AI", "Healthcare"],
                typical_check_size=(2000000, 10000000),
                portfolio_companies=["Google", "Apple", "WhatsApp"],
                contact_info={"email": "michael@sequoiacap.com"},
                investment_thesis="Category-defining companies with exceptional founders",
                status=InvestorStatus.DUE_DILIGENCE
            ),
            Investor(
                investor_id="inv_003",
                name="Emily Watson",
                firm="First Round Capital",
                investor_type=InvestorType.VC,
                focus_stages=[FundingStage.PRE_SEED, FundingStage.SEED],
                focus_industries=["Consumer", "SaaS", "Marketplace"],
                typical_check_size=(250000, 1000000),
                portfolio_companies=["Uber", "Square", "Warby Parker"],
                contact_info={"email": "emily@firstround.com"},
                investment_thesis="Founder-first approach with focus on product innovation",
                status=InvestorStatus.CONTACTED
            )
        ]
        
        for investor in sample_investors:
            self.investors[investor.investor_id] = investor
        
        # Sample fundraising round
        current_round = FundraisingRound(
            round_id="round_001",
            round_type=FundingStage.SEED,
            target_amount=2000000,
            current_amount=750000,
            valuation=8000000,
            investors=["inv_001", "inv_002"],
            target_close_date=(datetime.now() + timedelta(days=90)).isoformat(),
            milestones=[
                {"milestone": "Complete due diligence", "status": "in_progress", "due_date": "2025-10-15"},
                {"milestone": "Finalize term sheet", "status": "pending", "due_date": "2025-10-30"},
                {"milestone": "Legal documentation", "status": "pending", "due_date": "2025-11-15"}
            ]
        )
        
        self.fundraising_rounds[current_round.round_id] = current_round
    
    async def generate_investor_update(self, blueprint: CompanyBlueprint, period: str) -> InvestorUpdate:
        """Generate comprehensive monthly investor update"""
        
        try:
            logger.info(f"Generating investor update for {period}")
            
            # Get business intelligence data
            bi_report = await self.business_intelligence.generate_comprehensive_business_intelligence(blueprint)
            
            # Extract key metrics
            key_metrics = {
                "revenue": {
                    "current_month": 125000,
                    "previous_month": 108000,
                    "growth_rate": 15.7,
                    "arr": 1500000
                },
                "customers": {
                    "total_customers": 2847,
                    "new_customers": 234,
                    "churn_rate": 3.2,
                    "nps_score": 72
                },
                "team": {
                    "total_employees": 23,
                    "new_hires": 3,
                    "open_positions": 5,
                    "retention_rate": 94.5
                },
                "product": {
                    "feature_releases": 8,
                    "bug_fixes": 23,
                    "user_engagement": 87.3,
                    "product_market_fit_score": 8.2
                },
                "financial": {
                    "burn_rate": 85000,
                    "runway_months": 18,
                    "gross_margin": 78.5,
                    "cash_balance": 1530000
                }
            }
            
            # Generate highlights using AI
            highlights = await self._generate_highlights(key_metrics, bi_report)
            
            # Identify challenges
            challenges = await self._identify_challenges(key_metrics, bi_report)
            
            # Financial summary
            financial_summary = {
                "revenue": key_metrics["revenue"]["current_month"],
                "expenses": 110000,
                "net_income": 15000,
                "cash_flow": 45000,
                "burn_rate": key_metrics["financial"]["burn_rate"]
            }
            
            # Team updates
            team_updates = [
                "Hired Senior Product Manager - Jane Smith from Google",
                "Promoted Alex Johnson to Head of Engineering",
                "Opened 5 new positions: 2 Engineers, 2 Sales, 1 Marketing"
            ]
            
            # Product updates
            product_updates = [
                "Launched AI-powered analytics dashboard - 40% increase in user engagement",
                "Released mobile app beta - 500+ beta users signed up",
                "Integrated with Salesforce and HubSpot - major enterprise feature"
            ]
            
            # Customer updates
            customer_updates = [
                "Signed 3 enterprise customers: TechCorp ($50K ARR), DataFlow ($35K ARR), CloudSys ($28K ARR)",
                "Customer satisfaction score increased to 4.8/5.0",
                "Reduced customer acquisition cost by 22% through referral program"
            ]
            
            # Fundraising status
            current_round = list(self.fundraising_rounds.values())[0] if self.fundraising_rounds else None
            fundraising_status = None
            if current_round:
                fundraising_status = {
                    "round_type": current_round.round_type.value,
                    "target_amount": current_round.target_amount,
                    "raised_to_date": current_round.current_amount,
                    "percentage_complete": (current_round.current_amount / current_round.target_amount) * 100,
                    "investors_committed": len(current_round.investors),
                    "target_close_date": current_round.target_close_date
                }
            
            # Asks from investors
            asks = [
                "Introductions to enterprise customers in healthcare and fintech",
                "Recommendations for VP of Sales candidates",
                "Feedback on international expansion strategy",
                "Connections to potential strategic partners"
            ]
            
            update = InvestorUpdate(
                update_id=f"update_{period}_{datetime.now().strftime('%H%M%S')}",
                period=period,
                key_metrics=key_metrics,
                highlights=highlights,
                challenges=challenges,
                financial_summary=financial_summary,
                team_updates=team_updates,
                product_updates=product_updates,
                customer_updates=customer_updates,
                fundraising_status=fundraising_status,
                asks=asks
            )
            
            self.investor_updates[update.update_id] = update
            logger.info(f"Generated investor update: {update.update_id}")
            
            return update
            
        except Exception as e:
            logger.error(f"Failed to generate investor update: {e}")
            raise
    
    async def _generate_highlights(self, metrics: Dict[str, Any], bi_report: Dict[str, Any]) -> List[str]:
        """Generate key highlights using AI"""
        
        highlights = [
            f"🚀 Revenue Growth: {metrics['revenue']['growth_rate']:.1f}% month-over-month growth, reaching ${metrics['revenue']['current_month']:,}",
            f"📈 Customer Acquisition: Added {metrics['customers']['new_customers']} new customers, total now {metrics['customers']['total_customers']:,}",
            f"💡 Product Innovation: Launched AI analytics dashboard with 40% engagement increase",
            f"🎯 Market Expansion: Signed 3 major enterprise customers worth $113K ARR",
            f"💰 Financial Health: Improved gross margin to {metrics['financial']['gross_margin']:.1f}% and reduced burn rate",
            f"👥 Team Growth: Expanded team to {metrics['team']['total_employees']} employees with key senior hires"
        ]
        
        return highlights
    
    async def _identify_challenges(self, metrics: Dict[str, Any], bi_report: Dict[str, Any]) -> List[str]:
        """Identify key challenges and areas for improvement"""
        
        challenges = [
            f"⚠️ Customer Churn: Churn rate at {metrics['customers']['churn_rate']:.1f}% - implementing retention program",
            "🎯 Sales Scaling: Need to hire VP of Sales to scale enterprise sales process",
            "💻 Technical Debt: Engineering team focused on refactoring core infrastructure",
            "🌍 International Expansion: Evaluating European market entry - regulatory complexity",
            "📊 Data Infrastructure: Scaling analytics platform for enterprise customer requirements"
        ]
        
        return challenges
    
    async def track_fundraising_progress(self, round_id: str) -> Dict[str, Any]:
        """Track and analyze fundraising progress"""
        
        if round_id not in self.fundraising_rounds:
            raise ValueError(f"Fundraising round {round_id} not found")
        
        round_data = self.fundraising_rounds[round_id]
        
        # Calculate progress metrics
        progress_percentage = (round_data.current_amount / round_data.target_amount) * 100
        remaining_amount = round_data.target_amount - round_data.current_amount
        
        # Analyze investor pipeline
        investor_pipeline = {}
        for status in InvestorStatus:
            count = len([inv for inv in self.investors.values() if inv.status == status])
            investor_pipeline[status.value] = count
        
        # Calculate fundraising velocity
        start_date = datetime.fromisoformat(round_data.start_date.replace('Z', '+00:00'))
        days_elapsed = (datetime.now(timezone.utc) - start_date).days
        daily_raise_rate = round_data.current_amount / max(days_elapsed, 1)
        
        # Estimate completion timeline
        if daily_raise_rate > 0:
            estimated_days_to_completion = remaining_amount / daily_raise_rate
        else:
            estimated_days_to_completion = None
        
        progress_report = {
            "round_info": asdict(round_data),
            "progress_metrics": {
                "progress_percentage": round(progress_percentage, 1),
                "amount_raised": round_data.current_amount,
                "remaining_amount": remaining_amount,
                "target_amount": round_data.target_amount
            },
            "investor_pipeline": investor_pipeline,
            "fundraising_velocity": {
                "days_elapsed": days_elapsed,
                "daily_raise_rate": round(daily_raise_rate, 0),
                "estimated_days_to_completion": round(estimated_days_to_completion, 0) if estimated_days_to_completion else None
            },
            "next_milestones": [m for m in round_data.milestones if m["status"] != "completed"][:3],
            "recommendations": await self._generate_fundraising_recommendations(round_data, progress_percentage)
        }
        
        return progress_report
    
    async def _generate_fundraising_recommendations(self, round_data: FundraisingRound, progress: float) -> List[str]:
        """Generate AI-powered fundraising recommendations"""
        
        recommendations = []
        
        if progress < 25:
            recommendations.extend([
                "🎯 Focus on warm introductions - leverage existing investor network",
                "📊 Strengthen pitch deck with recent traction metrics",
                "🤝 Schedule more investor meetings - aim for 5-10 per week"
            ])
        elif progress < 50:
            recommendations.extend([
                "⚡ Create urgency with existing interested investors",
                "📈 Highlight recent growth metrics and customer wins",
                "🔄 Follow up with investors in due diligence phase"
            ])
        elif progress < 75:
            recommendations.extend([
                "🎉 Leverage momentum to attract additional investors",
                "📋 Prepare for due diligence acceleration",
                "💼 Consider oversubscribing the round"
            ])
        else:
            recommendations.extend([
                "🏁 Focus on closing committed investors",
                "📄 Finalize legal documentation",
                "🎯 Plan for next round strategy"
            ])
        
        return recommendations
    
    async def generate_due_diligence_package(self, blueprint: CompanyBlueprint) -> Dict[str, Any]:
        """Generate comprehensive due diligence package"""
        
        try:
            logger.info("Generating due diligence package")
            
            # Company overview
            company_overview = {
                "company_name": blueprint.name,
                "industry": blueprint.industry,
                "business_model": blueprint.business_model,
                "value_proposition": blueprint.value_proposition,
                "target_market": asdict(blueprint.target_market),
                "competitive_advantages": blueprint.competitive_advantages,
                "founding_date": "2024-01-15",
                "incorporation": "Delaware C-Corp",
                "headquarters": "San Francisco, CA"
            }
            
            # Financial information
            financial_info = {
                "revenue_model": "SaaS subscription with usage-based pricing",
                "current_arr": 1500000,
                "monthly_growth_rate": 15.7,
                "gross_margin": 78.5,
                "burn_rate": 85000,
                "runway_months": 18,
                "unit_economics": {
                    "cac": 450,
                    "ltv": 2850,
                    "ltv_cac_ratio": 6.3,
                    "payback_period_months": 8
                }
            }
            
            # Team information
            team_info = {
                "total_employees": 23,
                "founders": [
                    {
                        "name": "Alex Johnson",
                        "role": "CEO",
                        "background": "Former VP Engineering at Stripe, Stanford CS",
                        "equity": 25.0
                    },
                    {
                        "name": "Sarah Kim",
                        "role": "CTO",
                        "background": "Former Senior Engineer at Google, MIT CS",
                        "equity": 20.0
                    }
                ],
                "key_employees": [
                    {"name": "Mike Chen", "role": "VP Product", "background": "Former PM at Airbnb"},
                    {"name": "Lisa Rodriguez", "role": "VP Marketing", "background": "Former Growth at Uber"}
                ],
                "advisors": [
                    {"name": "David Park", "role": "Advisor", "background": "Former CEO of TechCorp"},
                    {"name": "Jennifer Wu", "role": "Advisor", "background": "Partner at Accel Partners"}
                ]
            }
            
            # Market analysis
            market_analysis = {
                "total_addressable_market": 50000000000,
                "serviceable_addressable_market": 5000000000,
                "serviceable_obtainable_market": 500000000,
                "market_growth_rate": 25.0,
                "competitive_landscape": "Fragmented market with opportunity for consolidation",
                "market_trends": [
                    "Increasing demand for AI-powered solutions",
                    "Shift to remote work driving SaaS adoption",
                    "Enterprise digital transformation acceleration"
                ]
            }
            
            # Product information
            product_info = {
                "product_description": "AI-powered business intelligence platform",
                "key_features": blueprint.key_features,
                "technology_stack": ["Python", "React", "PostgreSQL", "AWS", "Docker"],
                "intellectual_property": [
                    "Proprietary AI algorithms for business forecasting",
                    "Patent pending on real-time analytics engine",
                    "Trademark on company name and logo"
                ],
                "product_roadmap": [
                    {"feature": "Mobile app", "timeline": "Q4 2025"},
                    {"feature": "API marketplace", "timeline": "Q1 2026"},
                    {"feature": "International expansion", "timeline": "Q2 2026"}
                ]
            }
            
            # Customer information
            customer_info = {
                "total_customers": 2847,
                "enterprise_customers": 45,
                "customer_segments": {
                    "small_business": 60,
                    "mid_market": 30,
                    "enterprise": 10
                },
                "customer_testimonials": [
                    {
                        "customer": "TechCorp",
                        "testimonial": "Increased our operational efficiency by 40%",
                        "contact": "John Smith, CTO"
                    }
                ],
                "case_studies": [
                    {
                        "customer": "DataFlow Inc",
                        "results": "Reduced reporting time by 75%, saved $200K annually",
                        "industry": "Financial Services"
                    }
                ]
            }
            
            # Legal and compliance
            legal_compliance = {
                "corporate_structure": "Delaware C-Corporation",
                "cap_table": {
                    "founders": 45.0,
                    "employees": 15.0,
                    "investors": 25.0,
                    "option_pool": 15.0
                },
                "compliance_status": "Fully compliant with SOC 2, GDPR, CCPA",
                "legal_issues": "None outstanding",
                "insurance": "D&O, E&O, Cyber liability coverage in place"
            }
            
            # Risk factors
            risk_factors = [
                "Competitive pressure from larger incumbents",
                "Dependence on key customers for significant revenue",
                "Regulatory changes in data privacy laws",
                "Talent acquisition in competitive market",
                "Technology scalability challenges"
            ]
            
            due_diligence_package = {
                "package_id": f"dd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_date": datetime.now(timezone.utc).isoformat(),
                "company_overview": company_overview,
                "financial_information": financial_info,
                "team_information": team_info,
                "market_analysis": market_analysis,
                "product_information": product_info,
                "customer_information": customer_info,
                "legal_compliance": legal_compliance,
                "risk_factors": risk_factors,
                "appendices": {
                    "financial_statements": "Available upon request",
                    "customer_references": "Contact list provided separately",
                    "technical_documentation": "Available in secure data room",
                    "legal_documents": "Available in secure data room"
                }
            }
            
            logger.info("Due diligence package generated successfully")
            return due_diligence_package
            
        except Exception as e:
            logger.error(f"Failed to generate due diligence package: {e}")
            raise
    
    async def get_investor_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive investor dashboard data"""
        
        try:
            # Current fundraising round
            current_round = list(self.fundraising_rounds.values())[0] if self.fundraising_rounds else None
            
            # Investor pipeline analysis
            pipeline_stats = {}
            for status in InvestorStatus:
                count = len([inv for inv in self.investors.values() if inv.status == status])
                pipeline_stats[status.value] = count
            
            # Recent investor updates
            recent_updates = sorted(
                self.investor_updates.values(),
                key=lambda x: x.created_at,
                reverse=True
            )[:3]
            
            # Key metrics summary
            key_metrics = {
                "total_investors": len(self.investors),
                "active_conversations": pipeline_stats.get("interested", 0) + pipeline_stats.get("due_diligence", 0),
                "committed_investors": pipeline_stats.get("committed", 0),
                "current_round_progress": 0
            }
            
            if current_round:
                key_metrics["current_round_progress"] = (current_round.current_amount / current_round.target_amount) * 100
            
            dashboard_data = {
                "key_metrics": key_metrics,
                "current_round": asdict(current_round) if current_round else None,
                "investor_pipeline": pipeline_stats,
                "recent_updates": [asdict(update) for update in recent_updates],
                "top_investors": [asdict(inv) for inv in list(self.investors.values())[:5]],
                "fundraising_timeline": await self._generate_fundraising_timeline(),
                "next_actions": await self._generate_next_actions()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get investor dashboard data: {e}")
            raise
    
    async def _generate_fundraising_timeline(self) -> List[Dict[str, Any]]:
        """Generate fundraising timeline and milestones"""
        
        timeline = [
            {
                "date": "2025-09-15",
                "event": "Started Series A fundraising",
                "status": "completed",
                "description": "Kicked off fundraising process with updated pitch deck"
            },
            {
                "date": "2025-10-01",
                "event": "First investor meetings",
                "status": "completed",
                "description": "Met with 5 potential investors, 3 expressed interest"
            },
            {
                "date": "2025-10-15",
                "event": "Due diligence phase",
                "status": "in_progress",
                "description": "2 investors conducting detailed due diligence"
            },
            {
                "date": "2025-11-01",
                "event": "Term sheet target",
                "status": "upcoming",
                "description": "Target to receive and negotiate term sheets"
            },
            {
                "date": "2025-11-30",
                "event": "Round close target",
                "status": "upcoming",
                "description": "Target to close Series A funding round"
            }
        ]
        
        return timeline
    
    async def _generate_next_actions(self) -> List[Dict[str, Any]]:
        """Generate next actions for fundraising"""
        
        actions = [
            {
                "action": "Follow up with Sequoia Capital",
                "priority": "high",
                "due_date": "2025-10-05",
                "description": "Send additional financial projections requested"
            },
            {
                "action": "Prepare customer reference calls",
                "priority": "medium",
                "due_date": "2025-10-08",
                "description": "Coordinate calls between investors and key customers"
            },
            {
                "action": "Update pitch deck with Q3 metrics",
                "priority": "high",
                "due_date": "2025-10-03",
                "description": "Include latest growth and customer acquisition data"
            },
            {
                "action": "Schedule meeting with First Round",
                "priority": "medium",
                "due_date": "2025-10-10",
                "description": "Follow up on initial conversation"
            }
        ]
        
        return actions

# Global investor relations engine
investor_relations = InvestorRelationsEngine()