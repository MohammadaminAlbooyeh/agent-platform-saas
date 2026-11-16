"""Unit tests for quota service."""

import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest  # noqa: E402

from auth.api_key import generate, hash_key  # noqa: E402
from database.base import SessionLocal  # noqa: E402
from database.models.tenant import Tenant  # noqa: E402
from services.quota_service import QuotaService  # noqa: E402
from services.usage_service import UsageService  # noqa: E402


def test_get_plan_limits():
    svc = QuotaService()
    limits = svc.get_plan_limits("free")
    assert limits["tokens"] == 10_000


def test_check_quota_unknown_tenant_false():
    svc = QuotaService()
    assert svc.check_quota("does-not-exist", estimated_tokens=100) is False


@pytest.fixture
def free_tenant():
    """A real 'free' tenant (10,000 token quota) for cumulative-usage tests."""
    db = SessionLocal()
    try:
        tenant_id = str(uuid.uuid4())
        tenant = Tenant(id=tenant_id, name="Quota Test", plan="free", api_key_hash=hash_key(generate()))
        db.add(tenant)
        db.commit()
        return tenant_id
    finally:
        db.close()


def test_check_quota_accounts_for_cumulative_usage(free_tenant):
    svc = QuotaService()
    usage = UsageService()
    assert svc.check_quota(free_tenant, estimated_tokens=5_000) is True

    usage.record_usage(free_tenant, tokens=9_000, cost=0.0, tool_calls=1)

    # 9,000 used of a 10,000 quota: 5,000 more would exceed it, 1,000 would not.
    assert svc.check_quota(free_tenant, estimated_tokens=5_000) is False
    assert svc.check_quota(free_tenant, estimated_tokens=1_000) is True


def test_get_quota_status_ratio(free_tenant):
    svc = QuotaService()
    usage = UsageService()
    usage.record_usage(free_tenant, tokens=8_000, cost=0.0, tool_calls=1)

    status = svc.get_quota_status(free_tenant)
    assert status["limit"] == 10_000
    assert status["used"] == 8_000
    assert status["ratio"] == pytest.approx(0.8)
