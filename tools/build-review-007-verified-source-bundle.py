#!/usr/bin/env python3
"""Build a tightly bounded Review 007 source-image bundle after page verification.

This is a review-only helper. It consumes the local Review 007 segment map and
physical-page map, verifies every page in each proposed review range with the
same exact `pdftotext -layout` comparison used by the physical-page mapper, and
only then extracts a local PDF slice.

It does not establish child-record boundaries, promote records, mutate evidence
state, or publish source PDF bytes to Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return " ".join(text.replace("\f", " ").split())


def physical_page_text(pdftotext: str, pdf: Path, page: int) -> str:
    proc = subprocess.run(
        [pdftotext, "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else ""


def verify_same_index_range(pdftotext: str, pdf: Path, normalized: Path, start: int, end: int) -> dict:
    chunks = normalized.read_text(encoding="utf-8", errors="replace").split("\f")
    checks = []
    for page in range(start, end + 1):
        if page < 1 or page > len(chunks):
            checks.append({"text_page": page, "physical_page": None, "verified": False, "status": "TEXT_PAGE_OUT_OF_RANGE"})
            continue
        target = canonical(chunks[page - 1])
        if not target:
            checks.append({"text_page": page, "physical_page": None, "verified": False, "status": "EMPTY_NORMALIZED_TEXT"})
            continue
        physical = canonical(physical_page_text(pdftotext, pdf, page))
        ok = bool(physical) and physical == target
        checks.append({
            "text_page": page,
            "physical_page": page if ok else None,
            "verified": ok,
            "status": "EXACT_SAME_INDEX" if ok else "UNRESOLVED_NO_EXACT_MATCH",
        })
    return {
        "start": start,
        "end": end,
        "all_pages_verified": bool(checks) and all(x["verified"] for x in checks),
        "verified_count": sum(1 for x in checks if x["verified"]),
        "page_count": len(checks),
        "checks": checks,
    }


def extract_range(parent: Path, start: int, end: int, out: Path) -> str:
    qpdf = shutil.which("qpdf")
    if qpdf:
        subprocess.run([qpdf, str(parent), "--pages", str(parent), f"{start}-{end}", "--", str(out)], check=True)
        return "qpdf"
    sep, unite = shutil.which("pdfseparate"), shutil.which("pdfunite")
    if sep and unite:
        with tempfile.TemporaryDirectory(prefix="blackindex-review007-") as td:
            pattern = str(Path(td) / "page-%d.pdf")
            subprocess.run([sep, "-f", str(start), "-l", str(end), str(parent), pattern], check=True)
            pages = [str(Path(td) / f"page-{n}.pdf") for n in range(start, end + 1)]
            subprocess.run([unite, *pages, str(out)], check=True)
        return "pdfseparate+pdfunite"
    raise RuntimeError("requires qpdf or pdfseparate+pdfunite")


def anchor_map(physical: dict) -> dict[tuple[str, int], dict]:
    out = {}
    for target in physical.get("targets") or []:
        for pos in target.get("positions") or []:
            doc_id = str(pos.get("parent_doc_id") or "")
            text_page = int(pos.get("text_page_index") or 0)
            if doc_id and text_page:
                out[(doc_id, text_page)] = pos
    return out


def find_segment(segment_map: dict, candidate_id: str) -> tuple[str, int, int] | None:
    for target in segment_map.get("targets") or []:
        for pos in target.get("eo14040_candidate_positions") or []:
            for seg in pos.get("segments") or []:
                if seg.get("candidate_id") == candidate_id:
                    return str(pos.get("parent_doc_id")), int(seg.get("start_page")), int(seg.get("end_page"))
    return None


def find_benomrane_positions(segment_map: dict) -> tuple[str, list[int]] | None:
    for target in segment_map.get("targets") or []:
        if target.get("target_id") != "BENOMRANE-INTERVIEWS-2002":
            continue
        positions = target.get("eo14040_candidate_positions") or []
        if not positions:
            return None
        doc_id = str(positions[0].get("parent_doc_id") or "")
        pages = sorted({int(p.get("text_page_index")) for p in positions if p.get("text_page_index")})
        return (doc_id, pages) if doc_id and pages else None
    return None


def build_targets(segment_map: dict) -> list[dict]:
    targets = []
    for candidate_id in ("CAND-0005", "CAND-0013"):
        found = find_segment(segment_map, candidate_id)
        if found:
            doc_id, start, end = found
            targets.append({
                "target_id": candidate_id,
                "kind": "heuristic_candidate_review",
                "parent_doc_id": doc_id,
                "start": start,
                "end": end,
                "boundary_claim": False,
            })
    ben = find_benomrane_positions(segment_map)
    if ben:
        doc_id, pages = ben
        targets.append({
            "target_id": "BENOMRANE-GAP-WINDOW",
            "kind": "segmentation_gap_diagnostic",
            "parent_doc_id": doc_id,
            "start": max(1, min(pages) - 2),
            "end": max(pages) + 2,
            "anchor_pages": pages,
            "boundary_claim": False,
        })
    return targets


def main() -> int:
    ap = argparse.ArgumentParser(description="Build Review 007 source-image bundle from fully verified page ranges")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required")

    segment_map = load_json(root / "local/index/911-named-source-segment-map.json", {})
    physical_map = load_json(root / "local/index/911-review-007-physical-page-map.json", {})
    if physical_map.get("unresolved_position_count") not in (0, "0") or int(physical_map.get("verified_position_count") or 0) < 4:
        raise RuntimeError("Review 007 physical-page gate is not fully satisfied")

    anchors = anchor_map(physical_map)
    out_dir = root / "local/review/source-bundles/review-007-verified"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for target in build_targets(segment_map):
        doc_id = target["parent_doc_id"]
        meta = load_json(root / "metadata" / f"{doc_id}.json", {})
        raw = Path(str(meta.get("local_raw_path") or ""))
        normalized = Path(str(meta.get("normalized_text_path") or ""))
        expected_sha = str(meta.get("sha256") or "")
        result = {**target, "parent_sha256": expected_sha, "record_promoted": False, "evidence_state_mutated": False}

        if not raw.is_file() or not normalized.is_file():
            result.update({"status": "LOCAL_ARTIFACT_UNAVAILABLE", "range_verified": False})
            results.append(result)
            continue
        actual_sha = sha256_file(raw)
        if not expected_sha or actual_sha != expected_sha:
            result.update({"status": "PARENT_SHA_MISMATCH", "range_verified": False, "actual_parent_sha256": actual_sha})
            results.append(result)
            continue

        # Require any known recovery anchor within this range to have already
        # passed the dedicated exact physical-page checkpoint.
        relevant_anchors = [
            pos for (anchor_doc, page), pos in anchors.items()
            if anchor_doc == doc_id and target["start"] <= page <= target["end"]
        ]
        if not relevant_anchors or not all(bool(p.get("physical_page_verified")) for p in relevant_anchors):
            result.update({"status": "ANCHOR_GATE_UNSATISFIED", "range_verified": False})
            results.append(result)
            continue

        verification = verify_same_index_range(pdftotext, raw, normalized, target["start"], target["end"])
        result["range_verification"] = verification
        result["range_verified"] = verification["all_pages_verified"]
        if not verification["all_pages_verified"]:
            result["status"] = "PAGE_RANGE_UNRESOLVED"
            results.append(result)
            continue

        out = out_dir / f"{target['target_id']}-{doc_id}-p{target['start']}-{target['end']}.pdf"
        if out.exists():
            out.unlink()
        method = extract_range(raw, target["start"], target["end"], out)
        if out.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"invalid review PDF generated: {out}")
        result.update({
            "status": "REVIEW_SLICE_READY",
            "source_pdf": str(out),
            "source_pdf_sha256": sha256_file(out),
            "extraction_method": method,
            "physical_range": f"{target['start']}-{target['end']}",
            "boundary_verified": False,
        })
        results.append(result)

    manifest = {
        "schema_version": 1,
        "object_type": "review_007_verified_source_bundle",
        "purpose": "source-image review only after exact page-range verification",
        "record_promotions": 0,
        "evidence_state_mutated": False,
        "boundary_claims": False,
        "targets": results,
        "ready_count": sum(1 for r in results if r.get("status") == "REVIEW_SLICE_READY"),
        "target_count": len(results),
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "bundle": str(out_dir),
        "manifest": str(manifest_path),
        "targets": manifest["target_count"],
        "ready": manifest["ready_count"],
        "record_promotions": 0,
        "boundary_claims": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
