"""
Founder Orchestration System
Complete business orchestration platform for founders
Integrates all systems: project management, tools, AI, and business operations
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

from core.project_task_manager import project_task_manager, Project, Task
from core.universal_tool_integration import universal_tools
from core.ai_orchestration_engine import ai_orchestrator, AIRequest, AICapability
from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class BusinessPhase(Enum):
    IDEATION = "ideation"
    VALIDATION = "validation"
    MVP_DEVELOPMENT = "mvp_development"
    LAUNCH = "launch"
    GROWTH = "growth"
    SCALE = "scale"
    EXIT = "exit"

class OrchestrationPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

@dataclass
class BusinessContext:
    """Current business context and state"""
    company_blueprint: CompanyBlueprint
    current_phase: BusinessPhase
    active_projects: List[str] = field(default_factory=list)
    connected_tools: List[str] = field(default_factory=list)
    key_metrics: Dict[str, float] = field(default_factory=dict)
    current_challenges: List[str] = field(default_factory=list)
    upcoming_milestones: List[Dict[str, Any]] = field(default_factory=list)
    team_size: int = 1
    monthly_burn_rate: float = 0.0
    runway_months: float = 12.0
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class OrchestrationAction:
    """Automated action to be executed"""
    action_id: str
    action_type: str  # "create_task", "connect_tool", "ai_workflow", "notification"
    priority: OrchestrationPriority
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    scheduled_for: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_impact: str = "medium"  # "low", "medium", "high"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "pending"  # "pending", "executing", "completed", "failed"

@dataclass
class OrchestrationInsight:
    """AI-generated business insight"""
    insight_id: str
    category: str  # "opportunity", "risk", "optimization", "strategic"
    title: str
    description: str
    confidence_score: float  # 0-1
    potential_impact: str  # "low", "medium", "high"
    recommended_actions: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class FounderOrchestrationSystem:
    """
    Complete Business Orchestration Platform
    - Intelligent business management and automation
    - Unified project, task, and tool coordination
    - AI-powered insights and recommendations
    - Real-time business intelligence and optimization
    - Automated workflow execution across all business functions
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Business context and state
        self.business_contexts: Dict[str, BusinessContext] = {}
        self.current_context_id: Optional[str] = None
        
        # Orchestration management
        self.pending_actions: Dict[str, OrchestrationAction] = {}
        self.completed_actions: Dict[str, OrchestrationAction] = {}
        self.insights: Dict[str, OrchestrationInsight] = {}
        
        # Automation and workflows
        self.orchestration_rules: List[Dict[str, Any]] = []
        self.automation_schedules: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.orchestration_metrics: Dict[str, Any] = {
            "actions_executed": 0,
            "tools_connected": 0,
            "projects_managed": 0,
            "insights_generated": 0,
            "automation_success_rate": 0.0
        }
        
        self._initialize_orchestration_rules()
    
    def _initialize_orchestration_rules(self):
        """Initialize intelligent orchestration rules"""
        
        self.orchestration_rules = [
            {
                "name": "New Business Setup",
                "trigger": "business_context_created",
                "conditions": [
                    {"field": "current_phase", "operator": "equals", "value": "ideation"}
                ],
                "actions": [
                    {
                        "type": "create_project",
                        "template": "business_launch",
                        "priority": "high"
                    },
                    {
                        "type": "connect_essential_tools",
                        "tools": ["github", "slack", "notion", "stripe"],
                        "priority": "medium"
                    },
                    {
                        "type": "ai_workflow",
                        "workflow": "business_analysis_workflow",
                        "priority": "high"
                    }
                ]
            },
            {
                "name": "MVP Development Phase",
                "trigger": "phase_transition",
                "conditions": [
                    {"field": "new_phase", "operator": "equals", "value": "mvp_development"}
                ],
                "actions": [
                    {
                        "type": "create_tasks",
                        "template": "feature_development",
                        "priority": "high"
                    },
                    {
                        "type": "connect_dev_tools",
                        "tools": ["github", "vercel", "linear"],
                        "priority": "high"
                    },
                    {
                        "type": "setup_monitoring",
                        "tools": ["google_analytics", "mixpanel"],
                        "priority": "medium"
                    }
                ]
            },
            {
                "name": "Launch Phase Preparation",
                "trigger": "phase_transition",
                "conditions": [
                    {"field": "new_phase", "operator": "equals", "value": "launch"}
                ],
                "actions": [
                    {
                        "type": "create_tasks",
                        "template": "product_launch",
                        "priority": "critical"
                    },
                    {
                        "type": "connect_marketing_tools",
                        "tools": ["mailchimp", "google_analytics", "hubspot"],
                        "priority": "high"
                    },
                    {
                        "type": "ai_workflow",
                        "workflow": "content_creation_pipeline",
                        "priority": "high"
                    }
                ]
            },
            {
                "name": "Growth Phase Optimization",
                "trigger": "phase_transition",
                "conditions": [
                    {"field": "new_phase", "operator": "equals", "value": "growth"}
                ],
                "actions": [
                    {
                        "type": "setup_advanced_analytics",
                        "tools": ["mixpanel", "google_analytics", "hubspot"],
                        "priority": "high"
                    },
                    {
                        "type": "create_growth_experiments",
                        "priority": "medium"
                    },
                    {
                        "type": "optimize_conversion_funnel",
                        "priority": "high"
                    }
                ]
            },
            {
                "name": "Runway Alert",
                "trigger": "metric_threshold",
                "conditions": [
                    {"field": "runway_months", "operator": "less_than", "value": 6}
                ],
                "actions": [
                    {
                        "type": "create_tasks",
                        "template": "fundraising_round",
                        "priority": "urgent"
                    },
                    {
                        "type": "ai_workflow",
                        "workflow": "fundraising_preparation",
                        "priority": "urgent"
                    },
                    {
                        "type": "notification",
                        "message": "⚠️ Runway below 6 months - fundraising required",
                        "priority": "critical"
                    }
                ]
            },
            {
                "name": "Performance Optimization",
                "trigger": "daily_check",
                "conditions": [
                    {"field": "key_metrics.conversion_rate", "operator": "less_than", "value": 0.02}
                ],
                "actions": [
                    {
                        "type": "ai_analysis",
                        "focus": "conversion_optimization",
                        "priority": "medium"
                    },
                    {
                        "type": "create_optimization_tasks",
                        "priority": "medium"
                    }
                ]
            }
        ]
    
    async def create_business_context(self, blueprint: CompanyBlueprint, 
                                    initial_phase: BusinessPhase = BusinessPhase.IDEATION) -> str:
        """Create new business context and initialize orchestration"""
        
        context_id = f"ctx_{uuid.uuid4().hex[:8]}"
        
        # Create business context
        context = BusinessContext(
            company_blueprint=blueprint,
            current_phase=initial_phase,
            key_metrics={
                "monthly_revenue": 0.0,
                "customer_count": 0,
                "conversion_rate": 0.0,
                "churn_rate": 0.0,
                "customer_acquisition_cost": 0.0,
                "lifetime_value": 0.0
            },
            monthly_burn_rate=blueprint.funding_requirements * 0.1,  # Estimate 10% monthly burn
            runway_months=12.0
        )
        
        self.business_contexts[context_id] = context
        self.current_context_id = context_id
        
        # Trigger initial orchestration
        await self._trigger_orchestration_rules("business_context_created", {
            "context": context,
            "context_id": context_id
        })
        
        logger.info(f"Created business context {context_id} for {blueprint.name}")
        return context_id
    
    async def update_business_phase(self, context_id: str, new_phase: BusinessPhase) -> bool:
        """Update business phase and trigger phase-specific orchestration"""
        
        if context_id not in self.business_contexts:
            return False
        
        context = self.business_contexts[context_id]
        old_phase = context.current_phase
        context.current_phase = new_phase
        context.last_updated = datetime.now(timezone.utc).isoformat()
        
        # Trigger phase transition orchestration
        await self._trigger_orchestration_rules("phase_transition", {
            "context": context,
            "context_id": context_id,
            "old_phase": old_phase,
            "new_phase": new_phase
        })
        
        logger.info(f"Updated business phase from {old_phase.value} to {new_phase.value}")
        return True
    
    async def update_business_metrics(self, context_id: str, metrics: Dict[str, float]) -> bool:
        """Update business metrics and trigger metric-based orchestration"""
        
        if context_id not in self.business_contexts:
            return False
        
        context = self.business_contexts[context_id]
        
        # Update metrics
        for key, value in metrics.items():
            context.key_metrics[key] = value
        
        # Update runway calculation
        if "monthly_revenue" in metrics and "monthly_burn_rate" in context.__dict__:
            net_burn = context.monthly_burn_rate - metrics.get("monthly_revenue", 0)
            if net_burn > 0:
                # Estimate remaining funding (simplified)
                estimated_funding = context.company_blueprint.funding_requirements * 0.8
                context.runway_months = estimated_funding / net_burn
        
        context.last_updated = datetime.now(timezone.utc).isoformat()
        
        # Trigger metric-based orchestration
        await self._trigger_orchestration_rules("metric_threshold", {
            "context": context,
            "context_id": context_id,
            "updated_metrics": metrics
        })
        
        return True
    
    async def _trigger_orchestration_rules(self, trigger: str, context_data: Dict[str, Any]):
        """Trigger orchestration rules based on events"""
        
        for rule in self.orchestration_rules:
            if rule["trigger"] == trigger:
                if await self._evaluate_rule_conditions(rule.get("conditions", []), context_data):
                    await self._execute_rule_actions(rule["actions"], context_data)
    
    async def _evaluate_rule_conditions(self, conditions: List[Dict[str, Any]], 
                                       context_data: Dict[str, Any]) -> bool:
        """Evaluate orchestration rule conditions"""
        
        context = context_data.get("context")
        if not context:
            return False
        
        for condition in conditions:
            field = condition["field"]
            operator = condition["operator"]
            value = condition["value"]
            
            # Get field value from context
            if "." in field:
                # Handle nested fields like "key_metrics.conversion_rate"
                parts = field.split(".")
                field_value = getattr(context, parts[0], {})
                for part in parts[1:]:
                    field_value = field_value.get(part, 0) if isinstance(field_value, dict) else 0
            else:
                field_value = getattr(context, field, None)
                if hasattr(field_value, 'value'):  # Handle enums
                    field_value = field_value.value
            
            # Evaluate condition
            if operator == "equals" and field_value != value:
                return False
            elif operator == "less_than" and field_value >= value:
                return False
            elif operator == "greater_than" and field_value <= value:
                return False
        
        return True
    
    async def _execute_rule_actions(self, actions: List[Dict[str, Any]], 
                                   context_data: Dict[str, Any]):
        """Execute orchestration rule actions"""
        
        context = context_data["context"]
        context_id = context_data["context_id"]
        
        for action_config in actions:
            action = OrchestrationAction(
                action_id=f"action_{uuid.uuid4().hex[:8]}",
                action_type=action_config["type"],
                priority=OrchestrationPriority(action_config.get("priority", "medium")),
                description=f"Auto-generated: {action_config['type']}",
                parameters={
                    "context_id": context_id,
                    **{k: v for k, v in action_config.items() if k not in ["type", "priority"]}
                }
            )
            
            self.pending_actions[action.action_id] = action
            
            # Execute action immediately if high priority
            if action.priority in [OrchestrationPriority.HIGH, OrchestrationPriority.URGENT, OrchestrationPriority.CRITICAL]:
                await self._execute_orchestration_action(action)
    
    async def _execute_orchestration_action(self, action: OrchestrationAction):
        """Execute individual orchestration action"""
        
        action.status = "executing"
        
        try:
            context_id = action.parameters.get("context_id")
            context = self.business_contexts.get(context_id)
            
            if not context:
                raise ValueError(f"Context {context_id} not found")
            
            if action.action_type == "create_project":
                await self._execute_create_project_action(action, context)
            
            elif action.action_type == "create_tasks":
                await self._execute_create_tasks_action(action, context)
            
            elif action.action_type == "connect_essential_tools":
                await self._execute_connect_tools_action(action, context)
            
            elif action.action_type == "connect_dev_tools":
                await self._execute_connect_tools_action(action, context)
            
            elif action.action_type == "connect_marketing_tools":
                await self._execute_connect_tools_action(action, context)
            
            elif action.action_type == "ai_workflow":
                await self._execute_ai_workflow_action(action, context)
            
            elif action.action_type == "ai_analysis":
                await self._execute_ai_analysis_action(action, context)
            
            elif action.action_type == "notification":
                await self._execute_notification_action(action, context)
            
            else:
                logger.warning(f"Unknown action type: {action.action_type}")
            
            action.status = "completed"
            self.completed_actions[action.action_id] = action
            self.orchestration_metrics["actions_executed"] += 1
            
        except Exception as e:
            action.status = "failed"
            logger.error(f"Action execution failed: {action.action_id} - {e}")
        
        finally:
            if action.action_id in self.pending_actions:
                del self.pending_actions[action.action_id]
    
    async def _execute_create_project_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute create project action"""
        
        template = action.parameters.get("template", "business_launch")
        
        # Create project from blueprint
        project = await project_task_manager.create_project_from_blueprint(
            context.company_blueprint,
            template
        )
        
        # Update context
        context.active_projects.append(project.project_id)
        self.orchestration_metrics["projects_managed"] += 1
        
        logger.info(f"Created project {project.project_id} from template {template}")
    
    async def _execute_create_tasks_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute create tasks action"""
        
        template = action.parameters.get("template")
        
        if not context.active_projects:
            logger.warning("No active projects to add tasks to")
            return
        
        # Create tasks in the first active project
        project_id = context.active_projects[0]
        
        if template == "feature_development":
            variables = {
                "feature_name": "Core Product Features",
                "requirements": "Build MVP with essential features"
            }
        elif template == "product_launch":
            variables = {
                "product_name": context.company_blueprint.name
            }
        elif template == "fundraising_round":
            variables = {
                "round_type": "Seed",
                "target_amount": f"${context.company_blueprint.funding_requirements:,}"
            }
        else:
            variables = {"name": context.company_blueprint.name}
        
        task = await project_task_manager.create_task_from_template(
            project_id, template, variables
        )
        
        logger.info(f"Created task {task.task_id} from template {template}")
    
    async def _execute_connect_tools_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute connect tools action"""
        
        tools = action.parameters.get("tools", [])
        
        for tool_name in tools:
            if tool_name not in context.connected_tools:
                # In a real implementation, this would prompt for credentials
                # For now, we'll just mark as connected
                context.connected_tools.append(tool_name)
                self.orchestration_metrics["tools_connected"] += 1
                
                logger.info(f"Connected tool: {tool_name}")
    
    async def _execute_ai_workflow_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute AI workflow action"""
        
        workflow = action.parameters.get("workflow")
        
        if workflow == "business_analysis_workflow":
            inputs = {
                "business_idea": context.company_blueprint.name,
                "industry": context.company_blueprint.industry,
                "budget": context.company_blueprint.funding_requirements
            }
        elif workflow == "content_creation_pipeline":
            inputs = {
                "topic": f"{context.company_blueprint.name} launch",
                "target_audience": context.company_blueprint.target_market.primary_segment
            }
        else:
            inputs = {"business_context": context.company_blueprint.name}
        
        try:
            result = await ai_orchestrator.execute_workflow(workflow, inputs)
            
            # Generate insight from workflow result
            insight = OrchestrationInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                category="strategic",
                title=f"AI Analysis: {workflow}",
                description=f"Completed {workflow} with actionable insights",
                confidence_score=0.8,
                potential_impact="high",
                recommended_actions=[f"Review {workflow} results and implement recommendations"]
            )
            
            self.insights[insight.insight_id] = insight
            self.orchestration_metrics["insights_generated"] += 1
            
            logger.info(f"Executed AI workflow: {workflow}")
            
        except Exception as e:
            logger.error(f"AI workflow execution failed: {workflow} - {e}")
    
    async def _execute_ai_analysis_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute AI analysis action"""
        
        focus = action.parameters.get("focus", "general")
        
        # Create AI request for analysis
        prompt = f"""
        Analyze the current business situation for {context.company_blueprint.name}:
        
        Business Details:
        - Industry: {context.company_blueprint.industry}
        - Phase: {context.current_phase.value}
        - Key Metrics: {context.key_metrics}
        - Runway: {context.runway_months} months
        - Team Size: {context.team_size}
        
        Focus Area: {focus}
        
        Provide specific, actionable insights and recommendations.
        """
        
        request = AIRequest(
            request_id=f"req_{uuid.uuid4().hex[:8]}",
            capability=AICapability.ANALYSIS,
            prompt=prompt,
            quality_preference="quality"
        )
        
        try:
            response = await ai_orchestrator.execute_ai_request(request)
            
            # Create insight from analysis
            insight = OrchestrationInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                category="optimization",
                title=f"AI Analysis: {focus.replace('_', ' ').title()}",
                description=response.result.get("content", "Analysis completed"),
                confidence_score=0.85,
                potential_impact="medium",
                recommended_actions=["Review analysis and implement suggested optimizations"]
            )
            
            self.insights[insight.insight_id] = insight
            self.orchestration_metrics["insights_generated"] += 1
            
            logger.info(f"Completed AI analysis: {focus}")
            
        except Exception as e:
            logger.error(f"AI analysis failed: {focus} - {e}")
    
    async def _execute_notification_action(self, action: OrchestrationAction, context: BusinessContext):
        """Execute notification action"""
        
        message = action.parameters.get("message", "Orchestration notification")
        
        # In a real implementation, this would send notifications via Slack, email, etc.
        logger.info(f"NOTIFICATION: {message}")
        
        # Could also create a task for follow-up
        if context.active_projects:
            notification_task = await project_task_manager.create_task_from_template(
                context.active_projects[0],
                "feature_development",  # Use as generic template
                {
                    "feature_name": "Address Critical Alert",
                    "requirements": message
                }
            )
            logger.info(f"Created follow-up task: {notification_task.task_id}")
    
    async def run_daily_orchestration(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Run daily orchestration checks and optimizations"""
        
        target_context_id = context_id or self.current_context_id
        
        if not target_context_id or target_context_id not in self.business_contexts:
            return {"error": "No valid business context"}
        
        context = self.business_contexts[target_context_id]
        
        # Trigger daily checks
        await self._trigger_orchestration_rules("daily_check", {
            "context": context,
            "context_id": target_context_id
        })
        
        # Generate daily insights
        daily_insights = await self._generate_daily_insights(context)
        
        # Execute pending high-priority actions
        high_priority_actions = [
            action for action in self.pending_actions.values()
            if action.priority in [OrchestrationPriority.HIGH, OrchestrationPriority.URGENT, OrchestrationPriority.CRITICAL]
        ]
        
        for action in high_priority_actions:
            await self._execute_orchestration_action(action)
        
        return {
            "context_id": target_context_id,
            "daily_insights": len(daily_insights),
            "actions_executed": len(high_priority_actions),
            "pending_actions": len(self.pending_actions),
            "orchestration_health": "healthy" if len(self.pending_actions) < 10 else "needs_attention"
        }
    
    async def _generate_daily_insights(self, context: BusinessContext) -> List[OrchestrationInsight]:
        """Generate daily business insights"""
        
        insights = []
        
        # Runway insight
        if context.runway_months < 12:
            insights.append(OrchestrationInsight(
                insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                category="risk",
                title="Runway Management",
                description=f"Current runway: {context.runway_months:.1f} months. Consider fundraising or cost optimization.",
                confidence_score=0.9,
                potential_impact="high" if context.runway_months < 6 else "medium",
                recommended_actions=["Prepare fundraising materials", "Review and optimize expenses"]
            ))
        
        # Growth insight
        if context.key_metrics.get("monthly_revenue", 0) > 0:
            growth_rate = context.key_metrics.get("growth_rate", 0)
            if growth_rate < 0.1:  # Less than 10% monthly growth
                insights.append(OrchestrationInsight(
                    insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                    category="opportunity",
                    title="Growth Acceleration",
                    description="Monthly growth rate is below optimal. Focus on customer acquisition and retention.",
                    confidence_score=0.8,
                    potential_impact="high",
                    recommended_actions=["Analyze customer acquisition channels", "Implement retention strategies"]
                ))
        
        # Store insights
        for insight in insights:
            self.insights[insight.insight_id] = insight
        
        return insights
    
    def get_orchestration_dashboard(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive orchestration dashboard"""
        
        target_context_id = context_id or self.current_context_id
        
        if not target_context_id or target_context_id not in self.business_contexts:
            return {"error": "No valid business context"}
        
        context = self.business_contexts[target_context_id]
        
        # Recent insights
        recent_insights = sorted(
            self.insights.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:5]
        
        # Pending actions by priority
        actions_by_priority = {}
        for action in self.pending_actions.values():
            priority = action.priority.value
            actions_by_priority[priority] = actions_by_priority.get(priority, 0) + 1
        
        return {
            "business_context": {
                "company_name": context.company_blueprint.name,
                "current_phase": context.current_phase.value,
                "runway_months": context.runway_months,
                "team_size": context.team_size,
                "active_projects": len(context.active_projects),
                "connected_tools": len(context.connected_tools)
            },
            "key_metrics": context.key_metrics,
            "orchestration_status": {
                "pending_actions": len(self.pending_actions),
                "actions_by_priority": actions_by_priority,
                "recent_insights": len(recent_insights),
                "automation_health": "healthy" if len(self.pending_actions) < 10 else "needs_attention"
            },
            "recent_insights": [asdict(insight) for insight in recent_insights],
            "performance_metrics": self.orchestration_metrics,
            "recommendations": self._generate_dashboard_recommendations(context)
        }
    
    def _generate_dashboard_recommendations(self, context: BusinessContext) -> List[str]:
        """Generate dashboard recommendations"""
        
        recommendations = []
        
        # Phase-specific recommendations
        if context.current_phase == BusinessPhase.IDEATION:
            recommendations.append("🎯 Focus on market validation and customer discovery")
            recommendations.append("📊 Set up basic analytics and tracking")
        
        elif context.current_phase == BusinessPhase.MVP_DEVELOPMENT:
            recommendations.append("⚡ Prioritize core features for MVP")
            recommendations.append("🧪 Plan user testing and feedback collection")
        
        elif context.current_phase == BusinessPhase.LAUNCH:
            recommendations.append("🚀 Execute go-to-market strategy")
            recommendations.append("📈 Monitor key launch metrics closely")
        
        # Tool recommendations
        if len(context.connected_tools) < 5:
            recommendations.append("🔧 Connect more essential business tools")
        
        # Runway recommendations
        if context.runway_months < 6:
            recommendations.append("💰 Urgent: Prepare for fundraising")
        elif context.runway_months < 12:
            recommendations.append("📋 Start preparing fundraising materials")
        
        return recommendations

# Global founder orchestration system
founder_orchestrator = FounderOrchestrationSystem()