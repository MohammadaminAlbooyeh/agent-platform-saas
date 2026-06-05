import json
import threading
import numpy as np
import faiss
from typing import List, Tuple, Optional

from backend.utils.config import FAISS_INDEX_PATH, DOCUMENT_MAP_PATH
from backend.utils.logger import logger


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index: Optional[faiss.Index] = None
        self.doc_map: List[int] = []
        self._lock = threading.RLock()
        self._load()

    def _load(self):
        if FAISS_INDEX_PATH.exists() and DOCUMENT_MAP_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                with open(DOCUMENT_MAP_PATH) as f:
                    self.doc_map = json.load(f)
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}")
                self._create_new()
        else:
            self._create_new()

    def _create_new(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.doc_map = []
        logger.info("Created new FAISS index")

    def add_vectors(self, vectors: np.ndarray, doc_ids: List[int]):
        with self._lock:
            if self.index is None or self.index.is_trained is False:
                self._create_new()
            self.index.add(vectors)
            self.doc_map.extend(doc_ids)
            self._save()

    def search(self, query_vector: np.ndarray, top_k: int = 10) -> Tuple[List[int], List[float]]:
        with self._lock:
            if self.index is None or self.index.ntotal == 0:
                return [], []
            actual_k = min(top_k, self.index.ntotal)
            scores, indices = self.index.search(query_vector.reshape(1, -1), actual_k)
            result_ids = [self.doc_map[int(idx)] for idx in indices[0]]
            return result_ids, scores[0].tolist()

    def remove_vectors(self, doc_ids: List[int]):
        with self._lock:
            if not self.index:
                return
            ids_set = set(doc_ids)
            keep_mask = [i for i, did in enumerate(self.doc_map) if did not in ids_set]
            if len(keep_mask) == len(self.doc_map):
                return
            old_vectors = self.index.reconstruct_n(0, self.index.ntotal)
            kept_vectors = old_vectors[keep_mask]
            self.doc_map = [self.doc_map[i] for i in keep_mask]
            self._create_new()
            if len(kept_vectors) > 0:
                self.index.add(kept_vectors)
            self._save()

    def _save(self):
        if self.index:
            faiss.write_index(self.index, str(FAISS_INDEX_PATH))
        with open(DOCUMENT_MAP_PATH, "w") as f:
            json.dump(self.doc_map, f)

    @property
    def size(self) -> int:
        return self.index.ntotal if self.index else 0
