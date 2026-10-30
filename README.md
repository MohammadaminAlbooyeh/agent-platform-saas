# Agent Platform SaaS

Multi-tenant SaaS platform for LangGraph agents with usage-based billing,
per-tenant rate limiting, and MCP tool support.

## Structure

- `src/` — application source code
- `tests/` — unit and integration tests
- `scripts/` — DB bootstrap and seed scripts
- `docker/` — Docker Compose and Dockerfile
- `docs/` — architecture, billing model, API reference

## Setup

```bash
cp .env.example .env
# fill in your values
pip install -r requirements.txt
docker compose up -d
uvicorn src.main:app --reload
```
