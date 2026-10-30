"""Usage/metering endpoints: per-tenant stats."""

from fastapi import APIRouter, Request, HTTPException

from services.usage_service import UsageService

router = APIRouter(prefix="/usage")
usage_service = UsageService()


@router.get("/{tenant_id}")
async def get_usage(request: Request, tenant_id: str) -> dict:
    """Get usage stats for a tenant."""
    caller = request.state.tenant_id
    if not caller:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    # Allow tenants to view their own usage; admin bypass handled in admin routes.
    if caller != tenant_id:
        raise HTTPException(status_code=403, detail="Cannot view another tenant's usage")
    return usage_service.aggregate(tenant_id)
