"""Admin password hashing and bootstrap of the initial admin user."""

import logging
import uuid

import bcrypt

from config.settings import settings
from database.base import SessionLocal
from database.models.admin_user import AdminUser

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash an admin password for storage."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext admin password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        return False


def authenticate_admin(username: str, password: str) -> bool:
    """Return True if username/password match a stored admin user."""
    db = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == username).first()
        if not admin:
            return False
        return verify_password(password, admin.password_hash)
    finally:
        db.close()


def bootstrap_admin() -> None:
    """Create the initial admin user from settings if no admin user exists yet.

    This replaces the hardcoded admin/admin credential check with a real,
    DB-backed admin user, while keeping a working zero-config default for
    local development.
    """
    db = SessionLocal()
    try:
        if db.query(AdminUser).first() is not None:
            return
        admin = AdminUser(
            id=str(uuid.uuid4()),
            username=settings.admin_username,
            password_hash=hash_password(settings.admin_password),
        )
        db.add(admin)
        db.commit()
        if settings.app_env != "development" and settings.admin_password == "admin":
            logger.warning(
                "Bootstrapped admin user '%s' with the default password in a non-development "
                "environment (APP_ENV=%s). Set ADMIN_PASSWORD before deploying.",
                settings.admin_username,
                settings.app_env,
            )
    finally:
        db.close()
