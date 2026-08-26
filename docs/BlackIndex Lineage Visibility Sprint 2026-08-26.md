# BlackIndex Lineage Visibility Sprint — 2026-08-26

## Objective

Continue BlackIndex development without requiring source-PDF review or unresolved historical judgments. The sprint focused on making source genealogy visible, surfacing lineage-backfill work conservatively, and integrating those capabilities into normal platform health and dashboard startup.

## Delivered

### Source-lineage UI

`tools/source-lineage-ui.py` renders the compiled lineage graph to:

`local/dashboard/source-lineage.html`

The page shows encoded dependency edges, independence labels, shared upstream families, and a prominent warning that missing edges mean **not yet encoded**, not independent.

`tools/serve-dashboard.sh` now regenerates source lineage, dependency audits, the lineage page, and the evidence dashboard before serving. The main dashboard receives a **Source Lineage** control alongside **Resume FBI Review**.

### Conservative dependency audit

`tools/dependency-audit.py` scans durable document metadata and reviewed extractions for explicit BlackIndex document references that are not already represented by encoded dependency edges.

It writes local-only review queues:

- `local/index/dependency-audit.json`
- `local/index/dependency-audit.md`

It never creates source-dependency objects automatically.

Current Git-backed CI result:

- metadata documents inspected: 32
- encoded dependency edges: 2
- strict metadata/extraction reference candidates: 0

This does **not** mean the corpus has no additional source dependencies. It means the current durable metadata/extractions do not yet encode enough explicit document-to-document references for strict automatic backfill.

### Research-note cross-reference audit

`tools/research-reference-audit.py` scans `docs/reviews/` and `docs/research-clusters/` for:

- explicit BlackIndex document IDs; and
- exact, sufficiently distinctive metadata titles that uniquely resolve to a BlackIndex document.

The output is a research cross-reference queue only. Co-occurrence does not establish dependence, corroboration, agreement, contradiction, or evidence-flow direction.

Current Git-backed CI result:

- research files with recognized documents: 4
- unique document-pair cross-references: 31

This is the strongest current target for future lineage backfill: review those 31 pairs and encode only relationships that the underlying review/source record actually supports.

### Platform health and CI

`tools/platform-health.sh` now runs:

1. corpus integrity verification;
2. durable object validation;
3. source-lineage compilation;
4. strict dependency audit;
5. research-reference audit;
6. source-lineage UI rendering; and
7. unit tests.

`.github/workflows/object-quality.yml` now installs `jsonschema`, performs full schema validation, runs both audits, renders lineage UI, and runs the test suite.

Final verification for this sprint:

- durable objects checked: 37
- validation failures: 0
- validation notices: 0
- lineage nodes: 34
- encoded edges: 2
- shared upstream families currently encoded: 0
- unit tests: 9 passed
- object-quality workflow: PASS
- BlackIndex Tests workflow: PASS

## Methodological boundary

No source-dependency edge was inferred merely because two documents appeared in the same synthesis or research note. The new audit layers surface **where to review**, not **what conclusion to adopt**.

The paused FBI P0 source-review queue remains isolated and is not automatically promoted by any lineage tool.

## Next autonomous target

Use the 31 research-note document pairs as a ranked lineage-review backlog. For each pair, inspect the durable review text and existing source descriptions to determine whether it supports one of the explicit relationships already allowed by the BlackIndex source-dependency vocabulary. Encode only those relationships that are directly supported; otherwise retain the pair as unresolved cross-reference context.
