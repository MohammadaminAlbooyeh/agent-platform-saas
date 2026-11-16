"""Admin dashboard user accounts model."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from database.base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
