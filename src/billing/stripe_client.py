"""Wrapper around Stripe SDK."""

import stripe


class StripeClient:
    """Thin wrapper around the Stripe SDK."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = api_key

    async def create_customer(self, email: str) -> str:
        return ""
