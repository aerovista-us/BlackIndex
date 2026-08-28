#!/usr/bin/env python3
"""Review 007 structural boundary diagnostics for verified local source slices.

Review-only. This tool consumes the verified source-bundle manifest, re-verifies
physical↔normalized correspondence for each target plus one page on either side,
and records structural FBI-record signals without publishing source text.

It never promotes records, mutates evidence state, or treats heuristic output as
a confirmed child-record boundary.
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def normalized_page(chunks: list[str], page: int) -> str:
    if page < 1 or page > len(chunks):
        return ""
    return chunks[page - 1]


def clean_lines(text: str) -> list[str]:
    return [" ".join(line.split()) for line in text.splitlines() if line.strip()]


def header_signature(lines: list[str]) -> str:
    head = " | ".join(lines[:12]).upper()
    head = re.sub(r"\d", "#", head)
    head = re.sub(r"\s+", " ", head)
    return sha256_text(head) if head else ""


def identifier_signature(lines: list[str]) -> str:
    selected = []
    for line in lines[:40]:
        if re.search(r"\b(file|case|serial|investigation|bureau file|office file|classification)\b", line, re.I):
            selected.append(re.sub(r"\s+", " ", line).strip().upper())
    return sha256_text(" | ".join(selected)) if selected else ""


def page_marker(text: str) -> dict | None:
    patterns = [
        r"\bpage\s+(\d{1,4})\s+(?:of|/)\s+(\d{1,4})\b",
        r"\bpg\.?\s*(\d{1,4})\s+(?:of|/)\s+(\d{1,4})\b",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            current, total = int(m.group(1)), int(m.group(2))
            if current >= 1 and total >= current:
                return {"current": current, "total": total}
    return None


def features(text: str, page: int, normalized_text: str) -> dict:
    canon_phys = canonical(text)
    canon_norm = canonical(normalized_text)
    lines = clean_lines(text)
    marker = page_marker(text)
    exact = bool(canon_phys) and canon_phys == canon_norm
    return {
        "physical_page": page,
        "exact_same_index": exact,
        "char_count": len(canon_phys),
        "line_count": len(lines),
        "fbi_header": bool(re.search(r"FEDERAL\s+BUREAU\s+OF\s+INVESTIGATION", text, re.I)),
        "fd302_marker": bool(re.search(r"\bFD[-\s]?302(?:A)?\b", text, re.I)),
        "electronic_communication_marker": bool(re.search(r"\bELECTRONIC\s+COMMUNICATION\b", text, re.I)),
        "continuation_marker": bool(re.search(r"\bCONTINU(?:ED|ATION)\b", text, re.I)),
        "date_of_transcription_marker": bool(re.search(r"DATE\s+OF\s+TRANSCRIPTION", text, re.I)),
        "case_or_file_label": bool(re.search(r"\b(?:CASE|FILE)(?:\s+ID|\s+NO\.?|\s+NUMBER|\s*#)\b", text, re.I)),
        "interview_language_marker": bool(re.search(r"\b(?:WAS|WERE)\s+INTERVIEWED\b|\bINTERVIEW\s+OF\b", text, re.I)),
        "page_marker": marker,
        "header_signature_sha256": header_signature(lines),
        "identifier_signature_sha256": identifier_signature(lines),
    }


def same_nonempty(a: str, b: str) -> bool:
    return bool(a) and bool(b) and a == b


def transition_summary(before: dict | None, first: dict, last: dict, after: dict | None) -> dict:
    first_marker = first.get("page_marker") or {}
    last_marker = last.get("page_marker") or {}

    left_same_id = bool(before) and same_nonempty(before.get("identifier_signature_sha256", ""), first.get("identifier_signature_sha256", ""))
    right_same_id = bool(after) and same_nonempty(last.get("identifier_signature_sha256", ""), after.get("identifier_signature_sha256", ""))
    left_same_header = bool(before) and same_nonempty(before.get("header_signature_sha256", ""), first.get("header_signature_sha256", ""))
    right_same_header = bool(after) and same_nonempty(last.get("header_signature_sha256", ""), after.get("header_signature_sha256", ""))

    start_signal = bool(
        first.get("fbi_header")
        or first.get("fd302_marker")
        or first.get("electronic_communication_marker")
        or first.get("date_of_transcription_marker")
        or first_marker.get("current") == 1
    )
    terminal_signal = bool(last_marker and last_marker.get("current") == last_marker.get("total"))

    extends_left = bool(
        first.get("continuation_marker")
        or (first_marker.get("current") or 0) > 1
        or left_same_id
    )
    extends_right = bool(
        (last_marker and (last_marker.get("current") or 0) < (last_marker.get("total") or 0))
        or right_same_id
    )

    left_boundary_signal = bool(start_signal and not extends_left and not left_same_header)
    right_boundary_signal = bool(terminal_signal and not extends_right and not right_same_header)

    return {
        "left_same_identifier_signature": left_same_id,
        "right_same_identifier_signature": right_same_id,
        "left_same_header_signature": left_same_header,
        "right_same_header_signature": right_same_header,
        "start_record_signal": start_signal,
        "terminal_page_signal": terminal_signal,
        "extends_left_signal": extends_left,
        "extends_right_signal": extends_right,
        "left_boundary_signal": left_boundary_signal,
        "right_boundary_signal": right_boundary_signal,
    }


def disposition(kind: str, transition: dict, all_pages_exact: bool) -> str:
    if not all_pages_exact:
        return "UNRESOLVED_PAGE_MAPPING"
    if kind == "segmentation_gap_diagnostic":
        return "SEGMENTATION_GAP_WINDOW_REVIEW"
    if transition["extends_left_signal"] or transition["extends_right_signal"]:
        return "LIKELY_EXTENDS_OUTSIDE_PROPOSED_RANGE"
    if transition["left_boundary_signal"] and transition["right_boundary_signal"]:
        return "STRUCTURALLY_SELF_CONTAINED_CANDIDATE"
    return "MANUAL_IMAGE_REVIEW_REQUIRED"


def analyze_target(root: Path, pdftotext: str, target: dict) -> dict:
    doc_id = str(target.get("parent_doc_id") or "")
    start = int(target.get("start") or 0)
    end = int(target.get("end") or 0)
    kind = str(target.get("kind") or "")
    meta = load_json(root / "metadata" / f"{doc_id}.json", {})
    raw = Path(str(meta.get("local_raw_path") or ""))
    normalized = Path(str(meta.get("normalized_text_path") or ""))
    expected_sha = str(meta.get("sha256") or "")

    base = {
        "target_id": target.get("target_id"),
        "kind": kind,
        "parent_doc_id": doc_id,
        "parent_sha256": expected_sha,
        "proposed_start": start,
        "proposed_end": end,
        "boundary_verified": False,
        "record_promoted": False,
        "evidence_state_mutated": False,
    }

    if not raw.is_file() or not normalized.is_file() or start < 1 or end < start:
        return {**base, "status": "LOCAL_ARTIFACT_UNAVAILABLE", "disposition": "UNRESOLVED_PAGE_MAPPING"}
    actual_sha = sha256_file(raw)
    if actual_sha != expected_sha:
        return {**base, "status": "PARENT_SHA_MISMATCH", "actual_parent_sha256": actual_sha, "disposition": "UNRESOLVED_PAGE_MAPPING"}

    chunks = normalized.read_text(encoding="utf-8", errors="replace").split("\f")
    diagnostic_start = max(1, start - 1)
    diagnostic_end = min(len(chunks), end + 1)
    page_rows = []
    for page in range(diagnostic_start, diagnostic_end + 1):
        row = features(physical_page_text(pdftotext, raw, page), page, normalized_page(chunks, page))
        row["role"] = "before" if page < start else "after" if page > end else "candidate"
        page_rows.append(row)

    all_exact = bool(page_rows) and all(row["exact_same_index"] for row in page_rows)
    candidate_rows = [row for row in page_rows if row["role"] == "candidate"]
    before = next((row for row in page_rows if row["role"] == "before"), None)
    after = next((row for row in page_rows if row["role"] == "after"), None)
    if not candidate_rows:
        return {**base, "status": "NO_CANDIDATE_PAGES", "diagnostic_pages": page_rows, "disposition": "UNRESOLVED_PAGE_MAPPING"}

    trans = transition_summary(before, candidate_rows[0], candidate_rows[-1], after)
    return {
        **base,
        "status": "STRUCTURAL_DIAGNOSTIC_COMPLETE" if all_exact else "DIAGNOSTIC_PAGE_UNRESOLVED",
        "diagnostic_start": diagnostic_start,
        "diagnostic_end": diagnostic_end,
        "all_diagnostic_pages_exact": all_exact,
        "diagnostic_pages": page_rows,
        "transition": trans,
        "disposition": disposition(kind, trans, all_exact),
    }


def sanitize_target(result: dict) -> dict:
    # Result is already text-free. Keep only structured features/hashes.
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Run Review 007 structural boundary diagnostics")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required")

    manifest_path = root / "local/review/source-bundles/review-007-verified/manifest.json"
    manifest = load_json(manifest_path, {})
    ready = [t for t in manifest.get("targets") or [] if t.get("status") == "REVIEW_SLICE_READY"]
    if not ready:
        raise RuntimeError("verified Review 007 source bundle is unavailable or has no ready targets")

    results = [analyze_target(root, pdftotext, target) for target in ready]
    payload = {
        "schema_version": 1,
        "object_type": "review_007_boundary_diagnostic",
        "purpose": "structural source-boundary diagnostics; review only",
        "contains_text_previews": False,
        "boundary_claims": False,
        "record_promotions": 0,
        "evidence_state_mutated": False,
        "target_count": len(results),
        "targets": [sanitize_target(r) for r in results],
    }

    out_json = root / "local/index/911-review-007-boundary-diagnostic.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out_json),
        "targets": len(results),
        "contains_text_previews": False,
        "boundary_claims": False,
        "record_promotions": 0,
        "dispositions": {r["target_id"]: r["disposition"] for r in results},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
