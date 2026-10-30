# Architecture

System diagram and data flow for the Agent Platform SaaS.

## Overview

Clients authenticate with per-tenant API keys. The `TenantContextMiddleware`
resolves the tenant and injects it into the request context. Requests are
routed through `Orchestrator` to the appropriate LangGraph agent
(query, processor, research). Usage is tracked per call and aggregated for
billing. Stripe handles subscriptions and invoices.

## Data Flow

1. Client call -> API key auth -> tenant resolution
2. Rate limit + quota check (per plan)
3. Agent execution via orchestrator
4. Usage record written
5. Billing aggregation + invoice generation
