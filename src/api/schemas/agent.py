"""Request/response models for agent execution."""

from pydantic import BaseModel


class AgentExecuteRequest(BaseModel):
    agent_type: str
    payload: dict


class AgentExecuteResponse(BaseModel):
    task_id: str
    status: str
