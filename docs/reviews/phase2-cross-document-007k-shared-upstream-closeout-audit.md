# Phase 2 Cross-Document Review 007K — Shared-Upstream Closeout Audit

## Status

`COMPLETE — current official-layer counting controls audited; unresolved genealogy remains non-promotional`

## Purpose

Review 007 requires verification that multiple official publications are not being counted as multiple independent confirmations merely because the same proposition appears in more than one downstream document.

This pass audits the **encoded independence treatment** of the current 9/11 official-layer graph. It does not claim that every named upstream record has been recovered.

## Reproducible control

New audit tool:

`tools/audit-review-007-shared-upstream.py`

The tool fails closed if any of the currently identified high-risk official-layer dependency or classification objects disappears or silently changes its expected independence state.

CI coverage:

`tests/test_review007_shared_upstream_audit.py`

## Audit result

Current controlled set:

- source-dependency objects checked: **13**;
- official synthesis research classifications checked: **4**;
- Bayoumi/Thumairy temporal comparison guardrails checked: **2**;
- high-risk dependency edges marked `independent`: **0**;
- audit errors: **0**.

Dependency treatment:

- **11** high-risk edges are encoded `dependent`;
- **2** staff-monograph edges are encoded `partially-independent` because their source bases mix reused government material with some original Commission staff interviews/work;
- **0** high-risk edges are encoded `independent`.

## Pair-by-pair disposition

### Joint Inquiry ↔ Commission Final Report

`CONTROLLED — genealogy partial`

Both are treated as dependent syntheses for the California support-network propositions currently encoded. Named FBI source recovery remains incomplete, so unresolved overlap cannot increase corroboration strength.

### Commission staff work ↔ Commission Final Report

`CONTROLLED — structural shared institution/research base`

The final report is not treated as an independent source family merely because staff work also exists. Financing and Travel monographs retain `partially-independent` at the monograph source-base level, not `independent` relative to the final report.

### Joint Inquiry ↔ CIA OIG

`CONTROLLED — explicit dependency`

`SD-2005-cia-oig-to-joint-inquiry` encodes the OIG's explicit focus on Joint Inquiry findings relating to CIA. Review 007C2 additionally preserves the OIG's own interviews/analysis and its proposition-specific scope; the relationship is not flattened into either total identity or independent confirmation.

### Commission Final Report ↔ Operation Encore 2016

`CONTROLLED — exact overlap still incomplete`

The Commission and 2016 FBI EC both depend on FBI investigative material. The exact shared serial set is not fully recovered. BlackIndex therefore does **not** count the later EC as a fresh independent confirmation by default. The Bayoumi and Thumairy statement-comparison objects explicitly require lower-level source tracing before deciding whether a proposition materially changed.

### 2016 Operation Encore EC ↔ 2021 closing synthesis

`CONTROLLED — explicit dependency`

The later closing synthesis is encoded as dependent on the 2016 EC. Repetition does not increase evidence count.

### Commission Notes 22/23 ↔ May 2004 FBI Vault records

`CONTROLLED — exact recovered citation chains`

Review 007H visually confirmed the May 18 and May 17 FBI EC boundaries and encoded Commission Notes 22 and 23 as dependent on those recovered FBI records. The Commission's citation is a source address, not an additional witness/source event.

### Duplicate/release-family risk

`CONTROLLED`

Review 007J records the financing-monograph legacy PDF as a byte-different but text-identical release/acquisition variant and the standalone Chapter 7 PDF as a subset of the canonical full Commission Report. Neither can increase corroboration strength.

## What remains unresolved

The audit closes the **double-counting control**, not the full source-recovery program.

Still unresolved or partial:

- several named 2001–2004 FBI records cited by the Commission;
- exact source overlap between some Commission propositions and the 2016 Encore rereview;
- Benomrane record boundary recovery, on HOLD pending a new concrete lead;
- July 23, 2002 Abdullah ROI and May 19, 2004 Abdullah-investigation EC;
- several Thumairy and Bayoumi named upstream records;
- CIA `Al-Qa'ida Travel Issues` source recovery.

These gaps remain `unknown/unmapped` for independence purposes. They do **not** authorize an independence upgrade.

## Review 007 gate conclusion

The requirement to verify that no major current comparison is being counted twice through shared upstream sources is satisfied for the **present encoded corpus state**.

Any future object that changes one of these high-risk official-layer chains must update the audit deliberately and pass CI.

## Core rule

**Unresolved genealogy is a reason to withhold an independence claim, not a reason to assume one.**
