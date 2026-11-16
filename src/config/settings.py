"""Env-based configuration (DB, Redis, Stripe keys)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    redis_url: str = "redis://localhost:6379/0"
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    jwt_secret: str = "change-me"
    app_env: str = "development"
    admin_username: str = "admin"
    admin_password: str = "admin"
    file_tool_root: str = "./tenant_files"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
