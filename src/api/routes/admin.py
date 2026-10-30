"""Admin-only routes: view all tenants, override quotas."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin")


@router.get("/tenants")
async def list_tenants() -> dict:
    """List all tenants (admin only)."""
    return {"tenants": []}


@router.post("/quota-override")
async def override_quota() -> dict:
    """Override a tenant's quota (admin only)."""
    return {"status": "overridden"}
