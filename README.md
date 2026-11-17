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

## System Architecture

```text
                                 ┌─────────────────────┐
                                 │        Client        │
                                 │  (X-API-Key header)  │
                                 └──────────┬───────────┘
                                            │ HTTPS
                                            ▼
┌───────────────────────────────────────────────────────────────────────┐
│                         FastAPI app (src/main.py)                      │
│                                                                         │
│   Middleware chain (request order):                                    │
│   TenantContext ──▶ RateLimit ──▶ UsageTracker ──▶ ErrorHandler         │
│   (API-key hash   (Redis token   (times request,   (catches/formats    │
│    → tenant)        bucket per    records usage)     unhandled errors) │
│                      plan)                                             │
│                                                                         │
│   Routes: /agent  /tools  /tenants  /billing  /usage  /admin  /health   │
└───────────────┬───────────────────────────────────────────┬───────────┘
                │                                             │
                ▼                                             ▼
   ┌─────────────────────────┐                  ┌───────────────────────┐
   │        Services          │                  │   Redis (rate limit,  │
   │  tenant / quota / usage / │◀────────────────▶│   token bucket)       │
   │  billing / notification   │                  └───────────────────────┘
   └────────────┬──────────────┘
                │ quota OK
                ▼
   ┌─────────────────────────┐
   │       Orchestrator        │
   │     (src/agents)          │
   │                            │
   │  ┌─────────┐ ┌───────────┐ │     ┌───────────────────────────┐
   │  │  query  │ │ processor │ │────▶│        MCP tools            │
   │  │  agent  │ │  / research│ │     │  database | file | api      │
   │  └─────────┘ └───────────┘ │     │ (sandboxed, SSRF-guarded)   │
   └─────────────┬──────────────┘     └───────────────┬─────────────┘
                 │ usage record written                │
                 ▼                                      ▼
   ┌─────────────────────────────────────────────────────────────┐
   │             PostgreSQL (tenants, usage, invoices, admin)       │
   └───────────────────────────────┬───────────────────────────────┘
                                   │ billing aggregation
                                   ▼
                      ┌─────────────────────────┐
                      │   Stripe (invoices,       │
                      │   signed webhooks)         │
                      └─────────────────────────┘
```

```mermaid
flowchart TB
    Client["Client (X-API-Key)"]

    subgraph FastAPI["FastAPI app (src/main.py)"]
        direction TB
        MW1["TenantContextMiddleware\n(API-key hash → tenant)"]
        MW2["RateLimitMiddleware\n(Redis token bucket, per plan)"]
        MW3["UsageTrackerMiddleware\n(timing + usage capture)"]
        MW4["ErrorHandlerMiddleware"]
        Routes["Routes: /agent /tools /tenants\n/billing /usage /admin /health"]
        MW1 --> MW2 --> MW3 --> MW4 --> Routes
    end

    subgraph Services["Services"]
        TenantSvc["tenant_service"]
        QuotaSvc["quota_service"]
        UsageSvc["usage_service"]
        BillingSvc["billing_service"]
        NotifySvc["notification_service"]
    end

    subgraph Agents["Orchestrator (src/agents)"]
        Orchestrator["Orchestrator"]
        QueryAgent["query_agent"]
        ProcessorAgent["processor_agent"]
        ResearchAgent["research_agent"]
        Orchestrator --> QueryAgent
        Orchestrator --> ProcessorAgent
        Orchestrator --> ResearchAgent
    end

    subgraph MCP["MCP tools (src/mcp_tools)"]
        DBTool["database_tool\n(allowlisted queries)"]
        FileTool["file_tool\n(per-tenant sandbox)"]
        ApiTool["api_tool\n(SSRF-guarded fetch)"]
    end

    Redis[("Redis\ntoken bucket")]
    Postgres[("PostgreSQL\ntenants / usage / invoices / admin")]
    Stripe["Stripe\n(invoices, signed webhooks)"]

    Client -->|HTTPS| MW1
    MW2 <--> Redis
    Routes --> Services
    QuotaSvc -->|quota OK| Orchestrator
    QueryAgent --> DBTool
    ProcessorAgent --> FileTool
    ResearchAgent --> ApiTool
    DBTool --> Postgres
    FileTool --> Postgres
    ApiTool --> Postgres
    UsageSvc --> Postgres
    BillingSvc --> Postgres
    BillingSvc --> Stripe
    TenantSvc --> Postgres
```

See [`docs/architecture.md`](docs/architecture.md) for the full data-flow
narrative and MCP tool details.
