#!/usr/bin/env python3
"""Verify Review 007 normalized-text page positions against physical PDF pages.

This tool is deliberately conservative. It uses the same `pdftotext -layout`
method BlackIndex used to create normalized text, extracts individual physical
PDF pages, canonicalizes whitespace, and accepts a mapping only when the
canonical text is an exact match.

No OCR, fuzzy promotion, evidence-state mutation, child promotion, or source
slice creation occurs here. A unique exact match may verify a physical page;
ambiguous or unmatched positions remain unresolved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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


def digest(text: str) -> str:
    return hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()


def physical_page_text(pdftotext: str, pdf: Path, page: int) -> str:
    proc = subprocess.run(
        [pdftotext, "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout


def choose_exact(text_page: int, normalized_text: str, physical_texts: dict[int, str]) -> dict:
    target = canonical(normalized_text)
    if not target:
        return {
            "mapping_status": "EMPTY_NORMALIZED_TEXT",
            "physical_page_index": None,
            "physical_page_verified": False,
            "exact_match_pages": [],
        }
    matches = [page for page, value in sorted(physical_texts.items()) if canonical(value) == target]
    if len(matches) == 1:
        page = matches[0]
        return {
            "mapping_status": "EXACT_SAME_INDEX" if page == text_page else "EXACT_NEARBY",
            "physical_page_index": page,
            "physical_page_verified": True,
            "exact_match_pages": matches,
        }
    if len(matches) > 1:
        return {
            "mapping_status": "AMBIGUOUS_EXACT_MATCH",
            "physical_page_index": None,
            "physical_page_verified": False,
            "exact_match_pages": matches,
        }
    return {
        "mapping_status": "UNRESOLVED_NO_EXACT_MATCH",
        "physical_page_index": None,
        "physical_page_verified": False,
        "exact_match_pages": [],
    }


def map_positions(root: Path, radius: int = 4) -> dict:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required")

    segment_map = load_json(root / "local/index/911-named-source-segment-map.json", {})
    outputs = []
    cache: dict[tuple[str, int], str] = {}

    for target in segment_map.get("targets") or []:
        mapped_positions = []
        for pos in target.get("eo14040_candidate_positions") or []:
            doc_id = str(pos.get("parent_doc_id") or "")
            text_page = int(pos.get("text_page_index") or 0)
            meta = load_json(root / "metadata" / f"{doc_id}.json", {})
            raw = Path(str(meta.get("local_raw_path") or ""))
            normalized = Path(str(meta.get("normalized_text_path") or ""))
            if not raw.is_file() or not normalized.is_file() or text_page < 1:
                mapped_positions.append({
                    "parent_doc_id": doc_id,
                    "parent_sha256": pos.get("parent_sha256") or meta.get("sha256"),
                    "text_page_index": text_page,
                    "mapping_status": "LOCAL_ARTIFACT_UNAVAILABLE",
                    "physical_page_index": None,
                    "physical_page_verified": False,
                    "exact_match_pages": [],
                })
                continue

            chunks = normalized.read_text(encoding="utf-8", errors="replace").split("\f")
            if text_page > len(chunks):
                mapped_positions.append({
                    "parent_doc_id": doc_id,
                    "parent_sha256": pos.get("parent_sha256") or meta.get("sha256"),
                    "text_page_index": text_page,
                    "mapping_status": "TEXT_PAGE_OUT_OF_RANGE",
                    "physical_page_index": None,
                    "physical_page_verified": False,
                    "exact_match_pages": [],
                })
                continue

            normalized_chunk = chunks[text_page - 1]
            physical_texts: dict[int, str] = {}
            for page in range(max(1, text_page - radius), text_page + radius + 1):
                key = (doc_id, page)
                if key not in cache:
                    cache[key] = physical_page_text(pdftotext, raw, page)
                physical_texts[page] = cache[key]

            result = choose_exact(text_page, normalized_chunk, physical_texts)
            mapped_positions.append({
                "parent_doc_id": doc_id,
                "parent_sha256": pos.get("parent_sha256") or meta.get("sha256"),
                "text_page_index": text_page,
                "normalized_text_sha256": digest(normalized_chunk),
                "search_radius": radius,
                **result,
            })
        outputs.append({
            "target_id": target.get("target_id"),
            "label": target.get("label"),
            "positions": mapped_positions,
        })

    positions = [p for t in outputs for p in t["positions"]]
    return {
        "schema_version": 1,
        "object_type": "review_007_physical_page_map",
        "method": "exact canonical text comparison using pdftotext -layout on individual PDF pages",
        "ocr_used": False,
        "fuzzy_match_used": False,
        "evidence_state_mutated": False,
        "record_promotions": 0,
        "position_count": len(positions),
        "verified_position_count": sum(1 for p in positions if p.get("physical_page_verified")),
        "unresolved_position_count": sum(1 for p in positions if not p.get("physical_page_verified")),
        "targets": outputs,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# BlackIndex Review 007 — Physical Page Verification",
        "",
        "> A physical page is marked verified only when the normalized form-feed chunk has one unique exact canonical-text match in the checked physical-page window using the same `pdftotext -layout` method used for normalization.",
        "",
        f"- Positions checked: **{report['position_count']}**",
        f"- Positions verified: **{report['verified_position_count']}**",
        f"- Positions unresolved: **{report['unresolved_position_count']}**",
        "- OCR used: `false`",
        "- Fuzzy matching used: `false`",
        "- Record promotion: `none`",
        "",
    ]
    for target in report.get("targets") or []:
        lines += [f"## {target.get('label') or target.get('target_id')}", ""]
        for pos in target.get("positions") or []:
            lines += [
                f"- `{pos.get('parent_doc_id')}` text page `{pos.get('text_page_index')}`",
                f"  - mapping status: `{pos.get('mapping_status')}`",
                f"  - physical page: `{pos.get('physical_page_index') if pos.get('physical_page_verified') else 'UNVERIFIED'}`",
                f"  - verified: `{str(bool(pos.get('physical_page_verified'))).lower()}`",
            ]
            if pos.get("exact_match_pages"):
                lines.append(f"  - exact match page(s): `{', '.join(map(str, pos['exact_match_pages']))}`")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify Review 007 normalized text positions against physical PDF pages")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--radius", type=int, default=4)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    report = map_positions(root, max(0, args.radius))
    json_path = root / "local/index/911-review-007-physical-page-map.json"
    md_path = root / "local/review/911-review-007-physical-page-map.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "json": str(json_path),
        "markdown": str(md_path),
        "positions": report["position_count"],
        "verified": report["verified_position_count"],
        "unresolved": report["unresolved_position_count"],
        "ocr_used": False,
        "fuzzy_match_used": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
