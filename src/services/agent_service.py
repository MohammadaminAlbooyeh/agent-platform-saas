"""Core agent orchestration logic (tenant-scoped) service."""

from agents.orchestrator import Orchestrator


class AgentService:
    """Core agent orchestration, scoped by tenant."""

    def __init__(self) -> None:
        self.orchestrator = Orchestrator()

    async def execute(self, agent_type: str, payload: dict, tenant_id: str) -> dict:
        return await self.orchestrator.route(agent_type, payload, tenant_id)
