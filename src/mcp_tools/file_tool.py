"""File MCP tool."""

from mcp_tools.registry import Tool


class FileTool(Tool):
    name = "file"

    async def run(self, path: str, tenant_id: str) -> dict:
        return {"tool": "file", "path": path}
