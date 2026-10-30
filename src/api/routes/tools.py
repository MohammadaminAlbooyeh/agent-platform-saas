"""Tools listing and testing routes: /tools."""

from fastapi import APIRouter

router = APIRouter(prefix="/tools")


@router.get("")
async def list_tools() -> dict:
    """List available MCP tools."""
    return {"tools": []}


@router.post("/test")
async def test_tool() -> dict:
    """Test a specific tool."""
    return {"status": "ok"}
