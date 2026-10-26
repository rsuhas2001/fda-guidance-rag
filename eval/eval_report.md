# PharmaReg-RAG Evaluation Report (25-Question Golden Set)

## Executive Summary Metrics

| Metric | Value |
| :--- | :--- |
| **Total Evaluation Questions** | 40 (32 regulatory + 8 adversarial out-of-scope) |
| **Overall Benchmark Accuracy** | **100.0%** |
| **Top-1 Citation Accuracy (Precision@1)** | **100.0%** |
| **Top-4 Citation Recall (Recall@4)** | **100.0%** |
| **Factual Keyword Completeness** | **95.6%** |
| **Mean Groundedness Score** | **98.8%** |
| **Out-of-Scope Abstention Accuracy** | **100.0%** |
| **Latency (p50 / p95)** | **1.54 ms / 2.29 ms** |
| **Mean Estimated Token Cost / Query** | **$0.000148** |

## Per-Question Breakdown

| ID | Expected Doc | Top-1 Retrieved | Top-1 Hit | Keyword Recall | Groundedness | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Q01 | `FDA-CCS-1999` | `FDA-CCS-1999` | PASS | 75% | 100% | 2.58 |
| Q02 | `FDA-CCS-1999` | `FDA-CCS-1999` | PASS | 100% | 100% | 1.50 |
| Q03 | `FDA-CCS-1999` | `FDA-CCS-1999` | PASS | 100% | 100% | 1.54 |
| Q04 | `FDA-EL-PODP` | `FDA-EL-PODP` | PASS | 100% | 100% | 1.45 |
| Q05 | `FDA-EL-PODP` | `FDA-EL-PODP` | PASS | 100% | 99% | 1.55 |
| Q06 | `FDA-EL-PODP` | `FDA-EL-PODP` | PASS | 100% | 100% | 1.25 |
| Q07 | `FDA-CCIT-2008` | `FDA-CCIT-2008` | PASS | 100% | 99% | 1.57 |
| Q08 | `FDA-CCIT-2008` | `FDA-CCIT-2008` | PASS | 100% | 98% | 1.29 |
| Q09 | `FDA-CCIT-2008` | `FDA-CCIT-2008` | PASS | 100% | 99% | 2.28 |
| Q10 | `FDA-PFS-2024` | `FDA-PFS-2024` | PASS | 100% | 100% | 2.27 |
| Q11 | `FDA-PFS-2024` | `FDA-PFS-2024` | PASS | 100% | 99% | 1.75 |
| Q12 | `FDA-PFS-2024` | `FDA-PFS-2024` | PASS | 100% | 100% | 1.28 |
| Q13 | `FDA-ELASTOMERS-CMC` | `FDA-ELASTOMERS-CMC` | PASS | 100% | 99% | 1.39 |
| Q14 | `FDA-ELASTOMERS-CMC` | `FDA-ELASTOMERS-CMC` | PASS | 100% | 97% | 1.36 |
| Q15 | `FDA-ELASTOMERS-CMC` | `FDA-ELASTOMERS-CMC` | PASS | 75% | 93% | 1.81 |
| Q16 | `FDA-ELASTOMERS-CMC` | `FDA-ELASTOMERS-CMC` | PASS | 100% | 99% | 1.66 |
| Q17 | `FDA-Q9-ANNEX1-2023` | `FDA-Q9-ANNEX1-2023` | PASS | 75% | 100% | 1.38 |
| Q18 | `FDA-Q9-ANNEX1-2023` | `FDA-Q9-ANNEX1-2023` | PASS | 100% | 89% | 1.43 |
| Q19 | `FDA-Q9-ANNEX1-2023` | `FDA-Q9-ANNEX1-2023` | PASS | 100% | 96% | 1.54 |
| Q20 | `FDA-PFS-2024` | `FDA-PFS-2024` | PASS | 100% | 100% | 1.63 |
| Q21 | `FDA-EL-PODP` | `FDA-EL-PODP` | PASS | 100% | 98% | 1.39 |
| Q22 | `CFR-201-LABELING` | `CFR-201-LABELING` | PASS | 100% | 100% | 1.86 |
| Q23 | `CFR-201-LABELING` | `CFR-201-LABELING` | PASS | 100% | 100% | 1.65 |
| Q24 | `CFR-211-CGMP` | `CFR-211-CGMP` | PASS | 100% | 100% | 1.65 |
| Q25 | `CFR-211-CGMP` | `CFR-211-CGMP` | PASS | 100% | 99% | 1.73 |
| Q26 | `CFR-11-ERECORDS` | `CFR-11-ERECORDS` | PASS | 50% | 100% | 1.89 |
| Q27 | `CFR-11-ERECORDS` | `CFR-11-ERECORDS` | PASS | 100% | 100% | 1.57 |
| Q28 | `ICH-Q1A-STABILITY` | `ICH-Q1A-STABILITY` | PASS | 100% | 94% | 1.79 |
| Q29 | `ICH-Q1A-STABILITY` | `ICH-Q1A-STABILITY` | PASS | 75% | 97% | 1.32 |
| Q30 | `FDA-ASEPTIC-2004` | `FDA-ASEPTIC-2004` | PASS | 75% | 98% | 2.72 |
| Q31 | `FDA-OOS-2006` | `FDA-OOS-2006` | PASS | 100% | 100% | 1.76 |
| Q32 | `CFR-7-RECALLS-FAR` | `CFR-7-RECALLS-FAR` | PASS | 100% | 99% | 1.61 |
| Q33 | `NONE` | `FDA-Q9-ANNEX1-2023` | PASS | 100% | 100% | 0.97 |
| Q34 | `NONE` | `NONE` | PASS | 100% | 100% | 0.76 |
| Q35 | `NONE` | `ICH-Q1A-STABILITY` | PASS | 100% | 100% | 0.79 |
| Q36 | `NONE` | `FDA-CCS-1999` | PASS | 100% | 100% | 0.79 |
| Q37 | `NONE` | `FDA-CCS-1999` | PASS | 100% | 100% | 0.97 |
| Q38 | `NONE` | `FDA-ELASTOMERS-CMC` | PASS | 100% | 100% | 0.85 |
| Q39 | `NONE` | `CFR-11-ERECORDS` | PASS | 100% | 100% | 0.80 |
| Q40 | `NONE` | `FDA-ELASTOMERS-CMC` | PASS | 100% | 100% | 1.03 |
