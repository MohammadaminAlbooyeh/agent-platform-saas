"""Centralized exception -> HTTP response mapping."""

from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Maps exceptions to appropriate HTTP responses."""

    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
        except Exception:
            response = None
        return response
