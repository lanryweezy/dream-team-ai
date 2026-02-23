"""
AI-Powered Task Management Engine
Smart task prioritization, scheduling, and workflow optimization
Provides comprehensive project management with AI assistance
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics
import random

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"

class TaskStatus(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskCategory(Enum):
    PRODUCT = "product"
    MARKETING = "marketing"
    SALES = "sales"
    ENGINEERING = "engineering"
    DESIGN = "design"
    OPERATIONS = "operations"
    FINANCE = "finance"
    LEGAL = "legal"
    HR = "hr"
    STRATEGY = "strategy"

class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Individual task with AI-powered insights"""
    task_id: str
    title: str
    description: str
    
    # Classification
    category: TaskCategory
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    
    # Assignment
    assignee: Optional[str] = None
    assignee_team: Optional[str] = None
    reporter: Optional[str] = None
    
    # Timeline
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    due_date: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)  # Task IDs
    blocks: List[str] = field(default_factory=list)  # Task IDs this blocks
    
    # AI Insights
    ai_priority_score: float = 0.0  # 0-10
    ai_complexity_score: float = 0.0  # 0-10
    ai_impact_score: float = 0.0  # 0-10
    ai_recommendations: List[str] = field(default_factory=list)
    
    # Progress tracking
    progress_percentage: float = 0.0
    subtasks: List[str] = field(default_factory=list)
    comments: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    project_id: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Project:
    """Project containing multiple tasks"""
    project_id: str
    name: str
    description: str
    
    # Status and timeline
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[str] = None
    target_end_date: Optional[str] = None
    actual_end_date: Optional[str] = None
    
    # Team and ownership
    project_manager: Optional[str] = None
    team_members: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)
    
    # Progress and metrics
    progress_percentage: float = 0.0
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    
    # AI insights
    ai_health_score: float = 0.0  # 0-10
    ai_risk_factors: List[str] = field(default_factory=list)
    ai_recommendations: List[str] = field(default_factory=list)
    
    # Task management
    task_ids: List[str] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class WorkflowTemplate:
    """Reusable workflow template"""
    template_id: str
    name: str
    description: str
    category: TaskCategory
    
    # Template structure
    task_templates: List[Dict[str, Any]] = field(default_factory=list)
    estimated_duration_days: int = 0
    required_roles: List[str] = field(default_factory=list)
    
    # Usage tracking
    usage_count: int = 0
    success_rate: float = 0.0
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class TeamMember:
    """Team member with capacity and skills"""
    member_id: str
    name: str
    email: str
    role: str
    team: str
    
    # Capacity management
    weekly_capacity_hours: float = 40.0
    current_workload_hours: float = 0.0
    availability_percentage: float = 100.0
    
    # Skills and performance
    skills: List[str] = field(default_factory=list)
    performance_score: float = 8.0  # 0-10
    task_completion_rate: float = 0.95
    
    # Preferences
    preferred_task_types: List[TaskCategory] = field(default_factory=list)
    timezone: str = "UTC"
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AITaskManagementEngine:
    """
    Comprehensive AI-powered task management system that provides:
    - Smart task prioritization and scheduling
    - AI-powered project management
    - Automated workflow optimization
    - Team capacity management
    - Predictive project analytics
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.tasks: Dict[str, Task] = {}
        self.projects: Dict[str, Project] = {}
        self.workflow_templates: Dict[str, WorkflowTemplate] = {}
        self.team_members: Dict[str, TeamMember] = {}
        
        # AI configuration
        self.priority_weights = {
            "business_impact": 0.3,
            "urgency": 0.25,
            "complexity": 0.2,
            "dependencies": 0.15,
            "team_capacity": 0.1
        }
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample task management data"""
        
        # Sample team members
        sample_team = [
            TeamMember(
                member_id="tm_001",
                name="Sarah Chen",
                email="sarah@company.com",
                role="Product Manager",
                team="Product",
                skills=["Product Strategy", "User Research", "Roadmap Planning"],
                preferred_task_types=[TaskCategory.PRODUCT, TaskCategory.STRATEGY],
                current_workload_hours=32.0
            ),
            TeamMember(
                member_id="tm_002",
                name="Alex Rodriguez",
                email="alex@company.com",
                role="Senior Engineer",
                team="Engineering",
                skills=["React", "Python", "System Design", "API Development"],
                preferred_task_types=[TaskCategory.ENGINEERING],
                current_workload_hours=38.0
            ),
            TeamMember(
                member_id="tm_003",
                name="Maya Patel",
                email="maya@company.com",
                role="Marketing Manager",
                team="Marketing",
                skills=["Content Marketing", "SEO", "Analytics", "Campaign Management"],
                preferred_task_types=[TaskCategory.MARKETING],
                current_workload_hours=35.0
            ),
            TeamMember(
                member_id="tm_004",
                name="David Kim",
                email="david@company.com",
                role="UX Designer",
                team="Design",
                skills=["UI/UX Design", "Prototyping", "User Testing", "Figma"],
                preferred_task_types=[TaskCategory.DESIGN, TaskCategory.PRODUCT],
                current_workload_hours=30.0
            )
        ]
        
        for member in sample_team:
            self.team_members[member.member_id] = member
        
        # Sample projects
        sample_projects = [
            Project(
                project_id="proj_001",
                name="Q4 Product Launch",
                description="Launch new analytics dashboard with AI features",
                status=ProjectStatus.ACTIVE,
                start_date="2025-09-01",
                target_end_date="2025-12-15",
                project_manager="tm_001",
                team_members=["tm_001", "tm_002", "tm_003", "tm_004"],
                progress_percentage=65.0,
                budget=150000.0,
                actual_cost=95000.0,
                ai_health_score=7.8,
                ai_risk_factors=["Timeline pressure", "Resource constraints"],
                ai_recommendations=["Add 1 additional engineer", "Prioritize core features"]
            ),
            Project(
                project_id="proj_002",
                name="Marketing Campaign Optimization",
                description="Optimize conversion rates across all marketing channels",
                status=ProjectStatus.ACTIVE,
                start_date="2025-09-15",
                target_end_date="2025-11-30",
                project_manager="tm_003",
                team_members=["tm_003", "tm_004"],
                progress_percentage=40.0,
                budget=75000.0,
                actual_cost=28000.0,
                ai_health_score=8.5,
                ai_recommendations=["Focus on high-converting channels", "A/B test landing pages"]
            )
        ]
        
        for project in sample_projects:
            self.projects[project.project_id] = project
        
        # Sample tasks
        sample_tasks = [
            Task(
                task_id="task_001",
                title="Implement AI-powered analytics dashboard",
                description="Build the core analytics dashboard with real-time AI insights and predictive capabilities",
                category=TaskCategory.ENGINEERING,
                priority=TaskPriority.HIGH,
                status=TaskStatus.IN_PROGRESS,
                assignee="tm_002",
                assignee_team="Engineering",
                project_id="proj_001",
                due_date="2025-10-15",
                estimated_hours=40.0,
                actual_hours=28.0,
                progress_percentage=70.0,
                ai_priority_score=8.5,
                ai_complexity_score=7.8,
                ai_impact_score=9.2,
                ai_recommendations=["Break into smaller components", "Add unit tests", "Consider performance optimization"],
                tags=["ai", "dashboard", "analytics"]
            ),
            Task(
                task_id="task_002",
                title="Design user onboarding flow",
                description="Create intuitive onboarding experience for new users with interactive tutorials",
                category=TaskCategory.DESIGN,
                priority=TaskPriority.HIGH,
                status=TaskStatus.IN_REVIEW,
                assignee="tm_004",
                assignee_team="Design",
                project_id="proj_001",
                due_date="2025-10-08",
                estimated_hours=24.0,
                actual_hours=22.0,
                progress_percentage=90.0,
                ai_priority_score=8.0,
                ai_complexity_score=6.5,
                ai_impact_score=8.8,
                ai_recommendations=["User test with 5 participants", "Simplify step 3", "Add progress indicators"],
                tags=["onboarding", "ux", "tutorial"]
            ),
            Task(
                task_id="task_003",
                title="Launch social media campaign",
                description="Execute comprehensive social media campaign across LinkedIn, Twitter, and Facebook",
                category=TaskCategory.MARKETING,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.TODO,
                assignee="tm_003",
                assignee_team="Marketing",
                project_id="proj_002",
                due_date="2025-10-20",
                estimated_hours=16.0,
                ai_priority_score=7.2,
                ai_complexity_score=5.5,
                ai_impact_score=7.8,
                ai_recommendations=["Focus on LinkedIn for B2B", "Create video content", "Schedule posts for optimal times"],
                tags=["social-media", "campaign", "b2b"]
            ),
            Task(
                task_id="task_004",
                title="Optimize database performance",
                description="Improve query performance and implement caching for better user experience",
                category=TaskCategory.ENGINEERING,
                priority=TaskPriority.CRITICAL,
                status=TaskStatus.TODO,
                assignee="tm_002",
                assignee_team="Engineering",
                project_id="proj_001",
                due_date="2025-10-05",
                estimated_hours=20.0,
                ai_priority_score=9.5,
                ai_complexity_score=8.2,
                ai_impact_score=9.0,
                ai_recommendations=["Implement Redis caching", "Optimize slow queries", "Add database monitoring"],
                tags=["performance", "database", "optimization"],
                dependencies=["task_001"]
            ),
            Task(
                task_id="task_005",
                title="Conduct user research interviews",
                description="Interview 10 customers to understand pain points and feature requests",
                category=TaskCategory.PRODUCT,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.IN_PROGRESS,
                assignee="tm_001",
                assignee_team="Product",
                project_id="proj_001",
                due_date="2025-10-12",
                estimated_hours=15.0,
                actual_hours=8.0,
                progress_percentage=50.0,
                ai_priority_score=7.8,
                ai_complexity_score=4.5,
                ai_impact_score=8.5,
                ai_recommendations=["Focus on enterprise customers", "Ask about AI features", "Record sessions for analysis"],
                tags=["research", "interviews", "customer-feedback"]
            )
        ]
        
        for task in sample_tasks:
            self.tasks[task.task_id] = task
        
        # Sample workflow templates
        sample_templates = [
            WorkflowTemplate(
                template_id="wf_001",
                name="Feature Development Workflow",
                description="Standard workflow for developing new product features",
                category=TaskCategory.PRODUCT,
                task_templates=[
                    {"title": "Requirements Gathering", "category": "product", "estimated_hours": 8},
                    {"title": "Technical Design", "category": "engineering", "estimated_hours": 12},
                    {"title": "UI/UX Design", "category": "design", "estimated_hours": 16},
                    {"title": "Development", "category": "engineering", "estimated_hours": 40},
                    {"title": "Testing", "category": "engineering", "estimated_hours": 16},
                    {"title": "Documentation", "category": "product", "estimated_hours": 8},
                    {"title": "Launch", "category": "marketing", "estimated_hours": 12}
                ],
                estimated_duration_days=21,
                required_roles=["Product Manager", "Engineer", "Designer"],
                usage_count=12,
                success_rate=0.85
            ),
            WorkflowTemplate(
                template_id="wf_002",
                name="Marketing Campaign Workflow",
                description="Standard workflow for launching marketing campaigns",
                category=TaskCategory.MARKETING,
                task_templates=[
                    {"title": "Campaign Strategy", "category": "marketing", "estimated_hours": 12},
                    {"title": "Content Creation", "category": "marketing", "estimated_hours": 20},
                    {"title": "Design Assets", "category": "design", "estimated_hours": 16},
                    {"title": "Campaign Setup", "category": "marketing", "estimated_hours": 8},
                    {"title": "Launch Campaign", "category": "marketing", "estimated_hours": 4},
                    {"title": "Monitor & Optimize", "category": "marketing", "estimated_hours": 16}
                ],
                estimated_duration_days=14,
                required_roles=["Marketing Manager", "Designer"],
                usage_count=8,
                success_rate=0.92
            )
        ]
        
        for template in sample_templates:
            self.workflow_templates[template.template_id] = template
    
    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task with AI-powered insights"""
        
        try:
            logger.info(f"Creating task: {task_data.get('title')}")
            
            task = Task(
                task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title=task_data["title"],
                description=task_data["description"],
                category=TaskCategory(task_data["category"]),
                priority=TaskPriority(task_data.get("priority", "medium")),
                assignee=task_data.get("assignee"),
                assignee_team=task_data.get("assignee_team"),
                project_id=task_data.get("project_id"),
                due_date=task_data.get("due_date"),
                estimated_hours=task_data.get("estimated_hours"),
                tags=task_data.get("tags", [])
            )
            
            # Generate AI insights
            await self._generate_task_ai_insights(task)
            
            # Auto-assign if no assignee specified
            if not task.assignee:
                await self._auto_assign_task(task)
            
            # Store task
            self.tasks[task.task_id] = task
            
            # Update project if specified
            if task.project_id and task.project_id in self.projects:
                project = self.projects[task.project_id]
                project.task_ids.append(task.task_id)
                await self._update_project_metrics(project)
            
            logger.info(f"Created task: {task.task_id}")
            return task
            
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise
    
    async def _generate_task_ai_insights(self, task: Task):
        """Generate AI-powered insights for a task"""
        
        # Calculate AI priority score
        priority_factors = {
            TaskPriority.CRITICAL: 10.0,
            TaskPriority.URGENT: 9.0,
            TaskPriority.HIGH: 7.5,
            TaskPriority.MEDIUM: 5.0,
            TaskPriority.LOW: 2.5
        }
        
        base_priority = priority_factors.get(task.priority, 5.0)
        
        # Adjust based on due date urgency
        if task.due_date:
            due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
            days_until_due = (due_date - datetime.now(timezone.utc)).days
            
            if days_until_due <= 1:
                urgency_multiplier = 1.5
            elif days_until_due <= 3:
                urgency_multiplier = 1.3
            elif days_until_due <= 7:
                urgency_multiplier = 1.1
            else:
                urgency_multiplier = 1.0
            
            base_priority *= urgency_multiplier
        
        task.ai_priority_score = min(base_priority, 10.0)
        
        # Calculate complexity score based on estimated hours and category
        complexity_factors = {
            TaskCategory.ENGINEERING: 1.2,
            TaskCategory.DESIGN: 1.0,
            TaskCategory.PRODUCT: 0.9,
            TaskCategory.MARKETING: 0.8,
            TaskCategory.OPERATIONS: 0.7
        }
        
        base_complexity = (task.estimated_hours or 8.0) / 4.0  # Normalize to 0-10 scale
        category_multiplier = complexity_factors.get(task.category, 1.0)
        task.ai_complexity_score = min(base_complexity * category_multiplier, 10.0)
        
        # Calculate impact score
        impact_factors = {
            TaskCategory.PRODUCT: 9.0,
            TaskCategory.ENGINEERING: 8.5,
            TaskCategory.STRATEGY: 8.0,
            TaskCategory.MARKETING: 7.0,
            TaskCategory.DESIGN: 6.5,
            TaskCategory.SALES: 6.0,
            TaskCategory.OPERATIONS: 5.5
        }
        
        task.ai_impact_score = impact_factors.get(task.category, 6.0)
        
        # Generate recommendations
        recommendations = []
        
        if task.ai_complexity_score > 8.0:
            recommendations.append("Consider breaking this task into smaller subtasks")
        
        if task.ai_priority_score > 8.5 and not task.assignee:
            recommendations.append("Assign to senior team member due to high priority")
        
        if task.estimated_hours and task.estimated_hours > 20:
            recommendations.append("Large task - consider adding checkpoints and reviews")
        
        if task.category == TaskCategory.ENGINEERING:
            recommendations.extend([
                "Add unit tests and documentation",
                "Consider code review requirements",
                "Plan for deployment and rollback"
            ])
        
        task.ai_recommendations = recommendations
    
    async def _auto_assign_task(self, task: Task):
        """Automatically assign task to best available team member"""
        
        # Find team members with matching skills/preferences
        suitable_members = []
        
        for member in self.team_members.values():
            if task.category in member.preferred_task_types:
                # Calculate suitability score
                capacity_score = (member.weekly_capacity_hours - member.current_workload_hours) / member.weekly_capacity_hours
                performance_score = member.performance_score / 10.0
                
                suitability_score = (capacity_score * 0.6) + (performance_score * 0.4)
                
                suitable_members.append((member, suitability_score))
        
        if suitable_members:
            # Sort by suitability and assign to best match
            suitable_members.sort(key=lambda x: x[1], reverse=True)
            best_member = suitable_members[0][0]
            
            task.assignee = best_member.member_id
            task.assignee_team = best_member.team
            
            # Update member workload
            if task.estimated_hours:
                best_member.current_workload_hours += task.estimated_hours
    
    async def get_smart_task_recommendations(self, user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get AI-powered task recommendations for optimal productivity"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Get user's tasks
            user_tasks = [
                task for task in self.tasks.values()
                if task.assignee == user_context.get("user_id") and task.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]
            ]
            
            # Sort by AI priority score
            user_tasks.sort(key=lambda t: t.ai_priority_score, reverse=True)
            
            recommendations = []
            
            for task in user_tasks[:5]:  # Top 5 recommendations
                # Calculate urgency
                urgency = "medium"
                if task.due_date:
                    due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                    days_until_due = (due_date - current_time).days
                    
                    if days_until_due <= 1:
                        urgency = "critical"
                    elif days_until_due <= 3:
                        urgency = "high"
                    elif days_until_due <= 7:
                        urgency = "medium"
                    else:
                        urgency = "low"
                
                # Generate recommendation reason
                reasons = []
                if task.ai_priority_score > 8.0:
                    reasons.append("High business impact")
                if urgency in ["critical", "high"]:
                    reasons.append("Due soon")
                if task.status == TaskStatus.IN_PROGRESS:
                    reasons.append("Already in progress")
                if len(task.dependencies) == 0:
                    reasons.append("No blockers")
                
                recommendations.append({
                    "task_id": task.task_id,
                    "title": task.title,
                    "priority_score": task.ai_priority_score,
                    "urgency": urgency,
                    "estimated_hours": task.estimated_hours,
                    "progress": task.progress_percentage,
                    "reasons": reasons,
                    "ai_recommendations": task.ai_recommendations
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get task recommendations: {e}")
            raise
    
    async def optimize_team_workload(self) -> Dict[str, Any]:
        """Optimize workload distribution across team members"""
        
        try:
            optimization_results = {
                "team_utilization": {},
                "workload_balance": 0.0,
                "recommendations": [],
                "reassignments": []
            }
            
            # Calculate current utilization
            for member in self.team_members.values():
                utilization = (member.current_workload_hours / member.weekly_capacity_hours) * 100
                optimization_results["team_utilization"][member.name] = {
                    "utilization_percentage": round(utilization, 1),
                    "current_hours": member.current_workload_hours,
                    "capacity_hours": member.weekly_capacity_hours,
                    "status": "overloaded" if utilization > 100 else "optimal" if utilization > 80 else "underutilized"
                }
            
            # Calculate workload balance (lower is better)
            utilizations = [
                (member.current_workload_hours / member.weekly_capacity_hours) * 100
                for member in self.team_members.values()
            ]
            
            if utilizations:
                optimization_results["workload_balance"] = round(statistics.stdev(utilizations), 1)
            
            # Generate recommendations
            recommendations = []
            
            # Find overloaded members
            overloaded = [
                member for member in self.team_members.values()
                if (member.current_workload_hours / member.weekly_capacity_hours) > 1.0
            ]
            
            # Find underutilized members
            underutilized = [
                member for member in self.team_members.values()
                if (member.current_workload_hours / member.weekly_capacity_hours) < 0.8
            ]
            
            if overloaded:
                recommendations.append(f"{len(overloaded)} team members are overloaded - consider redistributing tasks")
            
            if underutilized:
                recommendations.append(f"{len(underutilized)} team members are underutilized - assign additional tasks")
            
            if optimization_results["workload_balance"] > 20:
                recommendations.append("High workload imbalance detected - rebalance task assignments")
            
            # Suggest specific reassignments
            reassignments = []
            
            for overloaded_member in overloaded:
                # Find tasks that could be reassigned
                member_tasks = [
                    task for task in self.tasks.values()
                    if task.assignee == overloaded_member.member_id and task.status == TaskStatus.TODO
                ]
                
                for task in member_tasks:
                    # Find suitable underutilized member
                    for underutilized_member in underutilized:
                        if task.category in underutilized_member.preferred_task_types:
                            reassignments.append({
                                "task_id": task.task_id,
                                "task_title": task.title,
                                "from_member": overloaded_member.name,
                                "to_member": underutilized_member.name,
                                "reason": "Workload balancing"
                            })
                            break
            
            optimization_results["recommendations"] = recommendations
            optimization_results["reassignments"] = reassignments[:5]  # Top 5 suggestions
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Failed to optimize team workload: {e}")
            raise
    
    async def create_project_from_template(self, template_id: str, project_data: Dict[str, Any]) -> Project:
        """Create a new project from a workflow template"""
        
        try:
            if template_id not in self.workflow_templates:
                raise ValueError(f"Template {template_id} not found")
            
            template = self.workflow_templates[template_id]
            
            # Create project
            project = Project(
                project_id=f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=project_data["name"],
                description=project_data["description"],
                project_manager=project_data.get("project_manager"),
                team_members=project_data.get("team_members", []),
                start_date=project_data.get("start_date"),
                target_end_date=project_data.get("target_end_date"),
                budget=project_data.get("budget")
            )
            
            # Create tasks from template
            task_ids = []
            
            for i, task_template in enumerate(template.task_templates):
                task_data = {
                    "title": task_template["title"],
                    "description": f"Task created from template: {template.name}",
                    "category": task_template["category"],
                    "estimated_hours": task_template["estimated_hours"],
                    "project_id": project.project_id
                }
                
                # Set dependencies (each task depends on previous one)
                if i > 0:
                    task_data["dependencies"] = [task_ids[i-1]]
                
                task = await self.create_task(task_data)
                task_ids.append(task.task_id)
            
            project.task_ids = task_ids
            
            # Update template usage
            template.usage_count += 1
            
            # Store project
            self.projects[project.project_id] = project
            
            logger.info(f"Created project from template: {project.project_id}")
            return project
            
        except Exception as e:
            logger.error(f"Failed to create project from template: {e}")
            raise
    
    async def get_project_health_analysis(self, project_id: str) -> Dict[str, Any]:
        """Get AI-powered project health analysis"""
        
        try:
            if project_id not in self.projects:
                raise ValueError(f"Project {project_id} not found")
            
            project = self.projects[project_id]
            project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
            
            # Calculate health metrics
            health_analysis = {
                "overall_health_score": 0.0,
                "progress_health": 0.0,
                "timeline_health": 0.0,
                "budget_health": 0.0,
                "team_health": 0.0,
                "risk_factors": [],
                "recommendations": [],
                "key_metrics": {}
            }
            
            # Progress health
            if project_tasks:
                avg_progress = statistics.mean([task.progress_percentage for task in project_tasks])
                expected_progress = 50.0  # Simplified calculation
                
                progress_variance = abs(avg_progress - expected_progress) / expected_progress
                health_analysis["progress_health"] = max(0, 10 - (progress_variance * 10))
            else:
                health_analysis["progress_health"] = 5.0
            
            # Timeline health
            if project.target_end_date:
                target_date = datetime.fromisoformat(project.target_end_date.replace('Z', '+00:00'))
                days_remaining = (target_date - datetime.now(timezone.utc)).days
                
                if days_remaining > 30:
                    health_analysis["timeline_health"] = 9.0
                elif days_remaining > 14:
                    health_analysis["timeline_health"] = 7.0
                elif days_remaining > 7:
                    health_analysis["timeline_health"] = 5.0
                elif days_remaining > 0:
                    health_analysis["timeline_health"] = 3.0
                else:
                    health_analysis["timeline_health"] = 1.0
            else:
                health_analysis["timeline_health"] = 5.0
            
            # Budget health
            if project.budget and project.actual_cost:
                budget_utilization = project.actual_cost / project.budget
                
                if budget_utilization < 0.7:
                    health_analysis["budget_health"] = 9.0
                elif budget_utilization < 0.9:
                    health_analysis["budget_health"] = 7.0
                elif budget_utilization < 1.0:
                    health_analysis["budget_health"] = 5.0
                else:
                    health_analysis["budget_health"] = 2.0
            else:
                health_analysis["budget_health"] = 5.0
            
            # Team health (based on workload and performance)
            team_performance_scores = []
            for member_id in project.team_members:
                if member_id in self.team_members:
                    member = self.team_members[member_id]
                    team_performance_scores.append(member.performance_score)
            
            if team_performance_scores:
                health_analysis["team_health"] = statistics.mean(team_performance_scores)
            else:
                health_analysis["team_health"] = 7.0
            
            # Overall health score
            health_analysis["overall_health_score"] = statistics.mean([
                health_analysis["progress_health"],
                health_analysis["timeline_health"],
                health_analysis["budget_health"],
                health_analysis["team_health"]
            ])
            
            # Risk factors
            risk_factors = []
            
            if health_analysis["timeline_health"] < 5.0:
                risk_factors.append("Timeline at risk - project may miss deadline")
            
            if health_analysis["budget_health"] < 5.0:
                risk_factors.append("Budget overrun risk - costs exceeding planned budget")
            
            if health_analysis["progress_health"] < 5.0:
                risk_factors.append("Progress behind schedule - tasks not completing as expected")
            
            blocked_tasks = len([task for task in project_tasks if task.status == TaskStatus.BLOCKED])
            if blocked_tasks > 0:
                risk_factors.append(f"{blocked_tasks} tasks are blocked - may impact delivery")
            
            health_analysis["risk_factors"] = risk_factors
            
            # Recommendations
            recommendations = []
            
            if health_analysis["overall_health_score"] < 6.0:
                recommendations.append("Project health is concerning - schedule review meeting with stakeholders")
            
            if health_analysis["timeline_health"] < 5.0:
                recommendations.append("Consider scope reduction or deadline extension")
            
            if health_analysis["budget_health"] < 5.0:
                recommendations.append("Review budget allocation and cost optimization opportunities")
            
            if blocked_tasks > 0:
                recommendations.append("Prioritize unblocking tasks to maintain project momentum")
            
            health_analysis["recommendations"] = recommendations
            
            # Key metrics
            health_analysis["key_metrics"] = {
                "total_tasks": len(project_tasks),
                "completed_tasks": len([task for task in project_tasks if task.status == TaskStatus.COMPLETED]),
                "in_progress_tasks": len([task for task in project_tasks if task.status == TaskStatus.IN_PROGRESS]),
                "blocked_tasks": blocked_tasks,
                "overdue_tasks": len([
                    task for task in project_tasks 
                    if task.due_date and datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) < datetime.now(timezone.utc)
                ])
            }
            
            return health_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze project health: {e}")
            raise
    
    async def get_task_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive task management dashboard data"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Task statistics
            total_tasks = len(self.tasks)
            completed_tasks = len([task for task in self.tasks.values() if task.status == TaskStatus.COMPLETED])
            in_progress_tasks = len([task for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS])
            overdue_tasks = len([
                task for task in self.tasks.values()
                if task.due_date and datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) < current_time
            ])
            
            # Project statistics
            total_projects = len(self.projects)
            active_projects = len([proj for proj in self.projects.values() if proj.status == ProjectStatus.ACTIVE])
            
            # Team statistics
            total_team_members = len(self.team_members)
            avg_utilization = statistics.mean([
                (member.current_workload_hours / member.weekly_capacity_hours) * 100
                for member in self.team_members.values()
            ]) if self.team_members else 0
            
            # Priority distribution
            priority_distribution = {}
            for priority in TaskPriority:
                count = len([task for task in self.tasks.values() if task.priority == priority])
                priority_distribution[priority.value] = count
            
            # Category distribution
            category_distribution = {}
            for category in TaskCategory:
                count = len([task for task in self.tasks.values() if task.category == category])
                if count > 0:
                    category_distribution[category.value] = count
            
            # Recent tasks
            recent_tasks = sorted(
                self.tasks.values(),
                key=lambda x: x.updated_at,
                reverse=True
            )[:10]
            
            # High priority tasks
            high_priority_tasks = [
                task for task in self.tasks.values()
                if task.priority in [TaskPriority.CRITICAL, TaskPriority.URGENT, TaskPriority.HIGH]
                and task.status != TaskStatus.COMPLETED
            ]
            
            # Team workload
            team_workload = {}
            for member in self.team_members.values():
                utilization = (member.current_workload_hours / member.weekly_capacity_hours) * 100
                team_workload[member.name] = {
                    "utilization": round(utilization, 1),
                    "current_tasks": len([
                        task for task in self.tasks.values()
                        if task.assignee == member.member_id and task.status != TaskStatus.COMPLETED
                    ]),
                    "status": "overloaded" if utilization > 100 else "optimal" if utilization > 80 else "available"
                }
            
            dashboard_data = {
                "task_overview": {
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "in_progress_tasks": in_progress_tasks,
                    "overdue_tasks": overdue_tasks,
                    "completion_rate": round((completed_tasks / max(total_tasks, 1)) * 100, 1)
                },
                "project_overview": {
                    "total_projects": total_projects,
                    "active_projects": active_projects,
                    "avg_project_health": round(statistics.mean([
                        proj.ai_health_score for proj in self.projects.values()
                        if proj.ai_health_score > 0
                    ]), 1) if any(proj.ai_health_score > 0 for proj in self.projects.values()) else 0
                },
                "team_overview": {
                    "total_members": total_team_members,
                    "avg_utilization": round(avg_utilization, 1),
                    "overloaded_members": len([
                        member for member in self.team_members.values()
                        if (member.current_workload_hours / member.weekly_capacity_hours) > 1.0
                    ])
                },
                "priority_distribution": priority_distribution,
                "category_distribution": category_distribution,
                "recent_tasks": [
                    {
                        "task_id": task.task_id,
                        "title": task.title,
                        "priority": task.priority.value,
                        "status": task.status.value,
                        "assignee": self.team_members.get(task.assignee, {}).get("name", "Unassigned") if task.assignee else "Unassigned",
                        "due_date": task.due_date,
                        "progress": task.progress_percentage
                    }
                    for task in recent_tasks
                ],
                "high_priority_tasks": [
                    {
                        "task_id": task.task_id,
                        "title": task.title,
                        "priority": task.priority.value,
                        "assignee": self.team_members.get(task.assignee, {}).get("name", "Unassigned") if task.assignee else "Unassigned",
                        "due_date": task.due_date,
                        "ai_priority_score": task.ai_priority_score
                    }
                    for task in sorted(high_priority_tasks, key=lambda x: x.ai_priority_score, reverse=True)[:5]
                ],
                "team_workload": team_workload,
                "ai_recommendations": await self._generate_dashboard_recommendations()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get task dashboard data: {e}")
            raise
    
    async def _generate_dashboard_recommendations(self) -> List[str]:
        """Generate AI-powered dashboard recommendations"""
        
        recommendations = []
        
        # Check for overdue tasks
        overdue_count = len([
            task for task in self.tasks.values()
            if task.due_date and datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) < datetime.now(timezone.utc)
        ])
        
        if overdue_count > 0:
            recommendations.append(f"🚨 {overdue_count} tasks are overdue - prioritize completion or reschedule")
        
        # Check team utilization
        overloaded_members = [
            member for member in self.team_members.values()
            if (member.current_workload_hours / member.weekly_capacity_hours) > 1.0
        ]
        
        if overloaded_members:
            recommendations.append(f"⚠️ {len(overloaded_members)} team members are overloaded - consider workload rebalancing")
        
        # Check project health
        unhealthy_projects = [
            proj for proj in self.projects.values()
            if proj.ai_health_score > 0 and proj.ai_health_score < 6.0
        ]
        
        if unhealthy_projects:
            recommendations.append(f"📊 {len(unhealthy_projects)} projects have low health scores - review and take action")
        
        # Check blocked tasks
        blocked_count = len([task for task in self.tasks.values() if task.status == TaskStatus.BLOCKED])
        
        if blocked_count > 0:
            recommendations.append(f"🚧 {blocked_count} tasks are blocked - identify and resolve blockers")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "✅ All systems running smoothly - maintain current productivity levels",
                "🎯 Consider creating new workflow templates for recurring processes",
                "📈 Review team performance metrics and identify optimization opportunities"
            ]
        
        return recommendations

# Global AI task management engine
ai_task_manager = AITaskManagementEngine()