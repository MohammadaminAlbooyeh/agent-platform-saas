"""Data-transformation LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState


def validate_payload(state: AgentState) -> AgentState:
    """Validate the incoming payload."""
    payload = state.get("input", {})
    if payload is None:
        state["error"] = "Missing payload"
    return state


def transform(state: AgentState) -> AgentState:
    """Transform the data (placeholder for real transformation logic)."""
    if state.get("error"):
        return state
    payload = state.get("input", {})
    state["result"] = {
        "agent": "processor",
        "tenant_id": state.get("tenant_id"),
        "payload": payload,
        "transformed": dict(payload) if isinstance(payload, dict) else {},
    }
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result."""
    return state


def build_graph() -> StateGraph:
    """Build the processor agent StateGraph."""
    workflow = StateGraph(AgentState)
    workflow.add_node("validate_payload", validate_payload)
    workflow.add_node("transform", transform)
    workflow.add_node("format_result", format_result)
    workflow.set_entry_point("validate_payload")
    workflow.add_edge("validate_payload", "transform")
    workflow.add_edge("transform", "format_result")
    workflow.add_edge("format_result", END)
    return workflow


graph = build_graph().compile()


class ProcessorAgent:
    """Agent that transforms data."""

    async def run(self, payload: dict, tenant_id: str) -> dict:
        """Transform the given payload for the tenant."""
        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "processor",
            "input": payload,
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "processor", "tenant_id": tenant_id, "error": final["error"]}
        return final.get("result", {"agent": "processor", "tenant_id": tenant_id})
