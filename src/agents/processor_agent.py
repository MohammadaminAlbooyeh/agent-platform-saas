"""Data-transformation LangGraph agent."""

from langgraph.graph import StateGraph


class ProcessorAgent:
    """Agent that transforms data."""

    async def run(self, payload: dict, tenant_id: str) -> dict:
        """Transform the given payload for the tenant."""
        return {"agent": "processor", "tenant_id": tenant_id, "payload": payload}


graph = StateGraph(dict)
