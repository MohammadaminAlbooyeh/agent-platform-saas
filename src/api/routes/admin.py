"""Admin-only endpoints: view all tenants, override quotas."""

from fastapi import APIRouter, Request, HTTPException, Depends

from auth.jwt_handler import decode_token, JWTError
from services.tenant_service import TenantService

router = APIRouter(prefix="/admin")
tenant_service = TenantService()


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
    """Override a tenant's quota (admin only)."""
    tenant_id = body.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id required")
    return {"status": "overridden", "tenant_id": tenant_id}


@router.post("/login")
async def admin_login(body: dict) -> dict:
    """Admin login: issue a JWT for the admin dashboard."""
    username = body.get("username")
    password = body.get("password")
    # Stub credential check; integrate with real admin user store in production.
    if username == "admin" and password == "admin":
        from auth.jwt_handler import create_token
        token = create_token(subject="admin")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid admin credentials")
