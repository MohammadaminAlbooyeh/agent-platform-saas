# Architecture

## System Overview

```
┌─────────────┐     ┌─────────────────────────────────────┐
│  React SPA  │────▶│          FastAPI Backend             │
│  (Vite)     │     │  ┌───────────────────────────────┐   │
└─────────────┘     │  │  /api/v1/search               │   │
                    │  │  /api/v1/documents             │   │
                    │  │  /api/v1/analytics             │   │
                    │  │  /api/v1/index                 │   │
                    │  └───────────────────────────────┘   │
                    │                                      │
                    │  ┌───────────────────────────────┐   │
                    │  │  Services Layer               │   │
                    │  │  ┌──────┐ ┌───────┐ ┌──────┐ │   │
                    │  │  │Search│ │Doc    │ │Analyt│ │   │
                    │  │  │Service│Service │ │Service│ │   │
                    │  │  └──┬───┘ └───┬───┘ └──┬───┘ │   │
                    │  └─────┼─────────┼─────────┼─────┘   │
                    │        │         │         │          │
                    │  ┌─────▼─────────▼─────────▼─────┐   │
                    │  │  Core Components               │   │
                    │  │  ┌────────┐ ┌────────┐ ┌────┐ │   │
                    │  │  │Embedder│ │FAISS   │ │NLP │ │   │
                    │  │  │(SBERT) │ │Vector  │ │Pipe│ │   │
                    │  │  └────────┘ │Store   │ └────┘ │   │
                    │  │             └────────┘        │   │
                    │  └───────────────────────────────┘   │
                    │                                      │
                    │  ┌───────────────────────────────┐   │
                    │  │  SQLite Database               │   │
                    │  │  (documents, users, indexes)   │   │
                    │  └───────────────────────────────┘   │
                    └─────────────────────────────────────┘
```

## Data Flow

1. **Indexing**: Documents → EmbeddingGenerator → FAISS Vector Store + SQLite
2. **Search**: Query → QueryProcessor → EmbeddingGenerator → FAISS Search → (optional) Cross-Encoder Rerank → Results
3. **Analytics**: Search events logged for usage insights

## Components

- **EmbeddingGenerator**: Wraps Sentence Transformers to produce normalized embeddings
- **VectorStore**: FAISS index with document ID mapping and persistence
- **Retriever**: Performs ANN search to get top-K candidates
- **Ranker**: Cross-encoder re-ranks candidates for higher precision
- **Indexer**: Manages document-to-vector indexing
- **NLP Pipeline**: Preprocessing, intent classification, entity extraction
