import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const client = axios.create({ baseURL: API_BASE });

export async function searchDocuments(query, topK = 10, useRerank = true) {
  const res = await client.post('/search', { query, top_k: topK, use_rerank: useRerank });
  return res.data;
}

export async function getDocuments(skip = 0, limit = 100) {
  const res = await client.get('/documents', { params: { skip, limit } });
  return res.data;
}

export async function getDocument(id) {
  const res = await client.get(`/documents/${id}`);
  return res.data;
}

export async function createDocument(doc) {
  const res = await client.post('/documents', doc);
  return res.data;
}

export async function updateDocument(id, doc) {
  const res = await client.put(`/documents/${id}`, doc);
  return res.data;
}

export async function deleteDocument(id) {
  await client.delete(`/documents/${id}`);
}

export async function getAnalyticsStats() {
  const res = await client.get('/analytics/stats');
  return res.data;
}

export async function getIndexInfo() {
  const res = await client.get('/index/info');
  return res.data;
}

export async function reindex() {
  const res = await client.post('/index/reindex');
  return res.data;
}

export async function generateEmbedding(text) {
  const res = await client.post('/embeddings', null, { params: { text } });
  return res.data;
}
