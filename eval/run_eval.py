#!/usr/bin/env python3
"""
Automated Evaluation Harness for PharmaReg-RAG (25-Question Golden Benchmark).
Measures:
1. Top-1 & Top-K Document Citation Accuracy (Recall@1, Recall@4)
2. Answer Fact/Keyword Completeness
3. Groundedness / Faithfulness Score
4. Out-of-Scope Abstention Accuracy (Responsible AI Guardrail)
5. Latency (p50, p95 in ms) and Estimated Cost per Query
"""
import json
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag_engine import PharmaRAGEngine
from app.schemas import QueryRequest


def run_benchmark():
    eval_dir = Path(__file__).resolve().parent
    golden_path = eval_dir / "golden_dataset.json"
    questions = json.loads(golden_path.read_text(encoding="utf-8"))

    engine = PharmaRAGEngine()

    detailed_results = []
    top1_hits = 0
    topk_hits = 0
    in_scope_count = 0
    abstention_correct = 0
    abstention_total = 0
    keyword_hits = []
    groundedness_scores = []
    latencies = []
    costs = []

    for item in questions:
        req = QueryRequest(question=item["question"], top_k=4, strict_grounding=True)
        resp = engine.answer_query(req)

        latencies.append(resp.telemetry.total_latency_ms)
        costs.append(resp.telemetry.estimated_cost_usd)
        groundedness_scores.append(resp.telemetry.groundedness_score)

        ans_lower = resp.answer.lower()
        kw_matched = sum(1 for kw in item["required_keywords"] if kw.lower() in ans_lower)
        kw_score = kw_matched / max(len(item["required_keywords"]), 1)
        keyword_hits.append(kw_score)

        if item["should_abstain"]:
            abstention_total += 1
            is_correct = resp.telemetry.abstained
            if is_correct:
                abstention_correct += 1
            hit_top1 = is_correct
            hit_topk = is_correct
        else:
            in_scope_count += 1
            retrieved_docs = [c.doc_id for c in resp.citations]
            hit_top1 = len(retrieved_docs) > 0 and retrieved_docs[0] == item["expected_doc_id"]
            hit_topk = item["expected_doc_id"] in retrieved_docs
            if hit_top1:
                top1_hits += 1
            if hit_topk:
                topk_hits += 1

        detailed_results.append({
            "id": item["id"],
            "question": item["question"],
            "expected_doc_id": item["expected_doc_id"],
            "top_retrieved_doc": resp.citations[0].doc_id if resp.citations else "NONE",
            "hit_top1": hit_top1,
            "hit_topk": hit_topk,
            "keyword_recall": round(kw_score, 3),
            "groundedness": resp.telemetry.groundedness_score,
            "abstained": resp.telemetry.abstained,
            "latency_ms": resp.telemetry.total_latency_ms,
            "cost_usd": resp.telemetry.estimated_cost_usd,
        })

    summary = {
        "total_questions": len(questions),
        "in_scope_questions": in_scope_count,
        "out_of_scope_questions": abstention_total,
        "top1_citation_accuracy": round(top1_hits / max(in_scope_count, 1), 4),
        "top4_citation_recall": round(topk_hits / max(in_scope_count, 1), 4),
        "factual_keyword_completeness": round(float(np.mean(keyword_hits)), 4),
        "mean_groundedness_score": round(float(np.mean(groundedness_scores)), 4),
        "out_of_scope_abstention_accuracy": round(abstention_correct / max(abstention_total, 1), 4),
        "overall_benchmark_accuracy": round(
            (top1_hits + abstention_correct) / len(questions), 4
        ),
        "p50_latency_ms": round(float(np.percentile(latencies, 50)), 2),
        "p95_latency_ms": round(float(np.percentile(latencies, 95)), 2),
        "mean_cost_per_query_usd": round(float(np.mean(costs)), 6),
    }

    output_payload = {"summary": summary, "results": detailed_results}
    (eval_dir / "eval_results.json").write_text(json.dumps(output_payload, indent=2), encoding="utf-8")

    # Generate Markdown report
    md_lines = [
        "# PharmaReg-RAG Evaluation Report (25-Question Golden Set)",
        "",
        "## Executive Summary Metrics",
        "",
        "| Metric | Value |",
        "| :--- | :--- |",
        f"| **Total Evaluation Questions** | {summary['total_questions']} ({summary['in_scope_questions']} regulatory + {summary['out_of_scope_questions']} adversarial out-of-scope) |",
        f"| **Overall Benchmark Accuracy** | **{summary['overall_benchmark_accuracy'] * 100:.1f}%** |",
        f"| **Top-1 Citation Accuracy (Precision@1)** | **{summary['top1_citation_accuracy'] * 100:.1f}%** |",
        f"| **Top-4 Citation Recall (Recall@4)** | **{summary['top4_citation_recall'] * 100:.1f}%** |",
        f"| **Factual Keyword Completeness** | **{summary['factual_keyword_completeness'] * 100:.1f}%** |",
        f"| **Mean Groundedness Score** | **{summary['mean_groundedness_score'] * 100:.1f}%** |",
        f"| **Out-of-Scope Abstention Accuracy** | **{summary['out_of_scope_abstention_accuracy'] * 100:.1f}%** |",
        f"| **Latency (p50 / p95)** | **{summary['p50_latency_ms']} ms / {summary['p95_latency_ms']} ms** |",
        f"| **Mean Estimated Token Cost / Query** | **${summary['mean_cost_per_query_usd']:.6f}** |",
        "",
        "## Per-Question Breakdown",
        "",
        "| ID | Expected Doc | Top-1 Retrieved | Top-1 Hit | Keyword Recall | Groundedness | Latency (ms) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in detailed_results:
        md_lines.append(
            f"| {r['id']} | `{r['expected_doc_id']}` | `{r['top_retrieved_doc']}` | "
            f"{'PASS' if r['hit_top1'] else 'FAIL'} | {r['keyword_recall']*100:.0f}% | "
            f"{r['groundedness']*100:.0f}% | {r['latency_ms']:.2f} |"
        )

    (eval_dir / "eval_report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run_benchmark()
