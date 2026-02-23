"""
Advanced Project & Task Management System
Comprehensive project orchestration with AI-powered task management
Integrates with all business tools and provides intelligent automation
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    FEATURE = "feature"
    BUG = "bug"
    RESEARCH = "research"
    MARKETING = "marketing"
    SALES = "sales"
    LEGAL = "legal"
    FINANCE = "finance"
    OPERATIONS = "operations"
    STRATEGIC = "strategic"

@dataclass
class TaskDependency:
    """Task dependency relationship"""
    task_id: str
    dependency_type: str  # "blocks", "depends_on", "related"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class TaskComment:
    """Task comment/update"""
    comment_id: str
    author: str
    content: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    attachments: List[str] = field(default_factory=list)

@dataclass
class TaskTimeLog:
    """Time tracking for tasks"""
    log_id: str
    user: str
    start_time: str
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Task:
    """Comprehensive task with AI-powered features"""
    task_id: str
    title: str
    description: str
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    project_id: str
    assignee: Optional[str] = None
    reporter: str = "system"
    
    # Scheduling
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    
    # Estimation & Tracking
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    story_points: Optional[int] = None
    
    # Relationships
    dependencies: List[TaskDependency] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    parent_task: Optional[str] = None
    
    # Collaboration
    comments: List[TaskComment] = field(default_factory=list)
    time_logs: List[TaskTimeLog] = field(default_factory=list)
    watchers: List[str] = field(default_factory=list)
    
    # AI Features
    ai_suggestions: List[str] = field(default_factory=list)
    automation_rules: List[Dict[str, Any]] = field(default_factory=list)
    
    # Integration
    external_links: Dict[str, str] = field(default_factory=dict)  # tool_name -> link
    tool_integrations: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProjectMilestone:
    """Project milestone tracking"""
    milestone_id: str
    name: str
    description: str
    due_date: str
    status: str  # "upcoming", "in_progress", "completed", "overdue"
    completion_percentage: float = 0.0
    associated_tasks: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Project:
    """Comprehensive project management"""
    project_id: str
    name: str
    description: str
    status: ProjectStatus
    owner: str
    
    # Timeline
    start_date: str
    end_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # Team & Resources
    team_members: List[str] = field(default_factory=list)
    budget: Optional[float] = None
    budget_spent: float = 0.0
    
    # Progress Tracking
    completion_percentage: float = 0.0
    milestones: List[ProjectMilestone] = field(default_factory=list)
    
    # Business Context
    business_objectives: List[str] = field(default_factory=list)
    success_metrics: List[Dict[str, Any]] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    # AI & Automation
    ai_insights: List[str] = field(default_factory=list)
    automation_workflows: List[Dict[str, Any]] = field(default_factory=list)
    
    # Integration
    connected_tools: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    external_project_ids: Dict[str, str] = field(default_factory=dict)  # tool -> project_id
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

class ProjectTaskManager:
    """
    Advanced Project & Task Management System
    - AI-powered task creation and management
    - Universal tool integration
    - Intelligent automation and orchestration
    - Real-time collaboration and tracking
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Storage
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_templates: Dict[str, Dict[str, Any]] = {}
        
        # AI & Automation
        self.ai_workflows: Dict[str, Dict[str, Any]] = {}
        self.automation_rules: List[Dict[str, Any]] = []
        
        # Integration Framework
        self.tool_connectors: Dict[str, Any] = {}
        self.integration_configs: Dict[str, Dict[str, Any]] = {}
        
        self._initialize_task_templates()
        self._initialize_automation_rules()
    
    def _initialize_task_templates(self):
        """Initialize common task templates"""
        
        self.task_templates = {
            "feature_development": {
                "title_template": "Develop {feature_name}",
                "description_template": "Implement {feature_name} with the following requirements:\n{requirements}",
                "task_type": TaskType.FEATURE,
                "estimated_hours": 8,
                "story_points": 5,
                "subtask_templates": [
                    "Research and design {feature_name}",
                    "Implement core functionality",
                    "Write unit tests",
                    "Integration testing",
                    "Documentation",
                    "Code review"
                ]
            },
            "marketing_campaign": {
                "title_template": "Launch {campaign_name} Campaign",
                "description_template": "Execute marketing campaign for {campaign_name}:\n{campaign_details}",
                "task_type": TaskType.MARKETING,
                "estimated_hours": 16,
                "story_points": 8,
                "subtask_templates": [
                    "Define campaign strategy",
                    "Create campaign assets",
                    "Set up tracking and analytics",
                    "Launch campaign",
                    "Monitor and optimize",
                    "Analyze results"
                ]
            },
            "fundraising_round": {
                "title_template": "{round_type} Fundraising Round",
                "description_template": "Execute {round_type} fundraising round to raise {target_amount}",
                "task_type": TaskType.STRATEGIC,
                "estimated_hours": 80,
                "story_points": 21,
                "subtask_templates": [
                    "Prepare pitch deck",
                    "Update financial models",
                    "Research target investors",
                    "Prepare due diligence materials",
                    "Conduct investor outreach",
                    "Manage investor meetings",
                    "Negotiate terms",
                    "Close funding round"
                ]
            },
            "product_launch": {
                "title_template": "Launch {product_name}",
                "description_template": "Complete product launch for {product_name}",
                "task_type": TaskType.STRATEGIC,
                "estimated_hours": 120,
                "story_points": 34,
                "subtask_templates": [
                    "Finalize product features",
                    "Complete QA testing",
                    "Prepare launch materials",
                    "Set up analytics and monitoring",
                    "Execute go-to-market strategy",
                    "Launch product",
                    "Monitor launch metrics",
                    "Post-launch optimization"
                ]
            }
        }
    
    def _initialize_automation_rules(self):
        """Initialize intelligent automation rules"""
        
        self.automation_rules = [
            {
                "name": "Auto-assign based on expertise",
                "trigger": "task_created",
                "conditions": [
                    {"field": "task_type", "operator": "equals", "value": "FEATURE"},
                    {"field": "assignee", "operator": "is_null"}
                ],
                "actions": [
                    {"type": "assign_to_expert", "skill_required": "development"}
                ]
            },
            {
                "name": "Escalate overdue high-priority tasks",
                "trigger": "daily_check",
                "conditions": [
                    {"field": "priority", "operator": "in", "value": ["HIGH", "URGENT", "CRITICAL"]},
                    {"field": "status", "operator": "not_in", "value": ["DONE", "CANCELLED"]},
                    {"field": "due_date", "operator": "overdue"}
                ],
                "actions": [
                    {"type": "notify_stakeholders"},
                    {"type": "create_escalation_task"}
                ]
            },
            {
                "name": "Auto-create follow-up tasks",
                "trigger": "task_completed",
                "conditions": [
                    {"field": "task_type", "operator": "equals", "value": "RESEARCH"}
                ],
                "actions": [
                    {"type": "create_implementation_task"},
                    {"type": "schedule_review_meeting"}
                ]
            }
        ]
    
    async def create_project_from_blueprint(self, blueprint: CompanyBlueprint, 
                                          project_type: str = "business_launch") -> Project:
        """Create comprehensive project from company blueprint"""
        
        try:
            project_id = f"proj_{uuid.uuid4().hex[:8]}"
            
            # Generate AI-powered project plan
            project_plan = await self._generate_ai_project_plan(blueprint, project_type)
            
            # Create main project
            project = Project(
                project_id=project_id,
                name=f"{blueprint.name} - {project_type.replace('_', ' ').title()}",
                description=project_plan["description"],
                status=ProjectStatus.PLANNING,
                owner="founder",
                start_date=datetime.now(timezone.utc).isoformat(),
                end_date=project_plan.get("estimated_end_date"),
                business_objectives=project_plan["objectives"],
                success_metrics=project_plan["success_metrics"],
                risk_factors=project_plan["risk_factors"],
                budget=blueprint.funding_requirements,
                tags=[blueprint.industry, project_type]
            )
            
            # Create milestones
            for milestone_data in project_plan["milestones"]:
                milestone = ProjectMilestone(
                    milestone_id=f"ms_{uuid.uuid4().hex[:8]}",
                    name=milestone_data["name"],
                    description=milestone_data["description"],
                    due_date=milestone_data["due_date"],
                    status="upcoming"
                )
                project.milestones.append(milestone)
            
            # Create initial tasks
            tasks = await self._create_tasks_from_plan(project_id, project_plan["tasks"])
            
            # Store project and tasks
            self.projects[project_id] = project
            for task in tasks:
                self.tasks[task.task_id] = task
            
            logger.info(f"Created project {project_id} with {len(tasks)} tasks")
            return project
            
        except Exception as e:
            logger.error(f"Project creation failed: {e}")
            raise
    
    async def _generate_ai_project_plan(self, blueprint: CompanyBlueprint, 
                                       project_type: str) -> Dict[str, Any]:
        """Generate AI-powered project plan"""
        
        prompt = f"""
        Create a comprehensive project plan for launching {blueprint.name}.
        
        Company Details:
        - Industry: {blueprint.industry}
        - Business Model: {blueprint.business_model}
        - Target Market: {blueprint.target_market.primary_segment}
        - Key Features: {', '.join(blueprint.key_features)}
        - Funding: ${blueprint.funding_requirements:,}
        
        Project Type: {project_type}
        
        Generate a detailed project plan with:
        1. Project description and scope
        2. 5-8 key business objectives
        3. Success metrics with targets
        4. Major risk factors
        5. 6-10 milestones with dates (6-month timeline)
        6. 20-30 high-level tasks organized by phase
        
        Format as JSON with clear structure.
        """
        
        try:
            response = await self.llm_manager.generate_structured_response(
                messages=[LLMMessage(role="user", content=prompt)],
                response_format="json"
            )
            
            return json.loads(response.content)
            
        except Exception as e:
            logger.warning(f"AI project plan generation failed: {e}")
            return self._fallback_project_plan(blueprint, project_type)
    
    def _fallback_project_plan(self, blueprint: CompanyBlueprint, 
                              project_type: str) -> Dict[str, Any]:
        """Fallback project plan if AI generation fails"""
        
        return {
            "description": f"Launch and scale {blueprint.name} in the {blueprint.industry} market",
            "objectives": [
                "Achieve product-market fit",
                "Build scalable technology platform",
                "Establish market presence",
                "Generate sustainable revenue",
                "Build strong team and culture"
            ],
            "success_metrics": [
                {"metric": "Monthly Recurring Revenue", "target": 50000, "unit": "USD"},
                {"metric": "Customer Acquisition", "target": 1000, "unit": "customers"},
                {"metric": "Product-Market Fit Score", "target": 40, "unit": "score"},
                {"metric": "Team Size", "target": 15, "unit": "employees"}
            ],
            "risk_factors": [
                "Market competition intensity",
                "Technology scalability challenges",
                "Customer acquisition cost optimization",
                "Funding runway management"
            ],
            "milestones": [
                {
                    "name": "MVP Development",
                    "description": "Complete minimum viable product",
                    "due_date": (datetime.now() + timedelta(days=60)).isoformat()
                },
                {
                    "name": "Beta Launch",
                    "description": "Launch beta version to early users",
                    "due_date": (datetime.now() + timedelta(days=90)).isoformat()
                },
                {
                    "name": "Public Launch",
                    "description": "Full public product launch",
                    "due_date": (datetime.now() + timedelta(days=120)).isoformat()
                },
                {
                    "name": "Series A Readiness",
                    "description": "Prepare for Series A fundraising",
                    "due_date": (datetime.now() + timedelta(days=180)).isoformat()
                }
            ],
            "tasks": [
                {"title": "Develop core product features", "type": "FEATURE", "priority": "HIGH"},
                {"title": "Set up development infrastructure", "type": "OPERATIONS", "priority": "HIGH"},
                {"title": "Create brand identity and website", "type": "MARKETING", "priority": "MEDIUM"},
                {"title": "Establish legal entity and compliance", "type": "LEGAL", "priority": "HIGH"},
                {"title": "Set up financial systems", "type": "FINANCE", "priority": "MEDIUM"}
            ],
            "estimated_end_date": (datetime.now() + timedelta(days=180)).isoformat()
        }
    
    async def _create_tasks_from_plan(self, project_id: str, 
                                     task_plans: List[Dict[str, Any]]) -> List[Task]:
        """Create tasks from project plan"""
        
        tasks = []
        
        for i, task_plan in enumerate(task_plans):
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            
            task = Task(
                task_id=task_id,
                title=task_plan["title"],
                description=task_plan.get("description", ""),
                task_type=TaskType(task_plan.get("type", "FEATURE").lower()),
                status=TaskStatus.BACKLOG,
                priority=TaskPriority(task_plan.get("priority", "MEDIUM").lower()),
                project_id=project_id,
                estimated_hours=task_plan.get("estimated_hours", 8),
                story_points=task_plan.get("story_points", 3),
                due_date=task_plan.get("due_date"),
                tags=task_plan.get("tags", [])
            )
            
            # Add AI suggestions
            task.ai_suggestions = await self._generate_task_suggestions(task)
            
            tasks.append(task)
        
        return tasks
    
    async def _generate_task_suggestions(self, task: Task) -> List[str]:
        """Generate AI-powered task suggestions"""
        
        suggestions = [
            f"Break down '{task.title}' into smaller, manageable subtasks",
            "Consider dependencies with other tasks in the project",
            "Define clear acceptance criteria and success metrics",
            "Identify required resources and team members"
        ]
        
        # Add type-specific suggestions
        if task.task_type == TaskType.FEATURE:
            suggestions.extend([
                "Create user stories and acceptance criteria",
                "Design technical architecture and API specifications",
                "Plan testing strategy and quality assurance"
            ])
        elif task.task_type == TaskType.MARKETING:
            suggestions.extend([
                "Define target audience and messaging",
                "Set up tracking and analytics",
                "Plan A/B testing for optimization"
            ])
        
        return suggestions
    
    async def create_task_from_template(self, project_id: str, template_name: str, 
                                      variables: Dict[str, Any]) -> Task:
        """Create task from predefined template"""
        
        if template_name not in self.task_templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.task_templates[template_name]
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        # Format template strings
        title = template["title_template"].format(**variables)
        description = template["description_template"].format(**variables)
        
        # Create main task
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            task_type=template["task_type"],
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            project_id=project_id,
            estimated_hours=template.get("estimated_hours"),
            story_points=template.get("story_points")
        )
        
        # Create subtasks if template has them
        if "subtask_templates" in template:
            for subtask_template in template["subtask_templates"]:
                subtask_id = f"task_{uuid.uuid4().hex[:8]}"
                subtask_title = subtask_template.format(**variables)
                
                subtask = Task(
                    task_id=subtask_id,
                    title=subtask_title,
                    description=f"Subtask of: {title}",
                    task_type=template["task_type"],
                    status=TaskStatus.BACKLOG,
                    priority=TaskPriority.MEDIUM,
                    project_id=project_id,
                    parent_task=task_id,
                    estimated_hours=template.get("estimated_hours", 8) / len(template["subtask_templates"])
                )
                
                task.subtasks.append(subtask_id)
                self.tasks[subtask_id] = subtask
        
        # Add AI suggestions
        task.ai_suggestions = await self._generate_task_suggestions(task)
        
        self.tasks[task_id] = task
        return task
    
    async def update_task_status(self, task_id: str, new_status: TaskStatus, 
                               user: str = "system") -> bool:
        """Update task status with automation triggers"""
        
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now(timezone.utc).isoformat()
        
        # Add status change comment
        comment = TaskComment(
            comment_id=f"comment_{uuid.uuid4().hex[:8]}",
            author=user,
            content=f"Status changed from {old_status.value} to {new_status.value}"
        )
        task.comments.append(comment)
        
        # Trigger automation rules
        await self._trigger_automation_rules("task_status_changed", {
            "task": task,
            "old_status": old_status,
            "new_status": new_status,
            "user": user
        })
        
        # Update project completion if task is done
        if new_status == TaskStatus.DONE:
            await self._update_project_completion(task.project_id)
        
        return True
    
    async def _trigger_automation_rules(self, trigger: str, context: Dict[str, Any]):
        """Trigger automation rules based on events"""
        
        for rule in self.automation_rules:
            if rule["trigger"] == trigger:
                if await self._evaluate_rule_conditions(rule["conditions"], context):
                    await self._execute_rule_actions(rule["actions"], context)
    
    async def _evaluate_rule_conditions(self, conditions: List[Dict[str, Any]], 
                                       context: Dict[str, Any]) -> bool:
        """Evaluate automation rule conditions"""
        
        for condition in conditions:
            field = condition["field"]
            operator = condition["operator"]
            value = condition["value"]
            
            # Get field value from context
            if "task" in context and hasattr(context["task"], field):
                field_value = getattr(context["task"], field)
                if hasattr(field_value, 'value'):  # Handle enums
                    field_value = field_value.value
            else:
                field_value = context.get(field)
            
            # Evaluate condition
            if operator == "equals" and field_value != value:
                return False
            elif operator == "not_equals" and field_value == value:
                return False
            elif operator == "in" and field_value not in value:
                return False
            elif operator == "not_in" and field_value in value:
                return False
            elif operator == "is_null" and field_value is not None:
                return False
            elif operator == "overdue":
                if field == "due_date" and field_value:
                    due_date = datetime.fromisoformat(field_value.replace('Z', '+00:00'))
                    if due_date > datetime.now(timezone.utc):
                        return False
        
        return True
    
    async def _execute_rule_actions(self, actions: List[Dict[str, Any]], 
                                   context: Dict[str, Any]):
        """Execute automation rule actions"""
        
        for action in actions:
            action_type = action["type"]
            
            if action_type == "assign_to_expert":
                await self._auto_assign_task(context["task"], action.get("skill_required"))
            elif action_type == "notify_stakeholders":
                await self._notify_stakeholders(context["task"])
            elif action_type == "create_escalation_task":
                await self._create_escalation_task(context["task"])
            elif action_type == "create_implementation_task":
                await self._create_follow_up_task(context["task"], "implementation")
            elif action_type == "schedule_review_meeting":
                await self._schedule_review_meeting(context["task"])
    
    async def _auto_assign_task(self, task: Task, skill_required: str):
        """Auto-assign task based on team expertise"""
        
        # Simplified assignment logic - in production, this would use team skill matrix
        skill_assignments = {
            "development": "tech_lead",
            "marketing": "marketing_manager",
            "sales": "sales_manager",
            "finance": "finance_manager",
            "legal": "legal_counsel"
        }
        
        assignee = skill_assignments.get(skill_required, "project_manager")
        task.assignee = assignee
        
        # Add assignment comment
        comment = TaskComment(
            comment_id=f"comment_{uuid.uuid4().hex[:8]}",
            author="system",
            content=f"Auto-assigned to {assignee} based on required skill: {skill_required}"
        )
        task.comments.append(comment)
    
    async def _update_project_completion(self, project_id: str):
        """Update project completion percentage"""
        
        if project_id not in self.projects:
            return
        
        project = self.projects[project_id]
        project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
        
        if not project_tasks:
            return
        
        completed_tasks = [task for task in project_tasks if task.status == TaskStatus.DONE]
        completion_percentage = (len(completed_tasks) / len(project_tasks)) * 100
        
        project.completion_percentage = completion_percentage
        project.updated_at = datetime.now(timezone.utc).isoformat()
        
        # Update milestone completion
        for milestone in project.milestones:
            milestone_tasks = [task for task in project_tasks 
                             if task.task_id in milestone.associated_tasks]
            if milestone_tasks:
                completed_milestone_tasks = [task for task in milestone_tasks 
                                           if task.status == TaskStatus.DONE]
                milestone.completion_percentage = (len(completed_milestone_tasks) / len(milestone_tasks)) * 100
                
                if milestone.completion_percentage == 100:
                    milestone.status = "completed"
                elif milestone.completion_percentage > 0:
                    milestone.status = "in_progress"
    
    async def create_sprint(self, sprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Minimal shim for quick-actions. Creates a synthetic sprint result using provided tasks.
        """
        sid = f"sprint_{uuid.uuid4().hex[:8]}"
        name = sprint_data.get("name", f"AI Sprint - {datetime.now(timezone.utc).strftime('%B %Y')}")
        tasks = sprint_data.get("tasks") or [
            {"title": "Kickoff and planning", "effort_hours": 2, "priority": "High"},
            {"title": "Implement core item", "effort_hours": 10, "priority": "High"},
            {"title": "Testing & QA", "effort_hours": 6, "priority": "Medium"},
        ]
        return {
            "id": sid,
            "name": name,
            "tasks": tasks,
            "estimated_completion": (datetime.now(timezone.utc) + timedelta(days=sprint_data.get("duration", 14))).isoformat()
        }

    async def get_ready_features(self, business_id: str) -> List[Dict[str, Any]]:
        """
        Minimal shim for quick-actions. Returns a small list of deployable features.
        """
        return [
            {"name": "Onboarding improvements", "version": "1.2.0"},
            {"name": "Analytics filters", "version": "1.1.5"},
            {"name": "Email notification tweaks", "version": "1.0.9"},
        ]

    def get_project_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive project dashboard data"""
        
        if project_id not in self.projects:
            return {}
        
        project = self.projects[project_id]
        project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
        
        # Task statistics
        task_stats = {
            "total": len(project_tasks),
            "by_status": {},
            "by_priority": {},
            "by_type": {},
            "overdue": 0,
            "completed_this_week": 0
        }
        
        for task in project_tasks:
            # Status distribution
            status = task.status.value
            task_stats["by_status"][status] = task_stats["by_status"].get(status, 0) + 1
            
            # Priority distribution
            priority = task.priority.value
            task_stats["by_priority"][priority] = task_stats["by_priority"].get(priority, 0) + 1
            
            # Type distribution
            task_type = task.task_type.value
            task_stats["by_type"][task_type] = task_stats["by_type"].get(task_type, 0) + 1
            
            # Overdue tasks
            if task.due_date and task.status != TaskStatus.DONE:
                due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                if due_date < datetime.now(timezone.utc):
                    task_stats["overdue"] += 1
            
            # Completed this week
            if task.status == TaskStatus.DONE:
                updated_date = datetime.fromisoformat(task.updated_at.replace('Z', '+00:00'))
                week_ago = datetime.now(timezone.utc) - timedelta(days=7)
                if updated_date > week_ago:
                    task_stats["completed_this_week"] += 1
        
        # Budget tracking
        budget_info = {
            "total_budget": project.budget or 0,
            "spent": project.budget_spent,
            "remaining": (project.budget or 0) - project.budget_spent,
            "burn_rate": project.budget_spent / max(1, (datetime.now(timezone.utc) - 
                        datetime.fromisoformat(project.created_at.replace('Z', '+00:00'))).days)
        }
        
        # Timeline analysis
        timeline_info = {
            "start_date": project.start_date,
            "end_date": project.end_date,
            "days_elapsed": (datetime.now(timezone.utc) - 
                           datetime.fromisoformat(project.start_date.replace('Z', '+00:00'))).days,
            "completion_percentage": project.completion_percentage,
            "milestones": [asdict(milestone) for milestone in project.milestones]
        }
        
        return {
            "project": asdict(project),
            "task_statistics": task_stats,
            "budget_tracking": budget_info,
            "timeline_analysis": timeline_info,
            "recent_activity": self._get_recent_activity(project_id),
            "ai_insights": []  # Will be populated by async method
        }
    
    def _get_recent_activity(self, project_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent project activity"""
        
        activities = []
        project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
        
        for task in project_tasks:
            # Task updates
            activities.append({
                "type": "task_updated",
                "timestamp": task.updated_at,
                "description": f"Task '{task.title}' updated",
                "task_id": task.task_id
            })
            
            # Comments
            for comment in task.comments[-3:]:  # Last 3 comments per task
                activities.append({
                    "type": "comment_added",
                    "timestamp": comment.created_at,
                    "description": f"Comment added to '{task.title}'",
                    "author": comment.author,
                    "task_id": task.task_id
                })
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:limit]
    
    def _generate_project_insights(self, project: Project, 
                                  tasks: List[Task]) -> List[str]:
        """Generate AI-powered project insights"""
        
        insights = []
        
        # Completion rate analysis
        if project.completion_percentage < 30:
            insights.append("🚨 Project progress is behind schedule. Consider reviewing task priorities and resource allocation.")
        elif project.completion_percentage > 80:
            insights.append("🎉 Project is nearing completion! Start planning post-launch activities.")
        
        # Task distribution analysis
        overdue_tasks = [task for task in tasks if task.due_date and task.status != TaskStatus.DONE and
                        datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) < datetime.now(timezone.utc)]
        
        if len(overdue_tasks) > 3:
            insights.append(f"⚠️ {len(overdue_tasks)} tasks are overdue. Consider reassigning or extending deadlines.")
        
        # Budget analysis
        if project.budget and project.budget_spent > project.budget * 0.8:
            insights.append("💰 Budget utilization is high. Monitor spending closely to avoid overruns.")
        
        # Team workload analysis
        assignee_counts = {}
        for task in tasks:
            if task.assignee and task.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]:
                assignee_counts[task.assignee] = assignee_counts.get(task.assignee, 0) + 1
        
        if assignee_counts:
            max_tasks = max(assignee_counts.values())
            if max_tasks > 5:
                insights.append("👥 Some team members may be overloaded. Consider redistributing tasks.")
        
        return insights
    
    def export_project_data(self, project_id: str, format: str = "json") -> Dict[str, Any]:
        """Export comprehensive project data"""
        
        if project_id not in self.projects:
            return {}
        
        project = self.projects[project_id]
        project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
        
        export_data = {
            "project": asdict(project),
            "tasks": [asdict(task) for task in project_tasks],
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "export_format": format
        }
        
        return export_data

# Global project task manager
project_task_manager = ProjectTaskManager()