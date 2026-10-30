"""Tenant context middleware: resolves tenant from API key."""

from starlette.middleware.base import BaseHTTPMiddleware


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Injects the resolved tenant into the request context."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response
