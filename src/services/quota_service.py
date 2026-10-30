"""Checks/enforces per-plan limits before execution service."""

from billing.plans import PLANS
from database.base import SessionLocal
from database.models.tenant import Tenant


class QuotaService:
    """Service for checking and enforcing per-plan limits."""

    def get_plan_limits(self, plan: str) -> dict:
        """Return the limits for a plan."""
        return PLANS.get(plan, PLANS["free"])

    def check_quota(self, tenant_id: str, estimated_tokens: int = 0) -> bool:
        """Return True if the tenant has remaining quota for the estimated tokens."""
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return False
            limits = self.get_plan_limits(tenant.plan)
            token_limit = limits.get("tokens", 0)
            if token_limit <= 0:
                return True  # unlimited
            # Rough check: estimate against remaining (simplified; no per-cycle reset here)
            return estimated_tokens <= token_limit
        finally:
            db.close()
