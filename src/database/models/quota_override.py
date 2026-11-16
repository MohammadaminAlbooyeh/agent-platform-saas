"""Admin-set per-tenant token quota override model."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.base import Base


class QuotaOverride(Base):
    __tablename__ = "quota_overrides"

    tenant_id = Column(String, ForeignKey("tenants.id"), primary_key=True)
    token_limit = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
