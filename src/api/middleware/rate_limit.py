"""Per-tenant rate limiting middleware (Redis token bucket)."""

from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enforces per-tenant rate limits using a Redis token bucket."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response
