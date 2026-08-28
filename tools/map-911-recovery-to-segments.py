#!/usr/bin/env python3
"""Map Review 007 EO 14040 recovery hits to existing segmentation candidates.

This tool is review-only. It maps normalized-text page positions to heuristic
segmentation ranges and existing P0 packet metadata where available. It does not
verify physical PDF pages, change evidence state, or promote child records.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
EO14040_RE = re.compile(r"^FBI-(?:2021|2022)-eo14040-")


def load_json(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def candidate_rows(payload: dict) -> list[dict]:
    for key in ("all_candidates", "top_candidates", "ranked", "candidates", "queue", "items"):
        rows = payload.get(key)
        if isinstance(rows, list):
            return rows
    return []


def row_key(row: dict) -> tuple[str, str] | None:
    doc_id = row.get("container_doc_id") or row.get("container") or row.get("doc_id")
    cand_id = row.get("candidate_id") or row.get("candidate")
    if not doc_id or not cand_id:
        return None
    return str(doc_id), str(cand_id)


def build_triage_index(root: Path) -> dict[tuple[str, str], dict]:
    path = root / "local/index/triage/911-fbi-segmentation-priority.json"
    payload = load_json(path, {})
    out = {}
    for row in candidate_rows(payload):
        key = row_key(row)
        if key:
            out[key] = row
    return out


def build_packet_index(root: Path) -> dict[tuple[str, str], dict]:
    payload = load_json(root / "local/review/911-fbi-p0/manifest.json", {})
    out = {}
    for row in payload.get("packets") or []:
        key = row_key(row)
        if key:
            out[key] = row
    return out


def segment_index(root: Path, doc_id: str) -> dict:
    return load_json(root / "local/index/segmentation" / f"{doc_id}.json", {})


def segment_hits(payload: dict, page: int) -> list[dict]:
    hits = []
    for row in payload.get("candidates") or []:
        try:
            start = int(row.get("start_page"))
            end = int(row.get("end_page"))
        except (TypeError, ValueError):
            continue
        if start <= page <= end:
            hits.append(row)
    return hits


def band_of(row: dict | None):
    if not row:
        return None
    return row.get("review_priority_band") or row.get("priority_band") or row.get("priority") or row.get("band")


def score_of(row: dict | None):
    if not row:
        return None
    return row.get("review_priority_score") or row.get("review_score") or row.get("score")


def map_recovery(root: Path) -> dict:
    recovery = load_json(root / "local/index/911-named-source-recovery.json", {})
    triage = build_triage_index(root)
    packets = build_packet_index(root)
    results = []
    mapped_positions = 0
    positions_without_segment = 0

    for target in recovery.get("targets") or []:
        eo_candidates = [c for c in target.get("candidates") or [] if EO14040_RE.match(str(c.get("doc_id") or ""))]
        if not eo_candidates:
            continue
        mapped = []
        for cand in eo_candidates:
            doc_id = str(cand.get("doc_id"))
            page = int(cand.get("text_page_index"))
            seg_payload = segment_index(root, doc_id)
            segs = segment_hits(seg_payload, page) if seg_payload else []
            if segs:
                mapped_positions += 1
            else:
                positions_without_segment += 1
            segment_rows = []
            for seg in segs:
                cand_id = str(seg.get("candidate_id") or "")
                key = (doc_id, cand_id)
                triage_row = triage.get(key)
                packet_row = packets.get(key)
                segment_rows.append({
                    "candidate_id": cand_id,
                    "start_page": seg.get("start_page"),
                    "end_page": seg.get("end_page"),
                    "record_type_guess": seg.get("record_type_guess"),
                    "entity_hits": seg.get("entity_hits") or [],
                    "date_hits": seg.get("date_hits") or [],
                    "serial_or_case_hits": seg.get("serial_or_case_hits") or [],
                    "priority_band": band_of(triage_row),
                    "priority_score": score_of(triage_row),
                    "p0_packet": packet_row.get("packet") if packet_row else None,
                    "p0_promotion_state": packet_row.get("promotion_state") if packet_row else None,
                    "physical_page_verified": False,
                    "boundary_verified": False,
                })
            mapped.append({
                "parent_doc_id": doc_id,
                "parent_sha256": cand.get("container_sha256"),
                "text_page_index": page,
                "physical_page_verified": False,
                "segment_index_present": bool(seg_payload),
                "segment_match_count": len(segment_rows),
                "segments": segment_rows,
            })
        results.append({
            "target_id": target.get("target_id"),
            "label": target.get("label"),
            "eo14040_candidate_positions": mapped,
        })

    return {
        "schema_version": 1,
        "object_type": "named_source_segment_map",
        "purpose": "map EO 14040 named-source recovery positions to heuristic segmentation candidates; review only",
        "physical_page_claim": False,
        "boundary_claim": False,
        "target_family_count": len(results),
        "candidate_position_count": sum(len(r["eo14040_candidate_positions"]) for r in results),
        "positions_with_segment_match": mapped_positions,
        "positions_without_segment_match": positions_without_segment,
        "targets": results,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# BlackIndex Review 007 — Named-Source → Segmentation Map",
        "",
        "> Review-only mapping. Segmentation ranges and normalized text-page indices are heuristic until checked against the source PDF. No child record is promoted by this map.",
        "",
        f"- EO 14040 target families: **{report['target_family_count']}**",
        f"- Candidate positions: **{report['candidate_position_count']}**",
        f"- Positions matched to segmentation candidates: **{report['positions_with_segment_match']}**",
        f"- Positions without segmentation match: **{report['positions_without_segment_match']}**",
        "",
    ]
    for target in report["targets"]:
        lines += [f"## {target.get('label')}", ""]
        for pos in target["eo14040_candidate_positions"]:
            lines += [
                f"### `{pos['parent_doc_id']}` · normalized text page `{pos['text_page_index']}`",
                "",
                "- Physical page: **UNVERIFIED**",
                f"- Segmentation index present: `{pos['segment_index_present']}`",
                f"- Matching segmentation candidates: **{pos['segment_match_count']}**",
            ]
            if not pos["segments"]:
                lines += ["- No heuristic segment currently contains this text-page position.", ""]
                continue
            for seg in pos["segments"]:
                lines += [
                    f"- `{seg['candidate_id']}` — heuristic pages `{seg['start_page']}–{seg['end_page']}`",
                    f"  - record type guess: `{seg.get('record_type_guess')}`",
                    f"  - priority band: `{seg.get('priority_band')}`",
                    f"  - P0 packet: `{seg.get('p0_packet')}`",
                    "  - boundary verified: `false`",
                    "  - physical page verified: `false`",
                ]
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Map Review 007 EO 14040 source hits to segmentation candidates")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    report = map_recovery(root)
    json_path = root / "local/index/911-named-source-segment-map.json"
    md_path = root / "local/review/911-named-source-segment-map.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "json": str(json_path),
        "markdown": str(md_path),
        "target_families": report["target_family_count"],
        "candidate_positions": report["candidate_position_count"],
        "positions_with_segment_match": report["positions_with_segment_match"],
        "physical_page_claim": False,
        "boundary_claim": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
