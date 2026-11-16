"""Request timing middleware.

Usage (tokens/cost/tool-calls) is recorded where the real cost is known —
by `AgentService.execute` right after an agent run — rather than guessed
here for every request.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class UsageTrackerMiddleware(BaseHTTPMiddleware):
    """Measures and reports per-request processing time."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
        return response
