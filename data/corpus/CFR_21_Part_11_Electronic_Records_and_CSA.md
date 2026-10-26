# DOC_ID: CFR-11-ERECORDS
# TITLE: 21 CFR Part 11 — Electronic Records, Electronic Signatures, and FDA Computer Software Assurance (CSA)
# SOURCE: U.S. Food and Drug Administration, 21 CFR Part 11 & Draft Guidance on Computer Software Assurance

## Section 1: Scope and ALCOA+ Data Integrity Principles
21 CFR Part 11 governs electronic records and electronic signatures created, modified, maintained, archived, retrieved, or transmitted under any FDA predicate rule (such as 21 CFR Part 211 or Part 820). All GxP electronic data must satisfy **ALCOA+** data integrity principles: **Attributable, Legible, Contemporaneous, Original, and Accurate** (+ Complete, Consistent, Enduring, and Available).

## Section 2: Closed System Technical Controls (21 CFR 11.10)
Persons who use closed systems to create, modify, maintain, or transmit electronic records must employ procedures and controls designed to ensure authenticity, integrity, and confidentiality:
1. **System Validation (21 CFR 11.10(a))**: Validation of systems to ensure accuracy, reliability, consistent intended performance, and the ability to discern invalid or altered records.
2. **Secure, Computer-Generated, Time-Stamped Audit Trails (21 CFR 11.10(e))**: Independently record the date and time of operator entries and actions that create, modify, or delete electronic records. Record changes shall **not obscure previously recorded information**, and audit trail documentation must be retained for a period at least as long as that required for the subject electronic records.
3. **Authority and Operational System Checks (21 CFR 11.10(f)-(g))**: Enforce permitted sequencing of steps and verify that only authorized individuals can sign electronic records, access the system, or alter a record.

## Section 3: Electronic Signature Manifestations (21 CFR 11.50 & 11.200)
Signed electronic records must clearly display:
- The **printed name** of the signer;
- The **date and time** when the signature was executed; and
- The **meaning** (such as review, approval, responsibility, or authorship) associated with the signature.
Non-biometric electronic signatures must employ at least **two distinct identification components** (such as an identification code/username and a secret password) during initial sign-on, and require password entry for each subsequent signing execution within a continuous session.
