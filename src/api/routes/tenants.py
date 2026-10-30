"""Tenant account and API key routes."""

from fastapi import APIRouter, HTTPException

from api.schemas.tenant import TenantCreate, TenantRead
from services.tenant_service import TenantService

router = APIRouter(prefix="/tenants")
tenant_service = TenantService()


@router.post("", status_code=201)
async def create_tenant(payload: TenantCreate) -> dict:
    """Create a new tenant account and issue an API key."""
    return tenant_service.create_tenant(name=payload.name, plan=payload.plan)


@router.get("/{tenant_id}", response_model=TenantRead)
async def get_tenant(tenant_id: str) -> dict:
    """Get a tenant by ID."""
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {
        "id": tenant.id,
        "name": tenant.name,
        "plan": tenant.plan,
        "created_at": tenant.created_at.isoformat() if tenant.created_at else None,
    }
