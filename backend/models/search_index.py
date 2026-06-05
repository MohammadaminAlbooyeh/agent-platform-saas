from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float

from backend.models.document import Base


class SearchIndex(Base):
    __tablename__ = "search_indexes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    model_name = Column(String(200), nullable=False)
    dimension = Column(Integer, nullable=False)
    num_documents = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model_name": self.model_name,
            "dimension": self.dimension,
            "num_documents": self.num_documents,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
