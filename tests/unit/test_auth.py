"""Unit tests for auth: API key hashing and JWT handling."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from auth.api_key import generate, hash_key, verify_key  # noqa: E402
from auth.jwt_handler import create_token, decode_token, validate_token  # noqa: E402


def test_generate_returns_nonempty_key():
    key = generate()
    assert isinstance(key, str) and len(key) > 0
    assert key.startswith("sk_")


def test_hash_and_verify_key():
    key = generate()
    hashed = hash_key(key)
    assert verify_key(key, hashed) is True
    assert verify_key("wrong-key", hashed) is False


def test_jwt_roundtrip():
    token = create_token(subject="admin")
    payload = decode_token(token)
    assert payload["sub"] == "admin"
    assert validate_token(token) is True
    assert validate_token("not-a-real-token") is False
