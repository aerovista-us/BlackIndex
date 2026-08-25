# BlackIndex Evidence Map Methodology

## Core rule

BlackIndex is an evidence map, not a verdict machine.

> **BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations. Conclusions remain provisional and may remain unresolved indefinitely.**

This preserves the original BlackIndex design: motive, capability, opportunity, evidence, unusual behavior, redactions, missing records, contradictions, and institutional incentives all remain important. The change is that none of those dimensions is allowed to silently become a final historical judgment.

## First-class research objects

BlackIndex maintains five core objects:

1. **Document** — a discrete archival artifact or release unit.
2. **Claim / Assertion** — an attributed statement made by a source, witness, investigator, agency, committee, analyst, journalist, historian, or other actor.
3. **Person / Organization** — actors, custodians, investigators, witnesses, agencies, contractors, courts, committees, and other entities.
4. **Event** — an action, meeting, decision, operation, disclosure, investigation, destruction event, declassification, or other occurrence.
5. **Record Integrity** — creation, custody, classification, withholding, destruction, reproduction, alteration, missing material, release history, and version conflicts.

## Evidence layers

Government interpretation must not be merged with the underlying artifact. Preserve separately:

- `primary_document`
- `official_interpretation`
- `independent_analysis`

An official conclusion is itself an attributed claim in the record.

## Required passage structure

Retire `PROVES`, `DOES NOT PROVE`, `Confirmed`, and equivalent verdict language from ongoing extraction work.

For every pivotal passage use:

### CLAIM
What assertion, allegation, proposal, observation, conclusion, or question is being evaluated?

### DOCUMENT CONTENT
Neutral description of what is actually present in the record.

### SOURCE ATTRIBUTION
Who is asserting it? Preserve role, institution, date, and whether the statement is firsthand, analytical, testimonial, retrospective, anonymous, or derivative.

### CORROBORATION
Other material supporting the same assertion. Mark whether corroboration is genuinely independent or derives from the same underlying source.

### CONFLICTS
Material inconsistent with, qualifying, disputing, or materially complicating the assertion.

### GAPS
Material absent, unavailable, destroyed, withheld, redacted, never requested, or otherwise missing from the evidentiary chain.

### ALTERNATIVE EXPLANATIONS
For anomalies, preserve the strongest reasonable mundane, procedural, innocent, or competing explanation alongside the concerning interpretation.

### UNRESOLVED QUESTIONS
What records, testimony, versions, technical evidence, or provenance would materially improve understanding?

### SOURCE
Primary-document citation, page/exhibit/message number, archive identifier, URL, and checksum as appropriate. Exact quotation and page citation are required for pivotal assertions that materially affect scoring, candidate patterns, contradictions, or record-integrity findings.

## Negative findings

A statement such as `investigators found no evidence of X` must be stored as an attributed negative finding, not converted into `there is no evidence of X`.

Capture:

- who made the finding
- employer/controlling institution
- investigator independence
- institutional interests/conflicts
- scope and authority
- evidence actually reviewed
- records unavailable/excluded/destroyed/not sought
- duration/resources
- interviews and omitted witnesses where known
- whether workpapers survive
- competing investigations/results
- reproducibility
- exact wording

`No evidence found`, `no credible evidence`, `unable to substantiate`, and `insufficient evidence` are not interchangeable.

## Investigator diagnostics

Where information permits, score `0–5`:

- `investigator_independence`
- `access_to_evidence`
- `method_transparency`
- `reproducibility`
- `conflict_exposure`

A low score does not mean an investigator lied. It means BlackIndex has limited grounds for independently relying on the conclusion.

## Research-state diagnostics

### Plausibility — 0–15
Retain:
- Motive `0–5`
- Capability `0–5`
- Opportunity `0–5`

This measures practical possibility, not involvement.

### Evidence Density — 0–30
Retain the original evidence dimensions but interpret the score as the amount, diversity, directness, and quality of relevant material collected — not a verdict.

### Obstruction / Anomaly — 0–20
Retain:
- record irregularities
- contradictory accounts
- evasion/non-cooperation
- misleading/concealment behavior

Evidence of concealment is evidence of concealment, not automatic proof of the underlying allegation.

### Archive Confidence — 0–5
Measures completeness and reconstructability of the accessible archive.

### Source Confidence
Belongs to each assertion/source, not an entire investigation. Consider firsthand vs hearsay, contemporaneous vs retrospective, independent vs derivative, access, conflicts, consistency, corroboration, and provenance.

### Inference Dependency
- `D0` directly stated/observable
- `D1` one modest inference
- `D2` multiple linked inferences
- `D3` depends on unresolved assumptions
- `D4` highly assumption-dependent/speculative

## State of Record

Replace final assessment classes with maturity codes:

| Code | State of Record |
|---|---|
| `R0` | Minimal material collected |
| `R1` | Preliminary record |
| `R2` | Multiple relevant sources |
| `R3` | Substantial corroborating and conflicting material |
| `R4` | Extensive multi-source record |
| `R5` | Mature record; major accessible sources reviewed |

`R5` means mature coverage, not historical certainty.

Legacy A/B/C/D/E/X labels are historical scoring snapshots only and must not be treated as permanent BlackIndex determinations.

## Record Integrity

For each investigation or document family preserve:

- `completeness` `0–5`
- `redaction_concern` `0–15`
- `known_destruction`
- `missing_referenced_records`
- `custodian_conflicts`
- `version_conflicts`
- `public_internal_contradictions`
- `archive_confidence` `0–5`
- `record_creator`
- `record_custodian`
- `declassification_authority`
- `withholding_authority`
- `artifact_type`
- `chain_of_custody`
- `document_integrity`
- `alternate_versions`

A custodian conflict is relevant when a potentially implicated person/institution also controls retention, withholding, destruction, or release. It is not itself evidence of wrongdoing.

## Missing evidence

`MISSING_EVIDENCE` is a first-class category. Track missing attachments, destroyed files, absent meeting minutes, missing tapes/logs, referenced documents not found, unavailable source material underlying later reports, classified/withheld items, unexplained archive gaps, and records expected to exist but not located.

For each item record how its prior existence is known, likely creator/custodian, last known location/date, destruction/withholding evidence, stated reason, likely relevance, alternative explanation for absence, and recovery path.

## Destruction chronology

Where destruction is documented capture who ordered it, who executed it, date, stated reason, retention rules, whether investigation/litigation/FOIA/congressional review was pending or foreseeable, what is known about destroyed contents, and whether duplicates or derivative records later surfaced.

## Classification/release chronology

Track:

`created → classified → review/extensions → exemptions → partial release → later release → less-redacted/full release`

Long withholding may be analytically interesting but is not inherently evidence of wrongdoing.

## Redaction integration

The Redaction Analysis Framework remains authoritative. Intake should also track:

- `redaction_count`
- `redaction_density`
- `critical_redactions`
- `redaction_impact`
- `exemption_codes`
- `alternate_versions`
- `redaction_clusters`

Clusters may form around a person, date, meeting, authorization, source, operation, financial link, target, or disputed event. Clustering identifies research priority, not guilt.

## Version comparison

Multiple releases of the same document should be linked and compared for changed wording, visible names/agencies, changed exemptions, removed/added redactions, missing/additional pages, changed classification markings, restored attachments, and metadata changes.

## Public vs internal record

Maintain explicit pairs where useful:

- contemporaneous public statement
- contemporaneous internal record
- later official interpretation
- later independent analysis

Differences are recorded and contextualized; they are not automatically characterized as deception.

## Timeline of official conclusions

Do not flatten multiple official assessments into one conclusion. Preserve chronology:

`initial lead → interim assessment → report/commission → follow-on investigation → later declassification → revised official statement`

Each stage must be linked to what evidence was available at that time.

## Archive-selection bias

Surviving records are a selected sample. Documents may never have been created, may have been verbal, compartmented, routinely or intentionally destroyed, lost, withheld, misfiled, or never transferred. Actors engaged in improper conduct may also avoid documentation.

This lowers confidence in completeness. It does not authorize BlackIndex to invent missing evidence.

## Workflow

`discovery → canonical acquisition → immutable raw vault → checksum → normalization → provenance metadata → assertion extraction → record-integrity review → cross-document analysis → provisional pattern/control/detection promotion`

Raw artifacts and normalized derivatives remain separate. Promotions describe reusable mechanisms; they do not convert disputed historical allegations into final truth claims.

## Current checkpoint

BlackIndex has demonstrated this full lifecycle across Church Committee, Northwoods, COINTELPRO, Family Jewels, VENONA, Pentagon Papers, Iran-Contra, MKULTRA, MINARET, SHAMROCK, TPAJAX, and PBSUCCESS. The latest P0 batch completed through `CIA-1954-pbsuccess-001` using the one-shot ingestion/publish pipeline.

The project has already identified recurring research mechanisms involving purpose drift, collection/resource-to-consequence chains, fragmented oversight, archival destruction, selector-layer policy bypass, third-party access normalization, financial provenance, record substitution, analytic reconstruction, and objective-first influence architecture. These remain research mechanisms and hypotheses, not final judgments.

## Hard rules

1. No source receives automatic truth status because it is governmental, congressional, journalistic, academic, classified, declassified, anonymous, or oppositional.
2. No negative finding becomes an absence-of-evidence fact without preserving scope, access, conflicts, wording, and reproducibility.
3. No redaction becomes evidence of underlying wrongdoing solely because it exists.
4. No missing record becomes proof of what it would have contained.
5. Proposal, approval, funding, implementation, execution, and outcome remain separate states.
6. Repetition does not equal independent corroboration.
7. Primary artifacts, official interpretations, and independent analyses remain distinguishable.
8. Conflicting assertions may coexist indefinitely.
9. All judgments remain provisional and some investigations may remain unresolved forever.
10. BlackIndex optimizes for an inspectable evidence map with preserved provenance and uncertainty.
