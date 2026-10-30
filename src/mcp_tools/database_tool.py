"""Database MCP tool."""

from mcp_tools.registry import Tool


class DatabaseTool(Tool):
    name = "database"
    allowed_plans = ["free", "pro", "enterprise"]

    async def run(self, query: str, tenant_id: str) -> dict:
        """Run a read-only database query scoped to the tenant."""
        return {
            "tool": "database",
            "tenant_id": tenant_id,
            "query": query,
            "rows": [],
            "row_count": 0,
        }
