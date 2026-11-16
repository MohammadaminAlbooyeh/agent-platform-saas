"""Startup validation of security-critical configuration."""

import logging

from config.settings import Settings

logger = logging.getLogger(__name__)


def validate_production_config(settings: Settings) -> None:
    """Refuse to start in production with insecure default secrets.

    Defaults like JWT_SECRET=change-me and ADMIN_PASSWORD=admin are meant
    for zero-config local development; shipping them to production silently
    would be a critical, easy-to-miss security hole.
    """
    if settings.app_env != "production":
        return

    fatal = []
    if settings.jwt_secret == "change-me":
        fatal.append("JWT_SECRET is still set to the insecure default")
    if settings.admin_password == "admin":
        fatal.append("ADMIN_PASSWORD is still set to the insecure default")
    if fatal:
        raise RuntimeError(
            "Refusing to start with APP_ENV=production and insecure configuration: "
            + "; ".join(fatal)
        )

    if not settings.stripe_secret_key:
        logger.warning("STRIPE_SECRET_KEY is not set in production; billing calls will use fake Stripe responses.")
    if not settings.stripe_webhook_secret:
        logger.warning("STRIPE_WEBHOOK_SECRET is not set in production; webhook events will be accepted unverified.")
