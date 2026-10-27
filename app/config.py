"""Central configuration. Every value can be overridden with an environment variable or a .env file."""
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rag:rag@localhost:5432/rag")

# Multilingual embedding model: questions in English can match German text.
# e5 models expect "query: " / "passage: " prefixes (handled in embeddings.py).
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-small")
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))  # must match vector(384) in sql/init.sql

# Any OpenAI-compatible endpoint works: Ollama (default, free, local), Groq, OpenAI, ...
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")  # Ollama ignores the key
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))  # characters; chosen in experiments/chunk_size.py
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "60"))
TOP_K = int(os.getenv("TOP_K", "5"))
KEYWORD_WEIGHT = float(os.getenv("KEYWORD_WEIGHT", "0.5"))  # weight of keyword results in hybrid search; see experiments/search_comparison.py

DATA_DIR = os.getenv("DATA_DIR", "data")
