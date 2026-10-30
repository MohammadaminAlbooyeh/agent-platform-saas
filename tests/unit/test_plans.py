"""Unit tests for plan definitions."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from billing.plans import get_plan, PLANS  # noqa: E402


def test_get_known_plan():
    plan = get_plan("pro")
    assert plan["id"] == "pro"
    assert plan["price_monthly"] == 49.0
    assert plan["tokens"] == 100_000


def test_get_unknown_plan_defaults_to_free():
    plan = get_plan("nonexistent")
    assert plan["id"] == "free"


def test_plans_have_required_fields():
    for pid, plan in PLANS.items():
        assert "price_monthly" in plan
        assert "tokens" in plan
        assert "tools" in plan
