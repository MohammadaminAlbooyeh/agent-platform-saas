"""Web/API research LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState


def validate_topic(state: AgentState) -> AgentState:
    """Validate the research topic."""
    topic = state.get("input", "")
    if not topic:
        state["error"] = "Empty topic"
    return state


def research(state: AgentState) -> AgentState:
    """Perform research (placeholder for real web/API search)."""
    if state.get("error"):
        return state
    topic = state.get("input", "")
    state["result"] = {
        "agent": "research",
        "tenant_id": state.get("tenant_id"),
        "topic": topic,
        "findings": [],
    }
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result."""
    return state


def build_graph() -> StateGraph:
    """Build the research agent StateGraph."""
    workflow = StateGraph(AgentState)
    workflow.add_node("validate_topic", validate_topic)
    workflow.add_node("research", research)
    workflow.add_node("format_result", format_result)
    workflow.set_entry_point("validate_topic")
    workflow.add_edge("validate_topic", "research")
    workflow.add_edge("research", "format_result")
    workflow.add_edge("format_result", END)
    return workflow


graph = build_graph().compile()


class ResearchAgent:
    """Agent that performs web/API research."""

    async def run(self, topic: str, tenant_id: str) -> dict:
        """Research the given topic for the tenant."""
        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "research",
            "input": topic,
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "research", "tenant_id": tenant_id, "error": final["error"]}
        return final.get("result", {"agent": "research", "tenant_id": tenant_id})
