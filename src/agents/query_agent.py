"""Database-query LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState


def validate_query(state: AgentState) -> AgentState:
    """Validate the incoming query."""
    query = state.get("input", "")
    if not query:
        state["error"] = "Empty query"
    return state


def execute_query(state: AgentState) -> AgentState:
    """Execute the database query (placeholder for real DB/Tool call)."""
    if state.get("error"):
        return state
    query = state.get("input", "")
    state["result"] = {
        "agent": "query",
        "tenant_id": state.get("tenant_id"),
        "query": query,
        "rows": [],
    }
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result."""
    return state


def build_graph() -> StateGraph:
    """Build the query agent StateGraph."""
    workflow = StateGraph(AgentState)
    workflow.add_node("validate_query", validate_query)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("format_result", format_result)
    workflow.set_entry_point("validate_query")
    workflow.add_edge("validate_query", "execute_query")
    workflow.add_edge("execute_query", "format_result")
    workflow.add_edge("format_result", END)
    return workflow


graph = build_graph().compile()


class QueryAgent:
    """Agent that executes database queries on behalf of a tenant."""

    async def run(self, query: str, tenant_id: str) -> dict:
        """Execute a query scoped to the given tenant."""
        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "query",
            "input": query,
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "query", "tenant_id": tenant_id, "error": final["error"]}
        return final.get("result", {"agent": "query", "tenant_id": tenant_id})
