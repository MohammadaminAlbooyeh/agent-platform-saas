from typing import List
from sqlalchemy.orm import Session

from backend.indexing.indexer import Indexer
from backend.indexing.batch_indexer import BatchIndexer
from backend.models.document import Document
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.utils.logger import logger


class EmbeddingService:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.indexer = Indexer(embedding_generator, vector_store)
        self.batch_indexer = BatchIndexer(embedding_generator, vector_store)

    def generate_embedding(self, text: str) -> List[float]:
        vector = self.embedding_generator.generate(text)
        return vector.tolist()

    def index_document(self, document: Document):
        self.indexer.index_document(document)

    def index_all_documents(self, db: Session):
        docs = db.query(Document).all()
        self.batch_indexer.index_documents(docs)
        logger.info(f"Indexed all {len(docs)} documents")
