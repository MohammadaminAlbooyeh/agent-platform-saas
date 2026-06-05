from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.document import Document
from backend.utils.logger import logger


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, title: str, content: str, source: str = "", author: str = "", metadata: dict = None) -> Document:
        doc = Document(
            title=title,
            content=content,
            source=source,
            author=author,
            metadata=metadata or {},
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        logger.info(f"Created document {doc.id}: {title[:50]}")
        return doc

    def get_document(self, doc_id: int) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == doc_id).first()

    def get_all_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        return self.db.query(Document).offset(skip).limit(limit).all()

    def update_document(self, doc_id: int, **kwargs) -> Optional[Document]:
        doc = self.get_document(doc_id)
        if not doc:
            return None
        for key, value in kwargs.items():
            if hasattr(doc, key) and value is not None:
                setattr(doc, key, value)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def delete_document(self, doc_id: int) -> bool:
        doc = self.get_document(doc_id)
        if not doc:
            return False
        self.db.delete(doc)
        self.db.commit()
        logger.info(f"Deleted document {doc_id}")
        return True

    def search_documents_by_title(self, query: str, limit: int = 20) -> List[Document]:
        return self.db.query(Document).filter(Document.title.ilike(f"%{query}%")).limit(limit).all()
