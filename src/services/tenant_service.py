"""Tenant creation, API key issuance/rotation service."""

class TenantService:
    """Service for managing tenants and API keys."""

    async def create_tenant(self, name: str, plan: str = "free") -> dict:
        return {"id": None, "name": name, "plan": plan}

    async def rotate_api_key(self, tenant_id: str) -> str:
        return ""
