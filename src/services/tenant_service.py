"""Tenant creation, API key issuance/rotation service."""

import uuid

from auth.api_key import generate, hash_key
from database.base import SessionLocal
from database.models.tenant import Tenant


class TenantService:
    """Service for managing tenants and API keys."""

    def create_tenant(self, name: str, plan: str = "free") -> dict:
        """Create a new tenant and issue an API key."""
        db = SessionLocal()
        try:
            tenant_id = str(uuid.uuid4())
            api_key = generate()
            tenant = Tenant(
                id=tenant_id,
                name=name,
                plan=plan,
                api_key_hash=hash_key(api_key),
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            return {
                "id": tenant.id,
                "name": tenant.name,
                "plan": tenant.plan,
                "api_key": api_key,
                "created_at": tenant.created_at.isoformat() if tenant.created_at else None,
            }
        finally:
            db.close()

    def get_tenant(self, tenant_id: str):
        """Fetch a tenant by ID (returns the ORM object or None)."""
        db = SessionLocal()
        try:
            return db.query(Tenant).filter(Tenant.id == tenant_id).first()
        finally:
            db.close()

    def rotate_api_key(self, tenant_id: str) -> str:
        """Issue a new API key for a tenant, invalidating the old one."""
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return ""
            api_key = generate()
            tenant.api_key_hash = hash_key(api_key)
            db.commit()
            return api_key
        finally:
            db.close()
