"""Core agent orchestration logic (tenant-scoped) service."""

from agents.orchestrator import Orchestrator
from billing.plans import COST_PER_1K_TOKENS
from services.notification_service import NotificationService
from services.quota_service import QuotaService
from services.token_estimator import estimate_tokens
from services.usage_service import UsageService

# Warn the tenant once cumulative usage crosses this fraction of their plan's quota.
QUOTA_WARNING_RATIO = 0.8


class AgentService:
    """Core agent orchestration, scoped by tenant."""

    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.quota = QuotaService()
        self.usage = UsageService()
        self.notifications = NotificationService()

    async def execute(self, agent_type: str, payload: dict, tenant_id: str) -> dict:
        """Execute an agent task after a quota check, then record real usage."""
        estimated_tokens = estimate_tokens(payload)
        if not self.quota.check_quota(tenant_id, estimated_tokens):
            await self.notifications.send_quota_warning(tenant_id, "Quota exceeded")
            return {"error": "Quota exceeded", "tenant_id": tenant_id}

        status = self.quota.get_quota_status(tenant_id)
        if status and status["limit"] > 0 and status["ratio"] >= QUOTA_WARNING_RATIO:
            await self.notifications.send_quota_warning(
                tenant_id, f"{status['ratio'] * 100:.0f}% of token quota used this cycle"
            )

        result = await self.orchestrator.route(agent_type, payload, tenant_id)

        tokens_used = result.get("tokens_used", estimated_tokens)
        tool_calls = result.get("tool_calls", 0)
        cost = round(tokens_used / 1000 * COST_PER_1K_TOKENS, 6)
        self.usage.record_usage(tenant_id, tokens=tokens_used, cost=cost, tool_calls=tool_calls)

        return result
