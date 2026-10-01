# Phase 2 NC3 Review 003 — Program-source genealogy

Status: COMPLETE TO PROGRAM-INDEX / SOURCE-GENEALOGY MILESTONE  
Date: 2026-10-01

## Scope

This pass moves below annual posture statements into public first-party program/budget records for SAOC and TACAMO while preserving a strict separation between program evidence and operating authority or use.

New preserved parent records:

- `DOD-2025-fy-2026-rdt-e-programs-r-1-001` — Department of Defense FY2026 RDT&E Programs R-1, SHA `502b6bf66bd9ff08e2a01686e913d92636e79a45bf6afdb66561073bd4ce51f9`.
- `US_NAVY-2025-fy-2026-rdt-e-budget-justification-books-001` — Department of the Navy FY2026 RDT&E BA1-3 book, SHA `4ac2a56535d4540dcb2a04203ed11c0448438b8f16c50660fbf2a742817df816`.

Corpus state after intake: **60 checked / 0 failures**.

## SAOC program-index evidence

The DoD FY2026 R-1 identifies PE `0604288F`, **Survivable Airborne Operations Center (SAOC)**.

In Budget Activity 5, the R-1 lists an FY2026 discretionary request of `$1,826,328` thousand, a reconciliation request of `$6,800` thousand, and an FY2026 total of **`$1,833,128` thousand**.
The same PE also appears in Budget Activity 4 with FY2024 actuals and FY2025 enacted/total values. That BA4 row must not be added to the BA5 FY2026 request as though it were a second FY2026 program request.

This R-1 establishes a formal DoD program element and budget-request context. It does **not** establish congressional appropriation, obligation/expenditure, aircraft delivery, operational readiness, nuclear-use authority, or actual mission use.

## TACAMO program-index evidence

The Navy FY2026 BA1-3 parent contains the R-1/index entry for PE `0605180N`, **TACAMO Modernization**.

The row lists FY2024 actuals of `$200,494` thousand, FY2025 enacted/total of `$755,316` thousand, and an FY2026 total request of **`$1,243,978` thousand**.

Critical boundary correction: TACAMO is Budget Activity 5. The preserved BA1-3 artifact therefore contains the R-1/index entry and points to the detailed program material, but it is **not** the detailed BA5 TACAMO justification.

The official FY2026 Navy budget folder separately lists `RDTEN_BA5_Book.pdf`; current NXCore retrieval attempts did not yield the artifact bytes. That source remains a public first-party retrieval gap, not evidence of nonexistence.

## Cross-layer genealogy

The 2026 USSTRATCOM posture statement names SAOC and TACAMO/E-130J modernization at the command-institutional level. The FY2026 budget records independently originate from DoD/Navy budget processes, but the repeated proposition that these are active programs shares the underlying program-of-record lineage.
Accordingly, the new SAOC and TACAMO source-dependency edges are `partially-independent`, not `independent`.

## Public first-party source gaps

`ME-NC3-public-program-source-gaps` now distinguishes public-source retrieval/capture gaps from controlled-governance gaps. It tracks:

- `AFGSCMD 63-101` — publicly indexed Air Force NC3 Center mission directive; current NXCore first-party artifact retrieval returns 403/404.
- Air Force FY2026 detailed SAOC justification for PE `0604288F`; official budget indexes identify the source, while NXCore currently encounters a TLS transport failure on the detailed Air Force volume.
- Navy FY2026 `RDTEN_BA5_Book.pdf`; officially listed, but current NXCore direct and browser-TLS attempts did not produce bytes.
- NAVAIR E-130J/TACAMO first-party HTML program pages; useful source-address evidence, but the current BlackIndex durable artifact path is PDF-oriented and should not manufacture a print-to-PDF surrogate.

These states mean **publicly known but not yet preserved**, not `does not exist`.

## Next gate

1. Add provenance-preserving first-party HTML capture support so official NAVAIR/USSTRATCOM program pages can enter BlackIndex without fake PDF conversion.
2. Periodically retry the first-party AFGSCMD 63-101, Air Force detailed SAOC volume, and Navy BA5 artifact paths.
3. If detailed parent artifacts become available, create companion/version families and refine genealogy without overwriting this program-index milestone.
4. Keep budget request, appropriation, expenditure, delivery, readiness, authority, procedure, and actual use as separate propositions.

No detailed operating procedure, authentication chain, execution procedure, or operational-use claim was promoted in this review.
