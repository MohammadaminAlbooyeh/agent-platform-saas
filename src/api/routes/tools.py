"""Tools listing and testing routes: /tools."""

from fastapi import APIRouter, Request, HTTPException
from mcp_tools.registry import Registry
from mcp_tools.database_tool import DatabaseTool
from mcp_tools.file_tool import FileTool
from mcp_tools.api_tool import APITool

router = APIRouter(prefix="/tools")

registry = Registry()
registry.register(DatabaseTool())
registry.register(FileTool())
registry.register(APITool())


@router.get("")
async def list_tools(request: Request) -> dict:
    """List available MCP tools for the tenant's plan."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    from database.base import SessionLocal
    from database.models.tenant import Tenant
    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        plan = tenant.plan if tenant else "free"
    finally:
        db.close()
    return {"tenant_id": tenant_id, "plan": plan, "tools": registry.list_tools(plan)}


@router.post("/test")
async def test_tool(request: Request, body: dict) -> dict:
    """Test a specific tool."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    tool_name = body.get("tool")
    tool = registry.get(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    from database.base import SessionLocal
    from database.models.tenant import Tenant
    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        plan = tenant.plan if tenant else "free"
    finally:
        db.close()
    if not registry.is_allowed(tool_name, plan):
        raise HTTPException(status_code=403, detail=f"Tool '{tool_name}' not allowed on plan '{plan}'")
    result = await tool.run(**{k: v for k, v in body.items() if k != "tool"}, tenant_id=tenant_id)
    return result
