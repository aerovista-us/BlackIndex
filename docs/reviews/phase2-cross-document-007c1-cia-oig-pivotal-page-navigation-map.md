# Phase 2 Cross-Document Review 007C1 — CIA OIG Pivotal-Page Navigation Map

## Status

`PREPARED — navigation leads only; official page-image verification still required`

This map narrows Review 007C to a small set of Executive Summary pages. It is **not** a source extraction and does not convert search-index or third-party transcription text into primary evidence.

Primary BlackIndex artifacts:

- `CIA-2005-9-11-cia-accountability-001` — full CIA OIG report, official CIA Reading Room release, image-only
- `CIA-2005-9-11-cia-accountability-executive-summary-001` — official 2007 Executive Summary companion from FDLP/GPO, image-only

The Executive Summary catalog description is pages `v–xxiii`, which is a 19-page Roman-numbered sequence. BlackIndex should verify the PDF page-label/physical-page correspondence locally before adopting any physical PDF page number below.

## Navigation-only source hierarchy

Use navigation sources only to locate candidate pages:

`search/index or transcription → page lead → official page image → reviewed extraction`

Never:

`search/index or transcription → quoted primary evidence`

The current candidate page labels were localized through publicly indexed text associated with the CIA report plus public reproductions that preserve the Roman page labels. They remain navigation leads until checked against the official BlackIndex artifact.

## Priority page-label map

### Executive Summary pages v–vii

**Research purpose:** scope, methodology/accountability frame, and the balanced overall finding.

Candidate content:

- scope of the review and relationship to Joint Inquiry findings relating to CIA;
- limits on conclusions concerning other agencies/personnel;
- accountability methodology and distinction between unsatisfactory performance and misconduct;
- finding that the Team found neither a single point of failure nor a silver bullet;
- paired finding that important process, operational follow-through, information-sharing, and analytic failures occurred.

Expected physical page positions **if** the 19-page PDF is ordered continuously from `v` through `xxiii`:

- `v` → physical PDF page 1
- `vi` → physical PDF page 2
- `vii` → physical PDF page 3

This correspondence is an inference from the cataloged page span and must be verified locally before citation.

### Executive Summary pages xiii–xvi

**Research purpose:** Hazmi/Mihdhar watchlisting and information sharing, FBI-channel follow-through, consequences, and accountability recommendations.

Candidate content:

- Malaysia-operation information-sharing section;
- failure to timely recommend watchlisting of Nawaf al-Hazmi and Khalid al-Mihdhar;
- large distribution/readership of CIA cables containing travel information;
- absence of a coherent functioning watchlisting process;
- failed or unconfirmed passage of travel information to FBI channels;
- lack of follow-through to ensure FBI receipt;
- additional missed opportunities between March 2000 and August 2001;
- stated potential consequences of earlier watchlisting/information sharing;
- recommendations that an Accountability Board review specified management performance.

Expected physical page positions **if** the 19-page PDF is ordered continuously from `v` through `xxiii`:

- `xiii` → physical PDF page 9
- `xiv` → physical PDF page 10
- `xv` → physical PDF page 11
- `xvi` → physical PDF page 12

Again, these are navigation expectations only until verified against the official Executive Summary artifact.

## Local verification gate

Review 007C1 should verify only these seven Executive Summary pages first:

`1, 2, 3, 9, 10, 11, 12`

For each page:

1. verify the parent artifact SHA-256 is `4ad41550122f7a92090f4da7c4e03c60f0c671a324b8b070b6292d9034587bd2`;
2. verify the PDF contains 19 pages;
3. render the page locally from the official artifact;
4. confirm the printed Roman page label;
5. record redactions that materially limit the proposition;
6. classify candidate passages as OIG finding, source-dependency statement, recommendation, or contextual explanation;
7. only after visual confirmation create reviewed extraction/investigator-review objects.

## Extraction priorities after page-image verification

### A. Scope / source dependence

Preserve the OIG's own framing of its dependence on Joint Inquiry findings concerning CIA and its limits regarding other agencies. This is needed to prevent false source independence.

### B. No-single-point / systemic-failure balance

Preserve both sides of the finding together. Do not reduce it to either `nothing could have been done` or `one failure caused the attacks`.

### C. Hazmi / Mihdhar information handling

Separate distinct propositions:

- watchlisting failure;
- information known within CIA;
- information passage or non-passage to FBI;
- operational follow-through;
- later accountability assessment.

Do not collapse those into one generalized claim.

### D. Accountability recommendations

A recommendation that an Accountability Board review performance is not itself a finding of misconduct. Preserve the OIG's separate statement about law/misconduct and its performance-accountability standard.

## Stop rule

If any expected Roman label does not correspond to the inferred physical page, stop and map the page labels before extraction. Do not compensate with OCR guessing or offset assumptions.

## Core rule

**Navigation text may tell BlackIndex where to look. Only the official page image can tell BlackIndex what to adopt as primary-source wording.**
