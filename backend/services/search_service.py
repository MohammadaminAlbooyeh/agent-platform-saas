from typing import List, Dict
from sqlalchemy.orm import Session

from backend.models.document import Document
from backend.search.embedding_generator import EmbeddingGenerator
from backend.search.vector_store import VectorStore
from backend.search.retriever import Retriever
from backend.search.ranker import Ranker
from backend.nlp.intent_classifier import IntentClassifier
from backend.utils.logger import logger


class SearchService:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore, db: Session):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.db = db
        self.retriever = Retriever(embedding_generator, vector_store)
        self.ranker = Ranker()
        self.intent_classifier = IntentClassifier()

    def search(self, query: str, top_k: int = 10, use_rerank: bool = True) -> Dict:
        intent = self.intent_classifier.classify(query)
        doc_ids, scores = self.retriever.retrieve(query, top_k=top_k * 5 if use_rerank else top_k)

        if not doc_ids:
            return {"query": query, "intent": intent, "results": [], "total": 0}

        doc_records = self.db.query(Document).filter(Document.id.in_(doc_ids)).all()
        doc_map = {d.id: d for d in doc_records}
        docs = [doc_map[doc_id] for doc_id in doc_ids if doc_id in doc_map]

        if use_rerank and docs:
            doc_texts = [(doc.id, doc.title + " " + doc.content) for doc in docs]
            reranked = self.ranker.rerank(query, doc_texts, top_k=top_k)
            results = []
            for doc_id, score in reranked:
                doc = next((d for d in docs if d.id == doc_id), None)
                if doc:
                    result = doc.to_dict()
                    result["score"] = score
                    results.append(result)
        else:
            results = []
            for doc, score in zip(docs, scores):
                result = doc.to_dict()
                result["score"] = score
                results.append(result)

        return {"query": query, "intent": intent, "results": results, "total": len(results)}
