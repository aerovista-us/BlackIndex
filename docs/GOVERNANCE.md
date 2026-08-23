# BlackIndex Governance Guardrails

## Evidence discipline
- Separate primary evidence from inference.
- Record redactions, missing annexes, provenance gaps, and later corrections.
- Prefer primary-source material and official repositories.
- Use corroboration before drawing operational conclusions from disputed claims.

## Operational discipline
- Convert historical patterns into observable signals, controls, and review criteria.
- Do not treat similarity as proof of intent.
- Require measurable thresholds where a detection could affect a person, account, vendor, or team.
- Record benign alternative explanations during review.

## Storage
- Raw source documents are immutable after intake.
- Raw corpora are stored on NXCore, not committed to Git.
- Git tracks schemas, metadata, research outputs, tools, controls, detections, and playbooks.
- Every ingested document should have a stable Doc ID and SHA-256 checksum.

## Promotion rule
A research item is promoted into operations only when it has:
1. a clearly stated risk,
2. an observable signal or failure mode,
3. a proportionate control or detection,
4. an owner,
5. evidence requirements, and
6. a review/retirement condition.

## Rabbit-hole control
If a call produces no usable operational output after two structured passes, narrow it, archive it, or retire it from active research.
