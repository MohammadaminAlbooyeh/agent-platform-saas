"""Data-transformation LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState
from services.token_estimator import estimate_tokens


def apply_transform(operation: str, data):
    """Apply a deterministic transform to `data`; raises ValueError if unsupported/mismatched."""
    op = (operation or "identity").strip().lower()
    if op in ("identity", "echo"):
        return data
    if op == "uppercase_keys":
        if not isinstance(data, dict):
            raise ValueError("uppercase_keys requires an object 'data' field")
        return {k: (v.upper() if isinstance(v, str) else v) for k, v in data.items()}
    if op == "sum":
        if not isinstance(data, list):
            raise ValueError("sum requires a list 'data' field")
        return {"sum": sum(float(x) for x in data)}
    if op == "count":
        return {"count": len(data) if hasattr(data, "__len__") else 0}
    if op == "dedupe":
        if not isinstance(data, list):
            raise ValueError("dedupe requires a list 'data' field")
        deduped = []
        for item in data:
            if item not in deduped:
                deduped.append(item)
        return deduped
    raise ValueError(f"Unsupported operation: {operation}")


def validate_payload(state: AgentState) -> AgentState:
    """Validate the incoming payload."""
    payload = state.get("input")
    if not isinstance(payload, dict):
        state["error"] = "Payload must be an object"
    return state


def transform(state: AgentState) -> AgentState:
    """Apply the requested transform to the payload's data."""
    if state.get("error"):
        return state
    payload = state.get("input") or {}
    operation = payload.get("operation", "identity")
    data = payload.get("data", payload)
    try:
        transformed = apply_transform(operation, data)
    except ValueError as exc:
        state["error"] = str(exc)
        return state
    state["result"] = {
        "agent": "processor",
        "tenant_id": state.get("tenant_id"),
        "operation": operation,
        "transformed": transformed,
    }
    state["tool_calls"] = 0
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result and estimate token usage."""
    if state.get("result") is not None:
        state["tokens_used"] = estimate_tokens(state.get("input")) + estimate_tokens(state["result"])
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
    """Agent that applies deterministic data transformations."""

    async def run(self, payload: dict, tenant_id: str) -> dict:
        """Transform the given payload for the tenant."""
        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "processor",
            "input": payload or {},
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "processor", "tenant_id": tenant_id, "error": final["error"]}
        result = final.get("result", {"agent": "processor", "tenant_id": tenant_id})
        result["tokens_used"] = final.get("tokens_used", 0)
        result["tool_calls"] = final.get("tool_calls", 0)
        return result
