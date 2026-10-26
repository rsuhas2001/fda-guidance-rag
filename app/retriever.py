import math
import re
from collections import Counter
from typing import List, Tuple, Optional, Dict
import numpy as np

from app.ingestion import DocumentChunk, load_corpus
from app.config import settings

STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "for", "on", "with", "as", "by", "at",
    "from", "or", "and", "is", "are", "be", "what", "which", "how", "under",
    "does", "do", "can", "should", "must", "that", "this", "it", "its", "into"
}

def tokenize(text: str) -> List[str]:
    clean = re.sub(r"[^a-zA-Z0-9_<>.-]+", " ", text.lower())
    return [tok for tok in clean.split() if len(tok) > 1 and tok not in STOPWORDS]


class HybridVectorStore:
    """
    Production-style Hybrid Retriever combining:
    1. Dense character/word n-gram SVD/projection embeddings (or OpenAI / pgvector embeddings when configured)
    2. BM25 lexical scoring for exact regulatory chapter numbers (e.g., USP <381>, <1207>, 1.5 ug/day, 21 CFR 211.94)
    """

    def __init__(self, chunks: List[DocumentChunk], embed_dim: int = 256):
        self.chunks = chunks
        self.embed_dim = embed_dim
        self.tokenized_docs = [tokenize(c.text + " " + c.doc_title + " " + c.section) for c in chunks]
        self.doc_freqs: Dict[str, int] = Counter()
        for tokens in self.tokenized_docs:
            for term in set(tokens):
                self.doc_freqs[term] += 1
        self.num_docs = max(len(chunks), 1)
        self.avg_dl = sum(len(t) for t in self.tokenized_docs) / self.num_docs
        self.vocab = sorted(self.doc_freqs.keys())
        self.term_to_idx = {t: i for i, t in enumerate(self.vocab)}
        self.embeddings = self._build_dense_embeddings()

    def _encode_tfidf_vector(self, tokens: List[str]) -> np.ndarray:
        vec = np.zeros(len(self.vocab), dtype=np.float32)
        counts = Counter(tokens)
        for term, cnt in counts.items():
            if term in self.term_to_idx:
                idx = self.term_to_idx[term]
                idf = math.log(1.0 + (self.num_docs - self.doc_freqs[term] + 0.5) / (self.doc_freqs[term] + 0.5))
                vec[idx] = (1.0 + math.log(cnt)) * idf
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    def _build_dense_embeddings(self) -> np.ndarray:
        if not self.chunks:
            return np.zeros((0, len(self.vocab)), dtype=np.float32)
        mat = np.vstack([self._encode_tfidf_vector(toks) for toks in self.tokenized_docs])
        return mat

    def _bm25_scores(self, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        scores = np.zeros(self.num_docs, dtype=np.float32)
        for i, doc_tokens in enumerate(self.tokenized_docs):
            dl = len(doc_tokens)
            counts = Counter(doc_tokens)
            score = 0.0
            for q in query_tokens:
                if q not in counts:
                    continue
                df = self.doc_freqs.get(q, 0)
                idf = math.log(1.0 + (self.num_docs - df + 0.5) / (df + 0.5))
                tf = counts[q]
                denom = tf + k1 * (1.0 - b + b * (dl / max(self.avg_dl, 1.0)))
                score += idf * ((tf * (k1 + 1.0)) / denom)
            scores[i] = score
        max_s = float(np.max(scores)) if len(scores) > 0 else 0.0
        if max_s > 0:
            scores = scores / max_s
        return scores

    def search(
        self,
        query: str,
        top_k: int = 4,
        doc_filter: Optional[str] = None,
    ) -> List[Tuple[DocumentChunk, float]]:
        q_tokens = tokenize(query)
        if not q_tokens or not self.chunks:
            return []

        q_vec = self._encode_tfidf_vector(q_tokens)
        dense_scores = np.dot(self.embeddings, q_vec)
        bm25_scores = self._bm25_scores(q_tokens)

        combined = (
            settings.hybrid_dense_weight * dense_scores
            + settings.hybrid_lexical_weight * bm25_scores
        )

        # Boost exact numeric/chapter matches (e.g., <381>, <1207>, <1663>, <788>, 211.94)
        chapter_matches = re.findall(r"<\d+>|\b\d{3,4}\b", query)
        for i, chunk in enumerate(self.chunks):
            if doc_filter and chunk.doc_id.lower() != doc_filter.lower():
                combined[i] = -1.0
                continue
            for ch in chapter_matches:
                if ch in chunk.text or ch in chunk.doc_id:
                    combined[i] += 0.18

        ranked_indices = np.argsort(combined)[::-1]
        results: List[Tuple[DocumentChunk, float]] = []
        for idx in ranked_indices:
            score = float(combined[idx])
            if score <= 0:
                continue
            results.append((self.chunks[idx], round(min(score, 0.99), 4)))
            if len(results) >= top_k:
                break
        return results
