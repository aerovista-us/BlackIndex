# BlackIndex — Living Status, Completion Ledger, and Backlog

**Status:** Authoritative project-progress ledger  
**Updated:** 2026-10-02
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

- Authoritative local verifier checkpoint: **70 checked / 0 failures** (`2026-10-02`; current corpus / Operation LOOKING GLASS FY2027 TACAMO longitudinal-schedule checkpoint)
- Historical Review 007M official-layer closeout checkpoint: **39 checked / 0 failures** (`2026-09-26`)
- Record Integrity coverage: **70 / 70 corpus documents** have durable record-integrity objects; **164 evidence objects / 0 validation failures** at this checkpoint.
- Historical Milestone 1: **25 verified / 0 failures**
- Operation Encore underlying-record acquisition: **4 / 4** large FBI artifacts acquired/resumed successfully
- Joint Inquiry final report is acquired/published as `US CONGRESS-2002-9-11-joint-inquiry-001`
- 9/11 Commission Final Report is acquired/published as `COMMISSION-2004-9-11-commission-001`
- Terrorist Financing staff monograph is acquired/published as `COMMISSION-2004-9-11-commission-terrorist-financing-staff-monograph-001`
- Terrorist Travel staff monograph is acquired/published as `COMMISSION-2004-9-11-commission-terrorist-travel-staff-monograph-001`
- CIA OIG 9/11 Accountability full report is acquired/published as `CIA-2005-9-11-cia-accountability-001`
- CIA OIG 2007 Executive Summary companion is acquired/published as `CIA-2005-9-11-cia-accountability-executive-summary-001`
- Review 007 local named-source scan: **25 normalized documents / 4657 text-page chunks / 15 targets**
- Review 007 localization result: **15/15 target families had a citation/synthesis hit; 2/15 also had EO 14040 FBI-container candidates; 13/15 remain citation-localized only**
- Review 007 physical-page result: **4/4 exact physical-page mappings; 0 unresolved; no OCR/fuzzy matching**
- Review 007 verified source bundle: **3/3 review slices ready; 0 boundary claims; 0 promotions**
- Review 007 visual boundary follow-up: **CAND-0005 corrected to physical pages 57-63; CAND-0013 confirmed at 116-122; Benomrane exact scan 138-210 remains on HOLD**
- Review 007C companion result: **official GPO/FDLP Executive Summary acquired; image-only; no OCR performed**
- Review 007G/007H Abdullah result: **official FBI April 2002 + May 2004 release bundles acquired; May 18 EC boundary confirmed at pp. 1-5 and May 17 EC boundary confirmed at pp. 6-13; no child promotion**
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
| Source genealogy / independence | `ACTIVE` | Report-level and named-source dependency maps encoded; local recovery scan distinguishes citations from container candidates. |
| Shared-upstream / anti-double-counting discipline | `COMPLETE` | Review 007K/L fail-closed audit covers 14 high-risk dependencies, 4 synthesis classifications, and 2 comparison guards; unresolved genealogy cannot raise corroboration strength. |
| Citation localization vs source recovery distinction | `COMPLETE` | 15/15 citation hits cannot be represented as 15 recovered source records; EO 14040 candidates are counted separately. |
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
| Grounded local AI research assistant | `COMPLETE` | Repo-backed assistant added in PR #25; local evidence context only. |
| AI research navigation modes | `COMPLETE` | Research-mode navigation added in PR #26. |
| Contextual help system | `COMPLETE` | In-product research guidance added in PR #27. |
| Inline meaning glossary | `COMPLETE` | Terminology definitions added in PR #28. |
| Grounded document comparison | `COMPLETE` | Document comparison added in PR #29 with source-grounded framing. |
| AI request reuse fix | `COMPLETE` | Browser Request-object reuse failure corrected in PR #30. |
| Nexus BlackIndex workspace launcher | `COMPLETE` | Registered in AeroVista Workspaces / Nexus; public path remains Cloudflare Access protected and launches the tailnet-only BlackIndex runtime. |
| Search/navigation utilities | `COMPLETE` | quick views, sort, shortcuts, deep links |
| Research Session observer safety fix | `COMPLETE` | idempotent/frame-coalesced observer path |
| Embedded dashboard favicon | `COMPLETE` | data-URI SVG; no external favicon asset required |
| Dashboard server reuse | `COMPLETE` | launcher reuses an existing healthy BlackIndex listener instead of drifting 8787→8788+ |
| FBI P0 Review Desk | `ACTIVE` | 27 P0 packets + source/boundary safeguards |
| Named-source recovery scanner | `COMPLETE` | read-only local normalized-text signature scanner; never promotes records or claims physical pages |
| Named Source Recovery UI | `COMPLETE` | standalone searchable page; separates Commission citation/synthesis hits from EO 14040 container candidates |
| Review 007 one-command local checkpoint | `COMPLETE` | executed successfully; sanitized self-report published |
| Physical PDF page mapper | `COMPLETE` | Review 007 exact mapper verified 4/4 named-source positions against physical PDF pages with no OCR/fuzzy matching |
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
| 9/11 Commission Final Report — official government edition | `PARTIAL` | acquired/resumed; Chapter 7 genealogy pass active |
| Terrorist Financing Staff Monograph | `PARTIAL` | acquired + published; normalized text available; principal negative finding encoded |
| 9/11 and Terrorist Travel monograph | `PARTIAL` | acquired + published; normalized text available |
| CIA IG 9/11 Accountability | `PARTIAL` | full report + 2007 Executive Summary preserved; seven pivotal Executive Summary pages visually verified without OCR; reviewed findings encoded; full-report/redaction comparison remains partial |
| Cross-document official-layer review 007 | `COMPLETE` | Review 007M closes the official-layer milestone at 39/0; residual named-source recovery, proposition-level genealogy, and targeted full-report/version work remain visible backlog |
| Review 007A named-source recovery map | `COMPLETE` | local scan complete: 15/15 any hits, 2/15 EO 14040 container-candidate families, 13/15 citation/synthesis only; unresolved targets carried into active named-source backlog |
| Review 007B shared-upstream risk register | `COMPLETE` | Review 007K audit checks 14 high-risk dependencies + 4 synthesis classifications + 2 comparison guardrails; 0 high-risk edges marked independent |
| Review 007C CIA OIG extraction plan | `PARTIAL` | required pivotal Executive Summary gate complete; targeted full-report/redaction/version comparison remains optional future research where material |
| Review 007C1 CIA OIG pivotal-page navigation map | `COMPLETE` | physical pages 1-3 and 9-12 visually confirmed as Roman v-vii and xiii-xvi; no OCR used |
| Review 007C2 CIA OIG pivotal-page verification | `COMPLETE` | scope/dependency, misconduct negative finding, no-single-point balance, watchlisting breakdown, and FBI-receipt uncertainty encoded as attributed investigator reviews |
| Review 007D recovery interpretation | `COMPLETE` | durable interpretation separates citation localization from underlying-container recovery; remaining recovery targets live in named-source backlog |
| Review 007E physical-page gate | `COMPLETE` | 4/4 target positions exact-mapped to physical PDF pages; 0 unresolved; no OCR/fuzzy matching |
| Review 007 verified source-image bundle | `COMPLETE` | 3/3 bounded review slices created only after every page in each range exact-matched the parent PDF |
| Review 007 boundary diagnostic | `COMPLETE` | structural pass preserved as historical precursor; later Review 007I visually corrected CAND-0005 and confirmed CAND-0013 |
| Review 007F boundary hypotheses | `COMPLETE` | historical hypotheses retained; Review 007I later corrected CAND-0005 to 57-63 and confirmed CAND-0013 at 116-122 |
| Review 007F Benomrane expansion | `COMPLETE` | exact physical-page scan 138-210 found no strong record-start signals and emitted no range; boundary recovery is on HOLD pending a new identifier/source lead |
| Review 007I EO 14040 visual boundary confirmation | `COMPLETE` | CAND-0005 corrected visually from 58-63 to 57-63; CAND-0013 visually confirmed at 116-122; no child promotion |
| Review 007J orphan raw artifact inventory | `COMPLETE` | all 41 raw artifacts audited against 39 metadata raw references; 2 legacy Commission artifacts inventoried, preserved, and classified as non-independent release/acquisition variants |
| Review 007K shared-upstream closeout audit | `COMPLETE` | 14 dependency edges, 4 synthesis classifications, and 2 comparison guardrails audited after Review 007L; no current high-risk official-layer chain is encoded independent |
| Review 007L Joint Inquiry Part Four release analysis | `COMPLETE` | current GovInfo Part Four public rendering and 2016 HPSCI declassified scan mapped as one dependent release family; “28 pages” distinguished from physical PDF count |
| Review 007M official-layer closeout reconciliation | `COMPLETE` | five original closeout gates satisfied to defined milestone; residual source recovery remains active backlog; next major corpus gate may open |
| Named upstream Thumairy source bundle | `ACTIVE` | Benomrane pages 173/175 are physically verified but boundary-unresolved on HOLD after exact scan 138-210; core 2002 Thumairy ECs remain unmapped |
| Named upstream Bayoumi source bundle | `ACTIVE` | visual boundaries now resolved: CAND-0005 = 57-63 (corrected), CAND-0013 = 116-122 (confirmed); neither later record is treated as the exact Commission-cited original interview; other Bayoumi records remain unmapped |
| Named upstream Mohdar Abdullah source bundle | `ACTIVE` | May 18 EC visually boundary-confirmed at FBI Vault parent pp. 1-5; May 17 EC visually boundary-confirmed at pp. 6-13; exact July 23, 2002 ROI and May 19, 2004 EC remain unresolved |
| Review 007G Abdullah official FBI recovery | `COMPLETE` | both official FBI parent release bundles acquired at 39/0; Review 007H confirmed May 17/18 record boundaries and found no duplicate copy in the current FBI corpus |
| Review 007H May 2004 FBI boundary confirmation | `COMPLETE` | Commission note 22 → May 18 EC pp. 1-5; note 23 → May 17 EC pp. 6-13; source-image confirmed, no child promotion |
| Official-layer source dependency objects | `ACTIVE` | Joint Inquiry, Commission final, staff monographs, CIA OIG, Encore and named source bundles encoded in part |
| Bayoumi statement evolution | `ACTIVE` | Commission 2004 vs FBI 2016 comparison object created; shared records still to map |
| Thumairy statement evolution | `ACTIVE` | Commission scoped negative finding vs later FBI rereview comparison object created |
| Principal negative-finding objects | `COMPLETE` | current closeout set includes Commission Thumairy/Bayoumi, financing-monograph, and scoped CIA OIG findings/uncertainties as attributed investigator reviews |
| Joint Inquiry “28 Pages” version family | `COMPLETE` | Review 007L maps current GovInfo Part Four rendering to the 2016 HPSCI declassified scan; same source family, dependent release lineage |
| Operation LOOKING GLASS official USAF baseline | `ACTIVE` | authority-family public layer, TACAMO/NIGHTWATCH baseline, NC3 governance/modernization layer, detailed Navy FY2026 and FY2027 BA5 TACAMO states, NAVAIR HTML program pages, E-130J award records, and contractor-primary SAOC risk-reduction flight-test evidence acquired; corpus 70/0; TACAMO execution-confirmation records, Air Force SAOC Volume II, AFGSCMD 63-101, and government acceptance/performance evidence remain explicit gaps |
| LOOKING GLASS DoD FY1966 program record | `COMPLETE` | contemporaneous DoD annual report preserved as `DOD-1967-department-of-defense-annual-reports-001`; PACCS/EC-135/airborne launch-control statements reviewed; exact authority chain not inferred |
| LOOKING GLASS AFGSCI 13-5302V2 directive | `COMPLETE TO SOURCE-MAP MILESTONE` | official 19 Jul 2017 ALCS crew Stan/Eval directive preserved as `USAF-2017-air-force-global-strike-command-instructions-001`; document is Canon, cited EWO/STRATCOM/technical-order family remains unresolved |
| LOOKING GLASS AFI 91-117 acquisition | `BLOCKED` | 29 Aug 2022 public first-party candidate identified; NXCore direct fetch 403 and both navigation/browser-TLS retries 404 on 2026-09-27; no mirror ingested, corpus remains 45/0 |
| LOOKING GLASS AFPD 13-5 / AFI 13-520 recovery | `COMPLETE TO VERSION/SOURCE-LINEAGE MILESTONE` | both official Air Force artifacts preserved; AFI 13-520 explicitly supersedes AFI 13-530 dated 8 Sep 2015; predecessor remains unrecovered from first-party host |
| LOOKING GLASS TACAMO / NIGHTWATCH baseline | `COMPLETE TO OFFICIAL MISSION/COMMAND BASELINE MILESTONE` | USSTRATCOM 2024 posture statement, Navy Program Guide 2017, and AFMAN 11-2E-4B V3 preserved; corpus 48/0; detailed procedures intentionally excluded from analytical findings |
| NC3 public governance / controlled-access baseline | `COMPLETE TO FIRST SOURCE-GENEALOGY MILESTONE` | DoDI 3741.01, DoDD 3700.01, CJCSI 5119.01C plus public placeholders for S-3730.01, S-3710.01 and S-5210.81 preserved; controlled contents not inferred |
| NC3 modernization / governance currency | `COMPLETE TO MODERNIZATION/CURRENCY MILESTONE` | 2022 NPR, 2025/2026 USSTRATCOM posture statements, S-5100.92 placeholder, 2024-2026 posture version family, and 2026-10-01 issuance-index currency snapshot encoded |
| NC3 program-source genealogy | `COMPLETE TO DETAILED NAVY-PARENT / PARTIAL AIR-FORCE-PARENT MILESTONE` | DoD FY2026 R-1 SAOC PE 0604288F index lineage and the detailed Navy FY2026 BA5 TACAMO PE 0605180N parent are preserved; the BA1-3 Navy index is explicitly dependent on the BA5 parent. Detailed Air Force SAOC Volume II remains transport-blocked from NXCore and AFGSCMD 63-101 remains unrecovered |
| NC3 TACAMO detailed BA5 recovery | COMPLETE TO DETAILED BUDGET-RECOVERY MILESTONE | Official Navy FY2026 BA5 PE 0605180N / Project 3259 parent preserved and reviewed; June 2025 schedule includes planned PDR/build/integration/CSIL/Integrated Test 1 states; corpus 68/0; no scheduled milestone is promoted as completed without later execution evidence |
| NC3 TACAMO FY2027 longitudinal update | `COMPLETE TO LONGITUDINAL BUDGET-STATE MILESTONE` | Official April 2026 Navy FY2027 BA5 PE 0605180N state preserved; source explicitly says the current program schedule was updated, records FY2026 funding at $1,043.978M after a $200M congressional directed reduction, funds purchase of three FY2027 SDTAs, and extends multiple aircraft-build/integration/CSIL/IT1 windows into FY2027-2031; corpus 70/0; completion/delivery/test/acceptance remains unresolved in `ME-NC3-tacamo-execution-confirmation` |
| NC3 HTML program-page capture | `COMPLETE TO HTML-CAPTURE/PROGRAM-PUBLICATION MILESTONE` | first-party NAVAIR product page and dated 2024 E-130J announcement preserved as immutable HTML with visible-text derivatives; corpus 62/0; PMA-271 shared lineage encoded |
| NC3 E-130J award-state resolution | `COMPLETE TO AWARD-STATE/RETRIEVAL-RETRY MILESTONE` | DoD 18 Dec 2024 contract action and Navy 19 Dec 2024 award announcement preserved; earlier planned-award state resolved at corpus 64/0; detailed Navy BA5 was later recovered; detailed SAOC/AFGSCMD retrieval gaps remain explicit |
| NC3 execution-milestone baseline | `ACTIVE — CONTRACTOR EXECUTION + TACAMO LONGITUDINAL LAYERS ADDED` | Historical government execution baseline closed at corpus 67/0; SAOC contract award, 95th Wing activation, NC3 Enterprise Center IOC, SNC contractor-primary reporting of the 7 Aug 2025 SAOC EMD risk-reduction flight, and the Navy FY2026→FY2027 TACAMO schedule revision are preserved as separate time-bounded states; current corpus 70/0. Neither budget scheduling nor SNC reporting is treated as government acceptance/certification/performance evidence; delivery/readiness/FOC/use remain uninferred |

### Assassination records

- JFK 2025–2026 releases — `QUEUED`
- MLK 2025 release — `QUEUED`
- RFK / KENSALT 2025 release — `QUEUED`

### Nuclear / continuity

- Operation LOOKING GLASS — `ACTIVE` — public ALCS authority-policy layer, TACAMO/NIGHTWATCH mission baseline, NC3 governance/modernization stack, detailed Navy FY2026 + FY2027 BA5 TACAMO states, first-party NAVAIR HTML capture, E-130J award action, SAOC contract action, 95th Wing activation, NEC IOC, and SNC contractor-primary SAOC risk-reduction flight-test reporting acquired; current corpus 70/0; next gate is first-party TACAMO PDR/build/CSIL/IT1/SDTA execution confirmation, U.S. government SAOC test/acceptance/certification/performance evidence, and periodic recovery of detailed Air Force SAOC plus AFGSCMD 63-101
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

## Controlled Sprint — 2026-08-27/28 — 9/11 Official-Layer Closeout

**Initial sprint script:** `tools/ingest-phase2-911-official-closeout.sh`  
**Initial run report:** `docs/run-reports/2026-08-27-911-official-closeout.md`  
**Collision-safe resume:** `tools/ingest-phase2-911-official-closeout-resume.sh`  
**Resume run report:** `docs/run-reports/2026-08-27-911-official-closeout-resume.md`  
**Review gate:** `docs/reviews/phase2-cross-document-007-911-official-closeout.md`  
**Named-source map:** `docs/reviews/phase2-cross-document-007a-911-named-source-recovery-map.md`  
**Shared-upstream control:** `docs/reviews/phase2-cross-document-007b-shared-upstream-risk-register.md`  
**CIA OIG extraction plan:** `docs/reviews/phase2-cross-document-007c-cia-oig-extraction-plan.md`  
**Named-source result analysis:** `docs/reviews/phase2-cross-document-007d-named-source-recovery-analysis.md`  
**Named-source run report:** `docs/run-reports/2026-08-27-review-007-named-source-recovery.md`  
**CIA OIG Executive Summary checkpoint:** `docs/run-reports/2026-08-28-review-007c-cia-oig-executive-summary.md`

### Final acquisition result

- Initial run: **2 / 4** successful/resumed; verifier **33 / 0**
- Collision-safe resume: **2 / 2** successful; verifier **36 / 0**
- CIA OIG Executive Summary companion: **1 / 1 acquired**; verifier **37 / 0**
- Final Report: existing artifact resumed successfully
- CIA OIG Accountability full report: acquired/published successfully
- CIA OIG Executive Summary: acquired/published successfully from official GPO/FDLP PURL as `CIA-2005-9-11-cia-accountability-executive-summary-001`; image-only; no OCR
- Financing monograph: recovered under dedicated canonical collection namespace
- Travel monograph: recovered under dedicated canonical collection namespace
- Existing immutable artifact from the failed shared namespace was preserved, not overwritten or deleted
- Core intake was hardened so future source labels and orphan raw slots cannot reproduce this class of collision

### Named-source recovery result

The controlled local Review 007 scan completed with **36 / 0** verifier status and no evidence-state mutation.

- 25 normalized documents scanned
- 4657 normalized text-page chunks scanned
- 15 named source target families
- 15 / 15 had at least one candidate occurrence somewhere in the corpus
- 2 / 15 also had candidate occurrences inside EO 14040 FBI release containers
- 13 / 15 were localized only through citation/synthesis text under the current signatures
- 0 child records promoted
- physical-page mapping later verified 4 / 4 target positions exactly

EO 14040 candidate families:

- Caysan Bin Don / Isamu Dyson → `FBI-2022-eo14040-2-c-001`, physical/normalized pages 60 and 118; mapped to bracketed P0 hypotheses CAND-0005 and CAND-0013
- Qualid Moncef Benomrane → `FBI-2021-eo14040-2-b-i-001`, physical/normalized pages 173 and 175; widened exact scan 138-210 found no strong boundary signal; boundary recovery is on HOLD

These remain **candidate localizations**, not automatically promoted child records. The remaining 13 source families remain `UNMAPPED_REFERENCED_EVIDENCE` rather than absent/destroyed.

### Source-genealogy result so far

The closeout sources are explicitly prevented from being counted as independent confirmations merely because they are separate official publications.

Encoded relationships include:

- Joint Inquiry support-network assertions → underlying FBI records
- Commission Chapter 7 → FBI/CIA source classes cited in its notes
- Commission Thumairy finding → named 2002–2004 FBI interview/EC source bundle
- Commission Bayoumi finding → named FBI/CIA interview, hotel, employment, telecom and analytic source bundle
- Commission Mohdar Abdullah treatment → named FBI interview/EC source bundle
- Financing staff monograph → classified intelligence, law-enforcement, State/Treasury files, interviews, and shared staff work
- Travel staff monograph → agency records, Commission interviews, prior DOJ OIG interviews, and shared staff work
- CIA OIG full report → Joint Inquiry findings relating to CIA
- CIA OIG Executive Summary → companion/subset release in the same CIA OIG lineage; not independent corroboration
- 2016 Operation Encore EC → underlying FBI serials/interviews/liaison/analysis
- 2021 closing synthesis → 2016 EC

A Commission citation is explicitly treated as a **source address**, not independent corroboration or proof that the cited record has been recovered.

### Sprint / Review 007 stop gate

Do **not** count repeated statements across Joint Inquiry, Commission staff work, Commission final report, CIA OIG full/summary releases, and Operation Encore as independent corroboration until the remaining named underlying source records are mapped.

## Current operational order

1. `COMPLETE 2026-09-26` — visually reviewed `CAND-0005` and `CAND-0013`; corrected 0005 to `57-63`, confirmed 0013 at `116-122`, and kept both unpromoted as source-recovery objects.
2. Leave the Benomrane boundary search on `HOLD` until a new identifier/source lead justifies reopening it.
3. `PARTIAL/ACTIVE` — Executive Summary pivotal-page gate is complete without OCR (Review 007C2); targeted full-report/redaction/version comparison remains open where materially useful.
4. Continue targeted recovery for citation-only named source families, especially the 2002 Thumairy ECs, Bayoumi interview/records set, Abdullah ECs, and CIA `Al-Qa'ida Travel Issues` report.
5. `COMPLETE TO CLOSEOUT MILESTONE 2026-09-26` — principal negative findings are encoded with exact wording/scope; add future findings only when new research questions require them.
6. `COMPLETE 2026-09-26` — Review 007K made the shared-upstream audit reproducible and fail-closed; unresolved genealogy remains non-independent and cannot raise corroboration strength.
7. Review the generated local record-integrity files deliberately; do not commit them merely to clean the working tree.
8. `COMPLETE 2026-09-26` — inventoried both metadata-unreferenced raw artifacts: financing monograph legacy byte variant and standalone Chapter 7 subset; both preserved immutably and linked through version-family objects.
9. `COMPLETE 2026-09-26` — Review 007L mapped the Joint Inquiry Part Four / “28 Pages” release family and encoded the 2016 release as dependent on the same source lineage.
10. `ACTIVE 2026-10-02` — Operation LOOKING GLASS / NC3 recovery now includes the ALCS authority-policy layer, TACAMO/NIGHTWATCH mission records, NC3 governance/modernization stack, SAOC PE 0604288F DoD budget lineage, detailed Navy FY2026 and FY2027 BA5 TACAMO PE 0605180N states, first-party NAVAIR HTML program publications, the Dec 2024 E-130J contract action, the Apr 2024 SAOC contract action, the Feb 2025 95th Wing activation, the Apr 2019 NEC IOC, and SNC contractor-primary reporting of the 7 Aug 2025 SAOC EMD risk-reduction flight. Corpus is 70/0. The April 2026 Navy budget explicitly updates the current TACAMO schedule and extends multiple build/integration/test windows into FY2027-2031. Next: first-party PDR/build/CSIL/IT1/SDTA execution confirmation, U.S. government SAOC acceptance/performance evidence, and periodic recovery of detailed Air Force SAOC Volume II plus AFGSCMD 63-101; controlled directive contents remain explicit gaps.
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
