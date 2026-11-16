"""Web/API research LangGraph agent."""

from langgraph.graph import StateGraph, END

from agents.state import AgentState
from mcp_tools.api_tool import APITool
from services.token_estimator import estimate_tokens


def validate_topic(state: AgentState) -> AgentState:
    """Validate the research topic."""
    payload = state.get("input") or {}
    topic = payload.get("topic")
    if not topic:
        state["error"] = "Missing 'topic' or 'url' in payload"
    return state


def research(state: AgentState) -> AgentState:
    """Build findings from the (already-fetched) source, if any."""
    if state.get("error"):
        return state
    payload = state.get("input") or {}
    fetched = payload.get("fetched")
    findings = []
    if fetched:
        if fetched.get("error"):
            findings.append({"source": fetched.get("url"), "error": fetched["error"]})
        else:
            findings.append(
                {
                    "source": fetched.get("url"),
                    "status_code": fetched.get("status_code"),
                    "snippet": (fetched.get("body") or "")[:500],
                }
            )
    state["result"] = {
        "agent": "research",
        "tenant_id": state.get("tenant_id"),
        "topic": payload.get("topic"),
        "findings": findings,
    }
    return state


def format_result(state: AgentState) -> AgentState:
    """Format the final result and estimate token usage."""
    if state.get("result") is not None:
        state["tokens_used"] = estimate_tokens(state.get("input")) + estimate_tokens(state["result"])
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
    """Agent that researches a topic, optionally fetching a URL via the API tool."""

    def __init__(self) -> None:
        self.tool = APITool()

    async def run(self, payload: dict, tenant_id: str) -> dict:
        """Research the given topic/url for the tenant."""
        payload = payload or {}
        url = payload.get("url")
        topic = payload.get("topic") or url
        fetched = None
        tool_calls = 0
        if url:
            fetched = await self.tool.run(url=url, tenant_id=tenant_id)
            tool_calls = 1

        initial: AgentState = {
            "tenant_id": tenant_id,
            "agent_type": "research",
            "input": {"topic": topic, "fetched": fetched},
            "steps": [],
        }
        final = graph.invoke(initial)
        if final.get("error"):
            return {"agent": "research", "tenant_id": tenant_id, "error": final["error"]}
        result = final.get("result", {"agent": "research", "tenant_id": tenant_id})
        result["tool_calls"] = tool_calls
        result["tokens_used"] = final.get("tokens_used", 0)
        return result
