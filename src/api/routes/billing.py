"""Billing routes: plan selection, invoices, Stripe webhook receiver."""

import json
import logging

import stripe
from fastapi import APIRouter, Request, HTTPException

from config.settings import settings
from services.billing_service import BillingService
from billing.invoice_generator import InvoiceGenerator
from services.notification_service import NotificationService
from services.usage_service import UsageService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing")
billing_service = BillingService()
invoice_generator = InvoiceGenerator()
usage_service = UsageService()
notification_service = NotificationService()

# Event types where we notify the tenant tied to the Stripe customer.
NOTIFIABLE_EVENTS = {"invoice.payment_succeeded", "invoice.payment_failed", "customer.subscription.deleted"}


@router.post("/subscribe")
async def subscribe(request: Request, body: dict) -> dict:
    """Select a plan and create a subscription."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    plan_id = body.get("plan_id", "free")
    return await billing_service.create_subscription(tenant_id, plan_id)


@router.post("/webhook")
async def stripe_webhook(request: Request) -> dict:
    """Verify and handle a Stripe webhook event."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if settings.stripe_webhook_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
        except (ValueError, stripe.error.SignatureVerificationError) as exc:
            raise HTTPException(status_code=400, detail=f"Invalid webhook signature: {exc}")
    else:
        logger.warning("STRIPE_WEBHOOK_SECRET not set; accepting webhook payload unverified")
        try:
            event = json.loads(payload)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")

    event_type = event.get("type", "unknown")
    data_object = event.get("data", {}).get("object", {})

    if event_type in NOTIFIABLE_EVENTS:
        tenant_ref = data_object.get("customer_email") or data_object.get("customer")
        if tenant_ref:
            await notification_service.send_invoice_event(tenant_ref, data_object.get("id", "unknown"), event_type)

    return {"status": "received", "type": event_type}


@router.post("/invoice")
async def generate_invoice(request: Request, body: dict) -> dict:
    """Generate an invoice from aggregated usage."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    usage = usage_service.aggregate(tenant_id)
    invoice = invoice_generator.generate(tenant_id, usage)
    created = await billing_service.generate_invoice(tenant_id, invoice["total"])
    if "error" not in created:
        await notification_service.send_invoice_event(tenant_id, created["id"], "created")
    return {"invoice": created, "usage": invoice}
