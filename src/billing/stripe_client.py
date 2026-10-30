"""Wrapper around Stripe SDK."""

import stripe


class StripeClient:
    """Thin wrapper around the Stripe SDK."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = api_key

    async def create_customer(self, email: str) -> str:
        """Create a Stripe customer and return the customer id."""
        if not self.api_key:
            return f"test_customer_{email}"
        customer = stripe.Customer.create(email=email)
        return customer.id

    async def create_checkout_session(self, price_id: str, customer_id: str) -> str:
        """Create a Stripe checkout session and return its URL."""
        if not self.api_key:
            return f"https://checkout.stripe.com/test/{price_id}"
        session = stripe.checkout.Session.create(
            customer=customer_id,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url="http://localhost:8000/billing/success",
            cancel_url="http://localhost:8000/billing/cancel",
        )
        return session.url
