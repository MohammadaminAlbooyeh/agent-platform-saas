from datetime import datetime
from typing import Dict, List
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.document import Document
from backend.utils.logger import logger


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def log_search(self, query: str, results_count: int, latency_ms: float):
        logger.info(f"Search | query={query[:50]} | results={results_count} | latency={latency_ms:.0f}ms")

    def get_document_stats(self) -> Dict:
        total_docs = self.db.query(func.count(Document.id)).scalar()
        latest_doc = self.db.query(Document).order_by(Document.created_at.desc()).first()
        return {
            "total_documents": total_docs or 0,
            "latest_document_title": latest_doc.title if latest_doc else None,
            "latest_document_date": latest_doc.created_at.isoformat() if latest_doc and latest_doc.created_at else None,
        }

    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        return self.db.query(Document).order_by(Document.created_at.desc()).limit(limit).all()
