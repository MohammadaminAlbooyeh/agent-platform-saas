"""Agent task history, scoped by tenant_id model."""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    agent_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
