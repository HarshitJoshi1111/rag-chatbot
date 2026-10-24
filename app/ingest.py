"""Ingestion: load documents -> split into chunks -> embed -> store in PostgreSQL.

Run from the project root:  python -m app.ingest data/
"""
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.db import get_conn
from app.embeddings import embed_passages

SUPPORTED = {".pdf", ".txt", ".md"}

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],  # prefer paragraph, then sentence boundaries
)


def load_pages(path: Path) -> list[tuple[int | None, str]]:
    """Return (page_number, text) pairs. Page numbers are 1-based; None for plain text files."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    return [(None, path.read_text(encoding="utf-8", errors="ignore"))]


def chunk_document(path: Path) -> list[dict]:
    chunks = []
    for page, text in load_pages(path):
        text = " ".join(text.split())  # collapse PDF line-break noise
        for piece in _splitter.split_text(text):
            if len(piece) >= 50:  # skip headers/footers and empty fragments
                chunks.append({"doc_name": path.name, "page": page, "content": piece})
    for i, c in enumerate(chunks):
        c["chunk_index"] = i
    return chunks


def ingest_file(conn, path: Path) -> int:
    chunks = chunk_document(path)
    if not chunks:
        print(f"  ! no text found in {path.name} (scanned PDF? needs OCR)")
        return 0
    vectors = embed_passages([c["content"] for c in chunks])
    with conn.cursor() as cur:
        # Re-ingesting a file replaces its old chunks, so the script is safe to run twice.
        cur.execute("DELETE FROM chunks WHERE doc_name = %s", (path.name,))
        cur.executemany(
            "INSERT INTO chunks (doc_name, page, chunk_index, content, embedding) VALUES (%s, %s, %s, %s, %s)",
            [(c["doc_name"], c["page"], c["chunk_index"], c["content"], v) for c, v in zip(chunks, vectors)],
        )
    return len(chunks)


def ingest_path(target: Path) -> None:
    files = [target] if target.is_file() else sorted(p for p in target.rglob("*") if p.suffix.lower() in SUPPORTED)
    if not files:
        print(f"No .pdf/.txt/.md files found in {target}")
        return
    with get_conn() as conn:
        for f in files:
            n = ingest_file(conn, f)
            print(f"  {f.name}: {n} chunks")


if __name__ == "__main__":
    ingest_path(Path(sys.argv[1] if len(sys.argv) > 1 else "data"))
