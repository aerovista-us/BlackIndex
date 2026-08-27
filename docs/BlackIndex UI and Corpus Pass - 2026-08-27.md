# BlackIndex UI and Corpus Pass — 2026-08-27

## Status

This pass continues the standalone BlackIndex research-workstation direction after the Record Context and browser-local Research Session layers.

Known local corpus checkpoint entering this pass:

- verifier: **31 checked / 0 failures**
- raw artifacts remain local-only
- GitHub remains the durable store for metadata, reviewed extractions, evidence-map objects, code, schemas, and governance

The local verifier remains authoritative for raw-corpus integrity. GitHub metadata counts are not a replacement for it.

---

## 1. UI continuation — Research Session export

New injector:

`tools/inject-research-export.py`

It extends the existing browser-local Research Session with:

- **Copy pinned IDs** — copies only the pinned document IDs;
- **Export JSON** — emits a small structured research-session bundle;
- **Export Markdown** — emits a human-readable pinned-record brief;
- **Clear recent** — clears browser-local recency history without touching pins.

The exported record summaries may include document ID, title, agency/source, date, type, source URL, State of Record, and Inference Dependency when those fields already exist in the dashboard data.

### Epistemic boundary

These exports are convenience artifacts only.

They are **not**:

- evidence objects;
- reviewed extractions;
- source-dependency assertions;
- investigator findings;
- repository state;
- synchronized case state.

The injector makes no network request and writes no server-side state. Browser `localStorage` remains the only session store.

The generated export includes an explicit notice that it is not BlackIndex evidence.

---

## 2. Why the next corpus pass stays inside the 9/11 cluster

The current Operation Encore work already has unusually deep underlying-record acquisition and segmentation. The highest-value next addition is therefore not another unrelated dramatic collection; it is the official interpretation/inquiry layer needed to compare changing assessments against the FBI source lineage already in BlackIndex.

Prepared batch:

`tools/ingest-phase2-911-official-baselines.sh`

The batch intentionally contains only four official records.

### A. Joint Inquiry final report — declassified public version

Official source: U.S. Government Publishing Office / Congress.

Artifact:

`https://www.govinfo.gov/content/pkg/CRPT-107hrpt792/pdf/CRPT-107hrpt792.pdf`

Landing page:

`https://www.govinfo.gov/app/details/CRPT-107hrpt792/CRPT-107hrpt792`

Research value:

- early congressional inquiry baseline;
- Hazmi/Mihdhar support-network material;
- Bayoumi and other U.S. associates;
- explicit declassification/redaction history;
- contemporaneous statement of investigative limits;
- foundation for later "28 Pages" release/version comparison.

Important record-integrity note: the public report itself states that the declassification review was for classification purposes and did not signify Intelligence Community agreement with the report's accuracy or conclusions. Preserve that distinction.

### B. 9/11 Commission Report — Chapter 7, *The Attack Looms*

Official source: National Commission on Terrorist Attacks Upon the United States.

Artifact:

`https://www.9-11commission.gov/report/911Report_Ch7.pdf`

Research value:

- Commission treatment of Hazmi and Mihdhar in California;
- Thumairy;
- Bayoumi;
- Mohdar Abdullah;
- distinctions between circumstantial evidence, investigator judgment, corroborated fact, and negative finding;
- direct comparison target for Operation Encore's later investigative record.

### C. 9/11 Commission Staff Monograph on Terrorist Financing

Artifact:

`https://www.9-11commission.gov/staff_statements/911_TerrFin_Monograph.pdf`

Research value:

- financing analysis;
- source-access and negative-finding questions;
- separation between Commission staff analysis and Commissioner-approved final report text.

The monograph must be stored as a **staff analytical/official interpretation layer**, not silently elevated to the same status as the Commission's final adopted report or underlying bank/FBI/intelligence records.

### D. *9/11 and Terrorist Travel* staff monograph

Artifact:

`https://www.9-11commission.gov/staff_statements/911_TerrTrav_Monograph.pdf`

Research value:

- entry/travel chronology;
- Hazmi/Mihdhar movements;
- watchlisting and border-system context;
- another official synthesis layer whose underlying sources may overlap with Commission/FBI records already present.

---

## 3. Required lineage treatment after ingestion

These four records must **not** be counted as four new independent confirmations of assertions already present in the 2016 EC or EO 14040 packages.

For each important assertion, map where possible:

`underlying record → Joint Inquiry / Commission staff synthesis → Commission final-report treatment → later FBI/Operation Encore synthesis → later rereview/closing assessment`

Repeated summaries that trace back to the same interview, FD-302, FBI serial, liaison report, financial record, or telecom record remain one underlying evidentiary lineage.

### Priority comparison topics

1. Hazmi/Mihdhar arrival and first two weeks in California.
2. King Fahd mosque / Thumairy treatment.
3. Bayoumi encounter and assistance.
4. Abdullah statements and reliability treatment.
5. Saudi institutional/support allegations and the exact confidence language used at each date.
6. Negative findings: who made them, what they reviewed, and what was unavailable or not pursued.
7. Redaction/release chronology, especially Joint Inquiry Part Four.

---

## 4. What this pass deliberately does not do

- No automatic conclusion reconciliation.
- No `PROVES / DOES NOT PROVE` field.
- No inference that a later investigation is automatically superior merely because it is later.
- No inference that a redaction establishes wrongdoing.
- No promotion of co-occurrence into a relationship.
- No automatic child-record promotion from the FBI P0 packets.
- No expansion into JFK/MLK/RFK/LOOKING GLASS in the same acquisition run.

Those remain separate research passes. Keeping this batch small makes source-dependency review tractable.

---

## 5. Local execution

After pulling the GitHub changes on NXCore:

```bash
cd /srv/Collab/mini.shops/blackindex
git pull --ff-only
bash tools/ingest-phase2-911-official-baselines.sh
```

Then run the complete platform gate:

```bash
bash tools/platform-health.sh
```

Start the refreshed workstation with:

```bash
bash tools/serve-dashboard.sh
```

The acquisition script tolerates individual source failures and reports them as **acquisition gaps, not evidence gaps**.

---

## 6. Next review gate

After local acquisition succeeds:

1. confirm the new verifier count and zero hash failures;
2. create reviewed extraction stubs for the four new records;
3. encode source-dependency relationships before using them as corroboration;
4. compare Joint Inquiry / Commission / Encore wording on Bayoumi and Thumairy;
5. add the 2016-released Joint Inquiry Part Four version as a dedicated version-family record if it is not already contained in the acquired public artifact/version lineage;
6. only then choose the next cluster expansion.

Candidate next expansion after this gate: **Operation LOOKING GLASS**, because it is already a defined P1 research cluster and remains absent from the current Git-backed metadata set.

---

## Core rule

**BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations.**
