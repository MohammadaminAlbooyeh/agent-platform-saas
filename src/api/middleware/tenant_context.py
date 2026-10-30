"""Tenant context middleware: resolves tenant from API key, injects into request state."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.api_key import verify_key
from database.base import SessionLocal
from database.models.tenant import Tenant


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Resolves the tenant from the X-API-Key header and injects it into request.state."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Attach a DB session to request state for downstream use
        request.state.db = SessionLocal()
        request.state.tenant = None
        request.state.tenant_id = None

        try:
            api_key = request.headers.get("x-api-key")
            if api_key:
                tenant = (
                    request.state.db.query(Tenant)
                    .filter(Tenant.api_key_hash.is_not(None))
                    .all()
                )
                for t in tenant:
                    if verify_key(api_key, t.api_key_hash):
                        request.state.tenant = t
                        request.state.tenant_id = t.id
                        break

            response = await call_next(request)
            return response
        finally:
            request.state.db.close()
