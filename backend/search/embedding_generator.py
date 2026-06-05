import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional

from backend.utils.config import EMBEDDING_MODEL_NAME
from backend.utils.logger import logger


class EmbeddingGenerator:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self._model: Optional[SentenceTransformer] = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def generate(self, text: str) -> np.ndarray:
        return self.model.encode(text, normalize_embeddings=True)

    def generate_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        return self.model.encode(texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
