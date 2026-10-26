"""Ingestion: load documents -> split into chunks -> embed -> store in PostgreSQL.

Run from the project root:  python -m app.ingest data/
"""
import re
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.db import get_conn
from app.embeddings import embed_passages

SUPPORTED = {".pdf", ".txt", ".md"}


# PDF text cleanup (German legal documents)
_PAGE_HEADER = re.compile(r"Seite \d+ von \d+")                                  # "Seite 3 von 12"
_SENTENCE_NUMBER = re.compile(r"(?<![\w§.,])\d{1,2}(?=[A-ZÄÖÜ][a-zäöüß])")      # "1Das" -> "Das"
_LINE_HYPHEN = re.compile(r"(\w) ?- (?!und\b|oder\b|bzw\b|sowie\b)([a-zäöüß])")  # "Prak- tikum" -> "Praktikum"


def clean_text(text: str) -> str:
    text = " ".join(text.split())  # collapse PDF line-break noise
    text = _PAGE_HEADER.sub(" ", text)
    text = _SENTENCE_NUMBER.sub("", text)
    text = _LINE_HYPHEN.sub(r"\1\2", text)
    return " ".join(text.split())


def make_splitter(chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],  # prefer paragraph, then sentence boundaries
        keep_separator="end",  # keep the full stop with its sentence instead of starting the next chunk
    )


def load_pages(path: Path) -> list[tuple[int | None, str]]:
    """Return (page_number, text) pairs. Page numbers are 1-based; None for plain text files."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    return [(None, path.read_text(encoding="utf-8", errors="ignore"))]


def chunk_document(
    path: Path, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP, clean: bool = True
) -> list[dict]:
    splitter = make_splitter(chunk_size, chunk_overlap)
    chunks = []
    for page, text in load_pages(path):
        text = clean_text(text) if clean else " ".join(text.split())
        for piece in splitter.split_text(text):
            if len(piece) >= 50:  # skip headers/footers and empty fragments
                chunks.append({"doc_name": path.name, "page": page, "content": piece})
    for i, c in enumerate(chunks):
        c["chunk_index"] = i
    return chunks


def ingest_file(
    conn, path: Path, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP, clean: bool = True
) -> int:
    chunks = chunk_document(path, chunk_size, chunk_overlap, clean)
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
        # Re-ingesting deletes rows; rebuild the indexes so the HNSW graph has no stale entries.
        conn.execute("REINDEX TABLE chunks")
        conn.execute("VACUUM ANALYZE chunks")


if __name__ == "__main__":
    ingest_path(Path(sys.argv[1] if len(sys.argv) > 1 else "data"))
