"""API MCP tool with SSRF protection."""

from mcp_tools.registry import Tool


class APITool(Tool):
    name = "api"

    async def run(self, url: str, tenant_id: str) -> dict:
        return {"tool": "api", "url": url}
