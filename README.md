# FDA Guidance Q&A Assistant (`fda-guidance-rag`)

[![FDA-Guidance-RAG CI](https://github.com/rsuhas2001/fda-guidance-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/rsuhas2001/fda-guidance-rag/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL pgvector](https://img.shields.io/badge/PostgreSQL-pgvector-336791.svg)](https://github.com/pgvector/pgvector)
[![License: MIT](https://img.shields.io/badge/Code_License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**FDA Guidance Q&A Assistant** is a Retrieval-Augmented Generation (RAG) system that answers regulatory, packaging, labeling, and cGMP manufacturing quality questions across **14 public-domain U.S. FDA guidance documents and Title 21 Code of Federal Regulations (21 CFR) standards**. Every response cites the exact `[DOC_ID::Section]` chunk used to generate the answer, and when a question falls outside the controlled regulatory corpus, the system **explicitly abstains (`ABSTAIN`) rather than guessing**.

---

## Live Interactive Demo & Preview

- **Live Streamlit App**: **[Launch FDA Guidance Q&A Assistant on Streamlit Cloud](https://fda-guidance-rag.streamlit.app)** *(or click the deployment link in the GitHub **About** sidebar)*
- **Interactive Features**:
  - Filter retrieval across all 14 FDA/21 CFR documents or scope to a specific guidance document.
  - Inspect retrieved `[DOC_ID::Chunk]` source excerpts alongside similarity scores.
  - View real-time GxP audit telemetry (`Groundedness Score`, `Retrieval + Synthesis Latency`, and `Estimated Cost per Query`).

```text
+-----------------------------------------------------------------------------------+
|  FDA Guidance Q&A Assistant | Regulatory & Sterile Packaging Intelligence         |
+-----------------------------------------------------------------------------------+
|  Query: "What are the FDA CMC functionality test limits for penetrability,        |
|          fragmentation, and self-sealing on elastomeric vial stoppers?"           |
|                                                                                   |
|  Grounded Regulatory Response:                                                    |
|  - Penetrability Force: Using a lubricated 21-gauge hypodermic needle at          |
|    200 mm/min, puncture force across 10 stoppers must not exceed 10 N (1.0 kgf)   |
|    [FDA-ELASTOMERS-CMC::C03]                                                      |
|  - Fragmentation (Coring Resistance): Across 48 total punctures, visible          |
|    elastomer fragments retained on a 50-um filter must be <= 5 fragments          |
|    [FDA-ELASTOMERS-CMC::C03]                                                      |
|  - Self-Sealing Capacity: After 10 punctures and immersion in 0.1% methylene      |
|    blue under 27 kPa vacuum, 0 out of 10 vials may exhibit dye ingress            |
|    [FDA-ELASTOMERS-CMC::C03]                                                      |
|                                                                                   |
|  Telemetry: Groundedness: 98.8% | Latency: 0.74 ms | Est. Cost: $0.00015          |
+-----------------------------------------------------------------------------------+
```

---

## System Architecture

```text
+---------------------------------------------------------------------------+
|         14 Public-Domain U.S. FDA Guidance & 21 CFR Documents             |
|  (`data/corpus/` — Container Closure, Labeling, cGMP, OOS, Aseptic, CCIT) |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|           Section-Aware Markdown Chunker (`app/ingestion.py`)             |
|  Splits on `## Section` headers, preserving `[DOC_ID | Section]` context  |
|  and paragraph overlap so tables and regulatory thresholds stay intact    |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|      Hybrid Semantic + Lexical Retriever (`app/retriever.py` & pgvector)  |
|  Score = 0.55 * Dense Cosine Similarity + 0.45 * BM25 + CFR/Code Boost    |
|  (Backed by PostgreSQL 16 `pgvector` HNSW index or in-memory NumPy store) |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|     Grounded Synthesis & Abstention Guardrail (`app/rag_engine.py`)       |
|  - Verifies domain token overlap & retrieval confidence (>= 0.25)         |
|  - Declines out-of-scope prompts (`ABSTAIN`) instead of hallucinating     |
|  - Computes token-level Groundedness Score, Latency (ms), and Cost ($)    |
+---------------------------------------------------------------------------+
```

---

## Evaluation Results (40-Question Golden Benchmark)

The repository includes an automated evaluation suite (`eval/run_eval.py`) scored against a **40-question golden dataset (`eval/golden_dataset.json`)** consisting of **32 in-scope FDA regulatory questions** with verified section citations and **8 out-of-scope adversarial questions** (finance, sports, cooking, networking, tax law, etc.).

### 1. End-to-End Pipeline Scorecard (`eval/eval_report.md`)

| Metric | Verified Result | Notes |
| :--- | :--- | :--- |
| **Total Evaluation Questions** | **40** | 32 in-scope FDA/CFR questions + 8 out-of-scope abstention tests |
| **Top-1 Document Citation Accuracy (`Precision@1`)** | **100.0% (32/32)** | Target FDA/CFR document ranked #1 on every in-scope query |
| **Top-4 Section Recall (`Recall@4`)** | **100.0% (32/32)** | Exact regulatory section retrieved within top-4 chunks |
| **Factual Specification & Keyword Recall** | **95.6%** | Verified against numeric thresholds (`1.5 µg/day`, `10 N`, `3,520 particles/m³`, `3 working days`) |
| **Mean Answer Groundedness Score** | **98.8%** | Proportion of substantive answer tokens backed directly by retrieved chunks |
| **Out-of-Scope Abstention Accuracy** | **100.0% (8/8)** | Correctly declines 100% of non-regulatory questions without guessing |
| **Response Time (`p50` / `p95` Latency)** | **0.74 ms / 0.93 ms** | Local hybrid execution (~480 ms when routed through OpenAI `gpt-4o-mini`) |
| **Estimated Cost per Query** | **$0.000148** | Calculated at `gpt-4o-mini` token pricing (`$0.15/1M` input, `$0.60/1M` output) |

### 2. Ablation Study: Dense-Only vs. Keyword-Only (BM25) vs. Hybrid Retrieval

| Retrieval Strategy | Top-1 Citation Accuracy | Factual Keyword Recall | Why It Happens |
| :--- | :--- | :--- | :--- |
| **Dense Embeddings Only (`weight = 1.0 / 0.0`)** | 84.4% (27/32) | 86.2% | Confuses semantically similar documents with different CFR part numbers (`21 CFR 211.84` vs `21 CFR 201.25`). |
| **BM25 Keyword Only (`weight = 0.0 / 1.0`)** | 90.6% (29/32) | 89.5% | Matches exact CFR numbers well, but misses conceptual paraphrases (e.g., *"stopper coring"* vs *"fragmentation"*). |
| **Hybrid Dense + BM25 (`weight = 0.55 / 0.45`)** | **100.0% (32/32)** | **95.6%** | Combines semantic phrasing with exact CFR/section token scoring. |

---

## How to Run Locally

```bash
# 1. Clone the repository and create a virtual environment
git clone https://github.com/rsuhas2001/fda-guidance-rag.git
cd fda-guidance-rag
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run unit tests and the 40-question evaluation benchmark
python3 tests/test_rag_api.py
python3 eval/run_eval.py

# 4. Launch the interactive Streamlit interface (http://localhost:8501)
python3 -m streamlit run ui/streamlit_app.py

# 5. (Optional) Launch the FastAPI REST server (http://localhost:8000/docs)
python3 -m uvicorn app.main:app --reload --port 8000

# 6. (Optional) Launch with PostgreSQL 16 + pgvector via Docker Compose
docker compose up --build
```

---

## API Key Security & Public Deployment Protection

- **No Hardcoded Secrets**: `.env` is excluded via `.gitignore`. All configuration in `app/config.py` reads from environment variables (`os.getenv("OPENAI_API_KEY")`) or Streamlit's encrypted **Secrets Manager** (`st.secrets`).
- **Zero-Cost Default Mode for Public Demos**: On the public Streamlit Community Cloud deployment, `LLM_PROVIDER` defaults to `local_extractive` so external visitors and recruiters can test unlimited queries without exposing an API key or incurring token charges. When running with an OpenAI or Azure OpenAI key, configure a hard monthly spend limit in the provider dashboard.

---

## Limitations & What I Would Improve Next

1. **Cross-Document Multi-Hop Reasoning**: Queries that require synthesizing rules across 3+ separate CFR parts (for example, linking a `21 CFR 211.192` OOS batch investigation to a `21 CFR 314.81` 3-day Field Alert Report and a `21 CFR Part 7` Class I recall) currently rely on top-K chunk pooling. Next, I would add a **query decomposition step** that retrieves sub-questions per CFR part before synthesis.
2. **Cross-Encoder Reranking**: Adding a lightweight cross-encoder reranker (such as `ms-marco-MiniLM-L-6-v2` or Cohere Rerank) over the top-15 hybrid candidates before selecting the final top-4 chunks would improve robustness on long, multi-clause regulatory prompts.
3. **PDF Table & Complex Diagram Parsing**: Currently, the corpus is curated into structured Markdown (`data/corpus/`). Next, I would integrate layout-aware PDF parsing (e.g., `pdfplumber` / `Docling`) to ingest raw multi-column Federal Register PDFs directly.

---

## Data Sources & Licenses

- **Regulatory Corpus (`data/corpus/`) — Public Domain (`17 U.S.C. § 105`)**: All 14 documents in `data/corpus/` are summaries and excerpts of official **U.S. Food and Drug Administration (FDA) Guidance for Industry documents** and **Title 21 of the Code of Federal Regulations (21 CFR Parts 4, 7, 11, 201, 211, 314, 600)** published by the U.S. federal government, along with publicly released FDA/ICH quality guidelines (`ICH Q1A(R2)`, `ICH Q9(R1)`) and public PQRI threshold recommendations. Works of the U.S. Government are in the public domain and free of copyright restrictions under `17 U.S.C. § 105`. No proprietary or subscription-licensed pharmacopeial text is included.
- **Source Code License**: Released under the **MIT License**.
