#!/usr/bin/env python3
"""Rank FBI segmentation candidates for *review priority* only.

This tool does not score truth, guilt, culpability, historical importance, or
probative weight. It reads local segmentation candidate indexes and produces a
local review queue under local/index/triage/.

Priority favors candidates that are easier to identify/reproduce and that touch
BlackIndex's current 9/11 research questions: named key entities, recognizable
FBI record types, serial/case markers, dates, and combinations of those signals.
Every candidate still requires review against the source PDF before promotion.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))

ENTITY_WEIGHT = {
    "Omar al-Bayoumi": 6,
    "Fahad al-Thumairy": 6,
    "Musaed al-Jarrah": 6,
    "Nawaf al-Hazmi": 5,
    "Khalid al-Mihdhar": 5,
}

TYPE_WEIGHT = {
    "fd_302": 7,
    "electronic_communication": 6,
    "fd_1057": 6,
    "fbi_information_report": 5,
    "memorandum": 4,
    "possible_fbi_record": 1,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def priority(candidate: dict) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    record_type = candidate.get("record_type_guess") or ""
    w = TYPE_WEIGHT.get(record_type, 0)
    if w:
        score += w
        reasons.append(f"record_type:{record_type}+{w}")

    entities = candidate.get("entity_hits") or []
    for name in entities:
        w = ENTITY_WEIGHT.get(name, 3)
        score += w
        reasons.append(f"entity:{name}+{w}")

    # Multiple key entities in the same candidate are especially useful for
    # relationship/source-genealogy review, but this remains only a queue signal.
    if len(entities) >= 2:
        score += 5
        reasons.append("multi_entity+5")
    if len(entities) >= 3:
        score += 3
        reasons.append("three_plus_entities+3")

    serials = candidate.get("serial_or_case_hits") or []
    if serials:
        score += 4
        reasons.append("serial_or_case_marker+4")

    dates = candidate.get("date_hits") or []
    if dates:
        score += 2
        reasons.append("date_marker+2")

    boundary = int(candidate.get("boundary_confidence") or 0)
    if boundary >= 3:
        score += 3
        reasons.append("strong_boundary+3")
    elif boundary == 2:
        score += 1
        reasons.append("moderate_boundary+1")

    # Reproducibility bonus: candidate has both identity/time and FBI locator.
    if serials and dates:
        score += 3
        reasons.append("reproducible_locator+3")

    return score, reasons


def band(score: int) -> str:
    if score >= 24:
        return "P0"
    if score >= 15:
        return "P1"
    if score >= 8:
        return "P2"
    return "P3"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build review-priority queue from FBI segmentation candidate indexes")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--top", type=int, default=30, help="number of top candidates to include in compact queue")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    seg_dir = root / "local/index/segmentation"
    if not seg_dir.is_dir():
        raise SystemExit(f"segmentation directory not found: {seg_dir}")

    rows: list[dict] = []
    source_counts: dict[str, int] = {}
    for path in sorted(seg_dir.glob("FBI-*.json")):
        data = load_json(path)
        container = data.get("container_doc_id") or path.stem
        candidates = data.get("candidates") or []
        source_counts[container] = len(candidates)
        for c in candidates:
            score, reasons = priority(c)
            row = {
                "container_doc_id": container,
                "candidate_id": c.get("candidate_id"),
                "start_page": c.get("start_page"),
                "end_page": c.get("end_page"),
                "record_type_guess": c.get("record_type_guess"),
                "boundary_confidence": c.get("boundary_confidence"),
                "entity_hits": c.get("entity_hits") or [],
                "serial_or_case_hits": c.get("serial_or_case_hits") or [],
                "date_hits": c.get("date_hits") or [],
                "preview": c.get("preview"),
                "review_priority_score": score,
                "review_priority_band": band(score),
                "priority_reasons": reasons,
                "review_required": True,
                "automatic_evidence_status": "none",
            }
            rows.append(row)

    rows.sort(key=lambda r: (-r["review_priority_score"], r["container_doc_id"], r["start_page"] or 0))
    bands = {b: sum(1 for r in rows if r["review_priority_band"] == b) for b in ("P0", "P1", "P2", "P3")}

    payload = {
        "schema_version": 1,
        "object_type": "segmentation_review_priority_queue",
        "generated_at": now(),
        "method": "review-priority heuristic only; not evidence weighting or culpability scoring",
        "automatic_evidence_status": "none",
        "candidate_count": len(rows),
        "source_candidate_counts": source_counts,
        "priority_band_counts": bands,
        "top_n": min(max(args.top, 0), len(rows)),
        "top_candidates": rows[: max(args.top, 0)],
        "all_candidates": rows,
    }

    out_dir = root / "local/index/triage"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "911-fbi-segmentation-priority.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    # Human-readable companion for quick terminal review.
    md = out_dir / "911-fbi-segmentation-priority.md"
    lines = [
        "# 9/11 FBI Segmentation — Review Priority Queue",
        "",
        "> Review priority only. This is not a truth, guilt, culpability, or evidence-strength score.",
        "",
        f"Candidates: **{len(rows)}**",
        f"Bands: P0={bands['P0']} · P1={bands['P1']} · P2={bands['P2']} · P3={bands['P3']}",
        "",
        "| Rank | Priority | Score | Container | Candidate | Pages | Type | Entities | Serial/case |",
        "|---:|---|---:|---|---|---:|---|---|---|",
    ]
    for i, r in enumerate(rows[: max(args.top, 0)], start=1):
        pages = str(r['start_page']) if r['start_page'] == r['end_page'] else f"{r['start_page']}-{r['end_page']}"
        entities = ", ".join(r['entity_hits']) or "—"
        serials = ", ".join(r['serial_or_case_hits'][:3]) or "—"
        lines.append(
            f"| {i} | {r['review_priority_band']} | {r['review_priority_score']} | "
            f"`{r['container_doc_id']}` | `{r['candidate_id']}` | {pages} | "
            f"{r['record_type_guess']} | {entities} | {serials} |"
        )
    lines += [
        "",
        "## Promotion rule",
        "",
        "A candidate may be promoted only after checking the original source PDF, confirming its real record boundaries, and preserving the parent container, page range, serial/case identifier, date, redactions, and source dependencies.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "candidate_count": len(rows),
        "priority_band_counts": bands,
        "top": min(max(args.top, 0), len(rows)),
        "json": str(out),
        "markdown": str(md),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
