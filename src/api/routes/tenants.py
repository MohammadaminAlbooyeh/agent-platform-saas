"""Tenant account and API key routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/tenants")


@router.post("")
async def create_tenant() -> dict:
    """Create a new tenant account."""
    return {"tenant_id": None}


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: str) -> dict:
    """Get a tenant by ID."""
    return {"tenant_id": tenant_id}
