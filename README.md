# Neural Search Engine

A semantic search engine that uses neural embeddings and FAISS vector search for intelligent document retrieval. Built with FastAPI, Sentence Transformers, and React.

## Features

- **Semantic Search**: Find documents by meaning, not just keywords
- **Neural Embeddings**: Uses Sentence-BERT models for high-quality text embeddings
- **Vector Search**: FAISS-powered similarity search at scale
- **Cross-Encoder Reranking**: Optional reranking for improved precision
- **Intent Classification**: Automatically detects search intent
- **REST API**: FastAPI backend with full CRUD for documents
- **React Frontend**: Modern UI with search, document management, and analytics

## Quick Start

```bash
# Install backend dependencies
pip install -r requirements.txt

# Initialize database and start server
uvicorn backend.main:app --reload

# In a separate terminal, start frontend
cd frontend && npm install && npm run dev
```

Visit `http://localhost:5173` for the UI, or `http://localhost:8000/docs` for API docs.
