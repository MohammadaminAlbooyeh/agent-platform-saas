"""Generated invoices per billing cycle model."""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
