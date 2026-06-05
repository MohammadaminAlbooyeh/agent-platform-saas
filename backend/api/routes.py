import time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.api.schemas import (
    DocumentCreate, DocumentUpdate, DocumentResponse,
    SearchRequest, SearchResponse, EmbeddingResponse,
    AnalyticsResponse, IndexInfoResponse,
)
from backend.services.search_service import SearchService
from backend.services.document_service import DocumentService
from backend.services.analytics_service import AnalyticsService
from backend.services.embedding_service import EmbeddingService
from backend.indexing.index_manager import IndexManager
from backend.api.dependencies import (
    get_search_service, get_document_service, get_analytics_service,
    get_embedding_service, get_index_manager, get_embedding_generator,
)
from backend.utils.logger import logger

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(payload: DocumentCreate, doc_service: DocumentService = Depends(get_document_service),
                    emb_service: EmbeddingService = Depends(get_embedding_service)):
    doc = doc_service.create_document(
        title=payload.title,
        content=payload.content,
        source=payload.source,
        author=payload.author,
        metadata=payload.metadata,
    )
    emb_service.index_document(doc)
    return doc.to_dict()


@router.get("/documents", response_model=list[DocumentResponse])
def list_documents(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500),
                   doc_service: DocumentService = Depends(get_document_service)):
    docs = doc_service.get_all_documents(skip=skip, limit=limit)
    return [doc.to_dict() for doc in docs]


@router.get("/documents/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: int, doc_service: DocumentService = Depends(get_document_service)):
    doc = doc_service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc.to_dict()


@router.put("/documents/{doc_id}", response_model=DocumentResponse)
def update_document(doc_id: int, payload: DocumentUpdate,
                    doc_service: DocumentService = Depends(get_document_service),
                    emb_service: EmbeddingService = Depends(get_embedding_service)):
    update_data = payload.model_dump(exclude_unset=True)
    doc = doc_service.update_document(doc_id, **update_data)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    emb_service.index_document(doc)
    return doc.to_dict()


@router.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: int, doc_service: DocumentService = Depends(get_document_service)):
    deleted = doc_service.delete_document(doc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")


@router.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest, search_service: SearchService = Depends(get_search_service)):
    start = time.perf_counter()
    result = search_service.search(payload.query, top_k=payload.top_k, use_rerank=payload.use_rerank)
    latency = (time.perf_counter() - start) * 1000
    logger.info(f"Search completed in {latency:.0f}ms for query: {payload.query[:50]}")
    return result


@router.get("/search", response_model=SearchResponse)
def search_get(q: str = Query(..., description="Search query"),
               top_k: int = Query(10, ge=1, le=100),
               use_rerank: bool = Query(True),
               search_service: SearchService = Depends(get_search_service)):
    start = time.perf_counter()
    result = search_service.search(q, top_k=top_k, use_rerank=use_rerank)
    latency = (time.perf_counter() - start) * 1000
    logger.info(f"Search completed in {latency:.0f}ms for query: {q[:50]}")
    return result


@router.post("/embeddings", response_model=EmbeddingResponse)
def generate_embedding(text: str = Query(..., description="Text to embed"),
                       emb_service: EmbeddingService = Depends(get_embedding_service),
                       emb_gen=Depends(get_embedding_generator)):
    embedding = emb_service.generate_embedding(text)
    return {"embedding": embedding, "dimension": len(embedding), "model": emb_gen.model_name}


@router.post("/index/reindex")
def reindex(db: Session = Depends(get_db), emb_service: EmbeddingService = Depends(get_embedding_service)):
    emb_service.index_all_documents(db)
    return {"message": "Reindexing completed"}


@router.get("/index/info", response_model=IndexInfoResponse)
def index_info(index_manager: IndexManager = Depends(get_index_manager),
               db: Session = Depends(get_db)):
    return index_manager.get_index_info(db)


@router.get("/analytics/stats", response_model=AnalyticsResponse)
def analytics_stats(analytics_service: AnalyticsService = Depends(get_analytics_service)):
    return analytics_service.get_document_stats()
