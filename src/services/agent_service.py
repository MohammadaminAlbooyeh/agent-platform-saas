"""Core agent orchestration logic (tenant-scoped) service."""

from agents.orchestrator import Orchestrator
from billing.plans import COST_PER_1K_TOKENS
from services.quota_service import QuotaService
from services.token_estimator import estimate_tokens
from services.usage_service import UsageService


class AgentService:
    """Core agent orchestration, scoped by tenant."""

    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.quota = QuotaService()
        self.usage = UsageService()

    async def execute(self, agent_type: str, payload: dict, tenant_id: str) -> dict:
        """Execute an agent task after a quota check, then record real usage."""
        estimated_tokens = estimate_tokens(payload)
        if not self.quota.check_quota(tenant_id, estimated_tokens):
            return {"error": "Quota exceeded", "tenant_id": tenant_id}

        result = await self.orchestrator.route(agent_type, payload, tenant_id)

        tokens_used = result.get("tokens_used", estimated_tokens)
        tool_calls = result.get("tool_calls", 0)
        cost = round(tokens_used / 1000 * COST_PER_1K_TOKENS, 6)
        self.usage.record_usage(tenant_id, tokens=tokens_used, cost=cost, tool_calls=tool_calls)

        return result
