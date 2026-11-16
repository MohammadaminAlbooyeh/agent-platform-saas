"""Database-query LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState
from mcp_tools.database_tool import run_scoped_query
from services.token_estimator import estimate_tokens


def validate_query(state: AgentState) -> AgentState:
    """Validate the incoming query payload."""
    payload = state.get("input") or {}
    query_name = payload.get("query") or payload.get("q") if isinstance(payload, dict) else None
    if not query_name:
        state["error"] = "Missing 'query' in payload"
    return state


def execute_query(state: AgentState) -> AgentState:
    """Execute an allowlisted, tenant-scoped database query."""
    if state.get("error"):
        return state
    payload = state.get("input") or {}
    query_name = payload.get("query") or payload.get("q")
    tenant_id = state.get("tenant_id")
    data = run_scoped_query(tenant_id, query_name)
    state["result"] = {
        "agent": "query",
        "tenant_id": tenant_id,
        "query": data["query"],
        "rows": data["rows"],
        "row_count": data["row_count"],
    }
    state["tool_calls"] = 1
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result and estimate token usage."""
    if state.get("result") is not None:
        state["tokens_used"] = estimate_tokens(state.get("input")) + estimate_tokens(state["result"])
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
    """Agent that executes allowlisted, tenant-scoped database queries."""

    async def run(self, payload: dict, tenant_id: str) -> dict:
        """Execute a query scoped to the given tenant."""
        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "query",
            "input": payload or {},
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "query", "tenant_id": tenant_id, "error": final["error"]}
        result = final.get("result", {"agent": "query", "tenant_id": tenant_id})
        result["tokens_used"] = final.get("tokens_used", 0)
        result["tool_calls"] = final.get("tool_calls", 0)
        return result
