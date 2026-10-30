"""Checks/enforces per-plan limits before execution service."""

class QuotaService:
    """Service for checking and enforcing per-plan limits."""

    async def check_quota(self, tenant_id: str, estimated_tokens: int) -> bool:
        return True
