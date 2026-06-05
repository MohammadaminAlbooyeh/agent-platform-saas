from typing import List
from sqlalchemy.orm import Session

from backend.models.document import Document
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.utils.logger import logger


class BatchIndexer:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def index_documents(self, documents: List[Document], batch_size: int = 32):
        texts = [f"{doc.title} {doc.content}" for doc in documents]
        doc_ids = [doc.id for doc in documents]

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            batch_ids = doc_ids[i : i + batch_size]
            vectors = self.embedding_generator.generate_batch(batch_texts)
            self.vector_store.add_vectors(vectors, batch_ids)
            logger.info(f"Indexed batch {i//batch_size + 1}: {len(batch_ids)} documents")

    def reindex_all(self, db: Session):
        docs = db.query(Document).all()
        if not docs:
            logger.warning("No documents to reindex")
            return
        self.vector_store._create_new()
        self.index_documents(docs)
        logger.info(f"Reindexed {len(docs)} documents")
