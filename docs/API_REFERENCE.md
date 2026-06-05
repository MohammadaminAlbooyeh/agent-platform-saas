# API Reference

Base URL: `http://localhost:8000/api/v1`

## Health

### `GET /health`
Returns service status.

## Documents

### `POST /documents`
Create a new document.

**Body:**
```json
{
  "title": "string",
  "content": "string",
  "source": "string (optional)",
  "author": "string (optional)",
  "metadata": "object (optional)"
}
```

### `GET /documents`
List all documents. Query params: `skip` (default 0), `limit` (default 100, max 500).

### `GET /documents/{id}`
Get a document by ID.

### `PUT /documents/{id}`
Update a document. Auto-reindexes on update.

### `DELETE /documents/{id}`
Delete a document.

## Search

### `POST /search`
Neural search across all documents.

**Body:**
```json
{
  "query": "string",
  "top_k": 10,
  "use_rerank": true
}
```

### `GET /search`
Search via query params: `q`, `top_k`, `use_rerank`.

## Embeddings

### `POST /embeddings?text=...`
Generate an embedding vector for text.

## Index

### `POST /index/reindex`
Rebuild the entire FAISS index from all documents.

### `GET /index/info`
Get index metadata (model, dimension, document count).

## Analytics

### `GET /analytics/stats`
Get document statistics (total count, latest document).
