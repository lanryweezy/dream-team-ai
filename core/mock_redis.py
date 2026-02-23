"""
Mock Redis implementation for testing
Provides Redis-like interface without requiring actual Redis server
"""

import asyncio
import json
import time
from typing import Dict, Any, List, Optional, Union
from collections import defaultdict, deque

class MockRedis:
    """Mock Redis client for testing"""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.lists: Dict[str, deque] = defaultdict(deque)
        self.expiry: Dict[str, float] = {}
        self.pubsub_channels: Dict[str, List] = defaultdict(list)
        
    async def ping(self) -> bool:
        """Mock ping - always returns True"""
        return True
        
    async def get(self, key: str) -> Optional[bytes]:
        """Get value by key"""
        self._cleanup_expired()
        
        if key in self.data and key not in self.expiry:
            value = self.data[key]
            return value.encode() if isinstance(value, str) else value
        elif key in self.data and key in self.expiry:
            if time.time() < self.expiry[key]:
                value = self.data[key]
                return value.encode() if isinstance(value, str) else value
            else:
                # Key expired
                del self.data[key]
                del self.expiry[key]
                return None
        return None
        
    async def set(self, key: str, value: Union[str, bytes]) -> bool:
        """Set key-value pair"""
        self.data[key] = value.decode() if isinstance(value, bytes) else value
        # Remove expiry if setting new value
        if key in self.expiry:
            del self.expiry[key]
        return True
        
    async def setex(self, key: str, seconds: int, value: Union[str, bytes]) -> bool:
        """Set key-value pair with expiration"""
        await self.set(key, value)
        self.expiry[key] = time.time() + seconds
        return True
        
    async def delete(self, *keys: str) -> int:
        """Delete keys"""
        deleted = 0
        for key in keys:
            if key in self.data:
                del self.data[key]
                deleted += 1
            if key in self.expiry:
                del self.expiry[key]
            if key in self.lists:
                del self.lists[key]
        return deleted
        
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        self._cleanup_expired()
        return key in self.data
        
    # List operations
    async def lpush(self, key: str, *values) -> int:
        """Left push to list"""
        for value in values:
            self.lists[key].appendleft(value)
        return len(self.lists[key])
        
    async def rpush(self, key: str, *values) -> int:
        """Right push to list"""
        for value in values:
            self.lists[key].append(value)
        return len(self.lists[key])
        
    async def lpop(self, key: str) -> Optional[bytes]:
        """Left pop from list"""
        if key in self.lists and self.lists[key]:
            value = self.lists[key].popleft()
            result = value.encode() if isinstance(value, str) else value
            return result
        return None
        
    async def rpop(self, key: str) -> Optional[bytes]:
        """Right pop from list"""
        if key in self.lists and self.lists[key]:
            value = self.lists[key].pop()
            result = value.encode() if isinstance(value, str) else value
            return result
        return None
        
    async def llen(self, key: str) -> int:
        """Get list length"""
        return len(self.lists.get(key, []))
        
    async def lrange(self, key: str, start: int, end: int) -> List[bytes]:
        """Get list range"""
        if key not in self.lists:
            return []
            
        items = list(self.lists[key])
        if end == -1:
            end = len(items)
        else:
            end = end + 1
            
        result = []
        for item in items[start:end]:
            if isinstance(item, str):
                result.append(item.encode())
            else:
                result.append(item)
        return result
        
    async def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim list to specified range"""
        if key in self.lists:
            items = list(self.lists[key])
            if end == -1:
                end = len(items) - 1
            self.lists[key] = deque(items[start:end + 1])
        return True
        
    # Pub/Sub operations
    async def publish(self, channel: str, message: Union[str, bytes]) -> int:
        """Publish message to channel"""
        if channel in self.pubsub_channels:
            for callback in self.pubsub_channels[channel]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message)
                    else:
                        callback(message)
                except Exception:
                    pass  # Ignore callback errors
            return len(self.pubsub_channels[channel])
        return 0
        
    def subscribe(self, channel: str, callback):
        """Subscribe to channel"""
        self.pubsub_channels[channel].append(callback)
        
    def unsubscribe(self, channel: str, callback=None):
        """Unsubscribe from channel"""
        if channel in self.pubsub_channels:
            if callback:
                try:
                    self.pubsub_channels[channel].remove(callback)
                except ValueError:
                    pass
            else:
                self.pubsub_channels[channel].clear()
                
    # Hash operations
    async def hget(self, key: str, field: str) -> Optional[bytes]:
        """Get hash field"""
        self._cleanup_expired()
        if key in self.data and isinstance(self.data[key], dict):
            value = self.data[key].get(field)
            return value.encode() if isinstance(value, str) else value
        return None
        
    async def hset(self, key: str, field: str, value: Union[str, bytes]) -> bool:
        """Set hash field"""
        if key not in self.data:
            self.data[key] = {}
        if not isinstance(self.data[key], dict):
            self.data[key] = {}
        self.data[key][field] = value.decode() if isinstance(value, bytes) else value
        return True
        
    async def hgetall(self, key: str) -> Dict[bytes, bytes]:
        """Get all hash fields"""
        self._cleanup_expired()
        if key in self.data and isinstance(self.data[key], dict):
            result = {}
            for k, v in self.data[key].items():
                key_bytes = k.encode() if isinstance(k, str) else k
                val_bytes = v.encode() if isinstance(v, str) else v
                result[key_bytes] = val_bytes
            return result
        return {}
        
    # Set operations
    async def sadd(self, key: str, *values) -> int:
        """Add to set"""
        if key not in self.data:
            self.data[key] = set()
        if not isinstance(self.data[key], set):
            self.data[key] = set()
            
        added = 0
        for value in values:
            if value not in self.data[key]:
                self.data[key].add(value)
                added += 1
        return added
        
    async def smembers(self, key: str) -> set:
        """Get set members"""
        self._cleanup_expired()
        if key in self.data and isinstance(self.data[key], set):
            return {v.encode() if isinstance(v, str) else v for v in self.data[key]}
        return set()
        
    async def srem(self, key: str, *values) -> int:
        """Remove from set"""
        if key in self.data and isinstance(self.data[key], set):
            removed = 0
            for value in values:
                if value in self.data[key]:
                    self.data[key].remove(value)
                    removed += 1
            return removed
        return 0
        
    # Utility methods
    def _cleanup_expired(self):
        """Clean up expired keys"""
        current_time = time.time()
        expired_keys = [
            key for key, expiry_time in self.expiry.items()
            if current_time >= expiry_time
        ]
        
        for key in expired_keys:
            if key in self.data:
                del self.data[key]
            del self.expiry[key]
            
    async def flushall(self) -> bool:
        """Clear all data"""
        self.data.clear()
        self.lists.clear()
        self.expiry.clear()
        self.pubsub_channels.clear()
        return True
        
    async def keys(self, pattern: str = "*") -> List[bytes]:
        """Get keys matching pattern"""
        self._cleanup_expired()
        # Simple pattern matching - just support * for now
        if pattern == "*":
            return [k.encode() if isinstance(k, str) else k for k in self.data.keys()]
        else:
            # Basic pattern matching
            import fnmatch
            matching_keys = []
            for key in self.data.keys():
                if fnmatch.fnmatch(key, pattern):
                    matching_keys.append(key.encode() if isinstance(key, str) else key)
            return matching_keys
            
    async def close(self):
        """Close connection (no-op for mock)"""
        pass
        
    def __repr__(self):
        return f"MockRedis(keys={len(self.data)}, lists={len(self.lists)})"