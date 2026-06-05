from fastapi import Depends
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.models.user import User
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.services.search_service import SearchService
from backend.services.document_service import DocumentService
from backend.services.analytics_service import AnalyticsService
from backend.services.embedding_service import EmbeddingService
from backend.indexing.index_manager import IndexManager
from backend.api.auth import get_current_user

_embedding_generator: EmbeddingGenerator | None = None
_vector_store: VectorStore | None = None


def get_embedding_generator() -> EmbeddingGenerator:
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        emb = get_embedding_generator()
        _vector_store = VectorStore(emb.dimension)
    return _vector_store


def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    return SearchService(get_embedding_generator(), get_vector_store(), db)


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(db)


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(get_embedding_generator(), get_vector_store())


def get_index_manager() -> IndexManager:
    return IndexManager(get_embedding_generator(), get_vector_store())
