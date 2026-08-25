# BlackIndex Evidence-Map Objects

`objects/` is the durable, Git-backed research-object layer. These files describe the state and integrity of the documentary record. They do **not** store raw corpus bytes or normalized full text.

## Object types

### `record_integrity/`
One sidecar per ingested document. Tracks completeness, redaction concern, destruction, missing referenced material, custody, alternate versions, release/classification chronology, version conflicts, public/internal contradictions, and archive confidence.

### `missing_evidence/`
Explicit records for referenced-but-absent attachments, destroyed files, unavailable workpapers, unexplained archival holes, missing minutes, omitted exhibits, or other materially absent evidence. Missing evidence is recorded as an unresolved fact about the archive, not as proof of what the missing material contained.

### `version_families/`
Groups multiple releases/scans/transcripts/reproductions of the same underlying record.

### `version_comparisons/`
Machine-generated normalized-text comparisons. Comparison output identifies changed text and similarity; human review determines significance.

### `source_dependencies/`
Edges describing whether apparently separate sources derive from a common informant, document, investigation, translation, or analytical chain. Three derivative reports do not automatically equal three independent sources.

### `statement_comparisons/`
Structured comparison between a public statement and an internal/contemporaneous record. Relationship values describe textual/evidentiary relationship only and remain revisable.

### `investigator_reviews/`
Context for investigative findings, especially negative findings. Preserve exact wording and record independence, access, scope, method transparency, reproducibility, conflicts, unavailable evidence, omitted witnesses, and surviving workpapers.

## Core rule

BlackIndex records assertions, evidence, provenance, contradictions, omissions, anomalies, and unresolved questions. It does not convert incomplete historical records into final determinations.

## CLI

Use `python3 tools/evidence_map.py --help`.

Typical lifecycle:

```bash
python3 tools/evidence_map.py bootstrap
python3 tools/evidence_map.py index
python3 tools/evidence_map.py dashboard
python3 tools/evidence_map.py publish --push
```

The generated dashboard is written beneath `local/` and remains local-only because it may embed normalized text excerpts.