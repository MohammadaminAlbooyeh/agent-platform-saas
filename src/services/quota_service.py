"""Checks/enforces per-plan limits before execution service."""

from billing.plans import PLANS
from database.base import SessionLocal
from database.models.tenant import Tenant
from services.usage_service import UsageService

# Token quotas reset on a rolling 30-day cycle.
BILLING_CYCLE_HOURS = 24 * 30


class QuotaService:
    """Service for checking and enforcing cumulative, per-plan token limits."""

    def __init__(self) -> None:
        self.usage = UsageService()

    def get_plan_limits(self, plan: str) -> dict:
        """Return the limits for a plan."""
        return PLANS.get(plan, PLANS["free"])

    def get_token_limit(self, tenant_id: str, plan: str) -> int:
        """Return the effective token limit for a tenant (plan default)."""
        return self.get_plan_limits(plan).get("tokens", 0)

    def get_quota_status(self, tenant_id: str) -> dict:
        """Return {limit, used, remaining, ratio} for the tenant's current billing cycle.

        Returns {} if the tenant does not exist.
        """
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        finally:
            db.close()
        if not tenant:
            return {}

        limit = self.get_token_limit(tenant_id, tenant.plan)
        used = self.usage.aggregate(tenant_id, hours=BILLING_CYCLE_HOURS)["tokens"]
        if limit <= 0:
            return {"limit": limit, "used": used, "remaining": float("inf"), "ratio": 0.0}
        remaining = max(limit - used, 0)
        return {"limit": limit, "used": used, "remaining": remaining, "ratio": used / limit}

    def check_quota(self, tenant_id: str, estimated_tokens: int = 0) -> bool:
        """Return True if the tenant has remaining quota, against cumulative usage this cycle."""
        status = self.get_quota_status(tenant_id)
        if not status:
            return False
        if status["limit"] <= 0:
            return True  # unlimited
        return estimated_tokens <= status["remaining"]
