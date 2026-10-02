# Phase 2 NC3 Review 005 — E-130J award resolution and detailed-parent retry

Status: COMPLETE TO AWARD-STATE / RETRIEVAL-RETRY MILESTONE
Date: 2026-10-02

## Scope

This pass resolves the dated award-planning statement captured in Review 004 and retries the remaining public first-party detailed NC3 program parents.

New preserved records:

- `DOD-2024-contract-announcements-001` — DoD 18 Dec 2024 E-130J TACAMO contract action, SHA `bfe2248e39d24838b44c5cb631339b834f8ac5cbd772b78304005c459ce255e7`.
- `US_NAVY-2024-press-releases-001` — Navy 19 Dec 2024 E-130J award announcement, SHA `c6f03de378c11125055b3f0348db20a47b2ac4d980f8edbb69ce736e565b600b`.

Corpus state after intake: **64 checked / 0 failures**.

## Award-state chronology

The 21 Oct 2024 NAVAIR announcement stated that the E-130J integration solicitation had closed and contract award was scheduled for January 2025.

The DoD daily contract record for 18 Dec 2024 records award of contract `N0001925C0130` to Northrop Grumman Systems Corp. for E-130J TACAMO engineering and manufacturing development, with a stated value of **$3,459,276,000**.
The Navy announcement dated 19 Dec 2024 reports the same award and supplies PMA-271 program context.

The award therefore occurred before the month forecast in the October planning statement. `SC-NC3-e130j-planned-to-awarded-2024` records that temporal state change without modifying the earlier source.

## Source genealogy

The DoD contract notice is classified `canon` at the public contract-action level.

The Navy announcement is classified `deuterocanon` and is `dependent` on the same underlying award event. It is not a second independent contract action.

This award evidence establishes the contract action stated by DoD. It does **not** establish later contract performance, option exercise, aircraft delivery, operational readiness, nuclear-use authority, or actual mission employment.

## Detailed-parent retry results

### Air Force FY2026 RDT&E Volume II — SAOC PE 0604288F

The current official SAF/FM index identifies the detailed SAOC material in FY2026 Air Force RDT&E Volume II.

NXCore direct curl failed with `TLSV1_ALERT_INTERNAL_ERROR`. The browser-TLS helper failed with the same TLS alert before artifact bytes were received. No surrogate was ingested.
### Navy FY2026 RDT&E BA5 — TACAMO Modernization PE 0605180N

The official Navy FY2026 budget folder continues to list `RDTEN_BA5_Book.pdf`.

The browser-TLS retrieval remained connected with zero bytes transferred through the bounded retry window. The process was terminated rather than allowing an indefinite fetch. No partial artifact was retained.

### AFGSCMD 63-101 — USAF NC3 Center

The official Air Force search layer still identifies the unrestricted 27 Jan 2020 mission directive and its NC3 Center mission/command scope. The direct first-party artifact URL currently returns HTTP 404, including through the browser-TLS path.

This is recorded as **indexed but artifact-unavailable**, not absent and not preserved evidence.

## Next gate

1. Continue periodic first-party recovery of the detailed SAOC Volume II, Navy BA5 TACAMO book, and AFGSCMD 63-101 artifact.
2. If a later first-party contract-performance, delivery, or test record is needed, preserve it as a new time-bounded state rather than inferring performance from the award.
3. Keep award, obligation, expenditure, delivery, readiness, authority, and actual use as separate propositions.
4. Do not substitute search-index text, unofficial mirrors, or reconstructed controlled contents for missing primary artifacts.
