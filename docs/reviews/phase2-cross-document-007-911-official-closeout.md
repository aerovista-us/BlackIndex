# Phase 2 Cross-Document Review 007 — 9/11 Official-Layer Closeout

## Status

`PREPARED — acquisition/review gate`

This review closes the currently defined official-interpretation layer around the existing Operation Encore corpus before BlackIndex opens a new major research cluster.

It does not render a final historical conclusion.

## Source set

### Already present

- `US CONGRESS-2002-9-11-joint-inquiry-001`
  - Joint Inquiry into Intelligence Community Activities Before and After the Terrorist Attacks of September 11, 2001 — declassified final report
  - early congressional inquiry / official interpretation layer
  - substantive review still pending

### Controlled closeout sprint

Prepared in:

`tools/ingest-phase2-911-official-closeout.sh`

1. **9/11 Commission Final Report — official U.S. Government edition**
   - GovInfo / GPO
   - final Commission report
   - includes Chapter 7 treatment of the California support network

2. **Monograph on Terrorist Financing — Staff Report to the Commission**
   - GovInfo-preserved government publication
   - staff analytical layer
   - not interchangeable with underlying bank/FBI/intelligence records

3. **9/11 and Terrorist Travel — Staff Report**
   - GovInfo-preserved government publication
   - staff analytical layer
   - the monograph itself states that Commissioners had not approved the text and that it did not necessarily reflect their views

4. **CIA OIG Report on CIA Accountability With Respect to the 9/11 Attacks**
   - CIA Office of Inspector General
   - official retrospective/accountability review
   - explicitly reviews CIA-related Joint Inquiry findings and conclusions

### Existing later investigative layer

- 2016 Operation Encore Electronic Communication
- EO 14040 §2(b)(i) Part 1
- EO 14040 §2(b)(i) Part 2
- EO 14040 §2(c) Part 1
- later rereview / closing-assessment lineage already encoded in part

## Source-class discipline

These sources must remain distinct:

| Layer | What it can establish directly |
|---|---|
| Joint Inquiry | what the congressional inquiry reported, reviewed, requested, and concluded at that time |
| Commission staff monograph | what Commission staff reported/analysed; not automatically Commissioner-approved findings |
| Commission final report | what the Commission formally published in its adopted final report |
| CIA OIG | what the CIA Inspector General review reported about CIA performance/accountability |
| FBI / Operation Encore | what the later FBI investigative record reported and how its assessment evolved |
| Underlying FD-302 / serial / financial / telecom / liaison record | the underlying recorded interview, transaction, communication, or investigative event itself |

Repeated statements across these layers are not independent corroboration when they derive from the same underlying record.

## Required comparison topics

### 1. Hazmi and Mihdhar — California arrival / early support

Capture separately:

- established chronology;
- source for chronology;
- assistance described;
- actor knowledge described or inferred;
- confidence language;
- later changes in assessment.

### 2. Omar al-Bayoumi

For every important statement record:

- exact wording;
- source layer;
- underlying source if identifiable;
- whether the statement is fact, witness report, investigator assessment, or inference;
- corroboration that is genuinely independent;
- contradictory material;
- omitted/unavailable records.

### 3. Fahad al-Thumairy

Separate:

- contact / association evidence;
- institutional role;
- alleged assistance;
- investigator treatment;
- negative findings;
- later rereview or revised assessment.

### 4. Mohdar Abdullah and other witnesses

Track:

- each statement version;
- reliability treatment;
- contradictions;
- source dependence;
- whether later summaries quote or merely paraphrase earlier reports.

### 5. Saudi institutional/support questions

Do not collapse:

`contact → assistance → knowledge → direction → institutional authorization`

into one relationship.

Each link requires separate evidence.

### 6. CIA information-sharing / accountability

Compare:

- Joint Inquiry findings;
- Commission treatment;
- CIA OIG review;
- scope of records reviewed;
- accountability findings;
- negative findings;
- later CIA public characterization.

### 7. Financing

Separate:

- hijacker operational financing;
- alleged third-party support;
- Saudi-government/institutional allegations;
- negative investigative findings;
- records actually reviewed by the investigators making those findings.

### 8. Travel / border / watchlisting

Use the Terrorist Travel monograph primarily for:

- entry chronology;
- visa / passport issues;
- watchlisting;
- border-system knowledge;
- government information flows.

Do not treat it as independent evidence for unrelated support-network claims without tracing its underlying sources.

## Negative-finding matrix

For every important `no evidence`, `unable to substantiate`, `no credible evidence`, or equivalent phrase, capture:

| Field | Required |
|---|---|
| institution / investigator | yes |
| exact wording | yes |
| date | yes |
| scope | yes |
| authority/access | yes |
| evidence actually reviewed | where recoverable |
| unavailable / destroyed / excluded material | where recoverable |
| competing finding | where applicable |
| reproducibility | assess separately |

Never normalize these phrases into a generic statement of factual absence.

## Source-dependency target graph

The desired graph is not:

`five official reports = five independent confirmations`

It is:

`underlying interview / serial / financial / telecom / liaison record`

`→ congressional or Commission staff synthesis`

`→ Commission final-report treatment`

`→ CIA OIG review where applicable`

`→ later FBI / Operation Encore synthesis and rereview`

The same underlying record may feed multiple downstream documents.

## Record-integrity questions

For each document family capture:

- release/declassification chronology;
- redaction chronology;
- missing attachments/workpapers;
- version family;
- custodian;
- source-access limitations;
- whether the public copy is complete or a release subset;
- whether later releases alter the evidentiary picture.

## Stop conditions

Do not open the next major corpus cluster until:

1. the controlled closeout sprint has run;
2. local verifier result is recorded;
3. each successfully ingested record has at least a review stub;
4. source-class distinctions above are preserved;
5. at least the Bayoumi / Thumairy / Hazmi-Mihdhar comparison is started;
6. no document is counted as independent corroboration merely because it repeats an earlier official narrative.

## Next cluster after gate

Default next controlled expansion remains **Operation LOOKING GLASS / nuclear command-and-control continuity**, beginning with official Air Force historical records rather than popular retellings.

## Core rule

**BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations.**
