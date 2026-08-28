# Phase 2 Cross-Document Review 007C — CIA OIG 9/11 Deliberate Extraction Plan

## Status

`ACTIVE — primary artifact preserved; release/version identity clarified; text extraction still requires page-image verification`

Primary BlackIndex record:

`CIA-2005-9-11-cia-accountability-001`

Local intake verified the official CIA artifact by SHA-256, but `pdftotext` found no usable text layer. The record therefore remains a valid primary artifact with `normalization_status: pdf-no-text-layer`.

This plan deliberately separates **artifact integrity** from **text convenience**.

## Non-negotiable rule

Do not silently OCR the primary source during intake and do not replace the official CIA PDF with a third-party transcription.

The official artifact remains primary evidence.

## 2026-08-28 release/version checkpoint

Review 007C verified that the BlackIndex artifact URL is the CIA Reading Room release:

`https://www.cia.gov/readingroom/docs/DOC_0006184107.pdf`

with CIA release identifier/native ID:

`C06184107`

CIA's 2015 release notice states that the Agency released a redacted version of the 2005 OIG report and separately notes that CIA had already released a redacted executive summary in 2007.

Official CIA release notice:

`https://www.cia.gov/stories/story/cia-releases-declassified-documents-related-to-9-11-attacks/`

This means the apparent searchable "2015 companion" discovered through public indexing is **not a second BlackIndex source artifact**. It is the same full-report CIA release already represented by `CIA-2005-9-11-cia-accountability-001`.

Do not create a duplicate document record merely because a public search system exposes machine-readable/indexed text for the same CIA PDF.

### 2007 executive-summary release remains a distinct companion target

A Federal Depository Library Program/GPO catalog record identifies the separately released official executive summary under persistent identifier:

`GPO/LPS93679`

Catalog metadata describes it as:

- United States Central Intelligence Agency, Inspector General;
- June 2005;
- approved for release August 2007;
- redacted;
- pages v-xxiii;
- SuDoc `PREX 3.2:AT 8/EXEC.SUM.`.

Persistent government identifier:

`https://purl.fdlp.gov/GPO/LPS93679`

Congressional release context is independently documented in section 605 of the Implementing Recommendations of the 9/11 Commission Act of 2007, which required CIA to prepare and make publicly available a version of the Executive Summary declassified to the maximum extent possible consistent with national security.

Official Senate statutory text:

`https://www.intelligence.senate.gov/2007/08/03/laws-implementing-recommendations-911-commission-act-2007/`

The 2007 executive summary may therefore be ingested later as a **separate companion/release object**, never as a replacement for the 2015 full-report artifact.

## Search/index text policy

Public search systems currently expose machine-readable text associated with the official CIA PDF even though BlackIndex's preserved artifact has no usable native text layer.

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

### Stage A — preserve primary artifact

Already complete:

- official CIA acquisition;
- immutable local raw artifact;
- SHA-256 provenance;
- durable metadata/extraction stub;
- local verifier clean;
- record-integrity object generated locally.

No transformation should alter that artifact.

### Stage B — official release/version mapping

Current state:

- full 2005 OIG report, redacted CIA Reading Room release published in 2015: **represented in BlackIndex**;
- 2007 redacted executive summary: **official companion target confirmed, not yet separately ingested**;
- public search/index rendering of `DOC_0006184107.pdf`: **navigation derivative only, not a separate source**.

If the FDLP/GPO persistent executive-summary URL is acquired successfully, ingest it as a separate companion record.

Suggested collection:

`9/11 CIA Accountability Executive Summary`

Suggested source token:

`CIA`

Suggested relationship after successful ingest:

`version_family / companion-release relationship`

with explicit note that the executive summary is a subset/summary, not a full-text surrogate for the complete released report.

### Stage C — use searchable transcriptions only as navigation aids

Searchable reproductions or search-index text may help locate phrases or section headings, but they must not become the cited primary evidence layer.

Permitted use:

`navigation transcription/index → page lead → verify against official CIA page/image`

Not permitted:

`navigation transcription/index → adopted as official text without verification`.

### Stage D — manual or vision-assisted page verification for pivotal passages

For any pivotal CIA OIG finding used in Review 007:

1. identify the passage using the official executive summary or a navigation transcription/index;
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
- August 2007 executive-summary release/approval chronology;
- 2015 CIA release of the redacted full report;
- relationship between the 2007 executive-summary artifact and the 2015 full-report release;
- page count and redaction differences;
- whether later CIA releases contain additional pages or reduced redactions;
- whether the persistent GPO/FDLP copy is byte-identical to CIA's 2007 executive-summary release or merely a preserved companion copy.

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
2. preserve the 2007 executive-summary versus 2015 full-report release distinction;
3. verify pivotal executive-summary findings against an official release/page image;
4. encode negative/accountability findings as attributed investigator-review objects;
5. record version/release limitations.

## Core rule

**When the primary artifact is image-only, BlackIndex should degrade convenience—not evidentiary discipline.**
