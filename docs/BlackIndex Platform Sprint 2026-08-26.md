# BlackIndex Platform Sprint — 2026-08-26

## Purpose

Advance the BlackIndex platform in areas that can be completed without human source-PDF judgment while the 9/11 FBI P0 review queue remains paused.

This sprint deliberately avoided promoting any unresolved FBI candidate and did not alter the project rule against automatic historical verdicts.

## Completed

### 1. Durable evidence-object schema

Added `objects/schema-v1.json` covering the seven durable evidence-map object types:

- `record_integrity`
- `missing_evidence`
- `version_family`
- `version_comparison`
- `source_dependency`
- `statement_comparison`
- `investigator_review`

The schema encodes research-state invariants rather than truth judgments. Investigator findings must preserve `conclusion_adopted_as_fact: false`.

### 2. Evidence-object validator

Added `tools/validate-evidence-objects.py`.

Checks include:

- object type vs directory type;
- required fields;
- document cross-references;
- version-family and version-comparison document references;
- source-dependency independence vocabulary;
- investigator-review conclusion discipline;
- full JSON Schema validation when `jsonschema` is available;
- dependency-free structural fallback when it is not.

CI validation of the current Git-backed object corpus checked **37 durable objects with zero validation failures**.

### 3. Source genealogy / evidence lineage compiler

Added `tools/source-lineage.py`.

Outputs:

- `local/index/source-lineage.json`
- `local/index/source-lineage.md`

The compiler combines durable `source_dependency` objects and document-level parent/source-dependency metadata into a directed graph. It also identifies sources sharing the same upstream dependency so derivative repetition is not accidentally treated as independent corroboration.

Initial Git-backed lineage compile produced:

- 34 nodes
- 2 dependency edges
- both encoded edges marked dependent
- 0 multi-source shared-lineage families currently encoded

The low edge count is a data-model coverage observation, not a historical finding. It shows that source-dependency encoding should expand as reviews proceed.

### 4. Unit tests

Added `tests/test_evidence_objects.py` covering:

- valid record-integrity object acceptance;
- rejection of investigator conclusions silently adopted as fact;
- shared-upstream lineage grouping.

The sprint also exposed stale pre-existing intake tests after provenance fields were added to `blackindex.py`. `tests/test_blackindex.py` was updated with a shared intake argument fixture covering `artifact_url`, `landing_url`, `native_id`, `record_group`, and `series`.

### 5. Automated quality gate

Added `.github/workflows/object-quality.yml`.

On relevant pushes/PRs it now:

1. validates durable evidence objects;
2. compiles source lineage;
3. runs all unit tests.

The new workflow passed after the test-drift repair. The existing `BlackIndex Tests` workflow also passed on the same commit.

### 6. Local platform health runner

Added `tools/platform-health.sh` combining:

1. raw corpus integrity verification;
2. durable evidence-object validation;
3. source-lineage compile;
4. unit tests.

Unlike GitHub CI, this local runner can also verify local-only source-vault bytes.

### 7. Documentation / cleanup

Updated `objects/README.md` with:

- schema usage;
- validator behavior;
- source-genealogy rules;
- `UNMAPPED_REFERENCED_EVIDENCE` distinction;
- platform health command.

Removed obsolete `objects/.mode-note` repo clutter.

## Evidence discipline preserved

The sprint reinforces the following BlackIndex rules:

- document count is not independent-source count;
- derivative repetition does not automatically create corroboration;
- investigative negative findings remain attributed statements;
- missing/unmapped material is not assigned imagined content;
- lineage tooling describes provenance/dependency, not guilt or truth;
- unresolved FBI segmentation candidates remain outside the durable evidence layer until human boundary review.

## Current research implication

BlackIndex now has the infrastructure needed to answer a key research question programmatically:

> Are apparently separate reports genuinely independent, or are they repetitions/syntheses of the same upstream record?

The next high-leverage autonomous work is to expand explicit source-dependency encoding across already-reviewed documents and expose the resulting lineage graph in the local dashboard. This does not require completing the paused FBI P0 review queue first.

## Verification checkpoint

GitHub Actions after the sprint:

- **BlackIndex object quality:** PASS
- **BlackIndex Tests:** PASS

No unresolved FBI candidate was promoted during this sprint.
