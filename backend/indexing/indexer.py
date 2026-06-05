from typing import Optional
from sqlalchemy.orm import Session

from backend.models.document import Document
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.utils.logger import logger


class Indexer:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def index_document(self, document: Document):
        text_to_embed = f"{document.title} {document.content}"
        vector = self.embedding_generator.generate(text_to_embed)
        self.vector_store.add_vectors(vector.reshape(1, -1), [document.id])
        logger.info(f"Indexed document {document.id}: {document.title[:50]}")

    def index_document_by_id(self, doc_id: int, db: Session):
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if doc:
            self.index_document(doc)
