"""Unit tests for production startup config validation."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest  # noqa: E402

from config.settings import Settings  # noqa: E402
from config.validation import validate_production_config  # noqa: E402


def test_dev_env_never_raises():
    settings = Settings(app_env="development", jwt_secret="change-me", admin_password="admin")
    validate_production_config(settings)  # should not raise


def test_production_with_default_jwt_secret_raises():
    settings = Settings(app_env="production", jwt_secret="change-me", admin_password="s3cret")
    with pytest.raises(RuntimeError):
        validate_production_config(settings)


def test_production_with_default_admin_password_raises():
    settings = Settings(app_env="production", jwt_secret="a-real-secret", admin_password="admin")
    with pytest.raises(RuntimeError):
        validate_production_config(settings)


def test_production_with_real_secrets_does_not_raise():
    settings = Settings(app_env="production", jwt_secret="a-real-secret", admin_password="s3cret")
    validate_production_config(settings)  # should not raise
