"""Billing routes: plan selection, invoices, Stripe webhook receiver."""

from fastapi import APIRouter

router = APIRouter(prefix="/billing")


@router.post("/subscribe")
async def subscribe() -> dict:
    """Select a plan and create a subscription."""
    return {"status": "subscribed"}


@router.post("/webhook")
async def stripe_webhook() -> dict:
    """Receive Stripe webhook events."""
    return {"status": "received"}
