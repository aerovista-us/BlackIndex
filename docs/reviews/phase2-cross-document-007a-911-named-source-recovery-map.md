# Phase 2 Cross-Document Review 007A — 9/11 Named-Source Recovery Map

## Status

`ACTIVE — upstream-source recovery`

This map pushes Review 007 below the report/synthesis layer and identifies the named records cited by the 9/11 Commission for the Southern California support-network questions.

It is a recovery map, not a historical finding.

## Why this layer matters

The Commission Final Report is not independent evidence for each factual proposition it contains. Chapter 7 explicitly relies on FBI electronic communications, reports of investigation, interviews, telephone records, hotel records, employment records, immigration records, CIA analysis, and Commission interviews.

A later FBI synthesis such as the April 4, 2016 Operation Encore EC may reuse or reassess some of the same underlying record classes. Therefore:

`Commission statement + later FBI statement != two independent confirmations`

until the underlying source genealogy is mapped.

## Commission source anchors

The official Government Printing Office edition places the relevant discussion in Chapter 7, with source detail in the Notes to Chapter 7. The highest-value notes for the current recovery pass are notes 9-23, especially 13-20.

### Thumairy source chain

Priority named records:

| Priority | Record | Why it matters | BlackIndex state |
|---|---|---|---|
| P0 | FBI EC `Fahad Al-Thumairy` — 2002-09-04 | Benomrane / mosque / possible consular-assistance lead; also Khallam-related reporting | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC `Fahad Althumairy` — 2002-10-25 | Thumairy / Mohdar Abdullah relationship and local-network reporting | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC `Fahad Al-Thumairy` — 2002-11-20 | telephone-contact evidence between Bayoumi and Thumairy | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI ROI/interview Mohdar Abdullah — 2002-07-23 | Abdullah's account of relationships and assistance | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | Qualid Moncef Benomrane FBI interviews — 2002-03-07, 2002-03-13, 2002-05-23 | lead tested by Commission before its scoped negative finding | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | Fahad al-Thumairy interviews — 2004-02-23 through 2004-02-25 | Thumairy denials / Commission direct interview layer | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | Ashour E. interview — 2004-05-20 | Benomrane / corroboration review | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | FBI LHMs on Mohamed Aliter and Mohammed bin Suleiman al Muhanna — 2002-12-02 / 2003-07-09 | Thumairy religious/institutional context | `UNMAPPED_REFERENCED_EVIDENCE` |
| P2 | DOS memo Karl Hoffman to Commission — 2004-06-08 | State Department entry/refusal and related materials | `UNMAPPED_REFERENCED_EVIDENCE` |

### Bayoumi source chain

| Priority | Record | Why it matters | BlackIndex state |
|---|---|---|---|
| P0 | FBI EC `Omar Ahmed Al Bayoumi` — 1999-06-07 | earlier counterterrorism investigation and closure | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI LHM investigation of Bayoumi — 2002-04-15 | employment / government-connection context | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC/interview of Bayoumi — 2003-09-17 | Commission's assessment of Bayoumi activities/knowledge | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | Omar al Bayoumi interview — 2003-10-16/17 | Feb. 1 encounter, Thumairy relationship, apartment/help narrative | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI ROI/interview Bayoumi — 2003-08-04/05 | earlier statement version for comparison | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI recovery of hotel records — 2002-01-15 | Bayoumi Los Angeles visit chronology | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI report `Connections of San Diego PENTTBOM Subjects to the Government of Saudi Arabia` — undated | government/employment/support-network context | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | Saudi Civil Aviation Authority employment records — 2000-03 through 2002-01 | salary/employment chronology cited by Commission | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | Caysan Bin Don interview — 2004-04-20 | restaurant/mosque chronology | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | FBI ROI/interview Isamu Dyson — 2001-10-08 | earlier Bin Don statement version | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | CIA analytic report `Al-Qa'ida Travel Issues`, CTC 2004-40002H — 2003-11-14 | passport/travel analytic context | `UNMAPPED_REFERENCED_EVIDENCE` |
| P2 | KSM interrogation intelligence report — 2003-08-18 | KSM denial of knowing Bayoumi; separate detainee-reporting caveats apply | `UNMAPPED_REFERENCED_EVIDENCE` |

### Mohdar Abdullah source chain

| Priority | Record | Why it matters | BlackIndex state |
|---|---|---|---|
| P0 | FBI ROI/interview Mohdar Abdullah — 2001-09-22 | early post-attack statement version | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI ROI/interview Mohdar Abdullah — 2002-01-15 | King Fahd mosque / Khallam recollection | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI ROI/interview Mohdar Abdullah — 2002-07-23 | Bayoumi-assistance account and later comparison anchor | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC `Abdullah investigation` — 2004-05-19 | Commission treatment of Abdullah assistance / advance-knowledge questions | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC interview Charles Sabah Toma — 2004-05-18 | inmate-attributed advance-knowledge account | `UNMAPPED_REFERENCED_EVIDENCE` |
| P0 | FBI EC interview — 2004-05-17 | separate inmate-attributed advance-knowledge account | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | Danny G. interviews — 2003-11-18 and 2004-05-24 | telephone/mood chronology cited in notes | `UNMAPPED_REFERENCED_EVIDENCE` |
| P1 | FBI Behavioral Analysis Activity report — 2001-10-04 | notebook attribution/context | `UNMAPPED_REFERENCED_EVIDENCE` |

## Current search result

Exact Git-backed repository searches did not locate the P0 named records as individually promoted BlackIndex documents.

This does **not** establish that the source records are absent from the local corpus. Large EO 14040 FBI containers are intentionally local-only and may contain these records without individual promotion.

Therefore the correct state is:

`UNMAPPED_REFERENCED_EVIDENCE`

not:

`MISSING FROM ARCHIVE`

and not:

`DESTROYED`.

## Recovery workflow

New local scanner:

`tools/recover-911-named-sources.py`

The scanner is intentionally read-only with respect to evidence state. It:

1. reads local metadata and normalized text;
2. searches for exact/variant name + date/title signatures from this map;
3. records candidate parent document IDs and text-page indices;
4. writes a local recovery report;
5. never promotes a child record automatically;
6. never labels a text-page index as a physical PDF page.

A hit means **candidate source recovery**, not proof that the entire named record boundary has been found.

## Promotion gate

A named source may be promoted only after:

- parent raw SHA is verified;
- candidate boundary is checked against the source PDF;
- physical-page mapping is established or explicitly marked unresolved;
- title/date/record type are visually confirmed;
- source relation to the Commission note is confirmed;
- any extended boundary receives the same source/boundary safeguards already used by the FBI P0 workflow.

## Immediate analytical payoff

Even before child promotion, the named source list sharpens the comparison:

- **Thumairy:** telephone/contact evidence is distinct from evidence of assistance, knowledge, or direction.
- **Bayoumi:** the chance-versus-design question for the February 1 encounter depends on interview versions, travel/hotel chronology, telephone evidence, employment records, and other source classes—not one report sentence.
- **Abdullah:** direct statements, inmate hearsay, and Commission inability to corroborate particular accounts must remain separate evidence types.

## Relationship to Review 007

This map is the upstream-source workstream for:

`docs/reviews/phase2-cross-document-007-911-official-closeout.md`

Review 007 remains open until at least the P0 named records above are searched across the local EO 14040 containers and the recovered/shared-source relationships are encoded.

## Core rule

**A cited source that has not yet been recovered is an evidence-recovery target, not a blank space that may be filled with inference.**
