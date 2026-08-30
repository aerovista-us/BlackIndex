# Phase 2 Cross-Document Review 007G — Mohdar Abdullah Official FBI Recovery

## Status

`PREPARED — two official FBI release bundles identified; ingest/review pending`

Review 007G narrows the Abdullah source-recovery problem to official FBI Vault material already publicly released. It does not treat the monthly bundles as independent corroboration merely because they are separate PDFs.

Primary unresolved BlackIndex object:

`ME-COMMISSION-2004-abdullah-named-upstream-records`

## Why this lane exists

The 9/11 Commission notes cite multiple FBI records concerning Mohdar Abdullah, including:

- FBI ROI/interview of Mohdar Abdullah — 2002-07-23;
- FBI EC Abdullah investigation — 2004-05-19;
- FBI EC interview of Charles Sabah Toma — 2004-05-18;
- FBI EC concerning Abdullah advance-knowledge claims — 2004-05-17.

The earlier Review 007 named-source scan localized these only as Commission citations and did not find an exact EO 14040 signature candidate.

A subsequent official-source search located two FBI Vault release bundles that materially improve the recovery path.

## Official FBI release candidate A — May 2004

FBI Vault title:

`9/11 Investigation 2004 05(May)`

Official URL:

`https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2004-05-may`

Observed public PDF characteristics:

- 13 physical PDF pages;
- first FBI EC dated `05/18/2004`;
- title concerns Mohdar Mohamed Abdullah / al-Qa'ida investigation;
- synopsis identifies the interview of Charles Sabah Toma;
- a second FBI EC begins on physical PDF page 6 and is dated `05/17/2004`;
- that EC records information attributed to detainee/inmate sources concerning alleged Abdullah advance knowledge and explicitly includes follow-up/validation work.

### Recovery interpretation

This bundle is a **direct official-source candidate** for Commission notes 22 and 23.

It does not, by itself, prove that every page is the exact source copy seen by the Commission. Release/version and source-dependency review remain required.

The May 19, 2004 `Abdullah investigation` EC cited separately by the Commission has not yet been positively identified in this bundle.

## Official FBI release candidate B — April 2002

FBI Vault title:

`9/11 Investigation 2002 04(Apr)`

Official URL:

`https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2002-04-apr/`

Observed public PDF characteristics:

- 12 physical PDF pages;
- lead EC dated `04/11/2002`, case `265A-NY-280350` / San Diego PENTTBOM;
- contains an FBI narrative summary of a `09/19/2001` Mohdar Abdullah interview;
- later pages include the document headed `Connections of San Diego PENTTBOMB Subjects to the Government of Saudi Arabia`.

### Recovery interpretation

This bundle is useful **upstream lineage/context**, but it is not the Commission-cited July 23, 2002 ROI merely because it discusses Abdullah.

Do not substitute this bundle for the still-unrecovered exact `2002-07-23` interview record.

## Controlled ingest decision

The next controlled local sprint should ingest both FBI Vault bundles as parent release artifacts.

Purpose:

1. preserve official FBI provenance and hashes;
2. make their native text searchable in BlackIndex;
3. test whether the May 17 and May 18 records correspond to the Commission's cited source records;
4. compare monthly-release wording/structure against later EO 14040 copies if overlap exists;
5. keep July 23, 2002 and May 19, 2004 explicitly unresolved until actually recovered.

## Source-independence rule

If a record in these monthly FBI Vault releases is later found duplicated inside an EO 14040 release package, the two public PDFs represent **release duplication**, not independent corroboration.

Required lineage shape:

`underlying FBI EC/ROI → one or more FBI public release packages → Commission citation/synthesis`

not:

`FBI Vault PDF + EO 14040 PDF + Commission report = three independent sources`

## Promotion rule

This sprint ingests **parent release bundles only**.

No child-record promotion is authorized merely because an expected date/title appears inside the PDF.

Any child promotion still requires:

- parent SHA verification;
- exact physical page boundaries;
- first/last page review;
- record identity/date/case continuity;
- duplicate-release check;
- reviewed extraction.

## Expected post-ingest state

If both official bundles ingest successfully:

- corpus verifier should increase by two records from the current `37 / 0` checkpoint;
- Abdullah recovery status should move from `official_fbi_release_candidates_located` toward `official_fbi_parent_bundles_acquired`;
- May 17 and May 18 should become source-boundary review targets;
- July 23, 2002 and May 19, 2004 remain unresolved unless separately recovered.

## Core rule

**A public FBI bundle can recover the source lineage without yet recovering the exact child record boundary.**
