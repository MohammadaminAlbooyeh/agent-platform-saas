"""File MCP tool."""

import os

from mcp_tools.registry import Tool


class FileTool(Tool):
    name = "file"
    allowed_plans = ["pro", "enterprise"]

    async def run(self, path: str, tenant_id: str) -> dict:
        """Read a file path (sandboxed, placeholder)."""
        return {
            "tool": "file",
            "tenant_id": tenant_id,
            "path": path,
            "exists": os.path.exists(path),
            "content": None,
        }
