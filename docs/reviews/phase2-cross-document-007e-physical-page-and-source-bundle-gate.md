# Phase 2 Cross-Document Review 007E — Physical Page and Source-Bundle Gate

## Status

**ACTIVE — physical-page correspondence verified; bounded source-image review prepared.**

## Physical-page result

The controlled Review 007 physical-page checkpoint completed with:

- corpus verifier: **36 checked / 0 failures**;
- positions checked: **4**;
- positions verified: **4**;
- positions unresolved: **0**;
- OCR used: **false**;
- fuzzy matching used: **false**;
- evidence-state mutation: **none**;
- record promotion: **none**.

The four normalized-text positions each had one unique exact canonical-text match at the same physical PDF page when re-extracted with `pdftotext -layout`:

| Parent | Named-source family | Text page | Verified physical page |
|---|---|---:|---:|
| `FBI-2022-eo14040-2-c-001` | Caysan Bin Don / Isamu Dyson | 60 | 60 |
| `FBI-2022-eo14040-2-c-001` | Caysan Bin Don / Isamu Dyson | 118 | 118 |
| `FBI-2021-eo14040-2-b-i-001` | Qualid Moncef Benomrane | 173 | 173 |
| `FBI-2021-eo14040-2-b-i-001` | Qualid Moncef Benomrane | 175 | 175 |

This verifies page correspondence only. It does **not** verify child-record boundaries.

## Segment result carried forward

- page 60 maps to `CAND-0005`, heuristic range `58–63`, P0, review packet present;
- page 118 maps to `CAND-0013`, heuristic range `116–122`, P0, review packet present;
- Benomrane pages 173/175 are not covered by any current heuristic segment.

The Benomrane result is therefore a segmentation-gap lead rather than a promotable child record.

## New source-image gate

`tools/build-review-007-verified-source-bundle.py` prepares exactly three local review targets:

1. `CAND-0005` — proposed review range `58–63`;
2. `CAND-0013` — proposed review range `116–122`;
3. `BENOMRANE-GAP-WINDOW` — diagnostic range `171–177` around the verified 173/175 anchors.

Before extracting any slice, the tool independently verifies **every page in the proposed range** against the corresponding physical PDF page using exact `pdftotext -layout` canonical-text comparison.

A slice is created only if the complete proposed range passes that check.

## Interpretation rule

`REVIEW_SLICE_READY` means only:

- the immutable parent PDF hash matched metadata;
- the relevant Review 007 anchor passed the dedicated physical-page gate;
- every page in the requested review range exact-matched the corresponding physical PDF page;
- the resulting slice is a safe local source-image review artifact.

It does **not** mean:

- the slice is exactly one complete FBI record;
- the first or last page is a confirmed record boundary;
- the record has been promoted;
- the content independently corroborates a later official report.

Boundary review and source genealogy remain separate gates.

## Legacy helper safety

The older generic FBI source-bundle helper is no longer allowed to silently treat heuristic text-page ranges as physical PDF pages. Its prior behavior now requires an explicit unsafe legacy override. Review 007 does not use that override.

## Next controlled checkpoint

Run:

```bash
bash tools/run-review-007-verified-source-bundle.sh
```

The checkpoint publishes only a sanitized Git-backed run report. Source PDF slices, detailed manifests, and review bytes remain local-only.

## Stop gate

Do not promote `CAND-0005`, `CAND-0013`, or the Benomrane gap window merely because a verified source-image slice exists. Review the source images for true first/last page boundaries, record type, dates, serial/case identifiers, redaction markings, attachments, and duplicate/overlapping release status first.
