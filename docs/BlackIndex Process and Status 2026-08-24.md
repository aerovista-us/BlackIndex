# BlackIndex Process and Status — 2026-08-24

## What BlackIndex is building

BlackIndex is a documents-first declassified-record research system designed to preserve raw evidence, provenance, competing assertions, archival gaps, redactions, record custody, official interpretations, independent analysis, and reusable operational lessons.

The project began from a simple concern: surviving government records are useful but incomplete. Actors may avoid documenting sensitive activity; records may be compartmented, destroyed, withheld, misfiled, or never created. That limitation matters, but it cannot be used to invent evidence. BlackIndex therefore maps both **what survives** and **the integrity/history of the surviving record**.

The consolidated posture is:

> **BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations. Conclusions remain provisional and may remain unresolved indefinitely.**

This does not remove motive/capability/opportunity analysis, evidence scoring, anomaly analysis, redaction analysis, or candidate mechanism detection. It makes those tools descriptive rather than verdict-producing.

---

# Current technical process

## 1. Source discovery

Identify the most authoritative available landing page and artifact URL, preferably Senate, FBI, CIA, NSA, NARA, National Security Archive, or another primary archival source.

Record the distinction between:

- underlying primary artifact
- official archive/agency description
- later official interpretation
- independent analysis

## 2. Acquisition

`tools/ingest-url.sh` downloads the artifact using archive-compatible request handling and refuses to ingest an HTML landing/error page as a PDF.

## 3. Immutable raw vault

Raw files are stored locally under:

`source-vault/raw/<source>/<collection>/`

Raw artifacts are never overwritten.

## 4. Provenance/hash gate

Each artifact receives SHA-256, source/artifact URLs, retrieval time, original filename, size, and local path.

The verifier recomputes hashes and fails if source or normalized derivatives have changed unexpectedly.

## 5. Normalization

PDF text is normalized with `pdftotext` when a usable text layer exists.

Normalized derivatives live under `normalized/text/` and never replace the source artifact.

## 6. Metadata

Durable metadata lives under `metadata/` and is publishable to GitHub. The metadata schema now supports:

- archive provenance / chain of custody
- creator/custodian/declassification/withholding authorities
- classification/release chronology
- alternate versions/version relationships
- source dependencies
- missing evidence / destruction chronology
- public/internal contradictions
- redaction counts/density/clusters
- record-integrity fields
- State of Record / Evidence Density / Archive Confidence diagnostics

The schema remains backward compatible with already-ingested records.

## 7. Extraction/review

New reviews use:

`CLAIM → DOCUMENT CONTENT → SOURCE ATTRIBUTION → CORROBORATION → CONFLICTS → GAPS → ALTERNATIVE EXPLANATIONS → UNRESOLVED QUESTIONS → SOURCE`

The old `PROVES / DOES NOT PROVE` framing is retired for ongoing methodology.

## 8. Record Integrity review

BlackIndex separately maps:

- completeness
- redaction concern
- destruction
- missing referenced records
- custodian conflicts
- version conflicts
- public/internal contradictions
- archive confidence

This is now a first-class research object rather than a side note.

## 9. Cross-document synthesis

Reviewed records are compared for recurring mechanisms and contradictions. Similarity does not establish common provenance or common command structure.

## 10. Promotion

Reusable patterns, controls, detections, training scenarios, and playbooks can be promoted when sufficiently grounded across records.

Promotion means the mechanism is useful and recurring. It does not establish a final verdict about every historical allegation associated with it.

---

# Current scoring posture

## Plausibility `0–15`

- Motive
- Capability
- Opportunity

This measures practical possibility only.

## Evidence Density `0–30`

Measures amount, directness, diversity, independence, and quality of collected material.

Conflicting evidence is not collapsed into a net winner; it is stored separately.

## Obstruction / Anomaly `0–20`

Tracks irregularities, contradictions, evasion/non-cooperation, and demonstrable misleading/concealment behavior.

## Archive Confidence `0–5`

Measures completeness/reconstructability of the accessible archive.

## State of Record

- `R0` minimal material
- `R1` preliminary
- `R2` multiple relevant sources
- `R3` substantial corroborating/conflicting material
- `R4` extensive multi-source record
- `R5` mature accessible record

These are maturity states, not truth labels.

---

# Negative-investigation findings

Statements such as `investigators found no evidence` are now stored as claims made by that investigator/institution.

BlackIndex records:

- investigator/institution
- controlling employer/institution
- independence/conflicts
- scope/authority/access
- evidence reviewed
- missing/excluded/not-sought material
- resources/duration
- interviews/omissions
- workpaper survival
- competing findings
- reproducibility
- exact wording

`No evidence found`, `unable to substantiate`, and `no credible evidence` remain distinct statements.

---

# Corpus progress so far

BlackIndex has now exercised the pipeline across these collections/records:

## Initial reviewed foundation

- Church Committee Book II
- Operation Northwoods
- COINTELPRO New Left — Alexandria
- CIA Family Jewels

## Expanded Phase 2

- VENONA — *The Venona Story*
- Pentagon Papers — NARA index/corpus map
- Iran-Contra — Diversion Memo
- Iran-Contra — Fallback Plan original/altered versions

## P0 core next set

- MKULTRA — 1977 Senate joint hearing
- MINARET — NSA watch-list testimony
- SHAMROCK — NSA/Allen-Abzug correspondence
- TPAJAX — 1953 finance/implementation record
- PBSUCCESS — 1954 Stage Two political/psychological planning record

The latest batch reached and published its final record:

`CIA-1954-pbsuccess-001`

Because the batch runner uses `set -e` and PBSUCCESS is the final item, reaching and publishing that record indicates the earlier items in that batch completed their preceding pipeline steps without an unhandled fatal error.

A final NXCore verify count should still be treated as the authoritative local corpus count.

---

# Major research mechanisms already identified

These are analytical mechanisms, not final historical judgments:

- purpose drift / objective-first justification
- collection/resource-to-consequence chain
- fragmented oversight / incomplete-chain review
- internal awareness without timely accountability
- analytic reconstruction provenance
- cross-program resource diversion
- record substitution under controlled custody
- archive destruction suppressing later accountability
- selector-layer policy bypass
- third-party access normalization
- financial administration as operational provenance
- objective-first influence architecture

Each can support controls/detections/training without requiring BlackIndex to declare a disputed historical hypothesis true or false.

---

# New first-class concepts integrated at this checkpoint

1. Raw artifact vs official interpretation vs independent analysis
2. `MISSING_EVIDENCE`
3. Chain of custody/provenance
4. Redaction fields integrated into ingestion metadata
5. Redaction clustering
6. Automatic/required version comparison where versions exist
7. Public statement vs internal record mapping
8. Timeline evolution of official conclusions
9. Source-independence/dependency tracking
10. Inference-dependency levels
11. Alternative explanations
12. Unresolved-question queue
13. Archive-selection bias
14. Record creator/custodian/declassification/withholding authority
15. Destruction chronology
16. Classification/release chronology
17. Confidence at assertion/source level
18. Investigator reliability diagnostics
19. Record Integrity as a first-class research object
20. State-of-Record maturity codes instead of final assessment classes

---

# Backlog additions captured

The backlog now explicitly includes:

- Atkinson / 2019 impeachment-related declassified material
- recently declassified domestic-terrorism Strategic Implementation Plan
- Amelia Earhart files as a lower-priority exploratory collection

The existing 9/11, assassination, intelligence/political, covert action, surveillance, detention/interrogation, continuity-government, scientific/unusual-program, and foreign-policy clusters remain intact.

---

# Next technical/methodology work

1. Migrate older reviewed extraction files away from legacy `PROVES / DOES NOT PROVE` or `A–E` verdict labels during substantive re-review; do not silently rewrite historical notes without review.
2. Update the CLI-generated extraction stub to point to/use `extractions/REVIEW_TEMPLATE.md`.
3. Add structured `MISSING_EVIDENCE` and Record Integrity objects to the local index/search layer.
4. Add version-comparison tooling for same-document releases.
5. Add source-dependency graphs so derivative corroboration is visible.
6. Add public/internal-statement comparison objects.
7. Add investigator-report objects and negative-finding diagnostics.
8. Continue ingestion with Gulf of Tonkin, MHCHAOS, deeper TPAJAX/PBSUCCESS, MKSEARCH/OFTEN/CHICKWIT, and then the 9/11 cluster.

---

# Preservation rule

Nothing in this consolidation removes the original BlackIndex goal or capability.

BlackIndex still asks:

- Who had motive?
- Who had capability?
- Who had opportunity?
- What does the surviving record contain?
- What corroborates it independently?
- What conflicts with it?
- What is missing?
- Who controlled the records?
- What was destroyed/redacted/withheld?
- Did public and internal accounts differ?
- Did official conclusions change?
- What innocent/ordinary explanations exist?
- What would we need to find next?

The difference is that BlackIndex now preserves those answers without prematurely converting them into permanent historical verdicts.
