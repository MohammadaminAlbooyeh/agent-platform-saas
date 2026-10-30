"""Unit tests for quota service."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.quota_service import QuotaService  # noqa: E402


def test_get_plan_limits():
    svc = QuotaService()
    limits = svc.get_plan_limits("free")
    assert limits["tokens"] == 10_000


def test_check_quota_unknown_tenant_false():
    svc = QuotaService()
    assert svc.check_quota("does-not-exist", estimated_tokens=100) is False
