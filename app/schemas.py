from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Regulatory or technical question about pharmaceutical packaging")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of chunks to retrieve")
    doc_filter: Optional[str] = Field(default=None, description="Optional DOC_ID filter (e.g. USP-381-ELASTOMERS)")
    strict_grounding: bool = Field(default=True, description="Enforce citation verification and abstention on out-of-scope queries")

class CitationItem(BaseModel):
    chunk_id: str
    doc_id: str
    doc_title: str
    section: str
    score: float
    excerpt: str

class TelemetryMetrics(BaseModel):
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float
    groundedness_score: float
    abstained: bool

class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: List[CitationItem]
    telemetry: TelemetryMetrics
    metadata: Dict[str, Any] = Field(default_factory=dict)
