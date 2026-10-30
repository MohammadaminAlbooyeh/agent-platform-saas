"""Emails/webhooks for quota warnings, invoice events service."""

class NotificationService:
    """Service for sending quota warnings and invoice notifications."""

    async def send_quota_warning(self, tenant_id: str) -> None:
        pass

    async def send_invoice_event(self, tenant_id: str, invoice_id: str) -> None:
        pass
