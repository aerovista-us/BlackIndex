# Phase 2 Cross-Document Review 007J — Orphan Raw Artifact Inventory

## Status

`COMPLETE — all current raw files without metadata references inventoried; no deletion or corpus inflation`

## Purpose

Review 007 required an explicit disposition for immutable raw artifacts left behind by early 9/11 Commission acquisition paths. This pass inventories every file under `source-vault/raw` that is not referenced by a current metadata record.

No raw file was renamed, overwritten, moved, or deleted.

## Inventory result

At the time of review:

- raw files under `source-vault/raw`: **41**;
- current metadata raw-path references: **39**;
- raw files without metadata references: **2**;
- unexplained orphan artifacts after this review: **0**.

Both unregistered raw files are identifiable legacy acquisition artifacts from the 9/11 Commission workstream.

## Artifact A — Terrorist Financing monograph legacy PDF

Path:

`source-vault/raw/9/11 commission/9-11-commission-staff-monographs/9/11 COMMISSION-2004-9-11-commission-staff-monographs-001.pdf`

- SHA-256: `685aded194a5afaf9f57c04069c8be476a9064fbf31efe2471ff2e7f744da38a`
- size: **537,715 bytes**
- pages: **155**
- embedded title: `9/11 Commission - Terrorist Financing`
- historical acquisition URL: `https://www.9-11commission.gov/staff_statements/911_TerrFin_Monograph.pdf`
- historical source token: `9/11 Commission`
- historical collection: `9/11 Commission Staff Monographs`

Canonical BlackIndex record:

`COMMISSION-2004-9-11-commission-terrorist-financing-staff-monograph-001`

Canonical GovInfo PDF SHA-256:

`596e3318674a4bd66acf1fd8f7725d20e9e9f596379089f6f0ac0cb71082c9db`

### Comparison

The two PDFs are byte-different, but complete `pdftotext -layout` normalization followed by whitespace normalization produced the **same normalized-text SHA-256** for both:

`414881dcb7d24f30843e23db07693ad8de4b2dd782e3d0f6f7123540cc740f60`

This establishes that, for BlackIndex's current text-level comparison, the legacy PDF and canonical GovInfo PDF carry the same monograph text. The byte difference is therefore preserved as a release/acquisition variant, not counted as an independent source.

Durable family object:

`VF-COMMISSION-2004-financing-release-family`

## Artifact B — standalone Commission Chapter 7 legacy PDF

Path:

`source-vault/raw/9/11 commission/9-11-commission-official-baselines/9/11 COMMISSION-2004-9-11-commission-official-baselines-001.pdf`

- SHA-256: `571a90941790c746d99336134dbae182d10af508d19361974708462e8e02aef8`
- size: **971,373 bytes**
- pages: **39**
- embedded title: `The 9/11 Commission Report`
- historical acquisition URL: `https://www.9-11commission.gov/report/911Report_Ch7.pdf`
- native ID requested by the script: `911Report-Ch7`

The artifact begins at printed report page **215** with Chapter 7, `THE ATTACK LOOMS`, and ends at printed page **253**. Its closing Chapter 7 sentence is also present in the normalized canonical full Commission Report.

Canonical BlackIndex parent record:

`COMMISSION-2004-9-11-commission-001`

The living ledger already marks the separate Chapter 7 acquisition target `SUPERSEDED` because the full official Government edition is the canonical acquired parent. Dedicated Chapter 7 dependency and research-classification objects preserve chapter-level analysis without inventing another independent source.

Durable family object:

`VF-COMMISSION-2004-chapter7-release-family`

## Why these files existed

The earlier official-baseline script used the source label `9/11 Commission` and legacy shared collection namespaces. Later controlled closeout work standardized on canonical source `COMMISSION`, separate collection namespaces, and GovInfo artifacts. The closeout resume explicitly preserved the existing immutable raw slots rather than overwriting them.

That recovery behavior was correct. The remaining problem was documentation, not deletion.

## Disposition

Both files are now:

`INVENTORIED — PRESERVE IMMUTABLY — DO NOT COUNT AS ADDITIONAL CORROBORATION`

Neither file should be removed merely because it is not metadata-registered. Neither should be promoted solely to make the raw-file count equal the metadata count.

## Review 007 gate contribution

The closeout requirement to `resolve or explicitly inventory the orphan immutable raw artifact from the failed first-pass monograph namespace` is satisfied. The inventory also captured the standalone Chapter 7 legacy subset discovered by the same raw-reference audit.

## Core rule

**An orphan raw artifact can be historically important as acquisition provenance even when it should not become another evidentiary source.**
