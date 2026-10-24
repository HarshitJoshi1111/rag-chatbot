"""PostgreSQL connection with pgvector support."""
import psycopg
from pgvector.psycopg import register_vector

from app.config import DATABASE_URL


def get_conn() -> psycopg.Connection:
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    register_vector(conn)  # lets us pass numpy arrays as `vector` parameters
    return conn
