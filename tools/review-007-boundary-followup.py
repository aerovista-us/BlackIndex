#!/usr/bin/env python3
"""Review 007 boundary follow-up: bracket hypotheses + Benomrane expansion.

Review-only. This tool consumes the structural boundary diagnostic for existing
P0 candidates and performs a wider exact-page structural scan around the
Benomrane recovery anchors. It may produce boundary *hypotheses* and a proposed
segmentation-gap review range, but never confirms a child-record boundary,
promotes a record, mutates evidence state, or publishes source text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
BENOMRANE_TARGET_ID = "BENOMRANE-INTERVIEWS-2002"


def load_json(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def canonical(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return " ".join(text.replace("\f", " ").split())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def physical_page_text(pdftotext: str, pdf: Path, page: int) -> str:
    proc = subprocess.run(
        [pdftotext, "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else ""


def page_marker(text: str) -> dict | None:
    for pattern in (
        r"\bpage\s+(\d{1,4})\s+(?:of|/)\s+(\d{1,4})\b",
        r"\bpg\.?\s*(\d{1,4})\s+(?:of|/)\s+(\d{1,4})\b",
    ):
        m = re.search(pattern, text, re.I)
        if m:
            current, total = int(m.group(1)), int(m.group(2))
            if 1 <= current <= total:
                return {"current": current, "total": total}
    return None


def structural_features(text: str, normalized_text: str, page: int) -> dict:
    marker = page_marker(text)
    fbi_header = bool(re.search(r"FEDERAL\s+BUREAU\s+OF\s+INVESTIGATION", text, re.I))
    fd302 = bool(re.search(r"\bFD[-\s]?302(?:A)?\b", text, re.I))
    ec = bool(re.search(r"\bELECTRONIC\s+COMMUNICATION\b", text, re.I))
    transcription = bool(re.search(r"DATE\s+OF\s+TRANSCRIPTION", text, re.I))
    case_label = bool(re.search(r"\b(?:CASE|FILE)(?:\s+ID|\s+NO\.?|\s+NUMBER|\s*#)\b", text, re.I))
    interview = bool(re.search(r"\b(?:WAS|WERE)\s+INTERVIEWED\b|\bINTERVIEW\s+OF\b", text, re.I))
    continuation = bool(re.search(r"\bCONTINU(?:ED|ATION)\b", text, re.I))
    strong_start = bool(
        (fbi_header and case_label)
        or fd302
        or ec
        or transcription
        or (marker and marker.get("current") == 1)
    )
    weak_start = bool(fbi_header or case_label or interview)
    return {
        "physical_page": page,
        "exact_same_index": bool(canonical(text)) and canonical(text) == canonical(normalized_text),
        "fbi_header": fbi_header,
        "fd302_marker": fd302,
        "electronic_communication_marker": ec,
        "date_of_transcription_marker": transcription,
        "case_or_file_label": case_label,
        "interview_language_marker": interview,
        "continuation_marker": continuation,
        "page_marker": marker,
        "strong_record_start_signal": strong_start,
        "weak_record_start_signal": weak_start,
    }


def candidate_boundary_hypotheses(boundary: dict) -> list[dict]:
    out = []
    for item in boundary.get("targets") or []:
        if item.get("kind") != "heuristic_candidate_review":
            continue
        pages = item.get("diagnostic_pages") or []
        candidate_pages = [p for p in pages if p.get("role") == "candidate"]
        after = next((p for p in pages if p.get("role") == "after"), None)
        transition = item.get("transition") or {}
        if not candidate_pages:
            continue
        first = candidate_pages[0]
        after_starts_new = bool(after and after.get("fbi_header") and after.get("case_or_file_label"))
        bracketed = bool(
            item.get("all_diagnostic_pages_exact")
            and transition.get("start_record_signal")
            and not transition.get("extends_left_signal")
            and not transition.get("extends_right_signal")
            and after_starts_new
        )
        out.append({
            "target_id": item.get("target_id"),
            "parent_doc_id": item.get("parent_doc_id"),
            "parent_sha256": item.get("parent_sha256"),
            "proposed_start": item.get("proposed_start"),
            "proposed_end": item.get("proposed_end"),
            "start_page_has_record_start_signal": bool(transition.get("start_record_signal")),
            "page_after_has_strong_new_record_signal": after_starts_new,
            "extends_left_signal": bool(transition.get("extends_left_signal")),
            "extends_right_signal": bool(transition.get("extends_right_signal")),
            "all_diagnostic_pages_exact": bool(item.get("all_diagnostic_pages_exact")),
            "hypothesis_status": (
                "BRACKETED_BY_NEXT_RECORD_START_PENDING_VISUAL_CONFIRMATION"
                if bracketed
                else "UNRESOLVED_BOUNDARY_HYPOTHESIS"
            ),
            "boundary_confirmed": False,
            "visual_confirmation_required": True,
            "record_promoted": False,
        })
    return out


def benomrane_anchor(root: Path) -> tuple[str, list[int]] | None:
    recovery = load_json(root / "local/index/911-named-source-segment-map.json", {})
    for target in recovery.get("targets") or []:
        if target.get("target_id") != BENOMRANE_TARGET_ID:
            continue
        positions = target.get("eo14040_candidate_positions") or []
        if not positions:
            return None
        doc_id = str(positions[0].get("parent_doc_id") or "")
        pages = sorted({int(p.get("text_page_index")) for p in positions if p.get("text_page_index")})
        if doc_id and pages:
            return doc_id, pages
    return None


def benomrane_expansion(root: Path, pdftotext: str, radius: int) -> dict:
    anchor = benomrane_anchor(root)
    if not anchor:
        return {"status": "ANCHORS_UNAVAILABLE", "boundary_confirmed": False, "record_promoted": False}
    doc_id, anchors = anchor
    meta = load_json(root / "metadata" / f"{doc_id}.json", {})
    raw = Path(str(meta.get("local_raw_path") or ""))
    normalized = Path(str(meta.get("normalized_text_path") or ""))
    expected_sha = str(meta.get("sha256") or "")
    base = {
        "target_id": "BENOMRANE-EXPANDED-GAP-SEARCH",
        "source_target_id": BENOMRANE_TARGET_ID,
        "parent_doc_id": doc_id,
        "parent_sha256": expected_sha,
        "anchor_pages": anchors,
        "search_radius": radius,
        "boundary_confirmed": False,
        "record_promoted": False,
        "evidence_state_mutated": False,
    }
    if not raw.is_file() or not normalized.is_file():
        return {**base, "status": "LOCAL_ARTIFACT_UNAVAILABLE"}
    actual_sha = sha256_file(raw)
    if not expected_sha or actual_sha != expected_sha:
        return {**base, "status": "PARENT_SHA_MISMATCH", "actual_parent_sha256": actual_sha}

    chunks = normalized.read_text(encoding="utf-8", errors="replace").split("\f")
    min_anchor, max_anchor = min(anchors), max(anchors)
    start = max(1, min_anchor - radius)
    end = min(len(chunks), max_anchor + radius)
    rows = []
    for page in range(start, end + 1):
        text = physical_page_text(pdftotext, raw, page)
        row = structural_features(text, chunks[page - 1] if page <= len(chunks) else "", page)
        rows.append(row)

    exact_rows = [r for r in rows if r.get("exact_same_index")]
    all_exact = len(exact_rows) == len(rows) and bool(rows)
    strong_starts = [r["physical_page"] for r in rows if r.get("strong_record_start_signal") and r.get("exact_same_index")]
    weak_starts = [r["physical_page"] for r in rows if r.get("weak_record_start_signal") and r.get("exact_same_index")]
    left_candidates = [p for p in strong_starts if p <= min_anchor]
    right_candidates = [p for p in strong_starts if p > max_anchor]
    left_start = max(left_candidates) if left_candidates else None
    right_start = min(right_candidates) if right_candidates else None
    proposed_start = left_start
    proposed_end = (right_start - 1) if right_start is not None else None
    span = (proposed_end - proposed_start + 1) if proposed_start and proposed_end and proposed_end >= proposed_start else None

    if not all_exact:
        status = "UNRESOLVED_PAGE_MAPPING_IN_SEARCH_WINDOW"
    elif proposed_start is not None and proposed_end is not None and proposed_start <= min_anchor <= max_anchor <= proposed_end:
        status = "BRACKETED_GAP_CANDIDATE_REVIEW" if span is not None and span <= 60 else "BRACKET_TOO_WIDE_REVIEW"
    elif proposed_start is not None or proposed_end is not None:
        status = "ONE_SIDED_GAP_BOUNDARY_REVIEW"
    else:
        status = "NO_STRONG_BOUNDARY_SIGNALS_IN_WINDOW"

    # No source text is retained. Only page numbers and structural booleans.
    return {
        **base,
        "status": status,
        "search_start": start,
        "search_end": end,
        "all_search_pages_exact": all_exact,
        "strong_record_start_pages": strong_starts,
        "weak_record_start_pages": weak_starts,
        "nearest_strong_start_at_or_before_anchors": left_start,
        "nearest_strong_start_after_anchors": right_start,
        "proposed_review_start": proposed_start,
        "proposed_review_end": proposed_end,
        "proposed_review_span_pages": span,
        "proposed_range_is_boundary_claim": False,
        "visual_confirmation_required": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Review 007 boundary hypotheses and Benomrane expansion")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--radius", type=int, default=35)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required")

    boundary = load_json(root / "local/index/911-review-007-boundary-diagnostic.json", {})
    if not boundary.get("targets"):
        raise RuntimeError("Review 007 boundary diagnostic is unavailable")

    candidates = candidate_boundary_hypotheses(boundary)
    benomrane = benomrane_expansion(root, pdftotext, max(5, args.radius))
    payload = {
        "schema_version": 1,
        "object_type": "review_007_boundary_followup",
        "purpose": "record bracket hypotheses plus widened Benomrane segmentation-gap search; review only",
        "contains_text_previews": False,
        "boundary_claims": False,
        "record_promotions": 0,
        "evidence_state_mutated": False,
        "candidate_boundary_hypotheses": candidates,
        "benomrane_expansion": benomrane,
    }
    out = root / "local/index/911-review-007-boundary-followup.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "candidate_hypotheses": {x["target_id"]: x["hypothesis_status"] for x in candidates},
        "benomrane_status": benomrane.get("status"),
        "benomrane_proposed_range": (
            [benomrane.get("proposed_review_start"), benomrane.get("proposed_review_end")]
            if benomrane.get("proposed_review_start") and benomrane.get("proposed_review_end")
            else None
        ),
        "contains_text_previews": False,
        "boundary_claims": False,
        "record_promotions": 0,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
