"""Turn text into vectors with a local sentence-transformers model (free, no API key)."""
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import EMBED_MODEL, MODEL_DEVICE

# e5 models were trained with these prefixes; other models (e.g. all-MiniLM) don't use them.
_USES_E5_PREFIX = "e5" in EMBED_MODEL.lower()


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL, device=MODEL_DEVICE)


def embed_passages(texts: list[str]) -> np.ndarray:
    if _USES_E5_PREFIX:
        texts = [f"passage: {t}" for t in texts]
    # normalize -> cosine similarity becomes a simple dot product
    return _model().encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=len(texts) > 64)


def embed_query(text: str) -> np.ndarray:
    if _USES_E5_PREFIX:
        text = f"query: {text}"
    return _model().encode(text, normalize_embeddings=True)
