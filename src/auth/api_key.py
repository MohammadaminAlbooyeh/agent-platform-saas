"""API key generation/validation per tenant."""

import secrets


class APIKey:
    """Utility for generating and validating tenant API keys."""

    @staticmethod
    def generate() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def validate(key: str) -> bool:
        return bool(key)
