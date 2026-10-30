"""Structured logging, tagged with tenant_id."""

import logging


def setup_logging() -> None:
    """Configure structured logging."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
