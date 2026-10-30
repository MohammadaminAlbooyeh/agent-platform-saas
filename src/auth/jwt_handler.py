"""Admin dashboard authentication (separate from tenant API keys)."""

from jose import jwt


class JWTHandler:
    """Handles JWT creation and validation for admin auth."""

    @staticmethod
    def create_token(subject: str, secret: str) -> str:
        return jwt.encode({"sub": subject}, secret, algorithm="HS256")

    @staticmethod
    def decode_token(token: str, secret: str) -> dict:
        return jwt.decode(token, secret, algorithms=["HS256"])
