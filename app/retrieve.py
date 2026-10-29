"""Retrieval: vector search, keyword search, and hybrid search with Reciprocal Rank Fusion (RRF)."""
import re

from app.config import KEYWORD_WEIGHT, RERANK, RERANK_CANDIDATES
from app.embeddings import embed_query

_COLS = "id, doc_name, page, content"

# Function words appear in almost every chunk, so they only add noise to keyword search.
STOPWORDS = frozenset("""
a an and are as at be by can do does for from how i if in is it many may me much my of on or the to what
when where which who why will with you your
aber als am an auch auf aus bei bin bis da das dass dem den der des die dies diese dieser dir du durch ein
eine einem einen einer eines er es für gibt hat hier ich ihr im in ist ja kann man mit muss nach nicht noch
nur oder ob sie sind so über um und uns von vor was welche welcher welches wenn wer wie wird wo zu zum zur
""".split())

_PREFIX_MIN_LEN = 4  # "credit" also matches "credits" and "Credits2)"


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


def keyword_terms(query: str) -> list[str]:
    """Content words of the query: lower-cased, without stop words and duplicates."""
    words = re.findall(r"\w+", query.lower())
    return [w for w in dict.fromkeys(words) if len(w) > 1 and w not in STOPWORDS]


def keyword_search(conn, query: str, k: int) -> list[dict]:
    """Full-text search with PostgreSQL. Finds exact terms embeddings can miss (§ numbers, codes, names)."""
    terms = keyword_terms(query)
    if not terms:
        return []
    # OR the terms; ts_rank rewards chunks that contain more of them. Longer terms match as prefixes.
    tsquery = " | ".join(f"{t}:*" if len(t) >= _PREFIX_MIN_LEN else t for t in terms)
    rows = conn.execute(
        f"""SELECT {_COLS}, ts_rank(tsv, to_tsquery('simple', %s)) AS score
            FROM chunks WHERE tsv @@ to_tsquery('simple', %s)
            ORDER BY score DESC LIMIT %s""",
        (tsquery, tsquery, k),
    ).fetchall()
    return _rows_to_dicts(rows, "keyword_score")


def rrf_merge(result_lists: list[list[dict]], weights: list[float] | None = None, rrf_k: int = 60) -> list[dict]:
    """Weighted Reciprocal Rank Fusion: score = sum over lists of weight / (rrf_k + rank). Needs no score tuning."""
    weights = weights or [1.0] * len(result_lists)
    merged: dict[int, dict] = {}
    for results, weight in zip(result_lists, weights):
        for rank, hit in enumerate(results, start=1):
            entry = merged.setdefault(hit["id"], {**hit, "score": 0.0})
            entry.update({key: val for key, val in hit.items() if key.endswith("_score")})
            entry["score"] += weight / (rrf_k + rank)
    return sorted(merged.values(), key=lambda h: h["score"], reverse=True)


def hybrid_search(conn, query: str, k: int, keyword_weight: float = KEYWORD_WEIGHT) -> list[dict]:
    """Vector and keyword results fused with RRF. Keyword search gets less weight because it cannot match
    English questions against German text and would push good vector hits down."""
    candidates = k * 4
    lists = [vector_search(conn, query, candidates), keyword_search(conn, query, candidates)]
    return rrf_merge(lists, [1.0, keyword_weight])[:k]


def drop_duplicates(hits: list[dict]) -> list[dict]:
    """Remove chunks whose text repeats a higher-ranked chunk (the same rule in two documents)."""
    seen, unique = set(), []
    for h in hits:
        key = " ".join(h["content"].lower().split())
        if key not in seen:
            seen.add(key)
            unique.append(h)
    return unique


def search(conn, query: str, k: int, mode: str = "hybrid", dedupe: bool = True, rerank: bool | None = None) -> list[dict]:
    """mode: "hybrid" (default), "vector" or "keyword". Fetches extra candidates so that k remain after dedupe.
    With rerank, the top RERANK_CANDIDATES results are re-ordered by a cross-encoder before taking k."""
    if RERANK if rerank is None else rerank:
        from app.rerank import rerank as rerank_hits  # imported lazily: loads a second model

        return rerank_hits(query, search(conn, query, max(k, RERANK_CANDIDATES), mode, dedupe, rerank=False), k)
    n = k * 3 if dedupe else k
    if mode == "vector":
        hits = [{**h, "score": h["vector_score"]} for h in vector_search(conn, query, n)]
    elif mode == "keyword":
        hits = [{**h, "score": h["keyword_score"]} for h in keyword_search(conn, query, n)]
    else:
        hits = hybrid_search(conn, query, n)
    return (drop_duplicates(hits) if dedupe else hits)[:k]
