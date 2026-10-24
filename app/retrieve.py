"""Retrieval: vector search, keyword search, and hybrid search with Reciprocal Rank Fusion (RRF)."""
import re

from app.embeddings import embed_query

_COLS = "id, doc_name, page, content"


def _rows_to_dicts(rows, score_name: str) -> list[dict]:
    return [{"id": r[0], "doc_name": r[1], "page": r[2], "content": r[3], score_name: float(r[4])} for r in rows]


def vector_search(conn, query: str, k: int) -> list[dict]:
    """Semantic search: nearest neighbours by cosine distance (<=>), served by the HNSW index."""
    q = embed_query(query)
    rows = conn.execute(
        f"SELECT {_COLS}, 1 - (embedding <=> %s) AS score FROM chunks ORDER BY embedding <=> %s LIMIT %s",
        (q, q, k),
    ).fetchall()
    return _rows_to_dicts(rows, "vector_score")


def keyword_search(conn, query: str, k: int) -> list[dict]:
    """Full-text search with PostgreSQL. Finds exact terms embeddings can miss (§ numbers, codes, names)."""
    words = re.findall(r"\w+", query.lower())
    if not words:
        return []
    tsquery = " | ".join(words)  # OR the words; ts_rank rewards chunks that contain more of them
    rows = conn.execute(
        f"""SELECT {_COLS}, ts_rank(tsv, to_tsquery('simple', %s)) AS score
            FROM chunks WHERE tsv @@ to_tsquery('simple', %s)
            ORDER BY score DESC LIMIT %s""",
        (tsquery, tsquery, k),
    ).fetchall()
    return _rows_to_dicts(rows, "keyword_score")


def hybrid_search(conn, query: str, k: int, rrf_k: int = 60) -> list[dict]:
    """Merge both rankings with RRF: score = sum(1 / (rrf_k + rank)). Robust and needs no score tuning."""
    candidates = k * 4
    merged: dict[int, dict] = {}
    for results in (vector_search(conn, query, candidates), keyword_search(conn, query, candidates)):
        for rank, hit in enumerate(results, start=1):
            entry = merged.setdefault(hit["id"], {**hit, "score": 0.0})
            entry.update({key: val for key, val in hit.items() if key.endswith("_score")})
            entry["score"] += 1.0 / (rrf_k + rank)
    return sorted(merged.values(), key=lambda h: h["score"], reverse=True)[:k]


def search(conn, query: str, k: int, mode: str = "hybrid") -> list[dict]:
    if mode == "vector":
        hits = vector_search(conn, query, k)
        for h in hits:
            h["score"] = h["vector_score"]
        return hits
    return hybrid_search(conn, query, k)
