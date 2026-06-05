import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INDEX_DIR = PROCESSED_DATA_DIR / "indexes"

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
RERANKER_MODEL_NAME = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "384"))

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/search_engine.db")
FAISS_INDEX_PATH = INDEX_DIR / "vectors.faiss"
DOCUMENT_MAP_PATH = PROCESSED_DATA_DIR / "doc_map.json"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

TOP_K_RETRIEVE = int(os.getenv("TOP_K_RETRIEVE", "50"))
TOP_K_RERANK = int(os.getenv("TOP_K_RERANK", "10"))
