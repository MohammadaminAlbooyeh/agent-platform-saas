"""Integration tests covering multi-tenant API flow."""

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_tenant_returns_api_key(client):
    r = client.post("/tenants", json={"name": "Acme", "plan": "free"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Acme"
    assert data["plan"] == "free"
    assert data.get("api_key") is not None


def test_agent_execute_requires_api_key(client):
    r = client.post("/agent/execute", json={"agent_type": "query", "payload": {}})
    assert r.status_code == 401


def test_agent_execute_success(client, tenant):
    tenant_id, api_key = tenant
    r = client.post(
        "/agent/execute",
        json={"agent_type": "query", "payload": {"q": "select 1"}},
        headers={"x-api-key": api_key},
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "completed"


def test_tools_respect_plan_allowlist(client, tenant):
    tenant_id, api_key = tenant
    r = client.get("/tools", headers={"x-api-key": api_key})
    assert r.status_code == 200
    assert "api" in r.json()["tools"]  # pro plan includes api


def test_usage_endpoint(client, tenant):
    tenant_id, api_key = tenant
    client.post(
        "/agent/execute",
        json={"agent_type": "query", "payload": {"q": "select 1"}},
        headers={"x-api-key": api_key},
    )
    r = client.get(f"/usage/{tenant_id}", headers={"x-api-key": api_key})
    assert r.status_code == 200
    body = r.json()
    assert body["tenant_id"] == tenant_id
    # Real usage recorded by the agent run, not the old always-zero placeholder.
    assert body["tokens"] > 0
    assert body["tool_calls"] > 0
    assert body["record_count"] == 1


def test_usage_cannot_view_other_tenant(client, tenant):
    _, api_key = tenant
    r = client.get("/usage/does-not-exist", headers={"x-api-key": api_key})
    assert r.status_code == 403


def test_admin_login_and_list_tenants(client):
    r = client.post("/admin/login", json={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    r = client.get("/admin/tenants", headers={"authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert "tenants" in r.json()


def test_admin_login_rejects_bad_credentials(client):
    r = client.post("/admin/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401


def test_stripe_webhook_unverified_without_secret_configured(client):
    # STRIPE_WEBHOOK_SECRET is unset in tests, so the webhook accepts the raw
    # event body without signature verification (logged as a warning).
    r = client.post(
        "/billing/webhook",
        json={"type": "invoice.payment_succeeded", "data": {"object": {"id": "in_123", "customer": "cus_1"}}},
    )
    assert r.status_code == 200
    assert r.json() == {"status": "received", "type": "invoice.payment_succeeded"}


def test_stripe_webhook_rejects_malformed_payload(client):
    r = client.post("/billing/webhook", content=b"not json", headers={"content-type": "application/json"})
    assert r.status_code == 400


def test_billing_invoice_generation(client, tenant):
    tenant_id, api_key = tenant
    r = client.post("/billing/invoice", json={}, headers={"x-api-key": api_key})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["invoice"]["tenant_id"] == tenant_id
    assert body["invoice"]["status"] == "draft"


def test_admin_quota_override_persists_and_is_enforced(client, tenant):
    tenant_id, api_key = tenant

    login = client.post("/admin/login", json={"username": "admin", "password": "admin"})
    token = login.json()["access_token"]
    headers = {"authorization": f"Bearer {token}"}

    r = client.post("/admin/quota-override", json={"tenant_id": tenant_id, "token_limit": 100}, headers=headers)
    assert r.status_code == 200, r.text
    assert r.json() == {"status": "overridden", "tenant_id": tenant_id, "token_limit": 100}

    # The override (100 tokens) is far below what a single agent call needs by
    # default, so the next call should now be quota-rejected (HTTP 402).
    r = client.post(
        "/agent/execute",
        json={"agent_type": "query", "payload": {"q": "select 1" * 500}},
        headers={"x-api-key": api_key},
    )
    assert r.status_code == 402
