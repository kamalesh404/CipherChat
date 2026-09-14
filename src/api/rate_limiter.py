"""Rate limiter middleware for WebSocket connections."""

import asyncio
import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class RateLimiter:
    """Token bucket rate limiter for WebSocket messages."""

    max_tokens: int = 30
    refill_rate: float = 1.0  # tokens per second
    _buckets: dict = field(default_factory=lambda: defaultdict(lambda: {"tokens": 30.0, "last_refill": time.monotonic()}))

    def allow(self, client_id: str) -> bool:
        """Check if a message from client_id is allowed."""
        bucket = self._buckets[client_id]
        now = time.monotonic()
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(self.max_tokens, bucket["tokens"] + elapsed * self.refill_rate)
        bucket["last_refill"] = now

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True
        return False

    def reset(self, client_id: str) -> None:
        """Reset a client's bucket (e.g. on disconnect)."""
        self._buckets.pop(client_id, None)


class RateLimitMiddleware:
    """WebSocket middleware that enforces per-client rate limits."""

    def __init__(self, max_tokens: int = 30, refill_rate: float = 1.0):
        self.limiter = RateLimiter(max_tokens=max_tokens, refill_rate=refill_rate)

    async def __call__(self, client_id: str, message: str, next_handler):
        """Process a message if rate limit allows, otherwise drop it."""
        if self.limiter.allow(client_id):
            return await next_handler(client_id, message)
        return None

    def disconnect(self, client_id: str) -> None:
        """Clean up when a client disconnects."""
        self.limiter.reset(client_id)
