# Phase 2 Cross-Document Review 007C — CIA OIG 9/11 Deliberate Extraction Plan

## Status

`PREPARED — primary artifact preserved; text extraction unresolved`

Primary BlackIndex record:

`CIA-2005-9-11-cia-accountability-001`

Local intake verified the official CIA artifact by SHA-256, but `pdftotext` found no usable text layer. The record therefore remains a valid primary artifact with `normalization_status: pdf-no-text-layer`.

This plan deliberately separates **artifact integrity** from **text convenience**.

## Non-negotiable rule

Do not silently OCR the primary source during intake and do not replace the official CIA PDF with a third-party transcription.

The official artifact remains primary evidence.

## Known source context

The released CIA OIG report is a retrospective/accountability review. Its executive summary states that the review focuses on Joint Inquiry findings relating to CIA and that the team coordinated with the DOJ Inspector General and the 9/11 Commission while limiting its own conclusions to CIA-related performance/accountability.

That makes it an official review layer, not independent proof of every underlying Joint Inquiry proposition.

## Extraction strategy

### Stage A — preserve primary artifact

Already complete:

- official CIA acquisition;
- immutable local raw artifact;
- SHA-256 provenance;
- durable metadata/extraction stub;
- local verifier clean;
- record-integrity object generated locally.

No transformation should alter that artifact.

### Stage B — acquire an official text-bearing companion if available

A Federal Depository Library Program/GPO catalog record identifies an official **Executive Summary** of the OIG report and gives persistent identifier:

`GPO/LPS93679`

Catalog metadata describes it as:

- United States Central Intelligence Agency, Inspector General;
- June 2005;
- approved for release August 2007;
- redacted;
- SuDoc `PREX 3.2:AT 8/EXEC.SUM.`

If the persistent government URL still resolves to a PDF, ingest it as a **separate companion record**, never as a replacement for the full CIA artifact.

Suggested collection:

`9/11 CIA Accountability Executive Summary`

Suggested source token:

`CIA`

Suggested relationship after successful ingest:

`version_family / companion-release relationship`

with explicit note that the executive summary is a subset/summary, not a full-text surrogate for the complete released report.

### Stage C — use secondary transcriptions only as navigation aids

Searchable third-party reproductions exist on the public web. They may help locate phrases or section headings, but they must not become the cited primary evidence layer.

Permitted use:

`secondary transcription → navigation lead → verify against official CIA page/image`

Not permitted:

`secondary transcription → adopted as official text without verification`.

### Stage D — manual page verification for pivotal passages

For any pivotal CIA OIG finding used in Review 007:

1. identify the passage using the official executive summary or a navigation transcription;
2. inspect the corresponding page in the official CIA artifact;
3. capture the physical PDF page/image location;
4. record exact wording conservatively;
5. note redactions that materially limit scope;
6. classify the passage as OIG finding, Joint Inquiry quotation/paraphrase, underlying fact claim, or recommendation.

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
- August 2007 release/approval chronology;
- whether the current Reading Room PDF is the same release version as the 2007 executive-summary artifact;
- page count and redaction differences;
- whether later CIA releases contain additional pages or reduced redactions;
- whether the persistent GPO/FDLP copy is byte-identical or merely a companion publication.

## OCR policy

OCR remains a **last-resort derivative**, not an intake default.

If OCR is eventually required:

- write output only under a derivative/local path;
- never change the raw artifact;
- record OCR engine/version/settings;
- preserve page-level confidence or manual review state;
- pivotal quotes require visual verification against the official page image;
- never treat OCR uncertainty as source uncertainty.

## Gate contribution

Review 007 can continue without completing full-document OCR. The minimum CIA OIG gate is:

1. preserve source-dependency relationship to Joint Inquiry;
2. verify pivotal executive-summary findings against an official release;
3. encode negative/accountability findings as attributed investigator-review objects;
4. record version/release limitations.

## Core rule

**When the primary artifact is image-only, BlackIndex should degrade convenience—not evidentiary discipline.**
