# BlackIndex Evidence-Map Objects

`objects/` is the durable, Git-backed research-object layer. These files describe the state and integrity of the documentary record. They do **not** store raw corpus bytes or normalized full text.

## Object schema

Durable evidence-map objects are governed by `objects/schema-v1.json`.

The schema intentionally validates structure and research-state invariants, not historical truth. In particular, an `investigator_review` must keep `conclusion_adopted_as_fact: false`; a finding such as “no evidence found” remains an attributed investigative statement rather than becoming an automatic fact about the underlying event.

Validate all durable objects with:

```bash
python3 tools/validate-evidence-objects.py --root .
```

If the optional `jsonschema` package is installed, the full JSON Schema is applied. On a minimal install, the validator falls back to dependency-free structural and cross-reference checks.

## Object types

### `record_integrity/`
One sidecar per ingested document. Tracks completeness, redaction concern, destruction, missing referenced material, custody, alternate versions, release/classification chronology, version conflicts, public/internal contradictions, and archive confidence.

### `missing_evidence/`
Explicit records for referenced-but-absent attachments, destroyed files, unavailable workpapers, unexplained archival holes, missing minutes, omitted exhibits, or other materially absent evidence. Missing evidence is recorded as an unresolved fact about the archive, not as proof of what the missing material contained.

`UNMAPPED_REFERENCED_EVIDENCE` should be used when material may exist in the corpus/archive but has not yet been individually mapped. Do not silently convert an indexing gap into a historical absence.

### `version_families/`
Groups multiple releases/scans/transcripts/reproductions of the same underlying record.

### `version_comparisons/`
Machine-generated normalized-text comparisons. Comparison output identifies changed text and similarity; human review determines significance.

### `source_dependencies/`
Edges describing whether apparently separate sources derive from a common informant, document, investigation, translation, or analytical chain. Three derivative reports do not automatically equal three independent sources.

Compile those edges into a source-genealogy report with:

```bash
python3 tools/source-lineage.py --root .
```

This writes local-only outputs:

```text
local/index/source-lineage.json
local/index/source-lineage.md
```

The compiler identifies shared upstream lineage families so derivative repetition is visible before corroboration judgments are made.

### `statement_comparisons/`
Structured comparison between a public statement and an internal/contemporaneous record. Relationship values describe textual/evidentiary relationship only and remain revisable.

### `investigator_reviews/`
Context for investigative findings, especially negative findings. Preserve exact wording and record independence, access, scope, method transparency, reproducibility, conflicts, unavailable evidence, omitted witnesses, and surviving workpapers.

## Source-genealogy rule

BlackIndex distinguishes **document count** from **independent evidentiary lineage**.

```text
raw interview / primary record
        ↓
serial / investigative record
        ↓
analytical synthesis
        ↓
official report or closing finding
        ↓
later public interpretation
```

Multiple downstream documents may be important for chronology, interpretation, or institutional behavior while still depending on one upstream evidentiary source. The lineage graph records that dependency instead of inflating corroboration by repetition.

## Core rule

BlackIndex records assertions, evidence, provenance, contradictions, omissions, anomalies, and unresolved questions. It does not convert incomplete historical records into final determinations.

## Platform health

Run the combined integrity, object validation, lineage compile, and unit-test pass with:

```bash
bash tools/platform-health.sh
```

## Evidence-map CLI

Use `python3 tools/evidence_map.py --help`.

Typical lifecycle:

```bash
python3 tools/evidence_map.py bootstrap
python3 tools/evidence_map.py index
python3 tools/evidence_map.py dashboard
python3 tools/evidence_map.py publish --push
```

The generated dashboard is written beneath `local/` and remains local-only because it may embed normalized text excerpts.
