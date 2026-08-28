# Phase 2 Cross-Document Review 007C — CIA OIG 9/11 Deliberate Extraction Plan

## Status

`ACTIVE — full report + official 2007 Executive Summary companion preserved; both image-only; pivotal page-image verification is next`

Primary BlackIndex records:

- `CIA-2005-9-11-cia-accountability-001` — redacted full report
- `CIA-2005-9-11-cia-accountability-executive-summary-001` — separately released Executive Summary companion

Local intake verified both official artifacts by SHA-256, but `pdftotext` found no usable native text layer in either. Both therefore remain valid primary/official release artifacts with `normalization_status: pdf-no-text-layer`.

This plan deliberately separates **artifact integrity** from **text convenience**.

## Non-negotiable rule

Do not silently OCR either official source during intake and do not replace either artifact with a third-party transcription.

The official artifacts remain the evidence layer.

## 2026-08-28 release/version checkpoint

The BlackIndex full-report artifact is the CIA Reading Room release:

`https://www.cia.gov/readingroom/docs/DOC_0006184107.pdf`

with CIA release identifier/native ID:

`C06184107`

CIA's 2015 release notice states that the Agency released a redacted version of the 2005 OIG report and separately notes that CIA had already released a redacted executive summary in 2007.

Official CIA release notice:

`https://www.cia.gov/stories/story/cia-releases-declassified-documents-related-to-9-11-attacks/`

The 2007 Executive Summary was subsequently acquired from the official FDLP/GPO persistent identifier:

`https://purl.fdlp.gov/GPO/LPS93679`

BlackIndex record:

`CIA-2005-9-11-cia-accountability-executive-summary-001`

SHA-256:

`4ad41550122f7a92090f4da7c4e03c60f0c671a324b8b070b6292d9034587bd2`

The companion also has no usable native text layer. No OCR was performed.

### Durable relationship encoding

BlackIndex now records both:

- `objects/source_dependencies/SD-2005-cia-oig-exec-summary-to-full-report.json`
- `objects/version_families/VF-CIA-2005-9-11-accountability-release-family.json`

The relationship is intentionally narrow:

`Executive Summary companion/subset → same CIA OIG report lineage`

It does **not** mean the two files are byte-level versions of the same full-text artifact, and it does **not** make them independent corroboration of each other.

## Search/index text policy

Public search systems may expose machine-readable text associated with the official CIA PDFs even though BlackIndex's preserved artifacts have no usable native text layer.

That indexed text may be used only as:

`public search/index text → navigation lead → locate candidate page → verify against official CIA page image`

It must **not** be represented as:

`search/index text → official quoted primary text`

or:

`search/index text → evidence object without page-image verification`.

This rule applies even when the search result points directly to the CIA domain.

## Known source context

The released CIA OIG report is a retrospective/accountability review. Its executive summary states that the review focuses on Joint Inquiry findings relating to CIA and that the team coordinated with the DOJ Inspector General and the 9/11 Commission while limiting its own conclusions to CIA-related performance/accountability.

That makes it an official review layer, not independent proof of every underlying Joint Inquiry proposition.

## Extraction strategy

### Stage A — preserve official artifacts

Complete:

- official CIA full-report acquisition;
- official FDLP/GPO Executive Summary acquisition;
- immutable local raw artifacts;
- SHA-256 provenance;
- durable metadata/extraction stubs;
- local verifier clean at **37 / 0** after companion acquisition;
- record-integrity sidecars generated locally;
- no OCR during intake.

No transformation should alter either artifact.

### Stage B — official release/version mapping

Complete to the current milestone:

- 2007 redacted Executive Summary: represented in BlackIndex;
- 2015 redacted full-report CIA release: represented in BlackIndex;
- companion/dependency relationship: encoded;
- release family: encoded;
- public search/index rendering: classified as navigation derivative only, not a separate source.

Open release-integrity questions remain suitable for later targeted comparison:

- exact redaction differences between summary and full report;
- whether later releases changed any redactions/pages;
- whether the FDLP/GPO copy is byte-identical to CIA's original 2007 public copy or a preserved government reproduction.

### Stage C — use searchable text only as navigation

Searchable reproductions or search-index text may help locate phrases or section headings, but they must not become the cited primary evidence layer.

Permitted use:

`navigation transcription/index → page lead → verify against official CIA page/image`

Not permitted:

`navigation transcription/index → adopted as official text without verification`.

### Stage D — manual or vision-assisted page verification for pivotal passages

This is the active next gate.

For any pivotal CIA OIG finding used in Review 007:

1. identify the candidate passage using a navigation transcription/index or document structure;
2. inspect the corresponding page in the official full report and/or Executive Summary artifact;
3. capture the physical PDF page/image location;
4. record exact wording conservatively;
5. note redactions that materially limit scope;
6. classify the passage as OIG finding, Joint Inquiry quotation/paraphrase, underlying fact claim, or recommendation;
7. when the same proposition appears in both releases, treat that as same-lineage repetition unless the comparison itself is the research object.

## Priority extraction topics

### 1. Scope / source dependence

Capture the OIG's statement that its review focuses on Joint Inquiry findings relating to CIA and the limitations on interviews outside CIA.

Purpose: establish why CIA OIG and Joint Inquiry findings cannot be counted as independent source families automatically.

### 2. No-single-point / systemic-failure formulation

Capture the OIG's finding concerning no single point of failure while separately identifying process, follow-through, information-sharing, and analytic failures.

Purpose: preserve the exact balance of the finding instead of simplifying it into either `CIA caused 9/11` or `no one was accountable`.

### 3. Hazmi / Mihdhar information handling

Identify OIG treatment of CIA knowledge, watchlisting, dissemination, and management of information concerning Hazmi and Mihdhar.

Purpose: compare CIA-accountability findings with Commission and Joint Inquiry chronology.

### 4. Management / accountability recommendations

Separate:

- institutional/process findings;
- individual-performance findings;
- recommendations for accountability review;
- later CIA leadership responses to those recommendations.

Do not convert a recommendation for accountability review into a factual finding of misconduct by a named person.

## Version / release integrity questions

Before marking CIA OIG review complete, capture:

- June 2005 preparation date;
- August 2007 executive-summary release/approval chronology;
- 2015 CIA release of the redacted full report;
- relationship between the 2007 Executive Summary artifact and the 2015 full-report release;
- page count and redaction differences;
- whether later CIA releases contain additional pages or reduced redactions;
- whether the persistent GPO/FDLP copy is byte-identical to CIA's 2007 executive-summary public copy or a preserved government reproduction.

## OCR policy

OCR remains a **last-resort derivative**, not an intake default.

If OCR is eventually required:

- write output only under a derivative/local path;
- never change the raw artifact;
- record OCR engine/version/settings;
- preserve page-level confidence or manual review state;
- pivotal quotes require visual verification against the official page image;
- never treat OCR uncertainty as source uncertainty.

Whole-document OCR is not required for the current Review 007 gate.

## Gate contribution

Review 007 can continue without completing full-document OCR. The current CIA OIG minimum gate is now:

1. preserve source-dependency relationship to Joint Inquiry;
2. preserve the 2007 Executive Summary versus 2015 full-report release distinction;
3. preserve the Executive Summary → full-report companion/dependency relationship;
4. verify pivotal findings against official page images;
5. encode negative/accountability findings as attributed investigator-review objects;
6. record remaining version/redaction limitations.

## Core rule

**When the primary artifact is image-only, BlackIndex should degrade convenience—not evidentiary discipline.**
