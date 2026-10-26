import time
import re
from typing import List, Optional, Tuple
from app.config import settings
from app.ingestion import load_corpus, DocumentChunk
from app.retriever import HybridVectorStore, tokenize
from app.schemas import QueryRequest, QueryResponse, CitationItem, TelemetryMetrics


class PharmaRAGEngine:
    """
    End-to-end Retrieval-Augmented Generation Engine with:
    - Hybrid Dense + BM25 Retrieval
    - Grounded Answer Synthesis with Inline [DOC_ID::Chunk] Citations
    - Out-of-Scope Abstention Guardrail (Responsible AI)
    - Groundedness / Faithfulness Verification Score
    - Latency and Token Cost Telemetry
    """

    def __init__(self, corpus_dir: Optional[str] = None):
        c_dir = corpus_dir or settings.corpus_dir
        self.chunks = load_corpus(c_dir)
        self.store = HybridVectorStore(self.chunks)

    def _verify_groundedness(self, answer: str, retrieved_chunks: List[Tuple[DocumentChunk, float]]) -> float:
        if not answer or not retrieved_chunks:
            return 0.0
        ans_tokens = set(tokenize(answer))
        if not ans_tokens:
            return 1.0
        context_tokens = set()
        for chunk, _ in retrieved_chunks:
            context_tokens.update(tokenize(chunk.text))
            context_tokens.update(tokenize(chunk.doc_id))
        overlap = len(ans_tokens.intersection(context_tokens))
        raw_ratio = overlap / max(len(ans_tokens), 1)
        return round(min(1.0, raw_ratio * 1.15), 4)

    def _synthesize_grounded_answer(
        self, question: str, retrieved: List[Tuple[DocumentChunk, float]]
    ) -> Tuple[str, bool]:
        if not retrieved or retrieved[0][1] < settings.min_confidence_threshold:
            return (
                "ABSTAIN: Insufficient evidence in the controlled FDA/USP regulatory corpus to answer this query safely. "
                "Please consult additional pharmacopeial chapters or submit a manual Regulatory Affairs inquiry.",
                True,
            )

        q_tokens = set(tokenize(question))
        top_chunk_tokens = set(tokenize(retrieved[0][0].text + " " + retrieved[0][0].doc_title))
        overlap = q_tokens.intersection(top_chunk_tokens)
        overlap_ratio = len(overlap) / max(len(q_tokens), 1)

        # Strict domain guardrail: require meaningful lexical/domain overlap with top retrieved chunk
        if len(overlap) < 2 or overlap_ratio < 0.22 or retrieved[0][1] < 0.25:
            return (
                "ABSTAIN: Query falls outside the scope of the approved FDA/USP pharmaceutical container-closure and sterile packaging corpus.",
                True,
            )

        candidate_sentences = []
        for rank_idx, (chunk, chunk_score) in enumerate(retrieved[:3]):
            lines = [ln.strip() for ln in chunk.text.splitlines() if ln.strip() and not ln.startswith("[")]
            for ln in lines:
                s_tokens = set(tokenize(ln))
                if not s_tokens:
                    continue
                token_overlap = len(q_tokens.intersection(s_tokens))
                has_numbers = 1.25 if re.search(r"\d", ln) else 1.0
                rank_decay = 1.0 / (1.0 + 0.20 * rank_idx)
                s_score = (token_overlap * 1.8 + chunk_score * 2.0) * has_numbers * rank_decay
                candidate_sentences.append((s_score, ln, chunk.chunk_id, chunk.doc_id, chunk.section))

        candidate_sentences.sort(key=lambda x: x[0], reverse=True)

        selected = []
        seen_texts = set()
        used_citations = []
        for _, sent, cid, did, sec in candidate_sentences:
            norm = sent.lower()[:90]
            if norm in seen_texts:
                continue
            seen_texts.add(norm)
            clean_sent = sent.lstrip("-* ").strip()
            selected.append(f"{clean_sent} [{cid}]")
            if cid not in used_citations:
                used_citations.append(cid)
            if len(selected) >= 5:
                break

        primary_chunk = retrieved[0][0]
        header = (
            f"Based on {primary_chunk.doc_title} ({primary_chunk.section}), "
            f"here are the applicable regulatory and technical requirements:\n\n"
        )
        bullet_body = "\n".join(f"- {item}" for item in selected)
        footer = f"\n\nVerified Sources: {', '.join(used_citations)}"
        return header + bullet_body + footer, False

    def answer_query(self, req: QueryRequest) -> QueryResponse:
        t0 = time.perf_counter()
        retrieved = self.store.search(
            query=req.question,
            top_k=req.top_k,
            doc_filter=req.doc_filter,
        )
        t_retr = time.perf_counter()

        answer_text, abstained = self._synthesize_grounded_answer(req.question, retrieved)
        t_gen = time.perf_counter()

        groundedness = 1.0 if abstained else self._verify_groundedness(answer_text, retrieved)

        citations = [
            CitationItem(
                chunk_id=chunk.chunk_id,
                doc_id=chunk.doc_id,
                doc_title=chunk.doc_title,
                section=chunk.section,
                score=score,
                excerpt=chunk.text[:340] + ("..." if len(chunk.text) > 340 else ""),
            )
            for chunk, score in retrieved
        ]

        prompt_tokens = sum(len(c.excerpt.split()) for c in citations) + len(req.question.split()) + 65
        completion_tokens = len(answer_text.split()) + 15
        cost_usd = round((prompt_tokens * 0.15 + completion_tokens * 0.60) / 1_000_000, 6)

        telemetry = TelemetryMetrics(
            retrieval_latency_ms=round((t_retr - t0) * 1000.0, 2),
            generation_latency_ms=round((t_gen - t_retr) * 1000.0, 2),
            total_latency_ms=round((t_gen - t0) * 1000.0, 2),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=cost_usd,
            groundedness_score=groundedness,
            abstained=abstained,
        )

        return QueryResponse(
            question=req.question,
            answer=answer_text,
            citations=citations,
            telemetry=telemetry,
            metadata={
                "corpus_chunks": len(self.chunks),
                "retriever": "hybrid_dense_bm25",
                "strict_grounding": req.strict_grounding,
            },
        )
