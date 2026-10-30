"""Plan definitions (free/pro/enterprise limits & pricing)."""

PLANS = {
    "free": {
        "id": "free",
        "name": "Free",
        "price_monthly": 0.0,
        "tokens": 10_000,
        "tools": ["database"],
    },
    "pro": {
        "id": "pro",
        "name": "Pro",
        "price_monthly": 49.0,
        "tokens": 100_000,
        "tools": ["database", "file", "api"],
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Enterprise",
        "price_monthly": 499.0,
        "tokens": 1_000_000,
        "tools": ["database", "file", "api"],
    },
}

PRICE_IDS = {
    "pro": "price_pro_monthly",
    "enterprise": "price_enterprise_monthly",
}


def get_plan(plan_id: str) -> dict:
    """Return plan definition by id."""
    return PLANS.get(plan_id, PLANS["free"])
