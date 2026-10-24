-- Runs automatically the first time the Postgres container starts.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id          BIGSERIAL PRIMARY KEY,
    doc_name    TEXT        NOT NULL,
    page        INT,
    chunk_index INT         NOT NULL,
    content     TEXT        NOT NULL,
    embedding   vector(384) NOT NULL,  -- must match EMBED_DIM
    -- 'simple' config = no language-specific stemming, so German and English both work
    tsv         tsvector GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- HNSW = approximate nearest-neighbour index for fast vector search
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);
-- GIN = inverted index for full-text (keyword) search
CREATE INDEX IF NOT EXISTS chunks_tsv_idx ON chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_doc_idx ON chunks (doc_name);
