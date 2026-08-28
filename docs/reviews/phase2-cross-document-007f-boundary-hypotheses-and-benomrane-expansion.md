# Review 007F — Boundary Hypotheses and Benomrane Expansion

**Status:** ACTIVE  
**Scope:** Operation Encore / EO 14040 source-boundary review  
**Epistemic posture:** review-only; no child promotion; no confirmed boundary claim

## Why this gate exists

The Review 007 structural boundary diagnostic completed at 36 checked / 0 failures and produced three conservative dispositions:

- `CAND-0005` → `MANUAL_IMAGE_REVIEW_REQUIRED`
- `CAND-0013` → `MANUAL_IMAGE_REVIEW_REQUIRED`
- `BENOMRANE-GAP-WINDOW` → `SEGMENTATION_GAP_WINDOW_REVIEW`

The first two candidates contain useful bracketing evidence that the original classifier intentionally did not convert into a confirmed boundary: each candidate starts with a record-start signal and the page immediately after the proposed range begins another FBI-labeled/case-labeled record. The absence of an explicit terminal-page marker prevented the stricter classifier from declaring the right edge structurally confirmed.

This review therefore records **boundary hypotheses**, not boundaries.

## Candidate hypothesis rule

A heuristic candidate may receive:

`BRACKETED_BY_NEXT_RECORD_START_PENDING_VISUAL_CONFIRMATION`

only when all of the following are true:

1. every diagnostic page has exact normalized-text ↔ physical-PDF correspondence;
2. the proposed first page has a record-start signal;
3. no structured signal indicates continuation from the preceding page;
4. no structured signal indicates continuation into the following page;
5. the first page after the proposed range has a strong new-record signal.

This status does **not** mean the final page itself contains an explicit terminal marker. It therefore remains a hypothesis pending visual/source-image confirmation.

## Benomrane rule

The Benomrane hits at physical pages 173 and 175 are not forced into a nearby heuristic segment.

`tools/review-007-boundary-followup.py` searches outward from those anchor pages for the nearest **strong record-start signals** before and after the anchors while re-verifying exact same-index physical-page correspondence across the search window.

A proposed range may be emitted only as a review range. It remains:

- not a confirmed FBI child record;
- not a promoted object;
- not independent corroboration;
- not proof that every page in the range concerns Benomrane;
- subject to visual confirmation and record-identifier review.

## Strong start signals

The widened search treats the following as strong structural starts:

- FBI header + case/file label;
- FD-302 / FD-302A marker;
- Electronic Communication marker;
- Date of Transcription marker;
- explicit page 1-of-N marker.

Weaker header/interview signals are retained separately but do not independently bracket the range.

## Stop conditions

Stop and preserve the gap as unresolved if:

- physical ↔ normalized page correspondence fails anywhere in the scan window;
- no strong boundary signal is found on one or both sides;
- the structural bracket becomes implausibly broad;
- the resulting range conflicts with known record identifiers or later image review.

## Promotion gate

No record from this pass is promotion-ready solely because it is bracketed.

Before promotion, BlackIndex still requires:

1. source-image confirmation of first and last pages;
2. coherent record type / form / date / case or serial identity;
3. duplicate/version review;
4. exact parent SHA provenance;
5. reviewed extraction with source-page citations;
6. explicit reviewer decision.

The project’s foundational rule remains unchanged: structural organization is evidence about record boundaries, not evidence that a substantive historical claim is true.
