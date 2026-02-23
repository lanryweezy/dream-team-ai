"""
Simple Message Bus (No Redis Required)
In-memory event system for testing
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class SimpleEventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: List[Dict[str, Any]] = []
        self.running = False
        
    async def start(self):
        """Start the event bus"""
        self.running = True
        logger.info("Simple Event Bus started")
        
    async def stop(self):
        """Stop the event bus"""
        self.running = False
        logger.info("Simple Event Bus stopped")
        
    async def publish_event(self, event_type: str, data: Dict[str, Any], agent_id: str = "system"):
        """Publish an event"""
        if not self.running:
            return
            
        event = {
            "event_type": event_type,
            "data": data,
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "event_id": f"evt_{len(self.event_history)}"
        }
        
        self.event_history.append(event)
        
        # Notify subscribers
        for callback in self.subscribers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"Error in event callback: {e}")
                
        logger.debug(f"Published event: {event_type} from {agent_id}")
        
    async def subscribe_to_events(self, event_type: str, callback: Callable):
        """Subscribe to events"""
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}")
        
    def get_event_history(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get event history"""
        if event_type:
            return [e for e in self.event_history if e["event_type"] == event_type]
        return self.event_history.copy()
        
    def clear_history(self):
        """Clear event history"""
        self.event_history.clear()

# Global instance for easy access
event_bus = SimpleEventBus()