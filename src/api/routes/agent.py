"""Agent execution routes: /agent/execute, /agent/stream, /agent/status."""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json

from api.schemas.agent import AgentExecuteRequest, AgentExecuteResponse
from services.agent_service import AgentService

router = APIRouter(prefix="/agent")
agent_service = AgentService()


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute(request: Request, payload: AgentExecuteRequest) -> dict:
    """Execute an agent task for the authenticated tenant."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    result = await agent_service.execute(
        payload.agent_type, payload.payload, tenant_id, estimated_tokens=0
    )
    if "error" in result:
        raise HTTPException(status_code=402, detail=result["error"])
    return {"task_id": result.get("agent", "task"), "status": "completed"}


@router.post("/stream")
async def stream(request: Request, payload: AgentExecuteRequest):
    """Stream agent execution events (SSE)."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    async def event_stream():
        result = await agent_service.execute(
            payload.agent_type, payload.payload, tenant_id, estimated_tokens=0
        )
        yield f"data: {json.dumps(result)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/status/{task_id}")
async def status(request: Request, task_id: str) -> dict:
    """Get the status of an agent task."""
    tenant_id = request.state.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    return {"task_id": task_id, "tenant_id": tenant_id, "status": "completed"}
