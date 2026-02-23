"""
Business Orchestration API
RESTful API for the complete founder orchestration system
Provides endpoints for all business management capabilities
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import asdict

from core.founder_orchestration_system import founder_orchestrator, BusinessPhase, OrchestrationPriority
from core.project_task_manager import project_task_manager, TaskStatus, TaskPriority
from core.universal_tool_integration import universal_tools
from core.ai_orchestration_engine import ai_orchestrator, AICapability
from core.company_blueprint_dataclass import CompanyBlueprint

logger = logging.getLogger(__name__)

class BusinessOrchestrationAPI:
    """
    Complete Business Orchestration API
    - Business context management
    - Project and task orchestration
    - Tool integration management
    - AI workflow execution
    - Real-time business intelligence
    """
    
    def __init__(self):
        self.orchestrator = founder_orchestrator
        self.project_manager = project_task_manager
        self.tool_integration = universal_tools
        self.ai_engine = ai_orchestrator
    
    # Convenience shims used by quick-actions (minimal mocks, upgrade later)
    async def get_business_context(self, business_id: str) -> Dict[str, Any]:
        return {
            "business_id": business_id,
            "business_type": "startup",
            "industry": "Technology",
            "stage": "Early Stage",
            "team_size": 8,
            "current_goals": "Growth and Product Development"
        }

    async def get_comprehensive_metrics(self, business_id: str) -> Dict[str, Any]:
        return {
            "revenue": 125000,
            "growth_rate": 23.5,
            "active_users": 2847,
            "team_size": 8,
            "runway_months": 12
        }

    async def get_team_members(self, business_id: str) -> List[Dict[str, Any]]:
        return [
            {"name": "Alice", "role": "Developer", "current_tasks": ["Feature A"], "completion_rate": 88, "blockers": []},
            {"name": "Bob", "role": "Designer", "current_tasks": ["UI Polish"], "completion_rate": 86, "blockers": []},
            {"name": "Carol", "role": "PM", "current_tasks": ["Planning"], "completion_rate": 90, "blockers": []},
        ]

    async def get_comprehensive_analytics(self, business_id: str) -> Dict[str, Any]:
        return {
            "revenue": 125000,
            "growth_rate": 23.5,
            "customers": 1345,
            "team_productivity": 87.2,
            "market_position": "Growing"
        }
    
    async def create_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new business and initialize orchestration"""
        
        try:
            # Create company blueprint
            blueprint = CompanyBlueprint(
                name=business_data["name"],
                industry=business_data["industry"],
                business_model=business_data["business_model"],
                target_market=business_data["target_market"],
                key_features=business_data.get("key_features", []),
                funding_requirements=business_data.get("funding_requirements", 100000)
            )
            
            # Create business context
            context_id = await self.orchestrator.create_business_context(
                blueprint,
                BusinessPhase(business_data.get("initial_phase", "ideation"))
            )
            
            return {
                "success": True,
                "context_id": context_id,
                "message": f"Business '{business_data['name']}' created successfully",
                "next_steps": [
                    "Connect essential tools",
                    "Set up initial project",
                    "Define key metrics"
                ]
            }
            
        except Exception as e:
            logger.error(f"Business creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_business_dashboard(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive business dashboard"""
        
        try:
            dashboard = self.orchestrator.get_orchestration_dashboard(context_id)
            
            if "error" in dashboard:
                return {
                    "success": False,
                    "error": dashboard["error"]
                }
            
            return {
                "success": True,
                "dashboard": dashboard
            }
            
        except Exception as e:
            logger.error(f"Dashboard retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_business_phase(self, context_id: str, new_phase: str) -> Dict[str, Any]:
        """Update business phase"""
        
        try:
            phase = BusinessPhase(new_phase)
            success = await self.orchestrator.update_business_phase(context_id, phase)
            
            if success:
                return {
                    "success": True,
                    "message": f"Business phase updated to {new_phase}",
                    "automated_actions": "Phase-specific orchestration triggered"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update business phase"
                }
                
        except Exception as e:
            logger.error(f"Phase update failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_business_metrics(self, context_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Update business metrics"""
        
        try:
            success = await self.orchestrator.update_business_metrics(context_id, metrics)
            
            if success:
                return {
                    "success": True,
                    "message": "Business metrics updated successfully",
                    "metrics_updated": list(metrics.keys())
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update business metrics"
                }
                
        except Exception as e:
            logger.error(f"Metrics update failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Project Management
    
    async def get_projects(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Get all projects for business context"""
        
        try:
            if context_id and context_id in self.orchestrator.business_contexts:
                context = self.orchestrator.business_contexts[context_id]
                projects = []
                
                for project_id in context.active_projects:
                    if project_id in self.project_manager.projects:
                        project = self.project_manager.projects[project_id]
                        projects.append(asdict(project))
                
                return {
                    "success": True,
                    "projects": projects,
                    "total_projects": len(projects)
                }
            else:
                # Return all projects
                projects = [asdict(project) for project in self.project_manager.projects.values()]
                return {
                    "success": True,
                    "projects": projects,
                    "total_projects": len(projects)
                }
                
        except Exception as e:
            logger.error(f"Project retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_project_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get detailed project dashboard"""
        
        try:
            dashboard = self.project_manager.get_project_dashboard(project_id)
            
            if not dashboard:
                return {
                    "success": False,
                    "error": "Project not found"
                }
            
            return {
                "success": True,
                "dashboard": dashboard
            }
            
        except Exception as e:
            logger.error(f"Project dashboard failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_task(self, project_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new task"""
        
        try:
            if "template" in task_data:
                # Create from template
                task = await self.project_manager.create_task_from_template(
                    project_id,
                    task_data["template"],
                    task_data.get("variables", {})
                )
            else:
                # Create custom task (would need to implement this method)
                return {
                    "success": False,
                    "error": "Custom task creation not yet implemented"
                }
            
            return {
                "success": True,
                "task_id": task.task_id,
                "message": f"Task '{task.title}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Task creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_task_status(self, task_id: str, new_status: str, user: str = "api") -> Dict[str, Any]:
        """Update task status"""
        
        try:
            status = TaskStatus(new_status)
            success = await self.project_manager.update_task_status(task_id, status, user)
            
            if success:
                return {
                    "success": True,
                    "message": f"Task status updated to {new_status}"
                }
            else:
                return {
                    "success": False,
                    "error": "Task not found"
                }
                
        except Exception as e:
            logger.error(f"Task status update failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Tool Integration Management
    
    async def get_tool_integrations(self) -> Dict[str, Any]:
        """Get status of all tool integrations"""
        
        try:
            status = self.tool_integration.get_integration_status()
            return {
                "success": True,
                "integrations": status
            }
            
        except Exception as e:
            logger.error(f"Tool integration status failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def connect_tool(self, tool_name: str, credentials: Dict[str, str], 
                          credential_type: str = "api_key") -> Dict[str, Any]:
        """Connect to a business tool"""
        
        try:
            success = await self.tool_integration.connect_tool(tool_name, credentials, credential_type)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully connected to {tool_name}",
                    "tool_name": tool_name,
                    "status": "connected"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to connect to {tool_name}"
                }
                
        except Exception as e:
            logger.error(f"Tool connection failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_tool_operation(self, tool_name: str, operation: str, 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operation on connected tool"""
        
        try:
            result = await self.tool_integration.execute_operation(tool_name, operation, parameters)
            
            return {
                "success": result.status == "success",
                "operation_id": result.operation_id,
                "result": result.result,
                "error": result.error_message if result.status == "failed" else None
            }
            
        except Exception as e:
            logger.error(f"Tool operation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sync_all_tools(self) -> Dict[str, Any]:
        """Sync data across all connected tools"""
        
        try:
            result = await self.tool_integration.sync_all_tools()
            return {
                "success": True,
                "sync_results": result
            }
            
        except Exception as e:
            logger.error(f"Tool sync failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # AI Workflow Management
    
    async def get_ai_capabilities(self) -> Dict[str, Any]:
        """Get available AI capabilities and models"""
        
        try:
            capabilities = self.ai_engine.get_ai_capabilities_summary()
            return {
                "success": True,
                "capabilities": capabilities
            }
            
        except Exception as e:
            logger.error(f"AI capabilities retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_ai_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI workflow"""
        
        try:
            result = await self.ai_engine.execute_workflow(workflow_id, inputs)
            
            return {
                "success": True,
                "execution_id": result["execution_id"],
                "status": result["status"],
                "results": result.get("results", {})
            }
            
        except Exception as e:
            logger.error(f"AI workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_ai_request(self, capability: str, prompt: str, 
                                parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute single AI request"""
        
        try:
            from core.ai_orchestration_engine import AIRequest
            import uuid
            
            request = AIRequest(
                request_id=f"req_{uuid.uuid4().hex[:8]}",
                capability=AICapability(capability),
                prompt=prompt,
                parameters=parameters or {}
            )
            
            response = await self.ai_engine.execute_ai_request(request)
            
            return {
                "success": True,
                "request_id": response.request_id,
                "result": response.result,
                "model_used": response.model_used,
                "cost": response.cost,
                "processing_time": response.processing_time
            }
            
        except Exception as e:
            logger.error(f"AI request failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Orchestration Management
    
    async def run_daily_orchestration(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Run daily orchestration cycle"""
        
        try:
            result = await self.orchestrator.run_daily_orchestration(context_id)
            
            return {
                "success": True,
                "orchestration_results": result
            }
            
        except Exception as e:
            logger.error(f"Daily orchestration failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_business_insights(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Get AI-generated business insights"""
        
        try:
            target_context_id = context_id or self.orchestrator.current_context_id
            
            if not target_context_id:
                return {
                    "success": False,
                    "error": "No business context available"
                }
            
            # Get recent insights
            recent_insights = sorted(
                self.orchestrator.insights.values(),
                key=lambda x: x.created_at,
                reverse=True
            )[:10]
            
            return {
                "success": True,
                "insights": [asdict(insight) for insight in recent_insights],
                "total_insights": len(self.orchestrator.insights)
            }
            
        except Exception as e:
            logger.error(f"Insights retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_pending_actions(self, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Get pending orchestration actions"""
        
        try:
            pending_actions = list(self.orchestrator.pending_actions.values())
            
            # Filter by context if specified
            if context_id:
                pending_actions = [
                    action for action in pending_actions
                    if action.parameters.get("context_id") == context_id
                ]
            
            return {
                "success": True,
                "pending_actions": [asdict(action) for action in pending_actions],
                "total_pending": len(pending_actions)
            }
            
        except Exception as e:
            logger.error(f"Pending actions retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Health and Status
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        
        try:
            # Check various system components
            tool_status = self.tool_integration.get_integration_status()
            ai_capabilities = self.ai_engine.get_ai_capabilities_summary()
            orchestration_metrics = self.orchestrator.orchestration_metrics
            
            health_score = 1.0
            issues = []
            
            # Check tool integrations
            if tool_status["connected"] < 3:
                health_score -= 0.2
                issues.append("Few tools connected")
            
            # Check pending actions
            if len(self.orchestrator.pending_actions) > 20:
                health_score -= 0.3
                issues.append("High number of pending actions")
            
            # Check AI availability
            if ai_capabilities["total_models"] < 3:
                health_score -= 0.2
                issues.append("Limited AI models available")
            
            health_status = "healthy" if health_score > 0.8 else "degraded" if health_score > 0.5 else "unhealthy"
            
            return {
                "success": True,
                "health_status": health_status,
                "health_score": health_score,
                "issues": issues,
                "system_metrics": {
                    "connected_tools": tool_status["connected"],
                    "available_ai_models": ai_capabilities["total_models"],
                    "pending_actions": len(self.orchestrator.pending_actions),
                    "active_businesses": len(self.orchestrator.business_contexts),
                    "orchestration_metrics": orchestration_metrics
                }
            }
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "health_status": "unknown"
            }

# Global API instance
business_api = BusinessOrchestrationAPI()