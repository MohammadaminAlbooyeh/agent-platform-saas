from typing import List, Tuple, Optional

from backend.utils.config import RERANKER_MODEL_NAME, TOP_K_RERANK
from backend.utils.logger import logger


class Ranker:
    def __init__(self, model_name: str = RERANKER_MODEL_NAME):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
                logger.info(f"Loading reranker model: {self.model_name}")
                self._model = CrossEncoder(self.model_name)
            except Exception as e:
                logger.warning(f"Could not load reranker: {e}. Using identity rank.")
                self._model = None
        return self._model

    def rerank(self, query: str, documents: List[Tuple[int, str]], top_k: int = TOP_K_RERANK) -> List[Tuple[int, float]]:
        if not documents or self.model is None:
            return [(doc_id, 0.0) for doc_id, _ in documents[:top_k]]

        pairs = [(query, doc_text) for _, doc_text in documents]
        scores = self.model.predict(pairs)
        scored = [(doc_id, float(score)) for (doc_id, _), score in zip(documents, scores)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
