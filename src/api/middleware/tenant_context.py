"""Tenant context middleware: resolves tenant from API key, injects into request state."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from auth.api_key import hash_key
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
                # hash_key is deterministic (sha256 of the key, not per-tenant
                # salted), so the hash can be looked up directly on the
                # indexed column instead of scanning every tenant and
                # verifying each one in turn.
                tenant = (
                    request.state.db.query(Tenant)
                    .filter(Tenant.api_key_hash == hash_key(api_key))
                    .first()
                )
                if tenant is not None:
                    request.state.tenant = tenant
                    request.state.tenant_id = tenant.id

            response = await call_next(request)
            return response
        finally:
            request.state.db.close()
