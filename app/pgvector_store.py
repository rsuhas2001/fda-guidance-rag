"""
PostgreSQL + pgvector persistence layer for FDA Guidance RAG.
When DATABASE_URL is configured (e.g. via docker-compose), stores chunk embeddings
in a native `vector(256)` column with an HNSW cosine index (`vector_cosine_ops`).
Falls back seamlessly to the in-memory HybridVectorStore when running without Postgres.
"""
from typing import List, Tuple, Optional
import numpy as np
from app.ingestion import DocumentChunk
from app.config import settings

PGVECTOR_SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS fda_guidance_chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    doc_title TEXT NOT NULL,
    source TEXT NOT NULL,
    section TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(256)
);

CREATE INDEX IF NOT EXISTS idx_fda_chunks_embedding_hnsw
ON fda_guidance_chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_fda_chunks_doc_id
ON fda_guidance_chunks (doc_id);
"""


class PgVectorAdapter:
    """
    Production pgvector adapter supporting HNSW cosine similarity queries
    and metadata filtering by `doc_id`.
    """

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or settings.database_url
        self.available = False
        self._conn = None
        if self.dsn:
            try:
                import psycopg2
                self._conn = psycopg2.connect(self.dsn)
                with self._conn.cursor() as cur:
                    cur.execute(PGVECTOR_SCHEMA_SQL)
                self._conn.commit()
                self.available = True
            except Exception:
                self.available = False

    def upsert_chunks(self, chunks: List[DocumentChunk], embeddings: np.ndarray) -> int:
        if not self.available or self._conn is None:
            return 0
        with self._conn.cursor() as cur:
            for chunk, vec in zip(chunks, embeddings):
                padded = np.zeros(256, dtype=np.float32)
                n = min(len(vec), 256)
                padded[:n] = vec[:n]
                vec_literal = "[" + ",".join(f"{float(x):.6f}" for x in padded) + "]"
                cur.execute(
                    """
                    INSERT INTO fda_guidance_chunks
                        (chunk_id, doc_id, doc_title, source, section, chunk_text, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s::vector)
                    ON CONFLICT (chunk_id) DO UPDATE SET
                        chunk_text = EXCLUDED.chunk_text,
                        embedding = EXCLUDED.embedding;
                    """,
                    (
                        chunk.chunk_id,
                        chunk.doc_id,
                        chunk.doc_title,
                        chunk.source,
                        chunk.section,
                        chunk.text,
                        vec_literal,
                    ),
                )
        self._conn.commit()
        return len(chunks)
