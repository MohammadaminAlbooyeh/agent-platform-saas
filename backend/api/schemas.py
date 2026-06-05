from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, field_validator


class DocumentCreate(BaseModel):
    title: str
    content: str
    source: str = ""
    author: str = ""
    metadata: Dict[str, Any] = {}


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    source: str
    author: str
    metadata: Dict[str, Any]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    score: Optional[float] = None

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    use_rerank: bool = True

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("query must not be empty")
        return v.strip()


class SearchResponse(BaseModel):
    query: str
    intent: str
    results: List[DocumentResponse]
    total: int


class AnalyticsResponse(BaseModel):
    total_documents: int
    latest_document_title: Optional[str] = None
    latest_document_date: Optional[str] = None


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int
    model: str


class IndexInfoResponse(BaseModel):
    name: str
    model_name: str
    dimension: int
    num_documents: int
