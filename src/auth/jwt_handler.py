"""Admin dashboard authentication (separate from tenant API keys)."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError

from config.settings import settings


def create_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token for an admin user."""
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=24))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])


def validate_token(token: str) -> bool:
    """Return True if the token is valid and not expired."""
    try:
        decode_token(token)
        return True
    except JWTError:
        return False
