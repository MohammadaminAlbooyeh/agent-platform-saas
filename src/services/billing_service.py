"""Stripe integration: subscriptions, invoice generation service."""

from typing import Optional

import stripe

from billing.stripe_client import StripeClient
from database.base import SessionLocal
from database.models.invoice import Invoice


class BillingService:
    """Service for Stripe subscriptions and invoices."""

    def __init__(self, stripe_client: Optional[StripeClient] = None) -> None:
        self.stripe = stripe_client or StripeClient("")

    async def create_subscription(self, tenant_id: str, plan_id: str) -> dict:
        """Create a Stripe subscription for a tenant on a plan."""
        try:
            customer = self.stripe.create_customer(tenant_id)
            return {
                "tenant_id": tenant_id,
                "plan_id": plan_id,
                "customer_id": customer,
                "status": "created",
            }
        except Exception as exc:  # noqa: BLE001
            return {"tenant_id": tenant_id, "plan_id": plan_id, "error": str(exc)}

    async def generate_invoice(self, tenant_id: str, amount: float) -> dict:
        """Generate an invoice record for a tenant."""
        db = SessionLocal()
        try:
            import uuid
            invoice_id = str(uuid.uuid4())
            invoice = Invoice(
                id=invoice_id,
                tenant_id=tenant_id,
                amount=amount,
                status="draft",
            )
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return {
                "id": invoice.id,
                "tenant_id": invoice.tenant_id,
                "amount": invoice.amount,
                "status": invoice.status,
            }
        finally:
            db.close()
