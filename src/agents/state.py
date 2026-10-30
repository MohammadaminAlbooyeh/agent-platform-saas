"""Shared state schema for LangGraph agent graphs."""

from typing import Any, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """State passed through an agent graph execution."""

    tenant_id: str
    agent_type: str
    input: Any
    result: Any
    error: Optional[str]
    steps: list
