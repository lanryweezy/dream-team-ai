"""
Enhanced Base Agent with concrete implementations
Fixes abstract method issues from test failures
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class ConcreteBaseAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing"""
    
    def __init__(self, agent_id: str, capabilities: List[AgentCapability]):
        super().__init__(agent_id, capabilities)
        self.daily_goals = []
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute a task - concrete implementation"""
        try:
            task_type = task.get("type", "unknown")
            
            if task_type == "test":
                return TaskResult(
                    success=True,
                    output={"message": "Test task completed successfully"},
                    cost_incurred=0.0,
                    evidence=["test_execution.log"],
                    next_steps=["Continue testing"]
                )
            elif task_type == "health_check":
                return TaskResult(
                    success=True,
                    output={"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()},
                    cost_incurred=0.0,
                    evidence=["health_check.json"],
                    next_steps=["Monitor system"]
                )
            else:
                return TaskResult(
                    success=True,
                    output={"message": f"Executed {task_type} task"},
                    cost_incurred=1.0,
                    evidence=[f"{task_type}_result.json"],
                    next_steps=["Review results"]
                )
                
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily goals - concrete implementation"""
        return [
            {
                "id": f"goal_{self.agent_id}_1",
                "description": f"Complete primary tasks for {self.agent_id}",
                "priority": "high",
                "estimated_duration": "2 hours",
                "status": "pending"
            },
            {
                "id": f"goal_{self.agent_id}_2", 
                "description": f"Monitor system health for {self.agent_id}",
                "priority": "medium",
                "estimated_duration": "30 minutes",
                "status": "pending"
            },
            {
                "id": f"goal_{self.agent_id}_3",
                "description": f"Report status to coordinator",
                "priority": "low",
                "estimated_duration": "15 minutes", 
                "status": "pending"
            }
        ]