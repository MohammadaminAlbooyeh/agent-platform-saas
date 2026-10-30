"""Stripe integration: subscriptions, invoice generation service."""

class BillingService:
    """Service for Stripe subscriptions and invoices."""

    async def create_subscription(self, tenant_id: str, plan_id: str) -> dict:
        return {"tenant_id": tenant_id, "plan_id": plan_id}

    async def generate_invoice(self, tenant_id: str) -> dict:
        return {"tenant_id": tenant_id, "amount": 0.0}
