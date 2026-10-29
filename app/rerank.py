"""Re-ranking: a cross-encoder reads question and passage together and scores how well the passage answers it.

Slower than embedding search (one model call per passage), so it only re-orders a short candidate list.
It was trained on prose and scores flattened table rows low, so the first `keep` candidates of the
original ranking always stay in the result (they replace the lowest re-ranked passages).
"""
from functools import lru_cache

from sentence_transformers import CrossEncoder

from app.config import MODEL_DEVICE, RERANK_KEEP, RERANK_MODEL


@lru_cache(maxsize=1)
def _model() -> CrossEncoder:
    return CrossEncoder(RERANK_MODEL, max_length=512, device=MODEL_DEVICE)


def rerank(query: str, hits: list[dict], k: int, keep: int = RERANK_KEEP) -> list[dict]:
    if not hits:
        return []
    scores = _model().predict([(query, h["content"]) for h in hits])
    ranked = sorted(
        ({**h, "rerank_score": float(s), "score": float(s)} for h, s in zip(hits, scores)),
        key=lambda h: h["rerank_score"],
        reverse=True,
    )
    top = ranked[:k]
    chosen = {h["id"] for h in top}
    kept = [h for h in ranked if h["id"] in {o["id"] for o in hits[:keep]} and h["id"] not in chosen]
    return top[: k - len(kept)] + kept
