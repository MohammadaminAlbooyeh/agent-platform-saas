"""Tool registration, tenant-aware (tool allowlists per plan)."""

from typing import Dict, List


class Registry:
    """Registers MCP tools and enforces per-plan allowlists."""

    def __init__(self) -> None:
        self.tools: Dict[str, object] = {}
        self.allowlists: Dict[str, List[str]] = {}

    def register(self, tool: object, plans: List[str]) -> None:
        self.tools[tool.name] = tool
        self.allowlists[tool.name] = plans

    def is_allowed(self, tool_name: str, plan: str) -> bool:
        return plan in self.allowlists.get(tool_name, [])
