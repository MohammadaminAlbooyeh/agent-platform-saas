"""Builds invoice line items from usage records."""

class InvoiceGenerator:
    """Builds invoice line items from usage records."""

    def generate(self, tenant_id: str, usage: dict) -> dict:
        return {"tenant_id": tenant_id, "line_items": [], "total": 0.0}
