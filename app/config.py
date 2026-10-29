"""Central configuration. Every value can be overridden with an environment variable or a .env file."""
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rag:rag@localhost:5432/rag")

# Multilingual embedding model: questions in English can match German text.
# e5 models expect "query: " / "passage: " prefixes (handled in embeddings.py).
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-small")
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))  # must match vector(384) in sql/init.sql
# Device for the embedding and re-ranking models. "cpu" leaves the GPU memory to the LLM: on an
# 8 GB Apple M1 the 7B model and these models on the GPU ("mps") together run out of memory.
MODEL_DEVICE = os.getenv("MODEL_DEVICE", "cpu")

# Any OpenAI-compatible endpoint works: Ollama (default, free, local), Groq, OpenAI, ...
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")  # Ollama ignores the key
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b")  # llama3.2 (3B) is ~3x faster but less accurate, see experiments/answer_quality.py
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v2")  # see PROMPTS in app/llm.py

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))  # characters; chosen in experiments/chunk_size.py
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "60"))
TOP_K = int(os.getenv("TOP_K", "5"))
KEYWORD_WEIGHT = float(os.getenv("KEYWORD_WEIGHT", "0.5"))  # weight of keyword results in hybrid search; see experiments/search_comparison.py

# Optional re-ranking of the hybrid candidates with a multilingual cross-encoder
RERANK = os.getenv("RERANK", "true").lower() in ("1", "true", "yes")
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")
RERANK_CANDIDATES = int(os.getenv("RERANK_CANDIDATES", "20"))
# The cross-encoder scores flattened table rows low, so the top hybrid results are always kept
RERANK_KEEP = int(os.getenv("RERANK_KEEP", "2"))  # see experiments/rerank_keep.py

DATA_DIR = os.getenv("DATA_DIR", "data")
