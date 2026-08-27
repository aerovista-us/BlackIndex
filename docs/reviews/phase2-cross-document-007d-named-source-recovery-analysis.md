# Phase 2 Cross-Document Review 007D — Named-Source Recovery Analysis

## Status

`ACTIVE — local scan interpreted; source-boundary review pending`

This note interprets the controlled local named-source recovery run without promoting any child record or changing historical evidence status.

Authoritative run record:

- `docs/run-reports/2026-08-27-review-007-named-source-recovery.md`
- local verifier: **36 checked / 0 failures**
- normalized documents scanned: **25**
- normalized text-page chunks scanned: **4657**
- named recovery targets: **15**
- targets with at least one candidate hit somewhere in the corpus: **15 / 15**

## Critical interpretation

`15 / 15 targets with candidate hits` does **not** mean 15 underlying source records were recovered.

The scan found two different classes of hit:

1. **Citation / synthesis localization** — the target title/date/name appears in an official synthesis document, principally the 9/11 Commission Final Report notes. This confirms that BlackIndex can navigate to the citation, but does not recover the underlying FBI/CIA record itself.
2. **Underlying-container candidate localization** — the target signature also appears inside a locally held EO 14040 FBI release container. This is materially stronger for recovery work, but still does not establish the complete source boundary or a verified physical page.

For this run:

- **15 / 15** target families had citation/synthesis localization somewhere in the corpus.
- **2 / 15** target families also had candidate hits inside EO 14040 FBI containers.
- **13 / 15** target families remain citation-localized only in this scan.
- **0** child source records were promoted.
- **0** physical page claims were made.

## EO 14040 container candidates

### Caysan Bin Don / Isamu Dyson interview source versions

Candidate EO 14040 locations:

- `FBI-2022-eo14040-2-c-001`
  - parent SHA-256: `c7960258fa7feff92d3386da7eb7b6cb0effa457780fd756cbf43ee5fc6985b6`
  - normalized text-page indices: `60`, `118`
  - physical page: **UNVERIFIED**

The same names also appear in Commission text. The FBI-container hits therefore require boundary review to determine whether either occurrence is the cited interview record itself, a later summary, or another FBI record that merely mentions those witnesses.

### Qualid Moncef Benomrane FBI interviews — 2002

Candidate EO 14040 locations:

- `FBI-2021-eo14040-2-b-i-001`
  - parent SHA-256: `288067203d5d22736a09f064020c529e06cc79db60b49fd7c665c032e44f3e00`
  - normalized text-page indices: `173`, `175`
  - physical page: **UNVERIFIED**

The Commission Final Report also contains citation hits for Benomrane. The EO 14040 hits are therefore promising recovery candidates, not proof that the complete March/May 2002 interview records have been isolated.

## Citation-localized only in this scan

The following target families were located in Commission text but did not produce an EO 14040 container candidate under the current signatures:

- FBI EC Fahad Al-Thumairy — 2002-09-04
- FBI EC Fahad Althumairy — 2002-10-25
- FBI EC Fahad Al-Thumairy — 2002-11-20
- FBI ROI/interview Mohdar Abdullah — 2002-07-23
- FBI EC Abdullah investigation — 2004-05-19
- FBI EC interview Charles Sabah Toma — 2004-05-18
- FBI EC Omar Ahmed Al Bayoumi — 1999-06-07
- FBI LHM investigation of Bayoumi — 2002-04-15
- FBI recovery of Bayoumi hotel records — 2002-01-15
- FBI EC/interview of Bayoumi — 2003-09-17
- Omar al Bayoumi interview — 2003-10-16/17
- FBI report `Connections of San Diego PENTTBOM Subjects to the Government of Saudi Arabia`
- CIA analytic report `Al-Qa'ida Travel Issues` — 2003-11-14

This state is `UNMAPPED_REFERENCED_EVIDENCE`, not evidence of destruction, withholding, or nonexistence.

## Consequences for source genealogy

The scan strengthens one methodological conclusion: the Commission's footnotes are functioning as a **source-address layer**, not as independent corroborating documents for the underlying claims.

For the 13 citation-only targets, the currently reproducible chain is:

`Commission proposition → Commission footnote/source citation → named underlying record not yet individually recovered`

For the two container-candidate families, the chain can provisionally be extended to:

`Commission proposition → Commission footnote/source citation → candidate occurrence inside EO 14040 FBI container`

It may only become:

`→ recovered underlying source record`

after source-boundary and physical-page review.

## Next review gate

Priority order:

1. inspect the §2(c) candidate boundaries around normalized text pages 60 and 118 for Caysan Bin Don / Isamu Dyson;
2. inspect the §2(b)(i) candidate boundaries around normalized text pages 173 and 175 for Benomrane;
3. map each candidate to the existing segmentation index / P0 review packets where possible;
4. do **not** promote either family until parent SHA, source boundary, record title/date/type, and physical-page evidence are verified;
5. keep the remaining 13 target families open as unmapped referenced evidence;
6. do not increase corroboration strength merely because a citation appears in both the Commission and a later FBI synthesis.

## Core rule

A candidate hit is a navigation lead. It is not a recovered record until the record boundary and provenance are established.
