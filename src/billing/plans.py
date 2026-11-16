"""Plan definitions (free/pro/enterprise limits & pricing)."""

PLANS = {
    "free": {
        "id": "free",
        "name": "Free",
        "price_monthly": 0.0,
        "tokens": 10_000,
        "tools": ["database"],
        "requests_per_minute": 30,
    },
    "pro": {
        "id": "pro",
        "name": "Pro",
        "price_monthly": 49.0,
        "tokens": 100_000,
        "tools": ["database", "file", "api"],
        "requests_per_minute": 120,
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Enterprise",
        "price_monthly": 499.0,
        "tokens": 1_000_000,
        "tools": ["database", "file", "api"],
        "requests_per_minute": 600,
    },
}

# Rate limit applied to requests with no resolved tenant (bad/missing API key,
# or pre-auth routes like tenant signup/admin login). Deliberately generous
# since these are shared by all unauthenticated callers, not one tenant.
ANONYMOUS_REQUESTS_PER_MINUTE = 60

# Metered cost per 1,000 tokens, used to price agent usage into invoice line items.
COST_PER_1K_TOKENS = 0.002

PRICE_IDS = {
    "pro": "price_pro_monthly",
    "enterprise": "price_enterprise_monthly",
}


def get_plan(plan_id: str) -> dict:
    """Return plan definition by id."""
    return PLANS.get(plan_id, PLANS["free"])
