"""Web/API research LangGraph agent."""

from langgraph.graph import StateGraph


class ResearchAgent:
    """Agent that performs web/API research."""

    async def run(self, topic: str, tenant_id: str) -> dict:
        """Research the given topic for the tenant."""
        return {"agent": "research", "tenant_id": tenant_id, "topic": topic, "findings": []}


graph = StateGraph(dict)
