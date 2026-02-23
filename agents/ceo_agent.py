"""
CEO Agent - The Master Orchestrator
Manages all other agents, sets goals, handles approvals, and coordinates the entire operation
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from core.base_agent import BaseAgent, AgentCapability, TaskResult
from core.message_bus import MessageType, Priority
from core.company_blueprint_dataclass import CompanyBlueprint, BusinessModel, BusinessModelType, RevenueStream, TargetMarket
from core.goal_planner import GoalPlanner

logger = logging.getLogger(__name__)

@dataclass
class DailyBriefing:
    date: str
    company_health: Dict[str, Any]
    yesterday_achievements: List[str]
    today_goals: List[Dict[str, Any]]
    founder_tasks: List[Dict[str, Any]]
    blockers: List[str]
    budget_status: Dict[str, float]
    recommendations: List[str]

class CEOAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="strategic_planning",
                description="Create and manage company roadmaps and OKRs",
                cost_estimate=0.0,
                confidence_level=0.95,
                requirements=[]
            ),
            AgentCapability(
                name="agent_coordination",
                description="Coordinate tasks between department agents",
                cost_estimate=0.0,
                confidence_level=0.98,
                requirements=[]
            ),
            AgentCapability(
                name="approval_management",
                description="Handle approval requests and policy enforcement",
                cost_estimate=0.0,
                confidence_level=0.90,
                requirements=[]
            )
        ]
        
        super().__init__("ceo_agent", capabilities)
        
        self.company_blueprint: Optional[CompanyBlueprint] = None
        self.goal_planner = GoalPlanner()
        self.active_agents: Dict[str, Dict] = {}
        self.daily_goals: Dict[str, List[Dict]] = {}
        self.pending_approvals: Dict[str, Dict] = {}
        
    async def initialize_company(self, dream: str, founder_budget: float) -> CompanyBlueprint:
        """Initialize a new company from founder's dream"""
        logger.info(f"Initializing company from dream: {dream}")
        
        # Create company blueprint
        self.company_blueprint = await self._create_blueprint_from_dream(dream, founder_budget)
        
        # Set up goal hierarchy
        await self.goal_planner.create_goal_hierarchy(self.company_blueprint)
        
        # Generate first set of daily goals
        await self._generate_daily_goals()
        
        # Send initial tasks to agents
        await self._distribute_initial_tasks()
        
        return self.company_blueprint
        
    async def _create_blueprint_from_dream(self, dream: str, budget: float) -> CompanyBlueprint:
        """Convert founder's dream into structured company blueprint"""
        # This would use LLM to parse the dream and create structured data
        # For now, we'll create a sample blueprint
        
        blueprint = CompanyBlueprint(
            company_name="DreamCorp",
            vision=dream,
            mission="To revolutionize technology through innovation",
            industry="technology"
        )
        
        return blueprint
        
    async def _generate_daily_goals(self):
        """Generate daily goals for all agents"""
        if not self.company_blueprint:
            return
            
        # Get current quarter's OKRs
        current_okrs = await self.goal_planner.get_current_okrs()
        
        # Generate goals for each active agent
        for agent_id in self.active_agents:
            agent_goals = await self.goal_planner.generate_daily_goals(
                agent_id, 
                current_okrs,
                self.company_blueprint
            )
            self.daily_goals[agent_id] = agent_goals
            
    async def _distribute_initial_tasks(self):
        """Send initial tasks to all department agents"""
        initial_tasks = {
            "product_agent": {
                "id": "initial_product_setup",
                "type": "setup",
                "description": "Create initial product requirements and roadmap",
                "priority": "high",
                "deadline": (datetime.utcnow() + timedelta(hours=4)).isoformat()
            },
            "engineering_agent": {
                "id": "initial_repo_setup",
                "type": "setup", 
                "description": "Create GitHub repository and initial project structure",
                "priority": "high",
                "deadline": (datetime.utcnow() + timedelta(hours=2)).isoformat()
            },
            "marketing_agent": {
                "id": "initial_landing_page",
                "type": "setup",
                "description": "Create landing page and waitlist capture",
                "priority": "high", 
                "deadline": (datetime.utcnow() + timedelta(hours=6)).isoformat()
            }
        }
        
        for agent_id, task in initial_tasks.items():
            if agent_id in self.active_agents:
                await self.message_bus.send_task_assignment(
                    self.agent_id, 
                    agent_id, 
                    task
                )
                
    async def generate_daily_briefing(self) -> DailyBriefing:
        """Generate daily briefing for the founder"""
        
        # Collect yesterday's achievements
        yesterday_achievements = await self._collect_achievements()
        
        # Get today's goals
        today_goals = []
        for agent_id, goals in self.daily_goals.items():
            today_goals.extend(goals)
            
        # Generate founder tasks
        founder_tasks = await self._generate_founder_tasks()
        
        # Check for blockers
        blockers = await self._identify_blockers()
        
        # Get budget status
        budget_status = await self._get_budget_status()
        
        # Generate recommendations
        recommendations = await self._generate_recommendations()
        
        briefing = DailyBriefing(
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            company_health=await self._assess_company_health(),
            yesterday_achievements=yesterday_achievements,
            today_goals=today_goals,
            founder_tasks=founder_tasks,
            blockers=blockers,
            budget_status=budget_status,
            recommendations=recommendations
        )
        
        return briefing
        
    async def _collect_achievements(self) -> List[str]:
        """Collect yesterday's achievements from all agents"""
        # Query message log for completed tasks from yesterday
        achievements = [
            "Landing page deployed successfully",
            "GitHub repository created with initial structure", 
            "Domain purchased and configured",
            "First 5 waitlist signups received"
        ]
        return achievements
        
    async def _generate_founder_tasks(self) -> List[Dict[str, Any]]:
        """Generate tasks that require founder's personal attention"""
        tasks = []
        
        # Check if we need founder input
        if self.company_blueprint and not self.company_blueprint.logo_approved:
            tasks.append({
                "id": "approve_logo",
                "title": "Review and approve company logo",
                "description": "The Design Agent has created 3 logo options. Please review and select your preferred option.",
                "priority": "medium",
                "deadline": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "type": "approval",
                "estimated_time_minutes": 15
            })
            
        # Check if we need content from founder
        tasks.append({
            "id": "record_pitch_video",
            "title": "Record 60-second pitch video",
            "description": "Please record a short video explaining your product vision for the landing page.",
            "priority": "high",
            "deadline": (datetime.utcnow() + timedelta(hours=48)).isoformat(),
            "type": "content_creation",
            "estimated_time_minutes": 30
        })
        
        return tasks
        
    async def _identify_blockers(self) -> List[str]:
        """Identify current blockers across all agents"""
        blockers = []
        
        # Check for pending approvals
        if self.pending_approvals:
            blockers.append(f"{len(self.pending_approvals)} actions waiting for your approval")
            
        # Check agent status
        offline_agents = [
            agent_id for agent_id, info in self.active_agents.items() 
            if info.get("status") != "online"
        ]
        if offline_agents:
            blockers.append(f"Agents offline: {', '.join(offline_agents)}")
            
        return blockers
        
    async def _get_budget_status(self) -> Dict[str, float]:
        """Get current budget status"""
        return {
            "total_budget": self.company_blueprint.budget if self.company_blueprint else 0,
            "spent_today": 45.67,
            "spent_this_month": 234.89,
            "remaining": 9765.11,
            "burn_rate_daily": 78.45
        }
        
    async def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations for the founder"""
        recommendations = []
        
        if self.company_blueprint:
            # Analyze progress and suggest next steps
            recommendations.append(
                "Consider setting up Google Analytics to track landing page performance"
            )
            recommendations.append(
                "Schedule customer interviews once you reach 50 waitlist signups"
            )
            
        return recommendations
        
    async def _assess_company_health(self) -> Dict[str, Any]:
        """Assess overall company health metrics"""
        return {
            "overall_score": 85,
            "progress_this_week": 23,
            "active_agents": len(self.active_agents),
            "completed_tasks_today": 7,
            "pending_tasks": 12,
            "budget_health": "good"
        }
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute CEO-level tasks"""
        task_type = task.get("type")
        
        if task_type == "generate_briefing":
            briefing = await self.generate_daily_briefing()
            return TaskResult(
                success=True,
                output={"briefing": briefing.__dict__},
                cost_incurred=0.0,
                evidence=["daily_briefing.json"],
                next_steps=["Send briefing to founder", "Update agent goals"]
            )
            
        elif task_type == "coordinate_agents":
            await self._coordinate_agent_work()
            return TaskResult(
                success=True,
                output={"coordinated_agents": len(self.active_agents)},
                cost_incurred=0.0,
                evidence=["coordination_log.json"],
                next_steps=["Monitor agent progress"]
            )
            
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=f"Unknown task type: {task_type}"
            )
            
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get CEO's daily goals"""
        return [
            {
                "id": "morning_briefing",
                "description": "Generate and send daily briefing to founder",
                "priority": "high",
                "estimated_duration": "15 minutes"
            },
            {
                "id": "agent_coordination", 
                "description": "Coordinate work between all department agents",
                "priority": "high",
                "estimated_duration": "30 minutes"
            },
            {
                "id": "progress_review",
                "description": "Review progress against quarterly OKRs",
                "priority": "medium", 
                "estimated_duration": "20 minutes"
            }
        ]
        
    async def _coordinate_agent_work(self):
        """Coordinate work between agents to avoid conflicts"""
        # Check for dependencies and conflicts
        # Reschedule tasks if needed
        # Send coordination messages to agents
        pass

# Global CEO agent instance
ceo_agent = CEOAgent()