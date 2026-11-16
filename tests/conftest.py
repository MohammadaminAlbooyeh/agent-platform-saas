"""Pytest configuration and shared fixtures."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from fastapi.testclient import TestClient

# Use a temp sqlite DB for tests so we don't clobber app.db.
tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db.name}"
os.environ["JWT_SECRET"] = "test-secret"

from database.base import Base, engine  # noqa: E402

# Import every model so its table is registered on Base.metadata before
# create_all() runs below — otherwise a model only imported lazily by a
# later test file would never get its table created, and tests would only
# pass by accident of file ordering (e.g. only after test_api.py's app
# startup imports everything first).
from database.models import (  # noqa: E402, F401
    admin_user,
    invoice,
    quota_override,
    task,
    tenant,
    usage_record,
)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient against the app."""
    from src.main import app  # noqa: E402

    with TestClient(app) as c:
        yield c


@pytest.fixture
def tenant(client):
    """Create a pro tenant and return (tenant_id, api_key)."""
    r = client.post("/tenants", json={"name": "Test Tenant", "plan": "pro"})
    assert r.status_code == 201, r.text
    data = r.json()
    return data["id"], data["api_key"]
