# Phase 2 Cross-Document Review 007B — Shared-Upstream Risk Register

## Status

`ACTIVE — anti-double-counting control`

This register identifies places where multiple BlackIndex documents may repeat, summarize, reinterpret, or audit the same upstream evidence.

Its purpose is to prevent document count from becoming evidence count.

## Core rule

**Two publications are not two independent corroborations when both depend on the same interview, serial, record check, financial record, telephone record, or prior synthesis.**

Independence must be evaluated at the lowest recoverable source layer.

## Current risk register

| Downstream documents | Shared-upstream risk | Current treatment | Next proof needed |
|---|---|---|---|
| Joint Inquiry + 9/11 Commission Final Report | `HIGH / PARTIALLY MAPPED` | both rely heavily on FBI investigative material concerning the California support network; do not count repeated Bayoumi/Thumairy facts twice | recover named FBI records and identify exact overlap |
| Commission staff work + Commission Final Report | `HIGH / STRUCTURAL` | same Commission institution; staff work fed hearings/statements/drafting; final report is an adopted synthesis, not an independent source family | map final-report footnotes to staff/source records where material |
| Terrorist Financing monograph + Commission Final Report | `HIGH / STRUCTURAL` | staff monograph and final report share Commission research and agency access | identify statements copied/reframed from shared staff work |
| Terrorist Travel monograph + Commission Final Report | `HIGH / STRUCTURAL` | shared Commission research; travel monograph also reuses prior DOJ OIG interview material | trace travel/watchlisting propositions to the underlying agency records/interviews |
| Joint Inquiry + CIA OIG 9/11 Accountability | `DEPENDENT / EXPLICIT` | CIA OIG states that its review focuses on Joint Inquiry findings relating to CIA | treat OIG as a review/accountability layer, not an independent confirmation of the Joint Inquiry finding itself |
| Commission Final Report + 2016 Operation Encore EC | `UNKNOWN-TO-HIGH / PARTIALLY OVERLAPPING` | both synthesize FBI interviews, communications and investigative records, but the exact shared serial set is not yet mapped | recover named 2001–2004 FBI records and compare against 2016 EC source chain |
| 2016 Operation Encore EC + 2021 closing synthesis | `DEPENDENT / ENCODED` | explicit dependency object already records reuse of the 2016 synthesis | no independent-count treatment unless a proposition is traced to genuinely new source material |
| Multiple later FBI rereviews | `UNKNOWN` | later date does not itself create independence | record which sources are new, which are reinterpreted, and which are copied forward |

## Topic-specific risks

### Bayoumi

Likely shared records include:

- Bayoumi interviews from 2003;
- Caysan Bin Don / Isamu Dyson statements;
- hotel/travel chronology;
- telephone records;
- employment records;
- FBI reporting concerning Saudi-government connections;
- earlier counterterrorism investigation records.

A later report that cites or paraphrases one of these records adds an institutional interpretation layer, not a new underlying observation.

### Thumairy

Likely shared records include:

- September/October/November 2002 FBI ECs concerning Thumairy;
- Mohdar Abdullah statements;
- Benomrane interviews;
- telephone-contact records;
- Thumairy's own 2004 interviews;
- mosque/community witness reporting.

Contact evidence, assistance evidence, knowledge, direction, and institutional authorization remain separate propositions even when derived from the same source record.

### Mohdar Abdullah

The highest overcount risk is statement recycling:

`Abdullah statement` → `FBI ROI/EC` → `Commission narrative` → `later FBI synthesis`

and separately:

`inmate statement about Abdullah` → `FBI EC` → `Commission narrative`.

Those are not independent corroboration chains unless a separate witness or record independently establishes the same proposition.

### Financing

Keep separate:

- al Qaeda organizational funding;
- funding of the 9/11 operation;
- domestic logistical assistance;
- financial transfers to individual support-network actors;
- government or institutional sponsorship.

A negative finding in one category must not be generalized into another.

## Evidence-counting rule for UI / analysis

Until a future formal corroboration counter exists, BlackIndex should use this manual rule:

1. Count the **underlying source event/record** once.
2. Preserve every downstream interpretation as a separate document/assertion.
3. Do not increase corroboration strength merely because several downstream documents repeat it.
4. Increase corroboration only when a genuinely independent source chain is identified.
5. Mark independence `unknown` when source genealogy is incomplete.

## Suggested future platform control

A later durable assertion/corroboration layer should expose:

- `source_family_id`
- `upstream_record_ids`
- `independence_status`
- `shared_upstream_count`
- `independent_source_count`

The UI should be able to say:

`5 downstream references / 2 independent upstream source families`

instead of showing a misleading raw count of five.

## Gate contribution

Review 007's shared-upstream requirement is considered **started and structurally controlled**, but not complete until the P0 named-source recovery scan in Review 007A has run against local EO 14040 text and high-confidence overlaps are encoded.

## Core rule

**Repetition measures narrative persistence. Independence measures corroboration. They are not the same thing.**
