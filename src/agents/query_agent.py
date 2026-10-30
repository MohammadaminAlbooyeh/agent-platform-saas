"""Database-query LangGraph agent."""

from langgraph.graph import StateGraph


class QueryAgent:
    """Agent that executes database queries on behalf of a tenant."""

    async def run(self, query: str, tenant_id: str) -> dict:
        """Execute a query scoped to the given tenant."""
        return {"agent": "query", "tenant_id": tenant_id, "query": query, "result": None}


graph = StateGraph(dict)
