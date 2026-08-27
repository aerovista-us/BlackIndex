# BlackIndex — Living Status, Completion Ledger, and Backlog

**Status:** Authoritative project-progress ledger  
**Updated:** 2026-08-27  
**Purpose:** Keep completed work visible while preserving the remaining research and implementation backlog.

> Completion here means the currently defined ingestion, review, or implementation milestone was reached. It does **not** mean the underlying historical question is resolved.

## Status legend

- `COMPLETE` — implemented or acquired/reviewed to the current milestone
- `ACTIVE` — in use and being extended
- `PARTIAL` — meaningful work exists; cluster/capability remains incomplete
- `PREPARED` — ingestion/code path exists; local execution or review still required
- `QUEUED` — explicitly in backlog; not yet materially implemented/ingested
- `HOLD` — deliberately paused pending a review/dependency
- `SUPERSEDED` — older implementation/acquisition target retained for history but replaced by a better current path

## Corpus checkpoint

- Authoritative local verifier checkpoint: **36 checked / 0 failures** (`2026-08-27` official-closeout resume)
- Historical Milestone 1: **25 verified / 0 failures**
- Operation Encore underlying-record acquisition: **4 / 4** large FBI artifacts acquired/resumed successfully
- Joint Inquiry final report is acquired/published as `US CONGRESS-2002-9-11-joint-inquiry-001`
- 9/11 Commission Final Report is acquired/published as `COMMISSION-2004-9-11-commission-001`
- Terrorist Financing staff monograph is acquired/published as `COMMISSION-2004-9-11-commission-terrorist-financing-staff-monograph-001`
- Terrorist Travel staff monograph is acquired/published as `COMMISSION-2004-9-11-commission-terrorist-travel-staff-monograph-001`
- CIA OIG 9/11 Accountability is acquired/published as `CIA-2005-9-11-cia-accountability-001`
- Raw source artifacts remain local-only
- GitHub stores metadata/provenance, reviewed extractions, evidence-map objects, lineage, schemas, governance, tooling, and controlled-run reports

The local verifier remains authoritative for raw-corpus integrity.

## Methodology / evidence-model status

| Item | Status | Notes |
|---|---|---|
| Neutral evidence-map posture; no mandatory `PROVES / DOES NOT PROVE` | `COMPLETE` | Core project rule established. |
| Investigator Reliability | `COMPLETE` | Investigator review object/tooling exists. |
| Negative Findings rule | `COMPLETE` | Official/investigative conclusions remain attributed claims. |
| Redaction Analysis | `COMPLETE` | Framework + metadata discipline established. |
| Record Integrity objects | `COMPLETE` | Durable object workflow implemented. |
| Missing Evidence objects | `COMPLETE` | Durable object workflow implemented. |
| Destruction chronology | `PARTIAL` | Methodology defined; encoded corpus-by-corpus. |
| Classification chronology | `PARTIAL` | Methodology defined; encoded when source record supports it. |
| Public vs Internal comparisons | `COMPLETE` | Statement-comparison tooling exists. |
| Timeline evolution of official conclusions | `ACTIVE` | 9/11 official-layer comparison 007 active; Bayoumi/Thumairy evolution objects exist. |
| Source genealogy / independence | `ACTIVE` | Report-level and named-source dependency maps now encoded; local source recovery scan is next gate. |
| Shared-upstream / anti-double-counting discipline | `ACTIVE` | Review 007B risk register now separates narrative repetition from independent corroboration. |
| Evidence Integrity | `PARTIAL` | Methodology locked; systematic digital/video/audio/physical records still expanding. |
| Capability Registry | `QUEUED` | First-class durable capability object family still needed. |
| Discovery Layer | `QUEUED` | First-class durable discovery workflow still needed. |
| Entity / relationship graph | `ACTIVE` | Explicit mentions + genealogy + research xrefs; no culpability inference. |
| State of Record `R0–R5` | `COMPLETE` | Investigation maturity, not truth. |
| Inference Dependency `D0–D4` | `COMPLETE` | Direct evidence vs inference-chain discipline. |

## Platform / UI status

| Component | Status | Notes |
|---|---|---|
| Core CLI | `COMPLETE` | init/intake/verify/manifest/search/normalize/publish |
| URL ingestion pipeline | `COMPLETE` | provenance/hash/dedupe/normalize |
| Intake source-token / orphan-raw hardening | `COMPLETE` | canonical/path-safe source IDs; legacy metadata enumeration; immutable raw slots reserve sequence numbers |
| FBI/CIA browser-TLS fallback | `COMPLETE` | normal curl → browser-navigation → browser-TLS impersonation on constrained official hosts |
| Durable evidence objects | `COMPLETE` | integrity, missing evidence, versions, dependencies, statements, investigator reviews |
| Object validation + CI | `COMPLETE` | object-quality workflow active |
| Source Lineage + UI | `ACTIVE` | dependency graph and independence discipline; official 9/11 layer and named-source bundles encoded |
| Entity Index + UI | `COMPLETE` | explicit metadata/genealogy only |
| Work Queue | `COMPLETE` | review backlog, missing refs, review-state drift |
| Record Context | `COMPLETE` | per-record traversal of encoded relationships/gaps/reviews/versions |
| Research Session | `COMPLETE` | browser-local pins + recent records |
| Research Session export | `COMPLETE` | pinned IDs, JSON, Markdown, clear recent |
| Search/navigation utilities | `COMPLETE` | quick views, sort, shortcuts, deep links |
| Research Session observer safety fix | `COMPLETE` | idempotent/frame-coalesced observer path |
| Embedded dashboard favicon | `COMPLETE` | data-URI SVG; no external favicon asset required |
| FBI P0 Review Desk | `ACTIVE` | 27 P0 packets + source/boundary safeguards |
| Named-source recovery scanner | `COMPLETE` | read-only local normalized-text signature scanner; never promotes records or claims physical pages |
| Named Source Recovery UI | `COMPLETE` | standalone searchable local page; candidate hit and physical-page warnings preserved |
| Review 007 one-command local checkpoint | `PREPARED` | scanner + audits + verifier + sanitized self-report in one command; local run still required |
| Physical PDF page mapper | `QUEUED` | required before segment/text-page indices can be treated as physical pages |
| Capability Registry UI | `QUEUED` | waits on durable capability object family |
| Discovery Inbox UI | `QUEUED` | waits on durable Discovery object workflow |

## Research / ingestion ledger

### Core covert activity / intelligence collection

| Cluster | Status |
|---|---|
| Operation NORTHWOODS | `COMPLETE` |
| MKULTRA | `COMPLETE` |
| MKSEARCH deeper material | `PARTIAL` |
| CIA Family Jewels | `COMPLETE` |
| Church Committee | `COMPLETE` |
| COINTELPRO | `COMPLETE` |
| SHAMROCK / MINARET | `COMPLETE` |
| Operation CHAOS / MHCHAOS | `PARTIAL` |

### Regime change / covert action

| Cluster | Status |
|---|---|
| TPAJAX — Iran 1953 | `PARTIAL` |
| PBSUCCESS — Guatemala 1954 | `PARTIAL` |
| Chile / Allende | `QUEUED` |
| Congo / Lumumba | `QUEUED` |
| Bay of Pigs | `QUEUED` |
| Operation MONGOOSE | `QUEUED` |

### Vietnam

| Cluster | Status |
|---|---|
| Pentagon Papers | `PARTIAL` |
| Gulf of Tonkin | `PARTIAL` |
| Cambodia / Laos covert-war records | `QUEUED` |

### 9/11 / Operation Encore

| Layer | Status | Notes |
|---|---|---|
| 2016 Operation Encore EC | `COMPLETE` | substantively reviewed/extracted |
| EO 14040 §2(b)(i) Part 1 | `COMPLETE` | acquired/verified |
| EO 14040 §2(b)(i) Part 2 | `COMPLETE` | acquired/verified |
| EO 14040 §2(c) Part 1 | `COMPLETE` | acquired/verified |
| Source-container segmentation | `COMPLETE` | 108 heuristic candidates |
| Candidate triage | `COMPLETE` | P0=27, P1=27, P2=34, P3=20 |
| P0 review packets | `COMPLETE` | 27 packets |
| P0 source-review bundle | `COMPLETE` | 7 FD-302 slices; 6 likely complete, 1 boundary review needed |
| Individual child promotion | `HOLD` | do not claim promotion until source/page/boundary checks are satisfied |
| Joint Inquiry final report | `PARTIAL` | acquired + published as `US CONGRESS-2002-9-11-joint-inquiry-001`; substantive review pending |
| 9/11 Commission Chapter 7 standalone acquisition target | `SUPERSEDED` | retain as review focus; acquisition replaced by full official GovInfo final report |
| 9/11 Commission Final Report — official government edition | `PARTIAL` | acquired/resumed as `COMMISSION-2004-9-11-commission-001`; Chapter 7 genealogy pass active |
| Terrorist Financing Staff Monograph | `PARTIAL` | acquired + published; normalized text available; principal negative finding encoded |
| 9/11 and Terrorist Travel monograph | `PARTIAL` | acquired + published; normalized text available |
| CIA IG 9/11 Accountability | `PARTIAL` | acquired + published; image-only primary PDF preserved; deliberate extraction plan 007C prepared |
| Cross-document official-layer review 007 | `ACTIVE` | acquisition closed at 36/0; source genealogy, wording evolution, negative findings and anti-double-counting controls active |
| Review 007A named-source recovery map | `ACTIVE` | named Thumairy/Bayoumi/Abdullah upstream records prioritized; local container scan pending |
| Review 007B shared-upstream risk register | `ACTIVE` | structural and proposition-level overcount risks explicitly recorded |
| Review 007C CIA OIG extraction plan | `PREPARED` | preserve primary image-only artifact; official text-bearing companion preferred; OCR last-resort derivative |
| Named upstream Thumairy source bundle | `ACTIVE` | dependency + `UNMAPPED_REFERENCED_EVIDENCE` object created; local recovery scan pending |
| Named upstream Bayoumi source bundle | `ACTIVE` | dependency + `UNMAPPED_REFERENCED_EVIDENCE` object created; local recovery scan pending |
| Named upstream Mohdar Abdullah source bundle | `ACTIVE` | dependency + `UNMAPPED_REFERENCED_EVIDENCE` object created; local recovery scan pending |
| Official-layer source dependency objects | `ACTIVE` | Joint Inquiry, Commission final, staff monographs, CIA OIG, Encore and named source bundles encoded in part |
| Bayoumi statement evolution | `ACTIVE` | Commission 2004 vs FBI 2016 comparison object created; shared records still to map |
| Thumairy statement evolution | `ACTIVE` | Commission scoped negative finding vs later FBI rereview comparison object created |
| Principal negative-finding objects | `ACTIVE` | Commission Thumairy, Commission Bayoumi, and financing-monograph findings preserved as attributed investigator reviews |
| Joint Inquiry “28 Pages” version family | `QUEUED` | dedicated release/version analysis after closeout comparison gate |

### Assassination records

- JFK 2025–2026 releases — `QUEUED`
- MLK 2025 release — `QUEUED`
- RFK / KENSALT 2025 release — `QUEUED`

### Nuclear / continuity

- Operation LOOKING GLASS — `QUEUED`
- SIOP / SAC / Emergency War Orders / TACAMO / NEACP / NIGHTWATCH — `QUEUED`

### Intelligence / political controversies

- 2016 ICA / 2025 CIA Tradecraft Review — `QUEUED`
- Durham Classified Appendix — `QUEUED`
- Crossfire Hurricane — `QUEUED`
- Atkinson / 2019 impeachment-related declassifications — `QUEUED`
- Strategic Implementation Plan for Countering Domestic Terrorism — `QUEUED`

### Detention / interrogation

- CIA Detention and Interrogation Program — `QUEUED`
- Senate torture-report materials — `QUEUED`
- DOJ interrogation memoranda — `QUEUED`
- Black-site / rendition / detainee-transfer records — `QUEUED`

### Other historical / scientific clusters

- VENONA — `QUEUED`
- Nazi war-crimes / intelligence recruitment — `QUEUED`
- Iran-Contra — `PARTIAL`
- Iraq WMD intelligence — `QUEUED`
- STARGATE — `QUEUED`
- UAP / AARO / IMMACULATE CONSTELLATION — `QUEUED`
- COVID origins releases — `QUEUED`
- Overseas biological laboratory records — `QUEUED`
- Edgewood / human experimentation — `QUEUED`
- Amelia Earhart government records — `QUEUED`

## Entity / capability / testimonial backlog

| Item | Status | Notes |
|---|---|---|
| Rothschild genealogy baseline | `PARTIAL` | baseline/entity methodology exists |
| Victor Rothschild / Blunt / MI5 | `QUEUED` | high-priority Rothschild evidence cluster |
| Toka organization record | `QUEUED` | separate company claims from independent reporting |
| Toka camera/IoT capability records | `QUEUED` | capability evidence only; not proof of use in an event |
| Itzhak Bentov / Gateway | `QUEUED` | primary writings → Monroe/Gateway → INSCOM → later interpretation |
| Project Camelot source class | `QUEUED` | testimonial/lead-generation layer only |
| Dr. Pete Peterson assertion node | `QUEUED` | claims stored individually |
| Weston Price / Vitamin K2 | `QUEUED` | lower-priority lead |
| Chimaera monstrosa | `QUEUED` | unresolved-context discovery |

## Controlled Sprint — 2026-08-27 — 9/11 Official-Layer Closeout

**Initial sprint script:** `tools/ingest-phase2-911-official-closeout.sh`  
**Initial run report:** `docs/run-reports/2026-08-27-911-official-closeout.md`  
**Collision-safe resume:** `tools/ingest-phase2-911-official-closeout-resume.sh`  
**Resume run report:** `docs/run-reports/2026-08-27-911-official-closeout-resume.md`  
**Review gate:** `docs/reviews/phase2-cross-document-007-911-official-closeout.md`  
**Named-source map:** `docs/reviews/phase2-cross-document-007a-911-named-source-recovery-map.md`  
**Shared-upstream control:** `docs/reviews/phase2-cross-document-007b-shared-upstream-risk-register.md`  
**CIA OIG extraction plan:** `docs/reviews/phase2-cross-document-007c-cia-oig-extraction-plan.md`

### Final acquisition result

- Initial run: **2 / 4** successful/resumed; verifier **33 / 0**
- Collision-safe resume: **2 / 2** successful; verifier **36 / 0**
- Final Report: existing artifact resumed successfully
- CIA OIG Accountability: newly acquired/published successfully
- Financing monograph: recovered under dedicated canonical collection namespace
- Travel monograph: recovered under dedicated canonical collection namespace
- Existing immutable artifact from the failed shared namespace was preserved, not overwritten or deleted
- Core intake was hardened so future source labels and orphan raw slots cannot reproduce this class of collision

### Source-genealogy result so far

The closeout sources are explicitly prevented from being counted as independent confirmations merely because they are separate official publications.

Encoded relationships now include:

- Joint Inquiry support-network assertions → underlying FBI records
- Commission Chapter 7 → FBI/CIA source classes cited in its notes
- Commission Thumairy finding → named 2002–2004 FBI interview/EC source bundle
- Commission Bayoumi finding → named FBI/CIA interview, hotel, employment, telecom and analytic source bundle
- Commission Mohdar Abdullah treatment → named FBI interview/EC source bundle
- Financing staff monograph → classified intelligence, law-enforcement, State/Treasury files, interviews, and shared staff work
- Travel staff monograph → agency records, Commission interviews, prior DOJ OIG interviews, and shared staff work
- CIA OIG CIA-accountability frame → Joint Inquiry findings relating to CIA
- 2016 Operation Encore EC → underlying FBI serials/interviews/liaison/analysis
- 2021 closing synthesis → 2016 EC

Exact Git-backed searches did not locate the highest-priority named Commission source records as individually promoted records. Their state is therefore `UNMAPPED_REFERENCED_EVIDENCE`, **not** absent/destroyed; they may already be embedded in the local EO 14040 containers.

### Local Review 007 checkpoint prepared

`tools/run-review-007-local.sh` is the next controlled local step. It:

1. scans local normalized records for the named source signatures;
2. runs dependency and review-state audits;
3. generates the Named Source Recovery UI;
4. runs the full corpus verifier;
5. writes local-only detailed recovery outputs;
6. publishes a **sanitized** Git-backed run report containing target labels, parent document IDs/SHA-256s and text-page indices, but no normalized-text previews;
7. performs no evidence-state mutation and no child promotion.

A scanner hit remains a candidate until the source boundary and physical page are verified.

### Sprint / Review 007 stop gate

Do **not** count repeated statements across Joint Inquiry, Commission staff work, Commission final report, CIA OIG, and Operation Encore as independent corroboration until the remaining named underlying source records are mapped.

## Current operational order

1. Run `tools/run-review-007-local.sh` on the local BlackIndex corpus; its sanitized report will self-publish if no unrelated files are already staged.
2. Read the published named-source recovery report and map high-confidence parent-container hits; do not promote child records yet.
3. Verify candidate source boundaries and physical pages before any child promotion.
4. Continue negative-finding encoding with exact wording, scope, evidence access and competing later findings.
5. Use Review 007B to audit shared-upstream source families before increasing corroboration strength.
6. Advance Review 007C using an official text-bearing CIA OIG companion if available; do not replace the image-only primary artifact or silently OCR it.
7. Review generated local record-integrity objects and publish them deliberately; do not commit them merely to clean the working tree.
8. Inventory the preserved orphan immutable raw artifact from the failed first-pass staff-monograph namespace rather than deleting it.
9. Implement the physical PDF page mapper before treating FBI segment/text indices as physical page citations.
10. Once the 9/11 official-layer comparison gate is satisfied, default next corpus expansion is Operation LOOKING GLASS.
11. Discovery objects, Capability Registry, Toka, and Bentov/Gateway remain queued platform/research work after the current corpus gate.

## Completion logging rule

**Never delete a completed backlog item.** Change its state instead:

`QUEUED → PREPARED → PARTIAL/ACTIVE → COMPLETE`

Use `SUPERSEDED` when an older target/path remains historically relevant but a safer or more authoritative replacement becomes the active path.

When possible, attach completion evidence:

- document IDs
- commit SHA
- verifier result
- extraction/review path
- evidence-map objects created
- known limitations/open questions

This file is the durable project-progress ledger. The full living methodology should carry this same completion state so BlackIndex can reconstruct how both the corpus and the method evolved over time.
