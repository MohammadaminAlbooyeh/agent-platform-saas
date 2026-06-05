from typing import List, Tuple

from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.utils.config import TOP_K_RETRIEVE
from backend.utils.logger import logger


class Retriever:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVE) -> Tuple[List[int], List[float]]:
        query_vector = self.embedding_generator.generate(query)
        doc_ids, scores = self.vector_store.search(query_vector, top_k=top_k)
        logger.debug(f"Retrieved {len(doc_ids)} documents for query: {query[:50]}")
        return doc_ids, scores
