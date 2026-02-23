"""
Enhanced Message Bus with Reliability and Acknowledgment
Addresses critical issues from improvement plan
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, List, Optional, Callable, Set
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from enum import Enum
import redis.asyncio as redis

from .mock_redis import MockRedis

logger = logging.getLogger(__name__)

class MessageStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"

class MessagePriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ReliableMessage:
    id: str
    type: str
    sender: str
    recipient: str
    data: Dict[str, Any]
    timestamp: str
    requires_response: bool = False
    priority: MessagePriority = MessagePriority.MEDIUM
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300
    status: MessageStatus = MessageStatus.PENDING
    processing_started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert enums to their values
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReliableMessage':
        """Create message from dictionary"""
        # Convert enum values back to enums
        if 'priority' in data:
            data['priority'] = MessagePriority(data['priority'])
        if 'status' in data:
            data['status'] = MessageStatus(data['status'])
        return cls(**data)

class EnhancedMessageBus:
    """Enhanced message bus with reliability, acknowledgment, and error handling"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", use_mock: bool = False):
        self.redis_url = redis_url
        self.use_mock = use_mock
        self.redis_client: Optional[redis.Redis] = None
        self.running = False
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.processing_messages: Dict[str, ReliableMessage] = {}
        self.dead_letter_queue: List[ReliableMessage] = []
        self.listener_tasks: List[asyncio.Task] = []
        self.cleanup_task: Optional[asyncio.Task] = None
        
        # Configuration
        self.max_message_log_size = 10000
        self.cleanup_interval = 300  # 5 minutes
        self.message_retention_hours = 24
        
    async def start(self):
        """Start the enhanced message bus"""
        try:
            if self.use_mock:
                self.redis_client = MockRedis()
            else:
                self.redis_client = redis.from_url(self.redis_url)
                # Test connection
                await self.redis_client.ping()
                
            self.running = True
            
            # Start cleanup task
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            
            logger.info("Enhanced message bus started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start enhanced message bus: {e}")
            # Fallback to mock
            self.redis_client = MockRedis()
            self.running = True
            logger.info("Started with mock Redis fallback")
            
    async def stop(self):
        """Stop the message bus gracefully"""
        self.running = False
        
        # Cancel all listener tasks
        for task in self.listener_tasks:
            task.cancel()
            
        # Cancel cleanup task
        if self.cleanup_task:
            self.cleanup_task.cancel()
            
        # Wait for tasks to complete
        if self.listener_tasks:
            await asyncio.gather(*self.listener_tasks, return_exceptions=True)
            
        # Close Redis connection
        if self.redis_client and not self.use_mock:
            await self.redis_client.close()
            
        logger.info("Enhanced message bus stopped")
        
    async def publish_reliable_message(
        self, 
        message_type: str, 
        data: Dict[str, Any], 
        sender: str,
        recipient: str = "all",
        requires_response: bool = False,
        priority: MessagePriority = MessagePriority.MEDIUM,
        timeout_seconds: int = 300
    ) -> str:
        """Publish a reliable message with acknowledgment tracking"""
        
        message = ReliableMessage(
            id=str(uuid.uuid4()),
            type=message_type,
            sender=sender,
            recipient=recipient,
            data=data,
            timestamp=datetime.now(timezone.utc).isoformat(),
            requires_response=requires_response,
            priority=priority,
            timeout_seconds=timeout_seconds
        )
        
        try:
            # Store message in Redis with expiration
            message_key = f"message:{message.id}"
            await self.redis_client.setex(
                message_key,
                timeout_seconds,
                json.dumps(message.to_dict())
            )
            
            # Add to appropriate queue based on priority
            queue_name = f"queue:{recipient}:priority_{priority.value}"
            await self.redis_client.lpush(queue_name, message.id)
            
            # Add to message log
            await self._add_to_message_log(message)
            
            # Track if response required
            if requires_response:
                response_key = f"response_pending:{message.id}"
                await self.redis_client.setex(response_key, timeout_seconds, "1")
                
            logger.info(f"Published reliable message {message.id} to {recipient}")
            return message.id
            
        except Exception as e:
            logger.error(f"Failed to publish reliable message: {e}")
            raise
            
    async def subscribe_reliable(
        self, 
        agent_id: str, 
        handler: Callable[[ReliableMessage], None]
    ):
        """Subscribe to reliable messages with acknowledgment"""
        self.message_handlers[agent_id] = handler
        
        # Start listener task for this agent
        task = asyncio.create_task(self._reliable_listener(agent_id))
        self.listener_tasks.append(task)
        
        logger.info(f"Agent {agent_id} subscribed to reliable messages")
        
    async def _reliable_listener(self, agent_id: str):
        """Listen for reliable messages for a specific agent"""
        while self.running:
            try:
                # Check queues in priority order
                for priority in [4, 3, 2, 1]:  # CRITICAL to LOW
                    queue_name = f"queue:{agent_id}:priority_{priority}"
                    
                    # Non-blocking pop
                    message_id = await self.redis_client.rpop(queue_name)
                    if message_id:
                        await self._process_reliable_message(message_id.decode(), agent_id)
                        break
                        
                # Also check 'all' queues
                for priority in [4, 3, 2, 1]:
                    queue_name = f"queue:all:priority_{priority}"
                    message_id = await self.redis_client.rpop(queue_name)
                    if message_id:
                        await self._process_reliable_message(message_id.decode(), agent_id)
                        break
                        
                # Brief sleep to prevent busy waiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in reliable listener for {agent_id}: {e}")
                await asyncio.sleep(1)
                
    async def _process_reliable_message(self, message_id: str, agent_id: str):
        """Process a reliable message with error handling and retries"""
        try:
            # Get message from Redis
            message_key = f"message:{message_id}"
            message_data = await self.redis_client.get(message_key)
            
            if not message_data:
                logger.warning(f"Message {message_id} not found or expired")
                return
                
            message = ReliableMessage.from_dict(json.loads(message_data))
            message.status = MessageStatus.PROCESSING
            message.processing_started_at = datetime.now(timezone.utc).isoformat()
            
            # Update message status
            await self.redis_client.setex(
                message_key,
                message.timeout_seconds,
                json.dumps(message.to_dict())
            )
            
            # Track processing
            self.processing_messages[message_id] = message
            
            try:
                # Call handler
                handler = self.message_handlers.get(agent_id)
                if handler:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(message)
                    else:
                        handler(message)
                        
                    # Mark as completed
                    await self._mark_message_completed(message_id)
                    
                else:
                    logger.warning(f"No handler found for agent {agent_id}")
                    await self._mark_message_failed(message_id, "No handler found")
                    
            except Exception as e:
                logger.error(f"Handler error for message {message_id}: {e}")
                await self._handle_message_failure(message_id, str(e))
                
        except Exception as e:
            logger.error(f"Failed to process reliable message {message_id}: {e}")
            
    async def _mark_message_completed(self, message_id: str):
        """Mark message as successfully completed"""
        try:
            message_key = f"message:{message_id}"
            message_data = await self.redis_client.get(message_key)
            
            if message_data:
                message = ReliableMessage.from_dict(json.loads(message_data))
                message.status = MessageStatus.COMPLETED
                message.completed_at = datetime.now(timezone.utc).isoformat()
                
                # Update in Redis
                await self.redis_client.setex(
                    message_key,
                    3600,  # Keep completed messages for 1 hour
                    json.dumps(message.to_dict())
                )
                
            # Remove from processing
            self.processing_messages.pop(message_id, None)
            
            logger.debug(f"Message {message_id} marked as completed")
            
        except Exception as e:
            logger.error(f"Failed to mark message {message_id} as completed: {e}")
            
    async def _mark_message_failed(self, message_id: str, error_message: str):
        """Mark message as failed"""
        try:
            message_key = f"message:{message_id}"
            message_data = await self.redis_client.get(message_key)
            
            if message_data:
                message = ReliableMessage.from_dict(json.loads(message_data))
                message.status = MessageStatus.FAILED
                message.error_message = error_message
                message.completed_at = datetime.now(timezone.utc).isoformat()
                
                # Update in Redis
                await self.redis_client.setex(
                    message_key,
                    3600,  # Keep failed messages for 1 hour
                    json.dumps(message.to_dict())
                )
                
            # Remove from processing
            self.processing_messages.pop(message_id, None)
            
            logger.warning(f"Message {message_id} marked as failed: {error_message}")
            
        except Exception as e:
            logger.error(f"Failed to mark message {message_id} as failed: {e}")
            
    async def _handle_message_failure(self, message_id: str, error_message: str):
        """Handle message processing failure with retry logic"""
        try:
            message_key = f"message:{message_id}"
            message_data = await self.redis_client.get(message_key)
            
            if not message_data:
                return
                
            message = ReliableMessage.from_dict(json.loads(message_data))
            message.retry_count += 1
            message.error_message = error_message
            
            if message.retry_count <= message.max_retries:
                # Retry the message
                message.status = MessageStatus.PENDING
                
                # Update message
                await self.redis_client.setex(
                    message_key,
                    message.timeout_seconds,
                    json.dumps(message.to_dict())
                )
                
                # Re-queue with exponential backoff
                delay = min(2 ** message.retry_count, 60)  # Max 60 seconds
                await asyncio.sleep(delay)
                
                queue_name = f"queue:{message.recipient}:priority_{message.priority.value}"
                await self.redis_client.lpush(queue_name, message_id)
                
                logger.info(f"Retrying message {message_id} (attempt {message.retry_count})")
                
            else:
                # Move to dead letter queue
                message.status = MessageStatus.DEAD_LETTER
                await self.redis_client.setex(
                    message_key,
                    86400,  # Keep dead letters for 24 hours
                    json.dumps(message.to_dict())
                )
                
                self.dead_letter_queue.append(message)
                logger.error(f"Message {message_id} moved to dead letter queue after {message.retry_count} retries")
                
            # Remove from processing
            self.processing_messages.pop(message_id, None)
            
        except Exception as e:
            logger.error(f"Failed to handle message failure for {message_id}: {e}")
            
    async def _add_to_message_log(self, message: ReliableMessage):
        """Add message to persistent log with size management"""
        try:
            log_key = "message_log"
            
            # Add message to log
            await self.redis_client.lpush(log_key, json.dumps(message.to_dict()))
            
            # Trim log to max size
            await self.redis_client.ltrim(log_key, 0, self.max_message_log_size - 1)
            
        except Exception as e:
            logger.error(f"Failed to add message to log: {e}")
            
    async def _cleanup_loop(self):
        """Periodic cleanup of expired messages and logs"""
        while self.running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired_messages()
                await self._cleanup_old_logs()
                
            except Exception as e:
                logger.error(f"Cleanup loop error: {e}")
                
    async def _cleanup_expired_messages(self):
        """Clean up expired and old messages"""
        try:
            # Clean up processing messages that have timed out
            current_time = datetime.now(timezone.utc)
            expired_messages = []
            
            for message_id, message in self.processing_messages.items():
                if message.processing_started_at:
                    start_time = datetime.fromisoformat(message.processing_started_at)
                    if (current_time - start_time).total_seconds() > message.timeout_seconds:
                        expired_messages.append(message_id)
                        
            for message_id in expired_messages:
                await self._handle_message_failure(message_id, "Processing timeout")
                
            if expired_messages:
                logger.info(f"Cleaned up {len(expired_messages)} expired messages")
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired messages: {e}")
            
    async def _cleanup_old_logs(self):
        """Clean up old log entries"""
        try:
            # This is handled by Redis TTL, but we can add additional cleanup here
            pass
            
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")
            
    async def get_message_status(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific message"""
        try:
            message_key = f"message:{message_id}"
            message_data = await self.redis_client.get(message_key)
            
            if message_data:
                return json.loads(message_data)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get message status for {message_id}: {e}")
            return None
            
    async def get_queue_stats(self) -> Dict[str, Any]:
        """Get statistics about message queues"""
        try:
            stats = {
                "processing_messages": len(self.processing_messages),
                "dead_letter_queue": len(self.dead_letter_queue),
                "active_subscribers": len(self.message_handlers),
                "queue_lengths": {}
            }
            
            # Get queue lengths
            for agent_id in self.message_handlers.keys():
                for priority in [1, 2, 3, 4]:
                    queue_name = f"queue:{agent_id}:priority_{priority}"
                    length = await self.redis_client.llen(queue_name)
                    if length > 0:
                        stats["queue_lengths"][queue_name] = length
                        
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get queue stats: {e}")
            return {}

# Global enhanced message bus instance
enhanced_message_bus = EnhancedMessageBus(use_mock=True)  # Default to mock for testing