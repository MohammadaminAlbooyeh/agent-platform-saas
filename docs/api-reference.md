# API Reference

## Endpoints

### Agent
- `POST /agent/execute` — execute an agent task
- `POST /agent/stream` — stream agent events
- `GET /agent/status/{task_id}` — get task status

### Tools
- `GET /tools` — list available MCP tools
- `POST /tools/test` — test a tool

### Tenants
- `POST /tenants` — create a tenant
- `GET /tenants/{id}` — get a tenant

### Billing
- `POST /billing/subscribe` — create a subscription
- `POST /billing/webhook` — Stripe webhook receiver

### Usage
- `GET /usage/{tenant_id}` — per-tenant usage stats

### Admin
- `GET /admin/tenants` — list all tenants
- `POST /admin/quota-override` — override a quota
