"""Tool registration, tenant-aware (tool allowlists per plan)."""

from typing import Dict, List, Optional


class Tool:
    """Base class for an MCP tool."""

    name: str = "base"
    allowed_plans: List[str] = ["free", "pro", "enterprise"]

    async def run(self, **kwargs) -> dict:
        raise NotImplementedError


class Registry:
    """Registers MCP tools and enforces per-plan allowlists."""

    def __init__(self) -> None:
        self.tools: Dict[str, Tool] = {}
        self.allowlists: Dict[str, List[str]] = {}

    def register(self, tool: Tool, plans: Optional[List[str]] = None) -> None:
        """Register a tool, optionally restricting it to specific plans."""
        plans = plans or tool.allowed_plans
        self.tools[tool.name] = tool
        self.allowlists[tool.name] = list(plans)

    def is_allowed(self, tool_name: str, plan: str) -> bool:
        """Return True if the tool is available for the given plan."""
        return plan in self.allowlists.get(tool_name, [])

    def get(self, tool_name: str) -> Optional[Tool]:
        """Retrieve a registered tool by name."""
        return self.tools.get(tool_name)

    def list_tools(self, plan: str) -> List[str]:
        """List tool names available to a given plan."""
        return [name for name, plans in self.allowlists.items() if plan in plans]
