"""
StateStore: simple async key-value store with TTL using Redis if available, else in-memory fallback.
Used for idempotency caching, rate limits, and lightweight task/status storage.
"""

import os
import json
import time
import asyncio
from typing import Any, Optional
from datetime import timedelta

try:
    import redis.asyncio as redis  # type: ignore
except Exception:
    redis = None

from .mock_redis import MockRedis


class StateStore:
    def __init__(self):
        self._redis_url = os.getenv("REDIS_URL")
        self._client = None
        self._lock = asyncio.Lock()
        # In-memory fallback structures
        self._mem = {}
        self._mem_expiry = {}

    async def _ensure_client(self):
        if self._client is not None:
            return
        async with self._lock:
            if self._client is not None:
                return
            if self._redis_url and redis is not None:
                try:
                    self._client = redis.from_url(self._redis_url)
                    await self._client.ping()
                    return
                except Exception:
                    # fall back to mock
                    pass
            # fallback to mock/in-memory
            self._client = MockRedis()

    async def get(self, key: str) -> Optional[str]:
        await self._ensure_client()
        try:
            val = await self._client.get(key)
            if val is None:
                return None
            return val.decode() if isinstance(val, (bytes, bytearray)) else (val if isinstance(val, str) else val)
        except Exception:
            # in-memory fallback path
            now = time.time()
            exp = self._mem_expiry.get(key)
            if exp is not None and exp < now:
                self._mem.pop(key, None)
                self._mem_expiry.pop(key, None)
                return None
            return self._mem.get(key)

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        await self._ensure_client()
        data = value if isinstance(value, (str, bytes, bytearray)) else json.dumps(value)
        try:
            if ttl_seconds:
                await self._client.setex(key, ttl_seconds, data)
            else:
                await self._client.set(key, data)
            return True
        except Exception:
            # in-memory fallback
            self._mem[key] = data if isinstance(data, str) else data.decode()
            if ttl_seconds:
                self._mem_expiry[key] = time.time() + ttl_seconds
            elif key in self._mem_expiry:
                self._mem_expiry.pop(key, None)
            return True

    async def delete(self, key: str) -> None:
        await self._ensure_client()
        try:
            await self._client.delete(key)
        except Exception:
            self._mem.pop(key, None)
            self._mem_expiry.pop(key, None)

    async def incr(self, key: str, ttl_seconds: Optional[int] = None) -> int:
        await self._ensure_client()
        try:
            # emulate INCR with get/set
            raw = await self._client.get(key)
            val = int(raw.decode() if isinstance(raw, (bytes, bytearray)) else (raw or 0)) if raw else 0
            val += 1
            if ttl_seconds:
                await self._client.setex(key, ttl_seconds, str(val))
            else:
                await self._client.set(key, str(val))
            return val
        except Exception:
            # in-memory
            now = time.time()
            exp = self._mem_expiry.get(key)
            if exp is not None and exp < now:
                self._mem[key] = "0"
                self._mem_expiry.pop(key, None)
            val = int(self._mem.get(key, "0")) + 1
            self._mem[key] = str(val)
            if ttl_seconds:
                self._mem_expiry[key] = time.time() + ttl_seconds
            return val


# Provide a module-level instance for convenience
state_store = StateStore()