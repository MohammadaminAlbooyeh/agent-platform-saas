"""FastAPI application entrypoint.

Registers middleware, startup/shutdown hooks, and includes API routers.
"""

from fastapi import FastAPI

app = FastAPI(title="Agent Platform SaaS")


@app.on_event("startup")
async def startup() -> None:
    """Run startup hooks."""
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    """Run shutdown hooks."""
    pass


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
