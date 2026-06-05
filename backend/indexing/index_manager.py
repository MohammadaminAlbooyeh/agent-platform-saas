from sqlalchemy.orm import Session

from backend.models.search_index import SearchIndex
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.utils.logger import logger


class IndexManager:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def get_index_info(self, db: Session) -> dict:
        index_record = db.query(SearchIndex).first()
        if index_record:
            return index_record.to_dict()
        return {
            "name": "default",
            "model_name": self.embedding_generator.model_name,
            "dimension": self.embedding_generator.dimension,
            "num_documents": self.vector_store.size,
        }

    def save_index_metadata(self, name: str, db: Session):
        record = db.query(SearchIndex).filter(SearchIndex.name == name).first()
        if record:
            record.num_documents = self.vector_store.size
        else:
            record = SearchIndex(
                name=name,
                model_name=self.embedding_generator.model_name,
                dimension=self.embedding_generator.dimension,
                num_documents=self.vector_store.size,
            )
            db.add(record)
        db.commit()
        logger.info(f"Saved index metadata: {name}")
