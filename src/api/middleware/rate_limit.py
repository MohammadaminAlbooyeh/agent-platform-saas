"""Per-tenant rate limiting middleware (Redis token bucket), limits scaled by plan."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from billing.plans import ANONYMOUS_REQUESTS_PER_MINUTE, PLANS

try:
    import redis

    _redis = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=True)
except Exception:  # pragma: no cover - Redis optional in local dev
    _redis = None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enforces per-tenant rate limits using a Redis token bucket.

    The limit is the tenant's plan `requests_per_minute` (set in
    billing.plans.PLANS); requests with no resolved tenant use a low
    anonymous default.
    """

    def __init__(self, app, per: int = 60) -> None:
        super().__init__(app)
        self.per = per

    def _rate_for(self, request: Request) -> int:
        tenant = getattr(request.state, "tenant", None)
        if tenant is None:
            return ANONYMOUS_REQUESTS_PER_MINUTE
        plan = PLANS.get(tenant.plan, PLANS["free"])
        return plan.get("requests_per_minute", ANONYMOUS_REQUESTS_PER_MINUTE)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        tenant_id = getattr(request.state, "tenant_id", None) or "anonymous"
        rate = self._rate_for(request)
        key = f"ratelimit:{tenant_id}"

        now = time.time()
        window_start = now - self.per

        if _redis is not None:
            try:
                pipe = _redis.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {str(now): now})
                pipe.expire(key, self.per + 1)
                results = pipe.execute()
                count = results[1]
                if count >= rate:
                    return Response(
                        content='{"detail":"Rate limit exceeded"}',
                        status_code=HTTP_429_TOO_MANY_REQUESTS,
                        media_type="application/json",
                    )
            except Exception:
                pass  # Fail open if Redis is unavailable

        response = await call_next(request)
        return response
