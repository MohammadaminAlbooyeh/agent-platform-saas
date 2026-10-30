"""API key generation, hashing, and validation per tenant."""

import hashlib
import secrets

from config.settings import settings


def generate() -> str:
    """Generate a new random API key."""
    return f"sk_{secrets.token_urlsafe(32)}"


def hash_key(key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256((settings.jwt_secret + key).encode()).hexdigest()


def verify_key(key: str, hashed: str) -> bool:
    """Verify a plaintext API key against its hash."""
    return hash_key(key) == hashed
