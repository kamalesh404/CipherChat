"""Tests for the rate limiter middleware."""

import time
import pytest
from src.api.rate_limiter import RateLimiter, RateLimitMiddleware


class TestRateLimiter:
    def test_allows_within_limit(self):
        limiter = RateLimiter(max_tokens=5, refill_rate=1.0)
        for _ in range(5):
            assert limiter.allow("client1") is True

    def test_blocks_over_limit(self):
        limiter = RateLimiter(max_tokens=3, refill_rate=0.1)
        for _ in range(3):
            limiter.allow("client1")
        assert limiter.allow("client1") is False

    def test_refill_over_time(self):
        limiter = RateLimiter(max_tokens=2, refill_rate=100.0)
        limiter.allow("client1")
        limiter.allow("client1")
        assert limiter.allow("client1") is False
        time.sleep(0.05)
        assert limiter.allow("client1") is True

    def test_separate_buckets(self):
        limiter = RateLimiter(max_tokens=1, refill_rate=0.1)
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is False
        assert limiter.allow("client2") is True

    def test_reset(self):
        limiter = RateLimiter(max_tokens=1, refill_rate=0.1)
        limiter.allow("client1")
        assert limiter.allow("client1") is False
        limiter.reset("client1")
        assert limiter.allow("client1") is True


class TestRateLimitMiddleware:
    @pytest.mark.asyncio
    async def test_allows_within_limit(self):
        middleware = RateLimitMiddleware(max_tokens=5, refill_rate=1.0)
        called = []

        async def handler(client_id, message):
            called.append(message)
            return "ok"

        result = await middleware("client1", "hello", handler)
        assert result == "ok"
        assert called == ["hello"]

    @pytest.mark.asyncio
    async def test_blocks_over_limit(self):
        middleware = RateLimitMiddleware(max_tokens=2, refill_rate=0.1)
        results = []

        async def handler(client_id, message):
            return "ok"

        for _ in range(2):
            await middleware("client1", "msg", handler)
        result = await middleware("client1", "blocked", handler)
        assert result is None

    def test_disconnect_cleans_up(self):
        middleware = RateLimitMiddleware(max_tokens=1, refill_rate=0.1)
        middleware.limiter.allow("client1")
        middleware.disconnect("client1")
        assert middleware.limiter.allow("client1") is True
