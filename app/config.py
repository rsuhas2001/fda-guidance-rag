import os
from dataclasses import dataclass

@dataclass
class Settings:
    app_name: str = "PharmaReg-RAG API"
    version: str = "1.2.0"
    corpus_dir: str = os.getenv("CORPUS_DIR", "data/corpus")
    chunk_size_words: int = int(os.getenv("CHUNK_SIZE_WORDS", "180"))
    chunk_overlap_words: int = int(os.getenv("CHUNK_OVERLAP_WORDS", "35"))
    top_k_default: int = int(os.getenv("TOP_K_DEFAULT", "4"))
    min_confidence_threshold: float = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.14"))
    hybrid_dense_weight: float = float(os.getenv("HYBRID_DENSE_WEIGHT", "0.55"))
    hybrid_lexical_weight: float = float(os.getenv("HYBRID_LEXICAL_WEIGHT", "0.45"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "local_extractive")  # "openai", "azure_openai", or "local_extractive"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    database_url: str = os.getenv("DATABASE_URL", "")  # Optional PostgreSQL + pgvector DSN

settings = Settings()
