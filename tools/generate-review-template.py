#!/usr/bin/env python3
"""Generate BlackIndex's neutral evidence-map review template for one document.

Existing substantive reviews are never overwritten. Legacy auto-generated TODO stubs
may be replaced safely.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path

ROOT = Path(os.environ.get("BLACKINDEX_ROOT", Path(__file__).resolve().parents[1]))


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_stub(text: str) -> bool:
    return "TODO" in text and ("## Evidence established by the document" in text or "## DOCUMENT SAYS" in text)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: generate-review-template.py DOC_ID", file=sys.stderr); return 2
    doc_id = sys.argv[1]
    meta_path = ROOT / "metadata" / f"{doc_id}.json"
    if not meta_path.is_file():
        print(f"error: metadata not found: {meta_path}", file=sys.stderr); return 2
    m = load(meta_path)
    out = ROOT / "extractions" / f"{doc_id}.md"
    if out.exists():
        existing = out.read_text(encoding="utf-8", errors="replace")
        if existing.strip() and not is_stub(existing):
            print(f"review preserved: {out}"); return 0
    artifact = m.get("artifact_url") or m.get("source_url") or "Not recorded"
    body = f"""# {m.get('title') or doc_id}

- **Doc ID:** `{doc_id}`
- **Call ID:** `{m.get('call_id') or 'UNASSIGNED'}`
- **Native ID:** {m.get('native_id') or 'Not recorded'}
- **Source:** {m.get('source') or 'Unknown'}
- **Document date:** {m.get('document_date') or 'Unknown'}
- **SHA-256:** `{m.get('sha256') or 'Not recorded'}`
- **Landing page:** {m.get('canonical_landing_url') or 'Not recorded'}
- **Artifact:** {artifact}
- **Normalized text:** {m.get('normalized_text_path') or 'Unavailable'}
- **State of record:** `R0` — intake complete; substantive review pending

> BlackIndex records assertions and the state of the surviving record. This review does not render a final historical verdict.

## CLAIM

- TODO: What assertion, allegation, proposal, event, or question is this passage relevant to?

## DOCUMENT CONTENT

- TODO: Neutrally describe what is actually present in the document. Preserve proposal / approval / implementation / execution / outcome distinctions.

## SOURCE ATTRIBUTION

- TODO: Who is asserting or recording the information? Note role, institution, date, proximity to events, and whether this is firsthand, investigative, retrospective, or derivative.

## CORROBORATION

- TODO: List genuinely independent supporting material. Record source dependencies rather than counting derivative reports as independent corroboration.

## CONFLICTS

- TODO: Record inconsistent documents, testimony, timelines, technical evidence, later findings, or competing interpretations.

## GAPS

- TODO: Redactions, missing attachments, destroyed records, unavailable workpapers, unexamined evidence, ambiguous identities, or other unresolved archive limitations.

## ALTERNATIVE EXPLANATIONS

- TODO: Record the strongest reasonable mundane, procedural, innocent, or competing explanation for each important anomaly.

## UNRESOLVED QUESTIONS

- TODO: What specific document, testimony, version, technical record, or archival recovery would materially improve the record?

## SOURCE

- TODO: Exact primary-source citation and page number for every pivotal passage.

## NEGATIVE FINDINGS / INVESTIGATOR STATEMENTS

- TODO where applicable. Preserve exact wording such as `no evidence found`, `unable to substantiate`, or `no credible evidence`. Attribute the statement to the investigator; do not silently convert it into a fact about the underlying event.

## RECORD INTEGRITY

- Completeness: `__/5`
- Redaction concern: `__/15`
- Known destruction: `Yes / No / Unknown`
- Missing referenced records: `__`
- Custodian conflicts: `Yes / No / Unknown`
- Version conflicts: `Yes / No / Unknown`
- Public/internal contradictions: `__`
- Archive confidence: `__/5`

## RESEARCH-STATE DIAGNOSTICS

- Plausibility: `__/15` — motive / capability / opportunity only
- Evidence density: `__/30`
- Obstruction / anomaly: `__/20`
- Source confidence: `__/5` per pivotal assertion/source
- Inference dependency: `D0 / D1 / D2 / D3 / D4`
- State of record: `R0 / R1 / R2 / R3 / R4 / R5`

These values describe the current evidence map. They are not final determinations.

## MECHANISMS / OPERATIONAL ANALOGS

- TODO

## CANDIDATE CONTROLS / DETECTIONS

- TODO

## REVIEW NOTES

- TODO
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"neutral review template: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
