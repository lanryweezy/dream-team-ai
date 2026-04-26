"""
Message Bus System for Agent Communication
Handles event-driven communication between all agents
"""

import json
import traceback
import asyncio
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import redis.asyncio as redis
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class MessageType(Enum):
    TASK_ASSIGNMENT = "task_assignment"
    TASK_COMPLETION = "task_completion"
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_RESPONSE = "approval_response"
    STATUS_UPDATE = "status_update"
    ERROR_REPORT = "error_report"
    RESOURCE_REQUEST = "resource_request"
    COORDINATION = "coordination"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Message:
    id: str
    type: MessageType
    sender: str
    recipient: str
    payload: Dict[str, Any]
    priority: Priority = Priority.MEDIUM
    timestamp: str = None
    correlation_id: Optional[str] = None
    requires_response: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

class MessageBus:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.running = False
        
    async def start(self):
        """Start the message bus"""
        await self.connect()
        self.running = True
        
    async def stop(self):
        """Stop the message bus"""
        await self.disconnect()
        self.running = False
        
    async def connect(self):
        """Initialize Redis connection"""
        self.redis_client = redis.from_url(self.redis_url)
        await self.redis_client.ping()
        logger.info("Connected to message bus")
        
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            
    async def publish(self, message: Message) -> bool:
        """Publish message to the bus"""
        try:
            channel = f"agent:{message.recipient}"
            # Convert message to dict with enum values as strings
            message_dict = asdict(message)
            message_dict['type'] = message.type.value
            message_dict['priority'] = message.priority.value
            message_data = json.dumps(message_dict)
            
            # Store in message log for audit
            message_log_data = message_dict.copy()
            await self.redis_client.lpush(
                "message_log", 
                json.dumps({
                    "message": message_log_data,
                    "published_at": datetime.utcnow().isoformat()
                })
            )
            
            # Publish to channel
            await self.redis_client.publish(channel, message_data)
            
            # Store for recipient if they're offline
            await self.redis_client.lpush(f"queue:{message.recipient}", message_data)
            
            logger.info(f"Published message {message.id} to {message.recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False
            
    async def subscribe(self, agent_id: str, handler: Callable[[Message], None]):
        """Subscribe agent to receive messages"""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(handler)
        
        # Start listening for this agent
        asyncio.create_task(self._listen_for_agent(agent_id))
        
    async def _listen_for_agent(self, agent_id: str):
        """Listen for messages for a specific agent"""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"agent:{agent_id}")
        
        try:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        msg_data = json.loads(message['data'])
                        msg = Message(**msg_data)
                        
                        # Call all handlers for this agent
                        for handler in self.subscribers.get(agent_id, []):
                            try:
                                await handler(msg)
                            except Exception as e:
                                logger.error(f"Handler error for {agent_id}: {e}")
                                error_details = traceback.format_exc()
                                # Push to DLQ
                                dlq_payload = {
                                    "message": msg_data,
                                    "error": str(e),
                                    "traceback": error_details,
                                    "failed_at": datetime.utcnow().isoformat(),
                                    "agent_id": agent_id
                                }
                                await self.redis_client.lpush("dlq:messages", json.dumps(dlq_payload))
                                
                    except Exception as e:
                        logger.error(f"Failed to process message for {agent_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Subscription error for {agent_id}: {e}")
        finally:
            await pubsub.unsubscribe(f"agent:{agent_id}")
            

    async def get_dlq_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get messages from the Dead Letter Queue"""
        if not self.redis_client:
            return []

        messages = await self.redis_client.lrange("dlq:messages", 0, limit - 1)
        return [json.loads(m) for m in messages]

    async def clear_dlq(self):
        """Clear the Dead Letter Queue"""
        if self.redis_client:
            await self.redis_client.delete("dlq:messages")

    async def get_pending_messages(self, agent_id: str) -> List[Message]:
        """Get pending messages for an agent"""
        messages = []
        queue_key = f"queue:{agent_id}"
        
        while True:
            msg_data = await self.redis_client.rpop(queue_key)
            if not msg_data:
                break
                
            try:
                msg = Message(**json.loads(msg_data))
                messages.append(msg)
            except Exception as e:
                logger.error(f"Failed to parse pending message: {e}")
                
        return messages
        
    async def send_task_assignment(self, sender: str, recipient: str, task: Dict[str, Any], 
                                 correlation_id: str = None) -> str:
        """Helper to send task assignment"""
        message = Message(
            id=f"task_{datetime.utcnow().timestamp()}",
            type=MessageType.TASK_ASSIGNMENT,
            sender=sender,
            recipient=recipient,
            payload={"task": task},
            priority=Priority.HIGH,
            correlation_id=correlation_id,
            requires_response=True
        )
        
        await self.publish(message)
        return message.id
        
    async def send_approval_request(self, sender: str, action: Dict[str, Any], 
                                  estimated_cost: float = 0) -> str:
        """Helper to send approval request to founder"""
        message = Message(
            id=f"approval_{datetime.utcnow().timestamp()}",
            type=MessageType.APPROVAL_REQUEST,
            sender=sender,
            recipient="founder",
            payload={
                "action": action,
                "estimated_cost": estimated_cost,
                "requires_approval": True
            },
            priority=Priority.HIGH,
            requires_response=True
        )
        
        await self.publish(message)
        return message.id
        
    async def send_status_update(self, sender: str, status: Dict[str, Any]):
        """Helper to send status update to CEO"""
        message = Message(
            id=f"status_{datetime.utcnow().timestamp()}",
            type=MessageType.STATUS_UPDATE,
            sender=sender,
            recipient="ceo_agent",
            payload={"status": status},
            priority=Priority.MEDIUM
        )
        
        await self.publish(message)

# Global message bus instance
message_bus = MessageBus()