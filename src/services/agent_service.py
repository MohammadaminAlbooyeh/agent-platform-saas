"""Core agent orchestration logic (tenant-scoped) service."""

from agents.orchestrator import Orchestrator
from services.quota_service import QuotaService


class AgentService:
    """Core agent orchestration, scoped by tenant."""

    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.quota = QuotaService()

    async def execute(self, agent_type: str, payload: dict, tenant_id: str, estimated_tokens: int = 0) -> dict:
        """Execute an agent task after quota check."""
        if not self.quota.check_quota(tenant_id, estimated_tokens):
            return {"error": "Quota exceeded", "tenant_id": tenant_id}
        return await self.orchestrator.route(agent_type, payload, tenant_id)
