"""File MCP tool: sandboxed, per-tenant file reads."""

from pathlib import Path
from typing import Optional

from config.settings import settings
from mcp_tools.registry import Tool

MAX_READ_BYTES = 64 * 1024


def _tenant_root(tenant_id: str) -> Path:
    """Return (creating if needed) the sandbox directory for a tenant."""
    root = Path(settings.file_tool_root).resolve()
    tenant_root = (root / tenant_id).resolve()
    tenant_root.mkdir(parents=True, exist_ok=True)
    return tenant_root


def resolve_safe_path(tenant_id: str, path: str) -> Optional[Path]:
    """Resolve `path` within the tenant's sandbox; return None if it would escape it."""
    tenant_root = _tenant_root(tenant_id)
    candidate = (tenant_root / path).resolve()
    try:
        candidate.relative_to(tenant_root)
    except ValueError:
        return None
    return candidate


class FileTool(Tool):
    name = "file"
    allowed_plans = ["pro", "enterprise"]

    async def run(self, path: str, tenant_id: str) -> dict:
        """Read a file from the tenant's sandboxed directory (no path traversal)."""
        resolved = resolve_safe_path(tenant_id, path)
        if resolved is None:
            return {
                "tool": "file",
                "tenant_id": tenant_id,
                "path": path,
                "error": "Path escapes tenant sandbox",
            }
        if not resolved.exists() or not resolved.is_file():
            return {"tool": "file", "tenant_id": tenant_id, "path": path, "exists": False, "content": None}

        raw = resolved.read_bytes()
        try:
            content: Optional[str] = raw[:MAX_READ_BYTES].decode("utf-8")
        except UnicodeDecodeError:
            content = None
        return {
            "tool": "file",
            "tenant_id": tenant_id,
            "path": path,
            "exists": True,
            "content": content,
            "truncated": len(raw) > MAX_READ_BYTES,
        }
