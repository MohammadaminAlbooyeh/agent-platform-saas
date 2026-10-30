"""Per-request usage log model."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.base import Base


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    tool_calls = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
