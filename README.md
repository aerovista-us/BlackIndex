# BlackIndex

**Declassified intelligence → operational knowledge.**

BlackIndex is a local-first research and implementation system for collecting named declassified document sets, preserving provenance, extracting patterns, and converting those lessons into practical controls, detections, training scenarios, and response playbooks.

## Core model

1. **Identify** high-value document collections and reports.
2. **Collect** primary-source records with provenance and checksums.
3. **Store** immutable originals separately from normalized derivatives.
4. **Extract** evidence, mechanisms, failure modes, and operational analogs.
5. **Call** the index when a relevant risk, incident, or question appears.
6. **Implement** controls, detections, training, and playbooks.
7. **Review** outcomes and retire weak or misleading patterns.

## Architecture

```text
blackindex/
├── bootstrap/         # location-relative deploy/bootstrap entrypoint
├── registry/          # Named collections / callable entries
├── source-vault/      # Raw source documents (local only; not Git)
├── normalized/        # Local normalized text
├── metadata/          # Provenance + hashes + document descriptors
├── extractions/       # Structured research summaries
├── patterns/          # Reusable mechanisms / failure modes
├── controls/          # Operational safeguards
├── detections/        # Monitoring and detection concepts
├── training/          # Training scenarios
├── playbooks/         # Response and implementation playbooks
├── local/             # Local indexes, cache and logs
├── docs/              # Governance, taxonomy, architecture
└── tools/             # Local indexing / intake utilities
```

## Canonical NXCore placement

BlackIndex is intended to live at:

```text
/srv/Collab/mini.shops/blackindex/
```

The repository itself is the application root. There is **no nested `system/` checkout**.

Deployment is location-relative. `bootstrap/deploy.sh` resolves its own directory and treats its parent as the BlackIndex app root.

For example:

```text
/srv/Collab/mini.shops/blackindex/bootstrap/deploy.sh
                                  └──── parent app root ────┘
```

So running:

```bash
cd /srv/Collab/mini.shops/blackindex
chmod +x bootstrap/deploy.sh
./bootstrap/deploy.sh
```

initializes and validates `/srv/Collab/mini.shops/blackindex/` directly.

Set `BLACKINDEX_UPDATE=1` when you intentionally want deployment to first perform a fast-forward-only Git pull.

## Important storage rule

Large raw PDFs and archive corpora belong in the local BlackIndex `source-vault/`, **not in GitHub**. GitHub stores the system definition, metadata, extractions, controls, detections, playbooks, and code. This keeps repository history useful and avoids turning Git into binary storage.

## Evidence discipline

BlackIndex distinguishes between:
- **Primary evidence** — what a source document directly establishes.
- **Corroboration** — independent records supporting the same point.
- **Inference** — conclusions derived from evidence.
- **Unknown / redacted** — material that cannot responsibly be concluded.

Declassified does not mean complete. Redactions, missing annexes, later corrections, and historical context must be recorded.

## Status

**v0.1 — Foundation build**

Initial work: registry, intake schema, source taxonomy, extraction format, control/detection libraries, location-relative NXCore deployment, and first research phase.
