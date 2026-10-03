# Phase 2 NC3 Review 012 — SAOC 2026 government contract-execution sequence

Status: COMPLETE TO GOVERNMENT CONTRACT-EXECUTION / EMD1-REPAIR MILESTONE
Date: 2026-10-02

## Scope

Preserve and review three official 2026 DoD/War.gov contract actions on SAOC contract FA2834-24-C-B002.

## Recovered states

- Jan. 30, 2026 / P00026: $26,375,510 modification for repair of stringer cracks on the Engineering and Manufacturing Development 1 aircraft.
- Mar. 30, 2026 / P00031: $20,082,388 funded modification on the same SAOC contract.
- Sept. 3, 2026 / P00037: $30,967,151 funded modification on the same SAOC contract.

The January record materially advances the evidence chain because it identifies an EMD1 aircraft-specific repair work package in a first-party government contract record.

## Evidence boundary

These records establish funded contract execution. They do not establish repair success, airworthiness, flight-test results, aircraft delivery, government acceptance, certification, readiness, IOC/FOC, or operational employment.

The three records share the same contract lineage and are not counted as three independent confirmations of the program narrative.

## Retrieval infrastructure

War.gov rejected ordinary HTML curl from NXCore with HTTP 403. BlackIndex HTML intake was narrowly extended to permit the existing guarded browser-TLS fallback for war.gov first-party URLs. The fallback preserved direct first-party bytes and passed the existing HTML/interstitial guard.

## Related open gaps

A dedicated missing-evidence object now tracks SAOC government test, delivery, acceptance, certification, and readiness evidence.

The detailed Air Force FY2026 RDT&E Volume II SAOC source was retried using its exact SAF/FM first-party URL. The artifact exists and is publicly indexed, but all NXCore acquisition tiers failed with TLSV1_ALERT_INTERNAL_ERROR. No mirror or search-cache substitute was ingested.

AFGSCMD 63-101 also remains unrecovered.

## Next gate

1. Find first-party completion/airworthiness or return-to-test evidence for the EMD1 repair.
2. Find government SAOC developmental flight-test results or acceptance evidence.
3. Find the first explicit SAOC EMD aircraft delivery/acceptance record.
4. Continue bounded retries for the detailed SAF/FM SAOC budget parent and AFGSCMD 63-101.
