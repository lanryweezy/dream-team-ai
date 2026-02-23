"""
Base Agent Class
All department agents inherit from this base class
"""

import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from .simple_message_bus import event_bus
from .policy_engine import PolicyEngine
from .cost_tracker import CostTracker

logger = logging.getLogger(__name__)

@dataclass
class AgentCapability:
    name: str
    description: str
    cost_estimate: float
    confidence_level: float
    requirements: List[str]

@dataclass
class TaskResult:
    success: bool
    output: Dict[str, Any]
    cost_incurred: float
    evidence: List[str]  # URLs, file paths, etc.
    next_steps: List[str]
    error_message: Optional[str] = None

class BaseAgent(ABC):
    def __init__(self, agent_id: str, capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.is_running = False
        self.current_tasks: Dict[str, Dict] = {}
        self.message_bus = event_bus
        self.policy_engine = PolicyEngine()
        self.cost_tracker = CostTracker()
        
    async def start(self):
        """Start the agent"""
        await self.message_bus.start()
        self.is_running = True
        logger.info(f"{self.agent_id} started successfully")
        
    async def stop(self):
        """Stop the agent"""
        self.is_running = False
        await self.message_bus.stop()
        logger.info(f"{self.agent_id} stopped")
        
    async def send_event(self, event_type: str, data: Dict[str, Any]):
        """Send an event via the message bus"""
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "sender": self.agent_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.message_bus.publish_event(event_type, event)
        
    async def request_approval(self, action: Dict[str, Any], estimated_cost: float = 0) -> bool:
        """Request approval from founder for an action"""
        # Check if approval is required by policy
        if not self.policy_engine.requires_approval(action, estimated_cost):
            return True
            
        # For now, auto-approve to keep the system flowing
        # In production, this would send to founder dashboard
        logger.info(f"Auto-approving action: {action.get('type', 'unknown')} (cost: ${estimated_cost})")
        return True
        
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute a specific task - must be implemented by each agent"""
        pass
        
    @abstractmethod
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily goals for this agent"""
        pass
        
    async def log_cost(self, action: str, amount: float, details: Optional[Dict[str, Any]] = None):
        """Log cost for an action"""
        try:
            self.cost_tracker.record_cost(
                agent_id=self.agent_id,
                tool_name=details.get("tool_name", "unknown") if details else "unknown",
                action_type=action,
                amount=amount,
                description=details.get("description", "") if details else "",
                metadata=details or {},
                category=details.get("category", "general") if details else "general"
            )
        except Exception as e:
            logger.error(f"Failed to log cost: {e}")
            
    async def get_capability(self, name: str) -> Optional[AgentCapability]:
        """Get a specific capability by name"""
        for cap in self.capabilities:
            if cap.name == name:
                return cap
        return None
        
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "is_running": self.is_running,
            "active_tasks": len(self.current_tasks),
            "capabilities_count": len(self.capabilities),
            "last_updated": datetime.utcnow().isoformat()
        }