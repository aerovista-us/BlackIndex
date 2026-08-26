# BlackIndex

**Declassified intelligence → operational knowledge.**

BlackIndex is a local-first research and implementation system for collecting named declassified document sets, preserving provenance, extracting patterns, and converting those lessons into practical controls, detections, training scenarios, and response playbooks.

## Core model

1. **Identify** high-value document collections and reports.
2. **Collect** primary-source records with provenance and checksums.
3. **Store** immutable originals separately from normalized derivatives.
4. **Extract** evidence, mechanisms, failure modes, and operational analogs.
5. **Compare** reviewed records and promote only mechanisms that survive cross-document review.
6. **Call** the index when a relevant risk, incident, or question appears.
7. **Implement** controls, detections, training, and playbooks.
8. **Review** outcomes and retire weak or misleading patterns.

## Architecture

```text
blackindex/
├── bootstrap/         # location-relative deploy/bootstrap entrypoint
├── registry/          # Named collections / callable entries
├── source-vault/      # Raw source documents (local only; not Git)
├── normalized/        # Local normalized text
├── metadata/          # Provenance + hashes + document descriptors
├── extractions/       # Structured evidence reviews
├── objects/           # Durable integrity/lineage/comparison objects
├── patterns/          # Reusable cross-document mechanisms / failure modes
├── controls/          # Operational safeguards
├── detections/        # Monitoring and detection concepts
├── training/          # Training scenarios
├── playbooks/         # Response and implementation playbooks
├── local/             # Local indexes, dashboards, review state, cache and logs
├── docs/              # Governance, taxonomy, architecture, synthesis reviews
└── tools/             # Local indexing / intake / review utilities
```

## Canonical NXCore placement

BlackIndex is intended to live at:

```text
/srv/Collab/mini.shops/blackindex/
```

The repository itself is the application root. There is **no nested `system/` checkout**.

Deployment is location-relative. `bootstrap/deploy.sh` resolves its own directory and treats its parent as the BlackIndex app root.

```bash
cd /srv/Collab/mini.shops/blackindex
chmod +x bootstrap/deploy.sh
./bootstrap/deploy.sh
```

Set `BLACKINDEX_UPDATE=1` when you intentionally want deployment to first perform a fast-forward-only Git pull.

## Storage and publication rule

BlackIndex deliberately splits **corpus storage** from the **durable research record**.

Local-only on NXCore:
- raw source PDFs and archives under `source-vault/`
- normalized text derivatives under `normalized/`
- indexes, dashboards, review queues, caches and logs under `local/`

Published to GitHub:
- document metadata and SHA-256 provenance records
- reviewed extraction files
- evidence-map objects and object schemas
- cross-document synthesis reviews and promoted patterns
- registries and source targets
- controls, detections, training scenarios and playbooks
- code, schemas and governance documentation

This keeps GitHub useful as the auditable knowledge/history layer without turning Git into bulk binary or derivative-text storage.

### Publish one ingested document

After intake, normalization and review, publish its durable record with:

```bash
chmod +x tools/publish-ingest.sh
./tools/publish-ingest.sh SENATE-1976-church-committee-001
```

The publish helper runs BlackIndex integrity verification first, stages only that document's metadata/extraction, rejects local corpus/runtime paths, then commits and pushes the durable record.

## Evidence discipline

BlackIndex distinguishes between:
- **Primary evidence** — what a source document directly establishes.
- **Corroboration** — independent records supporting the same point.
- **Inference** — conclusions derived from evidence.
- **Unknown / redacted** — material that cannot responsibly be concluded.

Declassified does not mean complete. Redactions, missing annexes, later corrections, and historical context must be recorded.

### Source genealogy

BlackIndex treats evidence lineage as a first-class research problem. Repetition through a shared upstream interview, serial, analytical product, report, translation, or investigation is not automatically independent corroboration.

Compile the currently encoded graph with:

```bash
python3 tools/source-lineage.py --root .
python3 tools/source-lineage-ui.py --root .
```

Audit for references that still need lineage review with:

```bash
python3 tools/dependency-audit.py --root .
python3 tools/research-reference-audit.py --root .
```

Both audit tools are conservative. They create local review queues only; they do **not** infer or publish dependency edges.

`bash tools/serve-dashboard.sh` regenerates the lineage/audit state and serves a **Source Lineage** page alongside the evidence dashboard. The dashboard also preserves the separate **Resume FBI Review** workflow for paused source-verification work.

### Promotion discipline

A dramatic excerpt is not automatically a reusable pattern. Promotion requires:

- direct-source grounding;
- proposal/approval/execution/outcome states kept distinct;
- review of alternative explanations and context gaps;
- preferably independent support from more than one reviewed record;
- explicit confidence and guardrails against guilt-by-similarity.

Current promoted patterns live under `patterns/` and cross-document reasoning under `docs/reviews/`.

## Platform health

Run the integrated local check with:

```bash
bash tools/platform-health.sh
```

It verifies corpus hashes, validates durable evidence objects against the object schema, compiles source lineage, audits unencoded references, renders the lineage UI, and runs unit tests. GitHub Actions repeats the Git-backed object/schema/lineage checks on relevant pushes and pull requests.

## Status

**v0.1 — Phase 2 evidence corpus underway**

The corpus and evidence-map layers are actively expanding. BlackIndex now includes durable evidence-object validation, source-lineage compilation, conservative lineage-backfill audits, local evidence/lineage dashboards, and gated source-review workflows in addition to the original documents-first research pipeline.
