import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

TEST_USER = {"username": "testuser", "email": "test@example.com", "password": "secret123"}


@pytest.fixture(scope="module")
def auth_headers():
    client.post("/api/v1/auth/register", params=TEST_USER)
    resp = client.post("/api/v1/auth/login", params={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestSearchFlow:
    def test_health(self):
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_create_and_search_document(self, auth_headers):
        resp = client.post("/api/v1/documents", json={
            "title": "Machine Learning",
            "content": "Machine learning is a subset of artificial intelligence.",
            "source": "test",
            "author": "tester",
        }, headers=auth_headers)
        assert resp.status_code == 201
        doc_id = resp.json()["id"]

        search_resp = client.post("/api/v1/search", json={
            "query": "artificial intelligence",
            "top_k": 10,
            "use_rerank": False,
        })
        assert search_resp.status_code == 200
        data = search_resp.json()
        assert data["total"] > 0
        assert any(r["id"] == doc_id for r in data["results"])

    def test_list_documents(self, auth_headers):
        before = client.get("/api/v1/documents")
        before_count = len(before.json())
        client.post("/api/v1/documents", json={
            "title": "Test", "content": "test content"
        }, headers=auth_headers)
        resp = client.get("/api/v1/documents")
        assert resp.status_code == 200
        assert len(resp.json()) == before_count + 1

    def test_get_document_not_found(self):
        resp = client.get("/api/v1/documents/999")
        assert resp.status_code == 404

    def test_delete_document(self, auth_headers):
        resp = client.post("/api/v1/documents", json={
            "title": "To Delete", "content": "delete me"
        }, headers=auth_headers)
        doc_id = resp.json()["id"]
        del_resp = client.delete(f"/api/v1/documents/{doc_id}", headers=auth_headers)
        assert del_resp.status_code == 204
        get_resp = client.get(f"/api/v1/documents/{doc_id}")
        assert get_resp.status_code == 404

    def test_update_document(self, auth_headers):
        resp = client.post("/api/v1/documents", json={
            "title": "Original Title", "content": "original content"
        }, headers=auth_headers)
        doc_id = resp.json()["id"]
        update_resp = client.put(f"/api/v1/documents/{doc_id}", json={
            "title": "Updated Title",
        }, headers=auth_headers)
        assert update_resp.status_code == 200
        assert update_resp.json()["title"] == "Updated Title"

    def test_search_rejects_empty_query(self):
        resp = client.post("/api/v1/search", json={
            "query": "",
            "top_k": 10,
            "use_rerank": False,
        })
        assert resp.status_code == 422

    def test_register_and_login(self):
        resp = client.post("/api/v1/auth/register", params={
            "username": "newuser",
            "email": "new@example.com",
            "password": "secret123",
        })
        assert resp.status_code == 200
        assert resp.json()["username"] == "newuser"

        login_resp = client.post("/api/v1/auth/login", params={
            "username": "newuser",
            "password": "secret123",
        })
        assert login_resp.status_code == 200
        assert "access_token" in login_resp.json()

    def test_auth_invalid_credentials(self):
        resp = client.post("/api/v1/auth/login", params={
            "username": "nobody",
            "password": "wrong",
        })
        assert resp.status_code == 401

    def test_create_document_requires_auth(self):
        resp = client.post("/api/v1/documents", json={
            "title": "Unauthorized", "content": "should fail",
        })
        assert resp.status_code == 401
