"""Agent execution routes: /agent/execute, /agent/stream, /agent/status."""

from fastapi import APIRouter

router = APIRouter(prefix="/agent")


@router.post("/execute")
async def execute() -> dict:
    """Execute an agent task."""
    return {"status": "accepted"}


@router.post("/stream")
async def stream() -> dict:
    """Stream agent execution events."""
    return {"status": "streaming"}


@router.get("/status/{task_id}")
async def status(task_id: str) -> dict:
    """Get the status of an agent task."""
    return {"task_id": task_id, "status": "unknown"}
