"""
Marketing Agent
Handles landing pages, social media, email campaigns, and growth marketing
"""

import asyncio
import logging
import json
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseAgent, AgentCapability, TaskResult
from toolkit.landing_generator import LandingPageGenerator
from toolkit.email_manager import EmailManager

logger = logging.getLogger(__name__)

class MarketingAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="create_landing_page",
                description="Generate and deploy modern landing pages",
                cost_estimate=5.0,
                confidence_level=0.9,
                requirements=["domain", "company_info"]
            ),
            AgentCapability(
                name="setup_waitlist",
                description="Create email capture and waitlist system",
                cost_estimate=2.0,
                confidence_level=0.95,
                requirements=["landing_page", "email_service"]
            ),
            AgentCapability(
                name="social_media_setup",
                description="Create and setup social media accounts",
                cost_estimate=0.0,
                confidence_level=0.8,
                requirements=["brand_assets", "company_info"]
            ),
            AgentCapability(
                name="email_campaign",
                description="Create and send email marketing campaigns",
                cost_estimate=10.0,
                confidence_level=0.85,
                requirements=["email_list", "campaign_content"]
            ),
            AgentCapability(
                name="content_creation",
                description="Generate marketing copy and content",
                cost_estimate=1.0,
                confidence_level=0.8,
                requirements=["brand_guidelines", "target_audience"]
            )
        ]
        
        super().__init__("marketing_agent", capabilities)
        self.landing_generator = LandingPageGenerator()
        self.email_manager = EmailManager()
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute marketing tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "create_landing_page":
                return await self._create_landing_page(task)
            elif task_type == "setup_waitlist":
                return await self._setup_waitlist(task)
            elif task_type == "social_media_setup":
                return await self._setup_social_media(task)
            elif task_type == "email_campaign":
                return await self._run_email_campaign(task)
            elif task_type == "content_creation":
                return await self._create_content(task)
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
            logger.error(f"Marketing task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _create_landing_page(self, task: Dict[str, Any]) -> TaskResult:
        """Create and deploy a landing page"""
        company_info = task.get("company_info", {})
        domain = task.get("domain", "example.com")
        
        # Check approval for deployment cost
        action = {
            "type": "deploy_landing_page",
            "domain": domain,
            "provider": "vercel"
        }
        
        if not await self.request_approval(action, 5.0):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Deployment not approved"
            )
            
        # Generate landing page
        result = await self.landing_generator.generate_landing_page(
            company_name=company_info.get("name", "DreamCorp"),
            description=company_info.get("description", "Building the future"),
            industry=company_info.get("industry", "technology"),
            target_audience=company_info.get("target_audience", "entrepreneurs")
        )
        
        if result["success"]:
            # Deploy to Vercel
            deploy_result = await self.landing_generator.deploy_to_vercel(
                result["output_dir"],
                domain
            )
            
            if deploy_result["success"]:
                # Record cost
                self.cost_tracker.record_expense("landing_page_deployment", 5.0)
                
                return TaskResult(
                    success=True,
                    output={
                        "landing_page_url": deploy_result["url"],
                        "deployment_id": deploy_result["deployment_id"],
                        "features": result["features"]
                    },
                    cost_incurred=5.0,
                    evidence=[deploy_result["url"], result["output_dir"]],
                    next_steps=[
                        "Setup analytics tracking",
                        "Create waitlist form",
                        "Launch social media accounts"
                    ]
                )
            else:
                return TaskResult(
                    success=False,
                    output=result,
                    cost_incurred=0.0,
                    evidence=[result["output_dir"]],
                    next_steps=["Fix deployment issues", "Try alternative hosting"],
                    error_message=deploy_result.get("error", "Deployment failed")
                )
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Debug page generation", "Check template files"],
                error_message=result.get("error", "Page generation failed")
            )
            
    async def _setup_waitlist(self, task: Dict[str, Any]) -> TaskResult:
        """Setup waitlist and email capture"""
        company_name = task.get("company_name", "DreamCorp")
        
        # Create waitlist email sequence
        sequence_result = await self.email_manager.create_waitlist_sequence(company_name)
        
        if sequence_result["success"]:
            return TaskResult(
                success=True,
                output={
                    "campaign_id": sequence_result["campaign_id"],
                    "total_emails": sequence_result["total_emails"],
                    "config_file": sequence_result["config_file"]
                },
                cost_incurred=2.0,
                evidence=[sequence_result["config_file"]],
                next_steps=[
                    "Integrate waitlist form with landing page",
                    "Test email delivery",
                    "Setup analytics tracking"
                ]
            )
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Debug email configuration", "Check API credentials"],
                error_message="Failed to create waitlist sequence"
            )
            
    async def _setup_social_media(self, task: Dict[str, Any]) -> TaskResult:
        """Setup social media accounts"""
        company_info = task.get("company_info", {})
        platforms = task.get("platforms", ["twitter", "instagram", "linkedin"])
        
        # This would integrate with social media APIs to create accounts
        # For now, we'll simulate the process
        
        created_accounts = []
        for platform in platforms:
            account_info = {
                "platform": platform,
                "username": f"@{company_info.get('name', 'dreamcorp').lower()}",
                "profile_url": f"https://{platform}.com/{company_info.get('name', 'dreamcorp').lower()}",
                "status": "created"
            }
            created_accounts.append(account_info)
            
        return TaskResult(
            success=True,
            output={
                "accounts": created_accounts,
                "total_platforms": len(platforms)
            },
            cost_incurred=0.0,
            evidence=[acc["profile_url"] for acc in created_accounts],
            next_steps=[
                "Upload brand assets to profiles",
                "Create content calendar",
                "Schedule first posts"
            ]
        )
        
    async def _run_email_campaign(self, task: Dict[str, Any]) -> TaskResult:
        """Run an email marketing campaign"""
        email_list = task.get("email_list", [])
        subject = task.get("subject", "Update from our team")
        content = task.get("content", "")
        
        if not email_list:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Build email list", "Import subscribers"],
                error_message="No email list provided"
            )
            
        # Estimate cost based on email count
        estimated_cost = len(email_list) * 0.01  # $0.01 per email
        
        # Check approval for campaign cost
        action = {
            "type": "send_email_campaign",
            "recipient_count": len(email_list),
            "subject": subject
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Campaign not approved"
            )
            
        # Send campaign
        result = await self.email_manager.send_campaign_email(
            email_list, subject, content
        )
        
        # Record actual cost
        actual_cost = result["sent"] * 0.01
        self.cost_tracker.record_expense("email_campaign", actual_cost)
        
        return TaskResult(
            success=result["sent"] > 0,
            output={
                "sent": result["sent"],
                "failed": result["failed"],
                "errors": result["errors"][:5]  # Limit error list
            },
            cost_incurred=actual_cost,
            evidence=[f"Campaign sent to {result['sent']} recipients"],
            next_steps=[
                "Monitor open rates",
                "Track click-through rates",
                "Analyze campaign performance"
            ]
        )
        
    async def _create_content(self, task: Dict[str, Any]) -> TaskResult:
        """Create marketing content"""
        content_type = task.get("content_type", "social_post")
        brand_info = task.get("brand_info", {})
        target_audience = task.get("target_audience", "general")
        
        # Generate content based on type
        if content_type == "social_post":
            content = await self._generate_social_post(brand_info, target_audience)
        elif content_type == "email_copy":
            content = await self._generate_email_copy(brand_info, target_audience)
        elif content_type == "ad_copy":
            content = await self._generate_ad_copy(brand_info, target_audience)
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Specify valid content type"],
                error_message=f"Unknown content type: {content_type}"
            )
            
        return TaskResult(
            success=True,
            output={
                "content_type": content_type,
                "content": content,
                "target_audience": target_audience
            },
            cost_incurred=1.0,
            evidence=[],
            next_steps=[
                "Review and approve content",
                "Schedule for publishing",
                "Track engagement metrics"
            ]
        )
        
    async def _generate_social_post(self, brand_info: Dict[str, Any], target_audience: str) -> str:
        """Generate social media post content"""
        company_name = brand_info.get("name", "DreamCorp")
        industry = brand_info.get("industry", "technology")
        
        posts = [
            f"🚀 Exciting news! {company_name} is revolutionizing the {industry} space. Join our waitlist to be the first to experience the future! #innovation #startup",
            f"Building something amazing at {company_name}! Our team is working around the clock to bring you the next big thing in {industry}. Stay tuned! 💪",
            f"The future of {industry} is here! {company_name} is launching soon. Be part of the revolution - sign up for early access today! 🌟"
        ]
        
        return posts[0]  # Return first post for now
        
    async def _generate_email_copy(self, brand_info: Dict[str, Any], target_audience: str) -> str:
        """Generate email marketing copy"""
        company_name = brand_info.get("name", "DreamCorp")
        
        return f"""
        Subject: You're invited to be part of something special
        
        Hi there!
        
        We're building {company_name} to solve real problems in the {brand_info.get('industry', 'technology')} space.
        
        As one of our early supporters, you'll get:
        • First access to our platform
        • Special launch pricing
        • Direct line to our founding team
        
        Ready to join the journey?
        
        Best,
        The {company_name} Team
        """
        
    async def _generate_ad_copy(self, brand_info: Dict[str, Any], target_audience: str) -> str:
        """Generate advertising copy"""
        company_name = brand_info.get("name", "DreamCorp")
        
        return f"Transform your {brand_info.get('industry', 'business')} with {company_name}. Join thousands of early adopters. Get started today!"
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily marketing goals"""
        return [
            {
                "goal": "Monitor landing page analytics",
                "priority": "high",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Engage with social media followers",
                "priority": "medium",
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Review and optimize email campaigns",
                "priority": "medium",
                "estimated_time": "1 hour"
            }
        ]

# Example usage
async def main():
    """Example usage of MarketingAgent"""
    agent = MarketingAgent()
    await agent.start()
    
    # Test landing page creation
    task = {
        "type": "create_landing_page",
        "company_info": {
            "name": "DreamCorp",
            "description": "AI-powered business automation",
            "industry": "technology",
            "target_audience": "entrepreneurs"
        },
        "domain": "dreamcorp.com"
    }
    
    result = await agent.execute_task(task)
    print("Landing page result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())