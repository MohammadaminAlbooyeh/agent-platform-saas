"""Builds invoice line items from usage records."""

from billing.plans import COST_PER_1K_TOKENS
from services.usage_service import UsageService


class InvoiceGenerator:
    """Builds invoice line items from usage records."""

    COST_PER_1K_TOKENS = COST_PER_1K_TOKENS

    def generate(self, tenant_id: str, usage: dict) -> dict:
        """Build an invoice from aggregated usage."""
        tokens = usage.get("tokens", 0)
        cost = round(tokens / 1000 * self.COST_PER_1K_TOKENS, 6)
        line_items = [
            {
                "description": "API tokens",
                "quantity": tokens,
                "unit_price": self.COST_PER_1K_TOKENS / 1000,
                "amount": cost,
            }
        ]
        return {
            "tenant_id": tenant_id,
            "line_items": line_items,
            "total": cost,
            "tokens": tokens,
        }
