"""FastAPI application entrypoint.

Registers middleware, startup/shutdown hooks, and includes API routers.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure the `src` directory is importable as a top-level package so that
# `config`, `database`, `api`, `services`, etc. resolve regardless of CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from config.settings import settings
from config.validation import validate_production_config
from database.base import init_db
from auth.admin_auth import bootstrap_admin

from api.middleware.error_handler import ErrorHandlerMiddleware
from api.middleware.tenant_context import TenantContextMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.usage_tracker import UsageTrackerMiddleware

from api.routes.agent import router as agent_router
from api.routes.tools import router as tools_router
from api.routes.tenants import router as tenants_router
from api.routes.billing import router as billing_router
from api.routes.usage import router as usage_router
from api.routes.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup hooks, then yield; no shutdown hooks are needed yet."""
    validate_production_config(settings)
    init_db()
    bootstrap_admin()
    yield


app = FastAPI(title="Agent Platform SaaS", version="0.1.0", lifespan=lifespan)


# Middleware (added in reverse order of execution; last added runs first)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(UsageTrackerMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantContextMiddleware)


# Routers
app.include_router(agent_router)
app.include_router(tools_router)
app.include_router(tenants_router)
app.include_router(billing_router)
app.include_router(usage_router)
app.include_router(admin_router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
