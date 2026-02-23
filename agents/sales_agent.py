"""
Sales Agent
Handles lead generation, outreach, CRM management, and sales processes
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

from core.base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class SalesAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="lead_generation",
                description="Find and qualify potential customers",
                cost_estimate=5.0,
                confidence_level=0.8,
                requirements=["target_market", "search_criteria"]
            ),
            AgentCapability(
                name="outreach_campaign",
                description="Execute personalized outreach campaigns",
                cost_estimate=10.0,
                confidence_level=0.85,
                requirements=["lead_list", "message_templates"]
            ),
            AgentCapability(
                name="crm_management",
                description="Manage customer relationships and pipeline",
                cost_estimate=2.0,
                confidence_level=0.9,
                requirements=["contact_data"]
            ),
            AgentCapability(
                name="follow_up_automation",
                description="Automate follow-up sequences",
                cost_estimate=3.0,
                confidence_level=0.9,
                requirements=["contact_list", "follow_up_schedule"]
            ),
            AgentCapability(
                name="sales_analytics",
                description="Analyze sales performance and metrics",
                cost_estimate=1.0,
                confidence_level=0.85,
                requirements=["sales_data"]
            )
        ]
        
        super().__init__("sales_agent", capabilities)
        self.crm_data = {}
        self.outreach_templates = {}
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute sales tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "lead_generation":
                return await self._generate_leads(task)
            elif task_type == "outreach_campaign":
                return await self._run_outreach_campaign(task)
            elif task_type == "crm_management":
                return await self._manage_crm(task)
            elif task_type == "follow_up_automation":
                return await self._setup_follow_ups(task)
            elif task_type == "sales_analytics":
                return await self._analyze_sales_performance(task)
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
            logger.error(f"Sales task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _generate_leads(self, task: Dict[str, Any]) -> TaskResult:
        """Generate leads based on target criteria"""
        target_market = task.get("target_market", {})
        search_criteria = task.get("search_criteria", {})
        lead_count = task.get("lead_count", 50)
        
        # Check approval for lead generation cost
        action = {
            "type": "lead_generation",
            "lead_count": lead_count,
            "target_market": target_market.get("industry", "general")
        }
        
        estimated_cost = lead_count * 0.10  # $0.10 per lead
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Lead generation not approved"
            )
            
        # Generate leads (this would integrate with lead generation APIs)
        leads = await self._search_leads(target_market, search_criteria, lead_count)
        
        # Save leads to CRM
        leads_file = f"sales_data/leads_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        os.makedirs("sales_data", exist_ok=True)
        
        with open(leads_file, "w") as f:
            json.dump(leads, f, indent=2)
            
        # Record cost
        actual_cost = len(leads) * 0.10
        self.cost_tracker.record_expense("lead_generation", actual_cost)
        
        return TaskResult(
            success=True,
            output={
                "leads_generated": len(leads),
                "leads_file": leads_file,
                "target_market": target_market,
                "qualified_leads": len([l for l in leads if l.get("qualified", False)])
            },
            cost_incurred=actual_cost,
            evidence=[leads_file],
            next_steps=[
                "Review and qualify leads",
                "Create outreach sequences",
                "Setup CRM tracking"
            ]
        )
        
    async def _search_leads(self, target_market: Dict[str, Any], criteria: Dict[str, Any], count: int) -> List[Dict[str, Any]]:
        """Search for leads based on criteria (mock implementation)"""
        industry = target_market.get("industry", "technology")
        company_size = criteria.get("company_size", "startup")
        location = criteria.get("location", "global")
        
        # Mock lead generation - in reality, this would use APIs like Apollo, ZoomInfo, etc.
        leads = []
        
        for i in range(count):
            lead = {
                "id": f"lead_{datetime.utcnow().timestamp()}_{i}",
                "company_name": f"{industry.title()} Corp {i+1}",
                "contact_name": f"John Doe {i+1}",
                "email": f"john.doe{i+1}@{industry}corp{i+1}.com",
                "title": "CEO" if i % 3 == 0 else "CTO" if i % 3 == 1 else "Founder",
                "company_size": company_size,
                "industry": industry,
                "location": location,
                "linkedin_url": f"https://linkedin.com/in/johndoe{i+1}",
                "company_website": f"https://{industry}corp{i+1}.com",
                "qualified": i % 4 == 0,  # 25% qualified rate
                "lead_score": min(100, 20 + (i % 80)),
                "source": "lead_generation_api",
                "created_at": datetime.utcnow().isoformat()
            }
            leads.append(lead)
            
        return leads
        
    async def _run_outreach_campaign(self, task: Dict[str, Any]) -> TaskResult:
        """Run personalized outreach campaign"""
        lead_list = task.get("lead_list", [])
        campaign_type = task.get("campaign_type", "email")
        message_template = task.get("message_template", "")
        
        if not lead_list:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Generate leads first", "Import lead list"],
                error_message="No leads provided for outreach"
            )
            
        # Estimate cost based on outreach volume
        estimated_cost = len(lead_list) * 0.05  # $0.05 per outreach
        
        # Check approval
        action = {
            "type": "outreach_campaign",
            "campaign_type": campaign_type,
            "lead_count": len(lead_list)
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Outreach campaign not approved"
            )
            
        # Execute outreach
        results = await self._execute_outreach(lead_list, campaign_type, message_template)
        
        # Save campaign results
        campaign_file = f"sales_data/campaign_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M')}.json"
        
        campaign_data = {
            "campaign_type": campaign_type,
            "total_leads": len(lead_list),
            "sent": results["sent"],
            "failed": results["failed"],
            "results": results,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(campaign_file, "w") as f:
            json.dump(campaign_data, f, indent=2)
            
        # Record cost
        actual_cost = results["sent"] * 0.05
        self.cost_tracker.record_expense("outreach_campaign", actual_cost)
        
        return TaskResult(
            success=results["sent"] > 0,
            output={
                "campaign_type": campaign_type,
                "total_sent": results["sent"],
                "total_failed": results["failed"],
                "success_rate": (results["sent"] / len(lead_list) * 100) if lead_list else 0,
                "campaign_file": campaign_file
            },
            cost_incurred=actual_cost,
            evidence=[campaign_file],
            next_steps=[
                "Monitor response rates",
                "Setup follow-up sequences",
                "Track engagement metrics"
            ]
        )
        
    async def _execute_outreach(self, leads: List[Dict], campaign_type: str, template: str) -> Dict[str, Any]:
        """Execute the actual outreach (mock implementation)"""
        sent = 0
        failed = 0
        results = []
        
        for lead in leads:
            try:
                # Personalize message
                personalized_message = await self._personalize_message(template, lead)
                
                # Simulate sending (in reality, this would use email/LinkedIn APIs)
                success = await self._send_outreach_message(lead, personalized_message, campaign_type)
                
                if success:
                    sent += 1
                    results.append({
                        "lead_id": lead.get("id"),
                        "status": "sent",
                        "sent_at": datetime.utcnow().isoformat()
                    })
                else:
                    failed += 1
                    results.append({
                        "lead_id": lead.get("id"),
                        "status": "failed",
                        "error": "Delivery failed"
                    })
                    
            except Exception as e:
                failed += 1
                results.append({
                    "lead_id": lead.get("id"),
                    "status": "failed",
                    "error": str(e)
                })
                
        return {
            "sent": sent,
            "failed": failed,
            "results": results
        }
        
    async def _personalize_message(self, template: str, lead: Dict[str, Any]) -> str:
        """Personalize outreach message for specific lead"""
        if not template:
            template = """Hi {contact_name},

I noticed {company_name} is doing interesting work in the {industry} space. 

We're building a solution that helps {industry} companies like yours streamline operations and boost productivity.

Would you be interested in a quick 15-minute chat to see if this could be valuable for {company_name}?

Best regards,
The Dream Team"""

        # Replace placeholders
        personalized = template.format(
            contact_name=lead.get("contact_name", "there"),
            company_name=lead.get("company_name", "your company"),
            industry=lead.get("industry", "technology"),
            title=lead.get("title", "")
        )
        
        return personalized
        
    async def _send_outreach_message(self, lead: Dict[str, Any], message: str, campaign_type: str) -> bool:
        """Send outreach message (mock implementation)"""
        # In reality, this would integrate with email/LinkedIn APIs
        # For now, simulate 85% success rate
        import random
        return random.random() < 0.85
        
    async def _manage_crm(self, task: Dict[str, Any]) -> TaskResult:
        """Manage CRM data and pipeline"""
        action = task.get("action", "update")
        contact_data = task.get("contact_data", {})
        
        if action == "add_contact":
            return await self._add_contact(contact_data)
        elif action == "update_contact":
            return await self._update_contact(contact_data)
        elif action == "get_pipeline":
            return await self._get_sales_pipeline()
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Specify valid CRM action"],
                error_message=f"Unknown CRM action: {action}"
            )
            
    async def _add_contact(self, contact_data: Dict[str, Any]) -> TaskResult:
        """Add new contact to CRM"""
        contact_id = f"contact_{datetime.utcnow().timestamp()}"
        
        contact = {
            "id": contact_id,
            "name": contact_data.get("name", ""),
            "email": contact_data.get("email", ""),
            "company": contact_data.get("company", ""),
            "title": contact_data.get("title", ""),
            "phone": contact_data.get("phone", ""),
            "stage": contact_data.get("stage", "lead"),
            "source": contact_data.get("source", "manual"),
            "notes": contact_data.get("notes", ""),
            "created_at": datetime.utcnow().isoformat(),
            "last_contact": datetime.utcnow().isoformat()
        }
        
        # Save to CRM file
        os.makedirs("sales_data", exist_ok=True)
        crm_file = "sales_data/crm_contacts.json"
        
        contacts = []
        if os.path.exists(crm_file):
            with open(crm_file, "r") as f:
                contacts = json.load(f)
                
        contacts.append(contact)
        
        with open(crm_file, "w") as f:
            json.dump(contacts, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "contact_id": contact_id,
                "contact": contact
            },
            cost_incurred=0.0,
            evidence=[crm_file],
            next_steps=[
                "Schedule follow-up",
                "Add to nurture sequence",
                "Update lead score"
            ]
        )
        
    async def _get_sales_pipeline(self) -> TaskResult:
        """Get current sales pipeline status"""
        crm_file = "sales_data/crm_contacts.json"
        
        if not os.path.exists(crm_file):
            return TaskResult(
                success=True,
                output={
                    "pipeline": {},
                    "total_contacts": 0,
                    "stages": {}
                },
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Add contacts to CRM"]
            )
            
        with open(crm_file, "r") as f:
            contacts = json.load(f)
            
        # Analyze pipeline
        stages = {}
        for contact in contacts:
            stage = contact.get("stage", "unknown")
            stages[stage] = stages.get(stage, 0) + 1
            
        pipeline = {
            "total_contacts": len(contacts),
            "stages": stages,
            "conversion_rates": {
                "lead_to_qualified": (stages.get("qualified", 0) / max(stages.get("lead", 1), 1)) * 100,
                "qualified_to_opportunity": (stages.get("opportunity", 0) / max(stages.get("qualified", 1), 1)) * 100,
                "opportunity_to_customer": (stages.get("customer", 0) / max(stages.get("opportunity", 1), 1)) * 100
            },
            "recent_activity": len([c for c in contacts if 
                                 datetime.fromisoformat(c.get("last_contact", "2020-01-01")) > 
                                 datetime.utcnow() - timedelta(days=7)])
        }
        
        return TaskResult(
            success=True,
            output=pipeline,
            cost_incurred=0.0,
            evidence=[crm_file],
            next_steps=[
                "Follow up with recent leads",
                "Nurture qualified prospects",
                "Close pending opportunities"
            ]
        )
        
    async def _setup_follow_ups(self, task: Dict[str, Any]) -> TaskResult:
        """Setup automated follow-up sequences"""
        contact_list = task.get("contact_list", [])
        follow_up_schedule = task.get("follow_up_schedule", [])
        
        if not contact_list or not follow_up_schedule:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Provide contact list and follow-up schedule"],
                error_message="Missing contact list or follow-up schedule"
            )
            
        # Create follow-up sequences
        sequences = []
        
        for contact in contact_list:
            for i, follow_up in enumerate(follow_up_schedule):
                sequence = {
                    "id": f"followup_{contact.get('id')}_{i}",
                    "contact_id": contact.get("id"),
                    "contact_email": contact.get("email"),
                    "sequence_step": i + 1,
                    "delay_days": follow_up.get("delay_days", 3),
                    "message_template": follow_up.get("message_template", ""),
                    "scheduled_date": (datetime.utcnow() + timedelta(days=follow_up.get("delay_days", 3))).isoformat(),
                    "status": "scheduled",
                    "created_at": datetime.utcnow().isoformat()
                }
                sequences.append(sequence)
                
        # Save follow-up sequences
        os.makedirs("sales_data", exist_ok=True)
        followup_file = f"sales_data/followup_sequences_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(followup_file, "w") as f:
            json.dump(sequences, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "total_sequences": len(sequences),
                "contacts_enrolled": len(contact_list),
                "followup_file": followup_file
            },
            cost_incurred=3.0,
            evidence=[followup_file],
            next_steps=[
                "Monitor sequence performance",
                "Adjust timing based on responses",
                "Update message templates"
            ]
        )
        
    async def _analyze_sales_performance(self, task: Dict[str, Any]) -> TaskResult:
        """Analyze sales performance and metrics"""
        period_days = task.get("period_days", 30)
        
        # Load sales data
        crm_file = "sales_data/crm_contacts.json"
        
        if not os.path.exists(crm_file):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Add contacts to CRM first"],
                error_message="No sales data available"
            )
            
        with open(crm_file, "r") as f:
            contacts = json.load(f)
            
        # Analyze performance
        analysis = await self._create_sales_analysis(contacts, period_days)
        
        # Save analysis
        analysis_file = f"sales_data/analysis_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        with open(analysis_file, "w") as f:
            json.dump(analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output=analysis,
            cost_incurred=1.0,
            evidence=[analysis_file],
            next_steps=[
                "Review performance trends",
                "Optimize underperforming areas",
                "Scale successful strategies"
            ]
        )
        
    async def _create_sales_analysis(self, contacts: List[Dict], period_days: int) -> Dict[str, Any]:
        """Create sales performance analysis"""
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Filter recent contacts
        recent_contacts = [
            c for c in contacts 
            if datetime.fromisoformat(c.get("created_at", "2020-01-01")) > cutoff_date
        ]
        
        # Calculate metrics
        total_leads = len([c for c in recent_contacts if c.get("stage") == "lead"])
        qualified_leads = len([c for c in recent_contacts if c.get("stage") == "qualified"])
        opportunities = len([c for c in recent_contacts if c.get("stage") == "opportunity"])
        customers = len([c for c in recent_contacts if c.get("stage") == "customer"])
        
        analysis = {
            "period_days": period_days,
            "analysis_date": datetime.utcnow().isoformat(),
            "metrics": {
                "total_contacts": len(recent_contacts),
                "total_leads": total_leads,
                "qualified_leads": qualified_leads,
                "opportunities": opportunities,
                "customers": customers,
                "conversion_rates": {
                    "lead_to_qualified": (qualified_leads / max(total_leads, 1)) * 100,
                    "qualified_to_opportunity": (opportunities / max(qualified_leads, 1)) * 100,
                    "opportunity_to_customer": (customers / max(opportunities, 1)) * 100,
                    "overall_conversion": (customers / max(len(recent_contacts), 1)) * 100
                }
            },
            "trends": {
                "daily_average_leads": total_leads / period_days,
                "weekly_conversion_rate": (customers / max(len(recent_contacts), 1)) * 100,
                "top_sources": self._get_top_sources(recent_contacts)
            },
            "recommendations": [
                "Focus on improving lead qualification process",
                "Increase follow-up frequency for opportunities",
                "Analyze successful customer acquisition patterns"
            ]
        }
        
        return analysis
        
    def _get_top_sources(self, contacts: List[Dict]) -> Dict[str, int]:
        """Get top lead sources"""
        sources = {}
        for contact in contacts:
            source = contact.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
            
        return dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5])
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily sales goals"""
        return [
            {
                "goal": "Follow up with warm leads",
                "priority": "high",
                "estimated_time": "1 hour"
            },
            {
                "goal": "Qualify new leads from yesterday",
                "priority": "high",
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Update CRM with recent interactions",
                "priority": "medium",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Research new prospects",
                "priority": "medium",
                "estimated_time": "1 hour"
            }
        ]

# Example usage
async def main():
    """Example usage of SalesAgent"""
    agent = SalesAgent()
    await agent.start()
    
    # Test lead generation
    task = {
        "type": "lead_generation",
        "target_market": {
            "industry": "technology",
            "company_size": "startup"
        },
        "search_criteria": {
            "location": "global",
            "title": "founder"
        },
        "lead_count": 25
    }
    
    result = await agent.execute_task(task)
    print("Lead generation result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())