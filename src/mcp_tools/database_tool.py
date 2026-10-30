"""Database MCP tool."""

from mcp_tools.registry import Tool


class DatabaseTool(Tool):
    name = "database"

    async def run(self, query: str, tenant_id: str) -> dict:
        return {"tool": "database", "query": query}
