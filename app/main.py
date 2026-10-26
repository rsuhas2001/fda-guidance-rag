from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.schemas import QueryRequest, QueryResponse
from app.rag_engine import PharmaRAGEngine

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "FDA & USP Pharmaceutical Container-Closure & Sterile Packaging RAG API "
        "with Hybrid Retrieval, Citation Grounding, and Telemetry."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = PharmaRAGEngine()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "indexed_chunks": len(rag_engine.chunks),
        "documents": sorted(list({c.doc_id for c in rag_engine.chunks})),
    }

@app.get("/documents")
def list_documents():
    docs = {}
    for c in rag_engine.chunks:
        if c.doc_id not in docs:
            docs[c.doc_id] = {
                "doc_id": c.doc_id,
                "title": c.doc_title,
                "source": c.source,
                "chunk_count": 0,
            }
        docs[c.doc_id]["chunk_count"] += 1
    return {"documents": list(docs.values())}

@app.post("/query", response_model=QueryResponse)
def query_regulatory_corpus(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    return rag_engine.answer_query(request)
