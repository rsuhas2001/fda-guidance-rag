import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import streamlit as st
from app.rag_engine import PharmaRAGEngine
from app.schemas import QueryRequest

st.set_page_config(
    page_title="PharmaReg-RAG | FDA & USP Packaging Intelligence",
    page_icon="🧪",
    layout="wide",
)

@st.cache_resource
def get_engine():
    return PharmaRAGEngine()

engine = get_engine()

st.title("🧪 PharmaReg-RAG: Injectable Packaging & Regulatory Assistant")
st.caption(
    "Retrieval-Augmented Generation over FDA Container-Closure Guidance, USP <381> Elastomers, "
    "USP <1207> Container Closure Integrity, USP <1663>/<1664> Extractables & Leachables, and EU GMP Annex 1."
)

with st.sidebar:
    st.header("Retrieval & Guardrail Controls")
    top_k = st.slider("Top-K Chunks Retrieved", min_value=2, max_value=8, value=4)
    doc_ids = ["All Documents"] + sorted(list({c.doc_id for c in engine.chunks}))
    selected_doc = st.selectbox("Filter by Regulatory Document", doc_ids)
    strict_mode = st.checkbox("Enforce GxP Citation & Abstention Guardrail", value=True)

    st.divider()
    st.subheader("Sample Regulatory Queries")
    sample_queries = [
        "What is the Safety Concern Threshold (SCT) and Analytical Evaluation Threshold (AET) formula for parenteral leachables under USP <1664>?",
        "What are the USP <381> functionality test limits for penetrability, fragmentation, and self-sealing on vial stoppers?",
        "What is the Kirsch Maximum Allowable Leakage Limit (MALL) in USP <1207> and why are deterministic methods preferred?",
        "How does soluble tungsten from staked-needle prefilled syringes affect biologics and how is it mitigated?",
        "What are the USP <788> sub-visible particulate limits for small-volume vs large-volume parenterals?",
    ]
    chosen_sample = st.radio("Click to populate:", sample_queries)

query_text = st.text_input("Ask a regulatory or packaging engineering question:", value=chosen_sample)

if st.button("Run Grounded Retrieval", type="primary"):
    doc_filter = None if selected_doc == "All Documents" else selected_doc
    req = QueryRequest(question=query_text, top_k=top_k, doc_filter=doc_filter, strict_grounding=strict_mode)
    resp = engine.answer_query(req)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Grounded Regulatory Response")
        if resp.telemetry.abstained:
            st.warning(resp.answer)
        else:
            st.markdown(resp.answer)

        st.subheader("Retrieved Source Citations")
        for cit in resp.citations:
            with st.expander(f"{cit.chunk_id} — {cit.doc_title} ({cit.section}) | Score: {cit.score:.3f}"):
                st.code(cit.excerpt, language="markdown")

    with col2:
        st.subheader("Telemetry & GxP Audit Metrics")
        st.metric("Groundedness Score", f"{resp.telemetry.groundedness_score * 100:.1f}%")
        st.metric("Total Latency", f"{resp.telemetry.total_latency_ms:.2f} ms")
        st.metric("Estimated Cost / Query", f"${resp.telemetry.estimated_cost_usd:.6f}")
        st.json(resp.telemetry.model_dump())
