"""Rough token estimation for usage metering (chars/4 heuristic)."""

import json
from typing import Any


def estimate_tokens(data: Any) -> int:
    """Estimate a token count for arbitrary JSON-serializable data."""
    if data is None:
        return 0
    text = data if isinstance(data, str) else json.dumps(data, default=str)
    return max(1, len(text) // 4)
