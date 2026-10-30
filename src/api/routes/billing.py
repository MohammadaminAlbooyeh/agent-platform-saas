"""Billing routes: plan selection, invoices, Stripe webhook receiver."""

from fastapi import APIRouter, Request, HTTPException

from services.billing_service import BillingService
from billing.invoice_generator import InvoiceGenerator
from services.usage_service import UsageService

router = APIRouter(prefix="/billing")
billing_service = BillingService()
invoice_generator = InvoiceGenerator()
usage_service = UsageService()


@router.post("/subscribe")
async def subscribe(request: Request, body: dict) -> dict:
    """Select a plan and create a subscription."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    plan_id = body.get("plan_id", "free")
    return await billing_service.create_subscription(tenant_id, plan_id)


@router.post("/webhook")
async def stripe_webhook() -> dict:
    """Receive Stripe webhook events."""
    return {"status": "received"}


@router.post("/invoice")
async def generate_invoice(request: Request, body: dict) -> dict:
    """Generate an invoice from aggregated usage."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    usage = usage_service.aggregate(tenant_id)
    invoice = invoice_generator.generate(tenant_id, usage)
    created = await billing_service.generate_invoice(tenant_id, invoice["total"])
    return {"invoice": created, "usage": invoice}
