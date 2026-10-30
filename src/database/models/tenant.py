"""Tenant table model."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from database.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    plan = Column(String, nullable=False, default="free")
    api_key_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
