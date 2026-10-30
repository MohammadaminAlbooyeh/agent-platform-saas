"""Orchestrator that routes incoming requests to the right agent."""

from .query_agent import QueryAgent
from .processor_agent import ProcessorAgent
from .research_agent import ResearchAgent


class Orchestrator:
    """Routes requests to query, processor, or research agents."""

    def __init__(self) -> None:
        self.agents = {
            "query": QueryAgent(),
            "processor": ProcessorAgent(),
            "research": ResearchAgent(),
        }

    async def route(self, agent_type: str, payload: dict, tenant_id: str) -> dict:
        """Route a request to the appropriate agent."""
        agent = self.agents.get(agent_type)
        if agent is None:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return await agent.run(payload, tenant_id)
