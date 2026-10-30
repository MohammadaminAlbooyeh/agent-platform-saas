"""Pydantic models for tenant CRUD."""

from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    plan: str = "free"


class TenantRead(BaseModel):
    id: str
    name: str
    plan: str
    created_at: str
