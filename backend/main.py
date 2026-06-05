import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.database import init_db
from backend.api.routes import router
from backend.api.auth import router as auth_router
from backend.utils.logger import logger

app = FastAPI(
    title="Neural Search Engine",
    description="Semantic search engine using neural embeddings and FAISS vector store",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized")


@app.get("/")
def root():
    return {"app": "Neural Search Engine", "version": "1.0.0"}
