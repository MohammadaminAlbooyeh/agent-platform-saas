"""Emails/webhooks for quota warnings, invoice events service."""

from typing import Optional


class NotificationService:
    """Service for sending quota warnings and invoice notifications."""

    async def send_quota_warning(self, tenant_id: str, message: Optional[str] = None) -> None:
        """Send a quota warning to a tenant (stub: integrate with email/webhook provider)."""
        print(f"[notification] quota warning for tenant {tenant_id}: {message or 'approaching limit'}")

    async def send_invoice_event(self, tenant_id: str, invoice_id: str, event: str = "created") -> None:
        """Send an invoice event notification (stub)."""
        print(f"[notification] invoice {event} for tenant {tenant_id}: invoice {invoice_id}")
