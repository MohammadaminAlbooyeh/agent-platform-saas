"""Aggregates usage records into billable units service."""

class UsageService:
    """Service for aggregating usage into billable units."""

    async def aggregate(self, tenant_id: str) -> dict:
        return {"tenant_id": tenant_id, "tokens": 0, "cost": 0.0}
