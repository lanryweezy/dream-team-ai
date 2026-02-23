"""
Investor Agent
Handles investor research, outreach, pitch deck creation, and fundraising
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from core.base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class InvestorAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="investor_research",
                description="Research and identify potential investors",
                cost_estimate=15.0,
                confidence_level=0.85,
                requirements=["company_stage", "industry", "funding_amount"]
            ),
            AgentCapability(
                name="pitch_deck_creation",
                description="Generate investor pitch decks and materials",
                cost_estimate=5.0,
                confidence_level=0.8,
                requirements=["company_data", "financial_projections"]
            ),
            AgentCapability(
                name="investor_outreach",
                description="Personalized outreach to investors",
                cost_estimate=20.0,
                confidence_level=0.75,
                requirements=["investor_list", "pitch_materials"]
            ),
            AgentCapability(
                name="fundraising_tracking",
                description="Track fundraising progress and metrics",
                cost_estimate=2.0,
                confidence_level=0.9,
                requirements=["investor_interactions"]
            ),
            AgentCapability(
                name="due_diligence_prep",
                description="Prepare due diligence materials",
                cost_estimate=10.0,
                confidence_level=0.85,
                requirements=["company_documents", "financial_records"]
            )
        ]
        
        super().__init__("investor_agent", capabilities)
        self.investor_database = {}
        self.pitch_materials = {}
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute investor-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "investor_research":
                return await self._research_investors(task)
            elif task_type == "pitch_deck_creation":
                return await self._create_pitch_deck(task)
            elif task_type == "investor_outreach":
                return await self._execute_investor_outreach(task)
            elif task_type == "fundraising_tracking":
                return await self._track_fundraising_progress(task)
            elif task_type == "due_diligence_prep":
                return await self._prepare_due_diligence(task)
            else:
                return TaskResult(
                    success=False,
                    output={},
                    cost_incurred=0.0,
                    evidence=[],
                    next_steps=[],
                    error_message=f"Unknown task type: {task_type}"
                )
                
        except Exception as e:
            logger.error(f"Investor task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _research_investors(self, task: Dict[str, Any]) -> TaskResult:
        """Research and identify potential investors"""
        company_stage = task.get("company_stage", "seed")
        industry = task.get("industry", "technology")
        funding_amount = task.get("funding_amount", 1000000)
        location = task.get("location", "global")
        
        # Check approval for research cost
        action = {
            "type": "investor_research",
            "funding_amount": funding_amount,
            "industry": industry
        }
        
        if not await self.request_approval(action, 15.0):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Investor research not approved"
            )
            
        # Research investors (this would integrate with investor databases)
        investors = await self._find_matching_investors(company_stage, industry, funding_amount, location)
        
        # Save investor research
        os.makedirs("investor_data", exist_ok=True)
        research_file = f"investor_data/research_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        research_data = {
            "search_criteria": {
                "company_stage": company_stage,
                "industry": industry,
                "funding_amount": funding_amount,
                "location": location
            },
            "investors": investors,
            "total_found": len(investors),
            "research_date": datetime.utcnow().isoformat()
        }
        
        with open(research_file, "w") as f:
            json.dump(research_data, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "investors_found": len(investors),
                "top_matches": investors[:10],  # Top 10 matches
                "research_file": research_file,
                "avg_check_size": sum(inv.get("typical_check_size", 0) for inv in investors) / len(investors) if investors else 0
            },
            cost_incurred=15.0,
            evidence=[research_file],
            next_steps=[
                "Review investor profiles",
                "Prioritize outreach list",
                "Prepare pitch materials",
                "Research warm introductions"
            ]
        )
        
    async def _find_matching_investors(self, stage: str, industry: str, amount: int, location: str) -> List[Dict[str, Any]]:
        """Find investors matching criteria (mock implementation)"""
        # In reality, this would query investor databases like Crunchbase, AngelList, etc.
        
        investor_types = {
            "pre_seed": ["angel_investors", "micro_vcs"],
            "seed": ["seed_funds", "angel_groups", "micro_vcs"],
            "series_a": ["series_a_funds", "growth_vcs"],
            "series_b": ["growth_vcs", "late_stage_funds"]
        }
        
        relevant_types = investor_types.get(stage, ["angel_investors"])
        
        investors = []
        for i in range(50):  # Generate 50 potential investors
            investor_type = relevant_types[i % len(relevant_types)]
            
            investor = {
                "id": f"investor_{i+1}",
                "name": f"{industry.title()} {investor_type.replace('_', ' ').title()} {i+1}",
                "type": investor_type,
                "focus_industries": [industry, "technology", "saas"],
                "focus_stages": [stage, "seed"] if stage != "seed" else ["pre_seed", "seed"],
                "typical_check_size": self._get_typical_check_size(investor_type, amount),
                "location": location if location != "global" else ["US", "Europe", "Global"][i % 3],
                "portfolio_companies": f"{20 + (i * 3)}",
                "recent_investments": f"{5 + (i % 10)}",
                "website": f"https://{investor_type.replace('_', '')}{i+1}.com",
                "linkedin": f"https://linkedin.com/company/{investor_type.replace('_', '')}{i+1}",
                "contact_email": f"investments@{investor_type.replace('_', '')}{i+1}.com",
                "investment_thesis": f"Focused on {industry} companies solving real-world problems",
                "match_score": min(100, 60 + (i % 40)),  # 60-100% match
                "last_investment_date": (datetime.utcnow() - timedelta(days=i*10)).isoformat(),
                "fund_size": f"${(i+1) * 10}M",
                "created_at": datetime.utcnow().isoformat()
            }
            investors.append(investor)
            
        # Sort by match score
        return sorted(investors, key=lambda x: x["match_score"], reverse=True)
        
    def _get_typical_check_size(self, investor_type: str, funding_amount: int) -> int:
        """Get typical check size based on investor type"""
        check_sizes = {
            "angel_investors": 25000,
            "micro_vcs": 100000,
            "seed_funds": 250000,
            "series_a_funds": 1000000,
            "growth_vcs": 2000000,
            "late_stage_funds": 5000000
        }
        
        base_size = check_sizes.get(investor_type, 50000)
        # Adjust based on funding amount
        return min(base_size, funding_amount // 10)
        
    async def _create_pitch_deck(self, task: Dict[str, Any]) -> TaskResult:
        """Create investor pitch deck"""
        company_data = task.get("company_data", {})
        financial_projections = task.get("financial_projections", {})
        deck_type = task.get("deck_type", "seed")
        
        # Generate pitch deck content
        pitch_deck = await self._generate_pitch_content(company_data, financial_projections, deck_type)
        
        # Save pitch deck
        os.makedirs("investor_materials", exist_ok=True)
        deck_file = f"investor_materials/pitch_deck_{deck_type}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(deck_file, "w") as f:
            json.dump(pitch_deck, f, indent=2)
            
        # Generate executive summary
        exec_summary = await self._generate_executive_summary(company_data, financial_projections)
        summary_file = f"investor_materials/executive_summary_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(summary_file, "w") as f:
            json.dump(exec_summary, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "pitch_deck": pitch_deck,
                "executive_summary": exec_summary,
                "deck_file": deck_file,
                "summary_file": summary_file,
                "slide_count": len(pitch_deck.get("slides", []))
            },
            cost_incurred=5.0,
            evidence=[deck_file, summary_file],
            next_steps=[
                "Review and refine pitch content",
                "Create visual presentation",
                "Practice pitch delivery",
                "Prepare for Q&A"
            ]
        )
        
    async def _generate_pitch_content(self, company_data: Dict, financials: Dict, deck_type: str) -> Dict[str, Any]:
        """Generate pitch deck content"""
        company_name = company_data.get("name", "DreamCorp")
        industry = company_data.get("industry", "Technology")
        
        slides = [
            {
                "slide_number": 1,
                "title": "Company Overview",
                "content": {
                    "company_name": company_name,
                    "tagline": company_data.get("tagline", f"Revolutionizing {industry}"),
                    "founded": company_data.get("founded", "2024"),
                    "location": company_data.get("location", "Global")
                }
            },
            {
                "slide_number": 2,
                "title": "Problem",
                "content": {
                    "problem_statement": company_data.get("problem", f"Current {industry.lower()} solutions are inefficient and costly"),
                    "market_pain_points": [
                        "High costs and complexity",
                        "Poor user experience",
                        "Limited scalability"
                    ],
                    "target_customers": company_data.get("target_customers", "SMBs and Enterprises")
                }
            },
            {
                "slide_number": 3,
                "title": "Solution",
                "content": {
                    "solution_overview": company_data.get("solution", f"AI-powered {industry.lower()} platform"),
                    "key_features": company_data.get("features", [
                        "Automated workflows",
                        "Real-time analytics",
                        "Seamless integrations"
                    ]),
                    "unique_value_prop": "10x faster, 50% cheaper, infinitely scalable"
                }
            },
            {
                "slide_number": 4,
                "title": "Market Opportunity",
                "content": {
                    "tam": financials.get("tam", "$100B"),
                    "sam": financials.get("sam", "$10B"),
                    "som": financials.get("som", "$1B"),
                    "market_growth_rate": "25% CAGR",
                    "market_trends": [
                        "Digital transformation acceleration",
                        "AI adoption increasing",
                        "Remote work normalization"
                    ]
                }
            },
            {
                "slide_number": 5,
                "title": "Business Model",
                "content": {
                    "revenue_model": company_data.get("revenue_model", "SaaS Subscription"),
                    "pricing_tiers": [
                        {"tier": "Starter", "price": "$99/month"},
                        {"tier": "Professional", "price": "$299/month"},
                        {"tier": "Enterprise", "price": "Custom"}
                    ],
                    "unit_economics": {
                        "ltv": "$12,000",
                        "cac": "$1,200",
                        "ltv_cac_ratio": "10:1"
                    }
                }
            },
            {
                "slide_number": 6,
                "title": "Traction",
                "content": {
                    "key_metrics": company_data.get("metrics", {
                        "users": "1,000+",
                        "revenue": "$50K ARR",
                        "growth_rate": "20% MoM"
                    }),
                    "milestones": [
                        "MVP launched",
                        "First paying customers",
                        "Product-market fit signals"
                    ],
                    "partnerships": company_data.get("partnerships", [])
                }
            },
            {
                "slide_number": 7,
                "title": "Financial Projections",
                "content": {
                    "revenue_forecast": financials.get("revenue_forecast", {
                        "year_1": "$500K",
                        "year_2": "$2M",
                        "year_3": "$8M"
                    }),
                    "key_assumptions": [
                        "Customer acquisition rate",
                        "Pricing model adoption",
                        "Market expansion"
                    ],
                    "funding_use": financials.get("funding_use", {
                        "product_development": "40%",
                        "sales_marketing": "35%",
                        "team_expansion": "20%",
                        "operations": "5%"
                    })
                }
            },
            {
                "slide_number": 8,
                "title": "Team",
                "content": {
                    "founders": company_data.get("founders", [
                        {"name": "Founder 1", "role": "CEO", "background": "10+ years industry experience"}
                    ]),
                    "key_team": company_data.get("team", []),
                    "advisors": company_data.get("advisors", []),
                    "hiring_plan": "Engineering and Sales focus"
                }
            },
            {
                "slide_number": 9,
                "title": "Funding Ask",
                "content": {
                    "funding_amount": financials.get("funding_amount", "$2M"),
                    "funding_stage": deck_type,
                    "use_of_funds": financials.get("funding_use", {}),
                    "timeline": "18-24 months runway",
                    "next_milestones": [
                        "Scale to $1M ARR",
                        "Expand team to 25 people",
                        "Launch enterprise features"
                    ]
                }
            },
            {
                "slide_number": 10,
                "title": "Contact",
                "content": {
                    "contact_info": {
                        "email": company_data.get("contact_email", "hello@dreamcorp.com"),
                        "website": company_data.get("website", "dreamcorp.com"),
                        "linkedin": company_data.get("linkedin", "linkedin.com/company/dreamcorp")
                    },
                    "call_to_action": "Let's build the future together"
                }
            }
        ]
        
        return {
            "deck_type": deck_type,
            "company_name": company_name,
            "created_at": datetime.utcnow().isoformat(),
            "slides": slides,
            "total_slides": len(slides)
        }
        
    async def _generate_executive_summary(self, company_data: Dict, financials: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            "company_name": company_data.get("name", "DreamCorp"),
            "executive_summary": f"""
            {company_data.get('name', 'DreamCorp')} is revolutionizing the {company_data.get('industry', 'technology')} 
            industry with our AI-powered platform. We're seeking ${financials.get('funding_amount', '$2M')} 
            to scale our proven solution and capture a significant share of the 
            ${financials.get('tam', '$100B')} market opportunity.
            
            Key Highlights:
            • Proven product-market fit with {company_data.get('metrics', {}).get('users', '1,000+')} users
            • Strong unit economics: LTV/CAC ratio of 10:1
            • Experienced team with deep industry expertise
            • Clear path to ${financials.get('revenue_forecast', {}).get('year_3', '$8M')} revenue by Year 3
            """,
            "investment_highlights": [
                "Large and growing market opportunity",
                "Differentiated technology solution",
                "Strong early traction and metrics",
                "Experienced founding team",
                "Clear monetization strategy"
            ],
            "funding_details": {
                "amount": financials.get("funding_amount", "$2M"),
                "stage": "Seed",
                "use_of_funds": financials.get("funding_use", {}),
                "timeline": "18-24 months"
            },
            "created_at": datetime.utcnow().isoformat()
        }
        
    async def _execute_investor_outreach(self, task: Dict[str, Any]) -> TaskResult:
        """Execute personalized investor outreach"""
        investor_list = task.get("investor_list", [])
        pitch_materials = task.get("pitch_materials", {})
        outreach_type = task.get("outreach_type", "email")
        
        if not investor_list:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Research investors first", "Import investor list"],
                error_message="No investors provided for outreach"
            )
            
        # Estimate cost based on outreach volume
        estimated_cost = len(investor_list) * 0.40  # $0.40 per investor outreach
        
        # Check approval for high-cost outreach
        action = {
            "type": "investor_outreach",
            "investor_count": len(investor_list),
            "outreach_type": outreach_type
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Investor outreach not approved"
            )
            
        # Execute outreach
        results = await self._send_investor_outreach(investor_list, pitch_materials, outreach_type)
        
        # Save outreach campaign
        os.makedirs("investor_data", exist_ok=True)
        campaign_file = f"investor_data/outreach_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M')}.json"
        
        campaign_data = {
            "outreach_type": outreach_type,
            "total_investors": len(investor_list),
            "sent": results["sent"],
            "failed": results["failed"],
            "results": results,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(campaign_file, "w") as f:
            json.dump(campaign_data, f, indent=2)
            
        return TaskResult(
            success=results["sent"] > 0,
            output={
                "outreach_type": outreach_type,
                "total_sent": results["sent"],
                "total_failed": results["failed"],
                "success_rate": (results["sent"] / len(investor_list) * 100) if investor_list else 0,
                "campaign_file": campaign_file,
                "expected_response_rate": "2-5%"
            },
            cost_incurred=results["sent"] * 0.40,
            evidence=[campaign_file],
            next_steps=[
                "Monitor response rates",
                "Follow up with interested investors",
                "Schedule pitch meetings",
                "Prepare due diligence materials"
            ]
        )
        
    async def _send_investor_outreach(self, investors: List[Dict], materials: Dict, outreach_type: str) -> Dict[str, Any]:
        """Send personalized outreach to investors"""
        sent = 0
        failed = 0
        results = []
        
        for investor in investors:
            try:
                # Personalize outreach message
                message = await self._personalize_investor_message(investor, materials)
                
                # Simulate sending (in reality, this would use email/LinkedIn APIs)
                success = await self._send_investor_message(investor, message, outreach_type)
                
                if success:
                    sent += 1
                    results.append({
                        "investor_id": investor.get("id"),
                        "investor_name": investor.get("name"),
                        "status": "sent",
                        "sent_at": datetime.utcnow().isoformat(),
                        "follow_up_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
                    })
                else:
                    failed += 1
                    results.append({
                        "investor_id": investor.get("id"),
                        "investor_name": investor.get("name"),
                        "status": "failed",
                        "error": "Delivery failed"
                    })
                    
            except Exception as e:
                failed += 1
                results.append({
                    "investor_id": investor.get("id"),
                    "investor_name": investor.get("name"),
                    "status": "failed",
                    "error": str(e)
                })
                
        return {
            "sent": sent,
            "failed": failed,
            "results": results
        }
        
    async def _personalize_investor_message(self, investor: Dict[str, Any], materials: Dict[str, Any]) -> str:
        """Personalize outreach message for specific investor"""
        template = """
        Subject: {company_name} - {industry} Investment Opportunity
        
        Hi {investor_name},
        
        I hope this email finds you well. I'm reaching out because {company_name} aligns perfectly with {investor_focus}.
        
        We're building {solution_brief} and have achieved {key_traction}. Given your investment in {portfolio_example}, 
        I believe you'd be interested in our approach to {problem_area}.
        
        Key highlights:
        • {highlight_1}
        • {highlight_2}  
        • {highlight_3}
        
        We're raising {funding_amount} to {funding_use}. Would you be open to a brief call to discuss how {company_name} 
        could be a strong addition to your portfolio?
        
        I've attached our executive summary for your review.
        
        Best regards,
        [Founder Name]
        {company_name}
        """
        
        # Extract data for personalization
        company_name = materials.get("company_name", "DreamCorp")
        
        personalized = template.format(
            company_name=company_name,
            industry=materials.get("industry", "Technology"),
            investor_name=investor.get("name", "").split()[0] if investor.get("name") else "there",
            investor_focus=", ".join(investor.get("focus_industries", ["technology"])[:2]),
            solution_brief=materials.get("solution_brief", "an AI-powered platform"),
            key_traction=materials.get("key_traction", "strong early adoption"),
            portfolio_example=f"companies in the {investor.get('focus_industries', ['technology'])[0]} space",
            problem_area=materials.get("problem_area", "industry inefficiencies"),
            highlight_1=materials.get("highlight_1", "Proven product-market fit"),
            highlight_2=materials.get("highlight_2", "Strong unit economics"),
            highlight_3=materials.get("highlight_3", "Experienced team"),
            funding_amount=materials.get("funding_amount", "$2M"),
            funding_use=materials.get("funding_use", "accelerate growth")
        )
        
        return personalized
        
    async def _send_investor_message(self, investor: Dict[str, Any], message: str, outreach_type: str) -> bool:
        """Send message to investor (mock implementation)"""
        # In reality, this would integrate with email/LinkedIn APIs
        # Simulate 70% success rate for investor outreach
        import random
        return random.random() < 0.70
        
    async def _track_fundraising_progress(self, task: Dict[str, Any]) -> TaskResult:
        """Track fundraising progress and metrics"""
        # Load fundraising data
        investor_files = []
        if os.path.exists("investor_data"):
            investor_files = [f for f in os.listdir("investor_data") if f.endswith(".json")]
            
        if not investor_files:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Start investor outreach first"],
                error_message="No fundraising data available"
            )
            
        # Analyze fundraising progress
        progress = await self._analyze_fundraising_progress(investor_files)
        
        # Save progress report
        progress_file = f"investor_data/progress_report_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(progress_file, "w") as f:
            json.dump(progress, f, indent=2)
            
        return TaskResult(
            success=True,
            output=progress,
            cost_incurred=2.0,
            evidence=[progress_file],
            next_steps=[
                "Follow up with interested investors",
                "Prepare for upcoming meetings",
                "Update pitch materials based on feedback"
            ]
        )
        
    async def _analyze_fundraising_progress(self, files: List[str]) -> Dict[str, Any]:
        """Analyze fundraising progress from data files"""
        total_outreach = 0
        total_responses = 0
        meetings_scheduled = 0
        
        # Mock analysis - in reality, would parse actual data
        for file in files:
            if "outreach" in file:
                total_outreach += 50  # Mock data
            elif "meetings" in file:
                meetings_scheduled += 5
                
        # Simulate some responses
        total_responses = int(total_outreach * 0.03)  # 3% response rate
        
        progress = {
            "fundraising_metrics": {
                "total_investors_contacted": total_outreach,
                "total_responses": total_responses,
                "response_rate": (total_responses / max(total_outreach, 1)) * 100,
                "meetings_scheduled": meetings_scheduled,
                "meetings_to_response_ratio": (meetings_scheduled / max(total_responses, 1)) * 100
            },
            "pipeline_status": {
                "initial_contact": total_outreach,
                "responded": total_responses,
                "meeting_scheduled": meetings_scheduled,
                "pitch_delivered": max(0, meetings_scheduled - 2),
                "due_diligence": max(0, meetings_scheduled - 4),
                "term_sheet": max(0, meetings_scheduled - 6)
            },
            "recommendations": [
                "Increase outreach volume if response rate is low",
                "Improve pitch materials based on feedback",
                "Focus on warm introductions",
                "Follow up consistently with interested investors"
            ],
            "next_actions": [
                "Schedule follow-up calls",
                "Prepare due diligence materials",
                "Refine pitch based on investor feedback"
            ],
            "analysis_date": datetime.utcnow().isoformat()
        }
        
        return progress
        
    async def _prepare_due_diligence(self, task: Dict[str, Any]) -> TaskResult:
        """Prepare due diligence materials"""
        company_documents = task.get("company_documents", {})
        financial_records = task.get("financial_records", {})
        
        # Create due diligence checklist and materials
        dd_materials = await self._create_dd_materials(company_documents, financial_records)
        
        # Save due diligence package
        os.makedirs("investor_materials/due_diligence", exist_ok=True)
        dd_file = f"investor_materials/due_diligence/dd_package_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(dd_file, "w") as f:
            json.dump(dd_materials, f, indent=2)
            
        return TaskResult(
            success=True,
            output=dd_materials,
            cost_incurred=10.0,
            evidence=[dd_file],
            next_steps=[
                "Review all documents for completeness",
                "Setup secure data room",
                "Prepare management presentations",
                "Brief legal team on investor questions"
            ]
        )
        
    async def _create_dd_materials(self, company_docs: Dict, financial_records: Dict) -> Dict[str, Any]:
        """Create due diligence materials package"""
        return {
            "due_diligence_checklist": {
                "corporate_documents": [
                    "Certificate of Incorporation",
                    "Bylaws",
                    "Cap Table",
                    "Board Resolutions",
                    "Shareholder Agreements"
                ],
                "financial_documents": [
                    "Financial Statements (3 years)",
                    "Management Reports",
                    "Budget and Forecasts",
                    "Audit Reports",
                    "Tax Returns"
                ],
                "legal_documents": [
                    "Material Contracts",
                    "IP Portfolio",
                    "Employment Agreements",
                    "Compliance Records",
                    "Litigation History"
                ],
                "business_documents": [
                    "Business Plan",
                    "Market Research",
                    "Customer References",
                    "Competitive Analysis",
                    "Technology Documentation"
                ]
            },
            "data_room_structure": {
                "01_Corporate": ["incorporation_docs", "governance", "cap_table"],
                "02_Financial": ["statements", "projections", "budgets"],
                "03_Legal": ["contracts", "ip", "compliance"],
                "04_Business": ["strategy", "market", "customers"],
                "05_Technology": ["architecture", "security", "roadmap"]
            },
            "management_presentation": {
                "agenda": [
                    "Company Overview",
                    "Market Opportunity", 
                    "Business Model",
                    "Financial Performance",
                    "Technology Platform",
                    "Team and Organization",
                    "Growth Strategy",
                    "Risk Factors",
                    "Q&A Session"
                ],
                "duration": "90 minutes",
                "attendees": ["CEO", "CTO", "CFO", "Key Team Members"]
            },
            "prepared_date": datetime.utcnow().isoformat(),
            "completion_status": "Ready for investor review"
        }
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily investor relations goals"""
        return [
            {
                "goal": "Follow up with investors from recent outreach",
                "priority": "high",
                "estimated_time": "1 hour"
            },
            {
                "goal": "Research new potential investors",
                "priority": "medium", 
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Update fundraising pipeline and metrics",
                "priority": "medium",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Prepare for upcoming investor meetings",
                "priority": "high",
                "estimated_time": "1 hour"
            }
        ]

# Example usage
async def main():
    """Example usage of InvestorAgent"""
    agent = InvestorAgent()
    await agent.start()
    
    # Test investor research
    task = {
        "type": "investor_research",
        "company_stage": "seed",
        "industry": "fintech",
        "funding_amount": 2000000,
        "location": "US"
    }
    
    result = await agent.execute_task(task)
    print("Investor research result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())Investor Agent
Handles investor research, outreach, pitch deck creation, and fundraising
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from core.base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class InvestorAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="investor_research",
                description="Research and identify potential investors",
                cost_estimate=15.0,
                confidence_level=0.85,
                requirements=["company_stage", "industry", "funding_amount"]
            ),
            AgentCapability(
                name="pitch_deck_creation",
                description="Generate investor pitch decks and materials",
                cost_estimate=5.0,
                confidence_level=0.8,
                requirements=["company_data", "financial_projections"]
            ),
            AgentCapability(
                name="investor_outreach",
                description="Personalized outreach to investors",
                cost_estimate=20.0,
                confidence_level=0.75,
                requirements=["investor_list", "pitch_materials"]
            ),
            AgentCapability(
                name="fundraising_tracking",
                description="Track fundraising progress and metrics",
                cost_estimate=2.0,
                confidence_level=0.9,
                requirements=["investor_interactions"]
            ),
            AgentCapability(
                name="due_diligence_prep",
                description="Prepare due diligence materials",
                cost_estimate=10.0,
                confidence_level=0.85,
                requirements=["company_documents", "financial_records"]
            )
        ]
        
        super().__init__("investor_agent", capabilities)
        self.investor_database = {}
        self.pitch_materials = {}
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute investor-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "investor_research":
                return await self._research_investors(task)
            elif task_type == "pitch_deck_creation":
                return await self._create_pitch_deck(task)
            elif task_type == "investor_outreach":
                return await self._execute_investor_outreach(task)
            elif task_type == "fundraising_tracking":
                return await self._track_fundraising_progress(task)
            elif task_type == "due_diligence_prep":
                return await self._prepare_due_diligence(task)
            else:
                return TaskResult(
                    success=False,
                    output={},
                    cost_incurred=0.0,
                    evidence=[],
                    next_steps=[],
                    error_message=f"Unknown task type: {task_type}"
                )
                
        except Exception as e:
            logger.error(f"Investor task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _research_investors(self, task: Dict[str, Any]) -> TaskResult:
        """Research and identify potential investors"""
        company_stage = task.get("company_stage", "seed")
        industry = task.get("industry", "technology")
        funding_amount = task.get("funding_amount", 1000000)
        location = task.get("location", "global")
        
        # Check approval for research cost
        action = {
            "type": "investor_research",
            "funding_amount": funding_amount,
            "industry": industry
        }
        
        if not await self.request_approval(action, 15.0):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Investor research not approved"
            )
            
        # Research investors (this would integrate with investor databases)
        investors = await self._find_matching_investors(company_stage, industry, funding_amount, location)
        
        # Save investor research
        os.makedirs("investor_data", exist_ok=True)
        research_file = f"investor_data/research_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        research_data = {
            "search_criteria": {
                "company_stage": company_stage,
                "industry": industry,
                "funding_amount": funding_amount,
                "location": location
            },
            "investors": investors,
            "total_found": len(investors),
            "research_date": datetime.utcnow().isoformat()
        }
        
        with open(research_file, "w") as f:
            json.dump(research_data, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "investors_found": len(investors),
                "top_matches": investors[:10],  # Top 10 matches
                "research_file": research_file,
                "avg_check_size": sum(inv.get("typical_check_size", 0) for inv in investors) / len(investors) if investors else 0
            },
            cost_incurred=15.0,
            evidence=[research_file],
            next_steps=[
                "Review investor profiles",
                "Prioritize outreach list",
                "Prepare pitch materials",
                "Research warm introductions"
            ]
        )
        
    async def _find_matching_investors(self, stage: str, industry: str, amount: int, location: str) -> List[Dict[str, Any]]:
        """Find investors matching criteria (mock implementation)"""
        # In reality, this would query investor databases like Crunchbase, AngelList, etc.
        
        investor_types = {
            "pre_seed": ["angel_investors", "micro_vcs"],
            "seed": ["seed_funds", "angel_groups", "micro_vcs"],
            "series_a": ["series_a_funds", "growth_vcs"],
            "series_b": ["growth_vcs", "late_stage_funds"]
        }
        
        relevant_types = investor_types.get(stage, ["angel_investors"])
        
        investors = []
        for i in range(50):  # Generate 50 potential investors
            investor_type = relevant_types[i % len(relevant_types)]
            
            investor = {
                "id": f"investor_{i+1}",
                "name": f"{industry.title()} {investor_type.replace('_', ' ').title()} {i+1}",
                "type": investor_type,
                "focus_industries": [industry, "technology", "saas"],
                "focus_stages": [stage, "seed"] if stage != "seed" else ["pre_seed", "seed"],
                "typical_check_size": self._get_typical_check_size(investor_type, amount),
                "location": location if location != "global" else ["US", "Europe", "Global"][i % 3],
                "portfolio_companies": f"{20 + (i * 3)}",
                "recent_investments": f"{5 + (i % 10)}",
                "website": f"https://{investor_type.replace('_', '')}{i+1}.com",
                "linkedin": f"https://linkedin.com/company/{investor_type.replace('_', '')}{i+1}",
                "contact_email": f"investments@{investor_type.replace('_', '')}{i+1}.com",
                "investment_thesis": f"Focused on {industry} companies solving real-world problems",
                "match_score": min(100, 60 + (i % 40)),  # 60-100% match
                "last_investment_date": (datetime.utcnow() - timedelta(days=i*10)).isoformat(),
                "fund_size": f"${(i+1) * 10}M",
                "created_at": datetime.utcnow().isoformat()
            }
            investors.append(investor)
            
        # Sort by match score
        return sorted(investors, key=lambda x: x["match_score"], reverse=True)
        
    def _get_typical_check_size(self, investor_type: str, funding_amount: int) -> int:
        """Get typical check size based on investor type"""
        check_sizes = {
            "angel_investors": 25000,
            "micro_vcs": 100000,
            "seed_funds": 250000,
            "series_a_funds": 1000000,
            "growth_vcs": 2000000,
            "late_stage_funds": 5000000
        }
        
        base_size = check_sizes.get(investor_type, 50000)
        # Adjust based on funding amount
        return min(base_size, funding_amount // 10)
        
    async def _create_pitch_deck(self, task: Dict[str, Any]) -> TaskResult:
        """Create investor pitch deck"""
        company_data = task.get("company_data", {})
        financial_projections = task.get("financial_projections", {})
        deck_type = task.get("deck_type", "seed")
        
        # Generate pitch deck content
        pitch_deck = await self._generate_pitch_content(company_data, financial_projections, deck_type)
        
        # Save pitch deck
        os.makedirs("investor_materials", exist_ok=True)
        deck_file = f"investor_materials/pitch_deck_{deck_type}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(deck_file, "w") as f:
            json.dump(pitch_deck, f, indent=2)
            
        # Generate executive summary
        exec_summary = await self._generate_executive_summary(company_data, financial_projections)
        summary_file = f"investor_materials/executive_summary_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(summary_file, "w") as f:
            json.dump(exec_summary, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "pitch_deck": pitch_deck,
                "executive_summary": exec_summary,
                "deck_file": deck_file,
                "summary_file": summary_file,
                "slide_count": len(pitch_deck.get("slides", []))
            },
            cost_incurred=5.0,
            evidence=[deck_file, summary_file],
            next_steps=[
                "Review and refine pitch content",
                "Create visual presentation",
                "Practice pitch delivery",
                "Prepare for Q&A"
            ]
        )
        
    async def _generate_pitch_content(self, company_data: Dict, financials: Dict, deck_type: str) -> Dict[str, Any]:
        """Generate pitch deck content"""
        company_name = company_data.get("name", "DreamCorp")
        industry = company_data.get("industry", "Technology")
        
        slides = [
            {
                "slide_number": 1,
                "title": "Company Overview",
                "content": {
                    "company_name": company_name,
                    "tagline": company_data.get("tagline", f"Revolutionizing {industry}"),
                    "founded": company_data.get("founded", "2024"),
                    "location": company_data.get("location", "Global")
                }
            },
            {
                "slide_number": 2,
                "title": "Problem",
                "content": {
                    "problem_statement": company_data.get("problem", f"Current {industry.lower()} solutions are inefficient and costly"),
                    "market_pain_points": [
                        "High costs and complexity",
                        "Poor user experience",
                        "Limited scalability"
                    ],
                    "target_customers": company_data.get("target_customers", "SMBs and Enterprises")
                }
            },
            {
                "slide_number": 3,
                "title": "Solution",
                "content": {
                    "solution_overview": company_data.get("solution", f"AI-powered {industry.lower()} platform"),
                    "key_features": company_data.get("features", [
                        "Automated workflows",
                        "Real-time analytics",
                        "Seamless integrations"
                    ]),
                    "unique_value_prop": "10x faster, 50% cheaper, infinitely scalable"
                }
            },
            {
                "slide_number": 4,
                "title": "Market Opportunity",
                "content": {
                    "tam": financials.get("tam", "$100B"),
                    "sam": financials.get("sam", "$10B"),
                    "som": financials.get("som", "$1B"),
                    "market_growth_rate": "25% CAGR",
                    "market_trends": [
                        "Digital transformation acceleration",
                        "AI adoption increasing",
                        "Remote work normalization"
                    ]
                }
            },
            {
                "slide_number": 5,
                "title": "Business Model",
                "content": {
                    "revenue_model": company_data.get("revenue_model", "SaaS Subscription"),
                    "pricing_tiers": [
                        {"tier": "Starter", "price": "$99/month"},
                        {"tier": "Professional", "price": "$299/month"},
                        {"tier": "Enterprise", "price": "Custom"}
                    ],
                    "unit_economics": {
                        "ltv": "$12,000",
                        "cac": "$1,200",
                        "ltv_cac_ratio": "10:1"
                    }
                }
            },
            {
                "slide_number": 6,
                "title": "Traction",
                "content": {
                    "key_metrics": company_data.get("metrics", {
                        "users": "1,000+",
                        "revenue": "$50K ARR",
                        "growth_rate": "20% MoM"
                    }),
                    "milestones": [
                        "MVP launched",
                        "First paying customers",
                        "Product-market fit signals"
                    ],
                    "partnerships": company_data.get("partnerships", [])
                }
            },
            {
                "slide_number": 7,
                "title": "Financial Projections",
                "content": {
                    "revenue_forecast": financials.get("revenue_forecast", {
                        "year_1": "$500K",
                        "year_2": "$2M",
                        "year_3": "$8M"
                    }),
                    "key_assumptions": [
                        "Customer acquisition rate",
                        "Pricing model adoption",
                        "Market expansion"
                    ],
                    "funding_use": financials.get("funding_use", {
                        "product_development": "40%",
                        "sales_marketing": "35%",
                        "team_expansion": "20%",
                        "operations": "5%"
                    })
                }
            },
            {
                "slide_number": 8,
                "title": "Team",
                "content": {
                    "founders": company_data.get("founders", [
                        {"name": "Founder 1", "role": "CEO", "background": "10+ years industry experience"}
                    ]),
                    "key_team": company_data.get("team", []),
                    "advisors": company_data.get("advisors", []),
                    "hiring_plan": "Engineering and Sales focus"
                }
            },
            {
                "slide_number": 9,
                "title": "Funding Ask",
                "content": {
                    "funding_amount": financials.get("funding_amount", "$2M"),
                    "funding_stage": deck_type,
                    "use_of_funds": financials.get("funding_use", {}),
                    "timeline": "18-24 months runway",
                    "next_milestones": [
                        "Scale to $1M ARR",
                        "Expand team to 25 people",
                        "Launch enterprise features"
                    ]
                }
            },
            {
                "slide_number": 10,
                "title": "Contact",
                "content": {
                    "contact_info": {
                        "email": company_data.get("contact_email", "hello@dreamcorp.com"),
                        "website": company_data.get("website", "dreamcorp.com"),
                        "linkedin": company_data.get("linkedin", "linkedin.com/company/dreamcorp")
                    },
                    "call_to_action": "Let's build the future together"
                }
            }
        ]
        
        return {
            "deck_type": deck_type,
            "company_name": company_name,
            "created_at": datetime.utcnow().isoformat(),
            "slides": slides,
            "total_slides": len(slides)
        }
        
    async def _generate_executive_summary(self, company_data: Dict, financials: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            "company_name": company_data.get("name", "DreamCorp"),
            "executive_summary": f"""
            {company_data.get('name', 'DreamCorp')} is revolutionizing the {company_data.get('industry', 'technology')} 
            industry with our AI-powered platform. We're seeking ${financials.get('funding_amount', '$2M')} 
            to scale our proven solution and capture a significant share of the 
            ${financials.get('tam', '$100B')} market opportunity.
            
            Key Highlights:
            • Proven product-market fit with {company_data.get('metrics', {}).get('users', '1,000+')} users
            • Strong unit economics: LTV/CAC ratio of 10:1
            • Experienced team with deep industry expertise
            • Clear path to ${financials.get('revenue_forecast', {}).get('year_3', '$8M')} revenue by Year 3
            """,
            "investment_highlights": [
                "Large and growing market opportunity",
                "Differentiated technology solution",
                "Strong early traction and metrics",
                "Experienced founding team",
                "Clear monetization strategy"
            ],
            "funding_details": {
                "amount": financials.get("funding_amount", "$2M"),
                "stage": "Seed",
                "use_of_funds": financials.get("funding_use", {}),
                "timeline": "18-24 months"
            },
            "created_at": datetime.utcnow().isoformat()
        }
        
    async def _execute_investor_outreach(self, task: Dict[str, Any]) -> TaskResult:
        """Execute personalized investor outreach"""
        investor_list = task.get("investor_list", [])
        pitch_materials = task.get("pitch_materials", {})
        outreach_type = task.get("outreach_type", "email")
        
        if not investor_list:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Research investors first", "Import investor list"],
                error_message="No investors provided for outreach"
            )
            
        # Estimate cost based on outreach volume
        estimated_cost = len(investor_list) * 0.40  # $0.40 per investor outreach
        
        # Check approval for high-cost outreach
        action = {
            "type": "investor_outreach",
            "investor_count": len(investor_list),
            "outreach_type": outreach_type
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Investor outreach not approved"
            )
            
        # Execute outreach
        results = await self._send_investor_outreach(investor_list, pitch_materials, outreach_type)
        
        # Save outreach campaign
        os.makedirs("investor_data", exist_ok=True)
        campaign_file = f"investor_data/outreach_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M')}.json"
        
        campaign_data = {
            "outreach_type": outreach_type,
            "total_investors": len(investor_list),
            "sent": results["sent"],
            "failed": results["failed"],
            "results": results,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(campaign_file, "w") as f:
            json.dump(campaign_data, f, indent=2)
            
        return TaskResult(
            success=results["sent"] > 0,
            output={
                "outreach_type": outreach_type,
                "total_sent": results["sent"],
                "total_failed": results["failed"],
                "success_rate": (results["sent"] / len(investor_list) * 100) if investor_list else 0,
                "campaign_file": campaign_file,
                "expected_response_rate": "2-5%"
            },
            cost_incurred=results["sent"] * 0.40,
            evidence=[campaign_file],
            next_steps=[
                "Monitor response rates",
                "Follow up with interested investors",
                "Schedule pitch meetings",
                "Prepare due diligence materials"
            ]
        )
        
    async def _send_investor_outreach(self, investors: List[Dict], materials: Dict, outreach_type: str) -> Dict[str, Any]:
        """Send personalized outreach to investors"""
        sent = 0
        failed = 0
        results = []
        
        for investor in investors:
            try:
                # Personalize outreach message
                message = await self._personalize_investor_message(investor, materials)
                
                # Simulate sending (in reality, this would use email/LinkedIn APIs)
                success = await self._send_investor_message(investor, message, outreach_type)
                
                if success:
                    sent += 1
                    results.append({
                        "investor_id": investor.get("id"),
                        "investor_name": investor.get("name"),
                        "status": "sent",
                        "sent_at": datetime.utcnow().isoformat(),
                        "follow_up_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
                    })
                else:
                    failed += 1
                    results.append({
                        "investor_id": investor.get("id"),
                        "investor_name": investor.get("name"),
                        "status": "failed",
                        "error": "Delivery failed"
                    })
                    
            except Exception as e:
                failed += 1
                results.append({
                    "investor_id": investor.get("id"),
                    "investor_name": investor.get("name"),
                    "status": "failed",
                    "error": str(e)
                })
                
        return {
            "sent": sent,
            "failed": failed,
            "results": results
        }
        
    async def _personalize_investor_message(self, investor: Dict[str, Any], materials: Dict[str, Any]) -> str:
        """Personalize outreach message for specific investor"""
        template = """
        Subject: {company_name} - {industry} Investment Opportunity
        
        Hi {investor_name},
        
        I hope this email finds you well. I'm reaching out because {company_name} aligns perfectly with {investor_focus}.
        
        We're building {solution_brief} and have achieved {key_traction}. Given your investment in {portfolio_example}, 
        I believe you'd be interested in our approach to {problem_area}.
        
        Key highlights:
        • {highlight_1}
        • {highlight_2}  
        • {highlight_3}
        
        We're raising {funding_amount} to {funding_use}. Would you be open to a brief call to discuss how {company_name} 
        could be a strong addition to your portfolio?
        
        I've attached our executive summary for your review.
        
        Best regards,
        [Founder Name]
        {company_name}
        """
        
        # Extract data for personalization
        company_name = materials.get("company_name", "DreamCorp")
        
        personalized = template.format(
            company_name=company_name,
            industry=materials.get("industry", "Technology"),
            investor_name=investor.get("name", "").split()[0] if investor.get("name") else "there",
            investor_focus=", ".join(investor.get("focus_industries", ["technology"])[:2]),
            solution_brief=materials.get("solution_brief", "an AI-powered platform"),
            key_traction=materials.get("key_traction", "strong early adoption"),
            portfolio_example=f"companies in the {investor.get('focus_industries', ['technology'])[0]} space",
            problem_area=materials.get("problem_area", "industry inefficiencies"),
            highlight_1=materials.get("highlight_1", "Proven product-market fit"),
            highlight_2=materials.get("highlight_2", "Strong unit economics"),
            highlight_3=materials.get("highlight_3", "Experienced team"),
            funding_amount=materials.get("funding_amount", "$2M"),
            funding_use=materials.get("funding_use", "accelerate growth")
        )
        
        return personalized
        
    async def _send_investor_message(self, investor: Dict[str, Any], message: str, outreach_type: str) -> bool:
        """Send message to investor (mock implementation)"""
        # In reality, this would integrate with email/LinkedIn APIs
        # Simulate 70% success rate for investor outreach
        import random
        return random.random() < 0.70
        
    async def _track_fundraising_progress(self, task: Dict[str, Any]) -> TaskResult:
        """Track fundraising progress and metrics"""
        # Load fundraising data
        investor_files = []
        if os.path.exists("investor_data"):
            investor_files = [f for f in os.listdir("investor_data") if f.endswith(".json")]
            
        if not investor_files:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Start investor outreach first"],
                error_message="No fundraising data available"
            )
            
        # Analyze fundraising progress
        progress = await self._analyze_fundraising_progress(investor_files)
        
        # Save progress report
        progress_file = f"investor_data/progress_report_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(progress_file, "w") as f:
            json.dump(progress, f, indent=2)
            
        return TaskResult(
            success=True,
            output=progress,
            cost_incurred=2.0,
            evidence=[progress_file],
            next_steps=[
                "Follow up with interested investors",
                "Prepare for upcoming meetings",
                "Update pitch materials based on feedback"
            ]
        )
        
    async def _analyze_fundraising_progress(self, files: List[str]) -> Dict[str, Any]:
        """Analyze fundraising progress from data files"""
        total_outreach = 0
        total_responses = 0
        meetings_scheduled = 0
        
        # Mock analysis - in reality, would parse actual data
        for file in files:
            if "outreach" in file:
                total_outreach += 50  # Mock data
            elif "meetings" in file:
                meetings_scheduled += 5
                
        # Simulate some responses
        total_responses = int(total_outreach * 0.03)  # 3% response rate
        
        progress = {
            "fundraising_metrics": {
                "total_investors_contacted": total_outreach,
                "total_responses": total_responses,
                "response_rate": (total_responses / max(total_outreach, 1)) * 100,
                "meetings_scheduled": meetings_scheduled,
                "meetings_to_response_ratio": (meetings_scheduled / max(total_responses, 1)) * 100
            },
            "pipeline_status": {
                "initial_contact": total_outreach,
                "responded": total_responses,
                "meeting_scheduled": meetings_scheduled,
                "pitch_delivered": max(0, meetings_scheduled - 2),
                "due_diligence": max(0, meetings_scheduled - 4),
                "term_sheet": max(0, meetings_scheduled - 6)
            },
            "recommendations": [
                "Increase outreach volume if response rate is low",
                "Improve pitch materials based on feedback",
                "Focus on warm introductions",
                "Follow up consistently with interested investors"
            ],
            "next_actions": [
                "Schedule follow-up calls",
                "Prepare due diligence materials",
                "Refine pitch based on investor feedback"
            ],
            "analysis_date": datetime.utcnow().isoformat()
        }
        
        return progress
        
    async def _prepare_due_diligence(self, task: Dict[str, Any]) -> TaskResult:
        """Prepare due diligence materials"""
        company_documents = task.get("company_documents", {})
        financial_records = task.get("financial_records", {})
        
        # Create due diligence checklist and materials
        dd_materials = await self._create_dd_materials(company_documents, financial_records)
        
        # Save due diligence package
        os.makedirs("investor_materials/due_diligence", exist_ok=True)
        dd_file = f"investor_materials/due_diligence/dd_package_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(dd_file, "w") as f:
            json.dump(dd_materials, f, indent=2)
            
        return TaskResult(
            success=True,
            output=dd_materials,
            cost_incurred=10.0,
            evidence=[dd_file],
            next_steps=[
                "Review all documents for completeness",
                "Setup secure data room",
                "Prepare management presentations",
                "Brief legal team on investor questions"
            ]
        )
        
    async def _create_dd_materials(self, company_docs: Dict, financial_records: Dict) -> Dict[str, Any]:
        """Create due diligence materials package"""
        return {
            "due_diligence_checklist": {
                "corporate_documents": [
                    "Certificate of Incorporation",
                    "Bylaws",
                    "Cap Table",
                    "Board Resolutions",
                    "Shareholder Agreements"
                ],
                "financial_documents": [
                    "Financial Statements (3 years)",
                    "Management Reports",
                    "Budget and Forecasts",
                    "Audit Reports",
                    "Tax Returns"
                ],
                "legal_documents": [
                    "Material Contracts",
                    "IP Portfolio",
                    "Employment Agreements",
                    "Compliance Records",
                    "Litigation History"
                ],
                "business_documents": [
                    "Business Plan",
                    "Market Research",
                    "Customer References",
                    "Competitive Analysis",
                    "Technology Documentation"
                ]
            },
            "data_room_structure": {
                "01_Corporate": ["incorporation_docs", "governance", "cap_table"],
                "02_Financial": ["statements", "projections", "budgets"],
                "03_Legal": ["contracts", "ip", "compliance"],
                "04_Business": ["strategy", "market", "customers"],
                "05_Technology": ["architecture", "security", "roadmap"]
            },
            "management_presentation": {
                "agenda": [
                    "Company Overview",
                    "Market Opportunity", 
                    "Business Model",
                    "Financial Performance",
                    "Technology Platform",
                    "Team and Organization",
                    "Growth Strategy",
                    "Risk Factors",
                    "Q&A Session"
                ],
                "duration": "90 minutes",
                "attendees": ["CEO", "CTO", "CFO", "Key Team Members"]
            },
            "prepared_date": datetime.utcnow().isoformat(),
            "completion_status": "Ready for investor review"
        }
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily investor relations goals"""
        return [
            {
                "goal": "Follow up with investors from recent outreach",
                "priority": "high",
                "estimated_time": "1 hour"
            },
            {
                "goal": "Research new potential investors",
                "priority": "medium", 
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Update fundraising pipeline and metrics",
                "priority": "medium",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Prepare for upcoming investor meetings",
                "priority": "high",
                "estimated_time": "1 hour"
            }
        ]

# Example usage
async def main():
    """Example usage of InvestorAgent"""
    agent = InvestorAgent()
    await agent.start()
    
    # Test investor research
    task = {
        "type": "investor_research",
        "company_stage": "seed",
        "industry": "fintech",
        "funding_amount": 2000000,
        "location": "US"
    }
    
    result = await agent.execute_task(task)
    print("Investor research result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())