"""Usage/metering endpoints: per-tenant stats."""

from fastapi import APIRouter

router = APIRouter(prefix="/usage")


@router.get("/{tenant_id}")
async def get_usage(tenant_id: str) -> dict:
    """Get usage stats for a tenant."""
    return {"tenant_id": tenant_id, "stats": {}}
