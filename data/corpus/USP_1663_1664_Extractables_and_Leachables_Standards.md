# DOC_ID: USP-1663-1664
# TITLE: USP <1663> Assessment of Extractables and USP <1664> Assessment of Drug Product Leachables
# SOURCE: United States Pharmacopeia (USP) General Chapters <1663> and <1664>

## Section 1: Definitions of Extractables versus Leachables
- **Extractables (USP <1663>)**: Organic and inorganic chemical entities that can be released from a pharmaceutical packaging/delivery system, packaging component, or manufacturing surface using laboratory extraction solvents and exaggerated conditions (elevated temperature, surface-to-volume ratio, and extraction duration) designed to be at least as aggressive as the drug product formulation.
- **Leachables (USP <1664>)**: Organic and inorganic chemical entities that are present in a packaged drug product because they have migrated from a packaging/delivery system or component into the drug formulation under normal conditions of storage and use over the product's shelf life. Leachables are typically a subset of extractables, or reaction/degradation products formed between drug formulation components and packaging extractables.

## Section 2: Safety Thresholds and Analytical Evaluation Threshold (AET)
The Product Quality Research Institute (PQRI) and USP <1664> define toxicological thresholds for Parenteral and Ophthalmic Drug Products (PODP):
- **Safety Concern Threshold (SCT)**: **1.5 micrograms/day (µg/day)** of an individual organic leachable. Below 1.5 µg/day, leachables generally present negligible risk of carcinogenicity or genotoxicity and do not require formal compound-specific toxicological qualification unless they belong to the "Cohort of Concern" (such as N-nitrosamines, polynuclear aromatic hydrocarbons [PAHs], or 2-mercaptobenzothiazole [2-MBT]).
- **Qualification Threshold (QT)**: **5.0 micrograms/day (µg/day)** for a non-genotoxic organic leachable. Any leachable exceeding 5.0 µg/day requires toxicological risk assessment based on Permitted Daily Exposure (PDE).

### Calculating the Analytical Evaluation Threshold (AET)
The Analytical Evaluation Threshold (AET) translates the dose-based SCT (in µg/day) into a concentration threshold (e.g., µg/mL) that analytical instruments must be able to detect and identify:
`AET (µg/mL) = (SCT [1.5 µg/day] / (Maximum Daily Dose [mL/day])) / Uncertainty Factor (UF)`

Where the **Uncertainty Factor (UF)** accounts for analytical response factor variability across chromatographic detectors (typically UF = 2.0 for GC-MS and LC-UV/MS when using an internal standard response factor). For example, if a parenteral drug has a maximum daily dose of 3.0 mL/day and a UF of 2.0 is applied, the final AET is `(1.5 / 3.0) / 2.0 = 0.25 µg/mL`.

## Section 3: Required Analytical Techniques for E&L Profiling
A comprehensive E&L screening protocol requires orthogonal analytical methods covering all volatility and polarity ranges:
1. **Volatile Organic Compounds (VOCs)**: Headspace Gas Chromatography coupled with Mass Spectrometry (HS-GC/MS) — targets residual solvents, monomer residues, and butylated hydroxytoluene (BHT) degradation fragments.
2. **Semi-Volatile Organic Compounds (SVOCs)**: Direct-injection GC/MS — targets vulcanization accelerators, plasticizers (such as phthalates), and antioxidants (e.g., Irganox 1010, Irgafos 168).
3. **Non-Volatile Organic Compounds (NVOCs)**: Ultra-High-Performance Liquid Chromatography coupled with Photodiode Array and High-Resolution Mass Spectrometry (UHPLC-PDA-HRMS / Q-TOF or Orbitrap) — targets large oligomers, curing agents, and halobutyl oligomers from elastomeric stoppers.
4. **Elemental Impurities (Inorganic Extractables/Leachables)**: Inductively Coupled Plasma Mass Spectrometry (ICP-MS) or ICP-OES in accordance with **ICH Q3D** and **USP <232>/<233>**, screening for catalytic metals (Pb, Cd, As, Hg, Co, V, Ni) and glass delamination elements (Si, B, Al, Na, Ba, Zn from zinc-cured elastomers).
