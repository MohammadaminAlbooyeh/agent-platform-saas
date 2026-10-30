"""Centralized exception -> HTTP response mapping."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Maps unhandled exceptions to a consistent JSON error response."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:  # noqa: BLE001
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error", "error": str(exc)},
            )
