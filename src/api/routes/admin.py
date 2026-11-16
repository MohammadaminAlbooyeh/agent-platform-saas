"""Admin-only endpoints: view all tenants, override quotas."""

from fastapi import APIRouter, Request, HTTPException, Depends

from auth.admin_auth import authenticate_admin
from auth.jwt_handler import decode_token, JWTError
from services.quota_service import QuotaService
from services.tenant_service import TenantService

router = APIRouter(prefix="/admin")
tenant_service = TenantService()
quota_service = QuotaService()


def require_admin(request: Request) -> str:
    """Validate admin JWT from the Authorization header."""
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing admin token")
    token = auth.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        return payload.get("sub", "admin")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")


@router.get("/tenants")
async def list_tenants(request: Request, admin: str = Depends(require_admin)) -> dict:
    """List all tenants (admin only)."""
    from database.base import SessionLocal
    from database.models.tenant import Tenant
    db = SessionLocal()
    try:
        tenants = db.query(Tenant).all()
        return {
            "tenants": [
                {"id": t.id, "name": t.name, "plan": t.plan} for t in tenants
            ]
        }
    finally:
        db.close()


@router.post("/quota-override")
async def override_quota(request: Request, body: dict, admin: str = Depends(require_admin)) -> dict:
    """Persist an admin-set token quota override for a tenant."""
    tenant_id = body.get("tenant_id")
    token_limit = body.get("token_limit")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id required")
    if not isinstance(token_limit, int) or token_limit < 0:
        raise HTTPException(status_code=400, detail="token_limit must be a non-negative integer")
    if not tenant_service.get_tenant(tenant_id):
        raise HTTPException(status_code=404, detail="Tenant not found")
    override = quota_service.set_override(tenant_id, token_limit)
    return {"status": "overridden", **override}


@router.post("/login")
async def admin_login(body: dict) -> dict:
    """Admin login: issue a JWT for the admin dashboard."""
    username = body.get("username")
    password = body.get("password")
    if username and password and authenticate_admin(username, password):
        from auth.jwt_handler import create_token
        token = create_token(subject=username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid admin credentials")
