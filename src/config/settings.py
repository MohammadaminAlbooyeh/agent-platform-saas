"""Env-based configuration (DB, Redis, Stripe keys)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    redis_url: str = "redis://localhost:6379/0"
    stripe_secret_key: str = ""
    jwt_secret: str = "change-me"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
