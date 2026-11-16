"""Unit tests for DB-backed admin authentication."""

import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from auth.admin_auth import authenticate_admin, hash_password, verify_password  # noqa: E402
from database.base import SessionLocal  # noqa: E402
from database.models.admin_user import AdminUser  # noqa: E402


def test_hash_and_verify_password():
    hashed = hash_password("s3cret")
    assert verify_password("s3cret", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_authenticate_admin_rejects_unknown_user():
    assert authenticate_admin("does-not-exist", "whatever") is False


def test_authenticate_admin_accepts_correct_credentials():
    db = SessionLocal()
    try:
        username = f"admin-{uuid.uuid4().hex[:8]}"
        admin = AdminUser(id=str(uuid.uuid4()), username=username, password_hash=hash_password("topsecret"))
        db.add(admin)
        db.commit()
    finally:
        db.close()

    assert authenticate_admin(username, "topsecret") is True
    assert authenticate_admin(username, "wrong") is False
