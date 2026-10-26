# DOC_ID: FDA-Q9-ANNEX1-2023
# TITLE: ICH Q9(R1) Quality Risk Management & EU GMP Annex 1 (2023): Contamination Control Strategy for Sterile Medicinal Products
# SOURCE: FDA / ICH Q9(R1) (May 2023) & EudraLex Volume 4 Annex 1 (August 2023)

## Section 1: Contamination Control Strategy (CCS) in Sterile Fill-Finish Operations
The revised **EU GMP Annex 1 (effective August 25, 2023)** and **FDA sterile manufacturing guidance** mandate a documented, holistic **Contamination Control Strategy (CCS)** across the entire sterile fill-finish facility. Primary packaging components—specifically ready-to-sterilize (RTS) and ready-to-use (RTU) vials, elastomeric stoppers, and prefilled syringe tubs—play a critical role in the facility CCS:
- **Grade A / ISO 5 Aseptic Core**: Filling and stoppering of sterile parenterals must take place within a Grade A laminar airflow environment (typically inside a Restricted Access Barrier System [RABS] or closed Isolator).
- **Endotoxin and Bioburden Reduction (Depyrogenation and Sterilization)**:
  - **Glass Vials**: Washed with Water for Injection (WFI) and depyrogenated via dry-heat tunnel to achieve at least a **3-log (99.9%) reduction in bacterial endotoxins** (USP <1228.1>), with residual endotoxin levels typically **< 0.001 EU/mL** or **< 0.25 EU/unit**.
  - **Elastomeric Stoppers and Plungers**: Washed with WFI to achieve a validated **3-log endotoxin reduction**, followed by moist-heat steam sterilization (autoclaving at **121.1°C for >= 15–30 minutes**) to achieve a **Sterility Assurance Level (SAL) of 10^-6** (at least a 6-log reduction of *Geobacillus stearothermophilus* biological indicators).

## Section 2: Sub-Visible and Visible Particulate Matter Control (USP <788>, <789>, <790>)
Sterile injectable drug products and their primary packaging components must strictly control particulate contamination:
- **Visible Particulates (USP <790>)**: 100% of filled parenteral units must undergo manual, semi-automated, or automated visual inspection so the lot is "essentially free" of visible particulates (> 100–150 µm), evaluated against an Acceptable Quality Limit (**AQL <= 0.65%** for major defects and **AQL = 0%** for critical defects affecting container integrity).
- **Sub-Visible Particulates in General Parenterals (USP <788>, Light Obscuration Method 1)**:
  - **Small-Volume Parenterals (SVP, nominal volume <= 100 mL)**: Maximum **6,000 particles per container >= 10 µm** and **600 particles per container >= 25 µm**.
  - **Large-Volume Parenterals (LVP, nominal volume > 100 mL)**: Maximum **25 particles per mL >= 10 µm** and **3 particles per mL >= 25 µm**.
- **Ophthalmic Intraocular Solutions (USP <789>)**: Much stricter limits apply: maximum **50 particles per mL >= 10 µm**, **5 particles per mL >= 25 µm**, and **2 particles per mL >= 50 µm**.

## Section 3: ICH Q9(R1) Quality Risk Management Applied to AI/Data Systems in GMP
Under **ICH Q9(R1)** and **FDA 21 CFR Part 11 / Computer Software Assurance (CSA)**, when deploying AI-assisted decision support or document retrieval systems in a GxP pharmaceutical environment:
1. **Formality Based on Risk to Patient Safety**: Systems that generate regulatory intelligence or retrieve SOP/guidance specifications are classified as GxP decision-support tools requiring **traceable source citations**, **deterministic audit trails**, and **human-in-the-loop (HITL) verification**.
2. **Hallucination and Groundedness Controls**: AI assistants must enforce strict abstention when a query cannot be answered from approved controlled documents, logging retrieval confidence scores, chunk citations, latency, and model version metadata for quality assurance review.
