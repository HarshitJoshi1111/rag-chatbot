"""FastAPI service: upload documents, ask questions, get cited answers.

Run locally:  uvicorn app.main:app --reload
Then open http://localhost:8000 (chat page) or http://localhost:8000/docs (API docs).
"""
import shutil
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.config import DATA_DIR, LLM_MODEL, TOP_K
from app.db import get_conn
from app.ingest import SUPPORTED, ingest_file
from app.llm import generate_answer
from app.retrieve import search

app = FastAPI(title="Ask the Regulations", description="Bilingual RAG over German documents")
STATIC = Path(__file__).parent / "static"


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=TOP_K, ge=1, le=20)
    mode: str = Field(default="hybrid", pattern="^(hybrid|vector|keyword)$")


class Source(BaseModel):
    n: int
    doc_name: str
    page: int | None
    score: float
    snippet: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    latency_ms: int


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health():
    with get_conn() as conn:
        n = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
    return {"status": "ok", "chunks": n, "llm": LLM_MODEL}


@app.get("/documents")
def documents():
    with get_conn() as conn:
        rows = conn.execute("SELECT doc_name, count(*) FROM chunks GROUP BY doc_name ORDER BY doc_name").fetchall()
    return [{"doc_name": r[0], "chunks": r[1]} for r in rows]


@app.post("/ingest")
def ingest(file: UploadFile):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED:
        raise HTTPException(400, f"Unsupported file type {suffix!r}; use {sorted(SUPPORTED)}")
    dest = Path(DATA_DIR) / Path(file.filename).name  # .name strips any path tricks in the filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as out:
        shutil.copyfileobj(file.file, out)
    with get_conn() as conn:
        n = ingest_file(conn, dest)
    return {"doc_name": dest.name, "chunks": n}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    start = time.perf_counter()
    with get_conn() as conn:
        hits = search(conn, req.question, req.top_k, req.mode)
    answer = generate_answer(req.question, hits)
    sources = [
        Source(n=i, doc_name=h["doc_name"], page=h["page"], score=round(h["score"], 4), snippet=h["content"][:300])
        for i, h in enumerate(hits, start=1)
    ]
    return AskResponse(answer=answer, sources=sources, latency_ms=int((time.perf_counter() - start) * 1000))
