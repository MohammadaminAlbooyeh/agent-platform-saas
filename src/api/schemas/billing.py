"""Pydantic models for plans and invoices."""

from pydantic import BaseModel


class Plan(BaseModel):
    id: str
    name: str
    price_monthly: float


class Invoice(BaseModel):
    id: str
    tenant_id: str
    amount: float
    status: str
