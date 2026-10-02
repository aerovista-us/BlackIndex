# Phase 2 NC3 Review 004 — Provenance-preserving HTML program pages

Status: COMPLETE TO HTML-CAPTURE / PROGRAM-PUBLICATION MILESTONE
Date: 2026-10-01

## Scope

This pass implements a durable first-party HTML artifact path so official program pages can enter BlackIndex without print-to-PDF substitution.

New preserved records:

- `NAVAIR-2026-product-pages-001` — NAVAIR E-6B Mercury / E-130J living product page, SHA `a3bdda57203a8f3011bd552fad07a7b759919c19f888fc60efa7230a55e0071a`.
- `NAVAIR-2024-news-releases-001` — 21 Oct 2024 NAVAIR/PMA-271 E-130J announcement, SHA `d1f0b06f9ba75549e9d434af30607f6de7a26a62f0a7b39028a808189715659c`.

Corpus state after intake: **62 checked / 0 failures**.

## Capture method

Raw HTML bytes are preserved immutably. Normalization now produces a deterministic visible-text derivative while excluding script, style, noscript, template, and SVG content.

Plain curl to NAVAIR returned a Cloudflare `Attention Required` interstitial. The new HTML runner rejected that response and used the existing first-party browser-TLS path with explicit `--expect html`.
## Program evidence

The living NAVAIR product page states that the TACAMO Recapitalization Program will replace the aging E-6B Mercury with E-130J, integrate mission equipment into a militarized C-130J-30, and use E-130J for the TACAMO mission.

The dated 21 Oct 2024 announcement identifies E-130J as the new TACAMO mission aircraft, states that PMA-271 is procuring it through the TACAMO Recapitalization Program, and describes the E-6B's current NC3 role.

The 2024 announcement also said contract award was scheduled for January 2025. That is preserved as a historical planning statement only. This review does **not** convert it into evidence that an award occurred.

## Source genealogy

Both NAVAIR pages are classified `deuterocanon` as official institutional/program-publication layers.

The living product page is `dependent` on the same PMA-271 public program lineage represented by the dated announcement.

The dated announcement is `partially-independent` from the FY2026 Navy budget/index layer because it is a separately issued PMA-271 publication but shares the same TACAMO/E-130J program-of-record lineage.

Repeated descriptions across product pages, public affairs releases, posture statements, and budget records must not be counted as fully independent corroboration without underlying source separation.
## Evidence boundary

These pages establish NAVAIR/PMA-271's public description of the TACAMO recapitalization program at the captured times.

They do not establish:

- detailed operating or authentication procedures;
- nuclear-use authority;
- congressional appropriation, obligation, or expenditure;
- aircraft delivery or operational readiness;
- actual mission use.

## Next gate

1. Preserve the first-party NAVAIR contract-award record if it materially resolves the 2024 planned-award statement.
2. Retry the detailed Navy FY2026 BA5 TACAMO and Air Force detailed SAOC parent artifacts.
3. Continue first-party NC3 Enterprise Center / SAOC / E-130J source genealogy without inferring controlled directive contents.
4. Keep living HTML pages as retrieval-state snapshots; future changes should become version evidence rather than silently replacing the captured bytes.
