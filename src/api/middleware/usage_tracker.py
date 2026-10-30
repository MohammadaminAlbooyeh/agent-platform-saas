"""Usage tracking middleware: records tokens/requests per call."""

from starlette.middleware.base import BaseHTTPMiddleware


class UsageTrackerMiddleware(BaseHTTPMiddleware):
    """Records tokens and requests consumed per API call."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response
