#!/usr/bin/env python3
"""Build small source-PDF review artifacts for triaged FBI candidates.

Review-only: this extracts heuristic candidate page ranges from immutable parent
containers into local/review/source-bundles so a reviewer can confirm true
record boundaries against the source images. It does not ingest or promote the
extracted files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract(parent: Path, start: int, end: int, out: Path) -> str:
    qpdf = shutil.which("qpdf")
    if qpdf:
        subprocess.run([qpdf, str(parent), "--pages", str(parent), f"{start}-{end}", "--", str(out)], check=True)
        return "qpdf"
    sep, unite = shutil.which("pdfseparate"), shutil.which("pdfunite")
    if sep and unite:
        with tempfile.TemporaryDirectory(prefix="blackindex-review-") as td:
            pattern = str(Path(td) / "page-%d.pdf")
            subprocess.run([sep, "-f", str(start), "-l", str(end), str(parent), pattern], check=True)
            pages = [str(Path(td) / f"page-{n}.pdf") for n in range(start, end + 1)]
            subprocess.run([unite, *pages, str(out)], check=True)
        return "pdfseparate+pdfunite"
    raise RuntimeError("requires qpdf or pdfseparate+pdfunite")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build review-only source PDF bundle from FBI triage")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--triage", default="local/index/triage/911-fbi-segmentation-priority.json")
    ap.add_argument("--band", default="P0")
    ap.add_argument("--record-type", default="fd_302", help="Filter record_type_guess; empty means any")
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    triage = Path(args.triage)
    if not triage.is_absolute():
        triage = root / triage
    payload = load(triage)
    rows = payload.get("all_candidates") or payload.get("top_candidates") or payload.get("candidates") or []

    chosen = []
    for row in rows:
        band = row.get("review_priority_band") or row.get("priority_band") or row.get("priority") or row.get("band")
        rtype = row.get("record_type_guess") or row.get("record_type") or row.get("type")
        if band != args.band:
            continue
        if args.record_type and rtype != args.record_type:
            continue
        chosen.append(row)
        if args.limit and len(chosen) >= args.limit:
            break

    out_dir = root / "local/review/source-bundles/911-fbi-first-promotion"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx, row in enumerate(chosen, 1):
        doc_id = row.get("container_doc_id") or row.get("container") or row.get("doc_id")
        cand = row.get("candidate_id") or row.get("candidate")
        start = int(row.get("start_page") or row.get("page_start"))
        end = int(row.get("end_page") or row.get("page_end") or start)
        meta = load(root / "metadata" / f"{doc_id}.json")
        parent = Path(meta["local_raw_path"])
        if sha256(parent) != meta.get("sha256"):
            raise RuntimeError(f"parent SHA mismatch: {doc_id}")
        out = out_dir / f"{idx:02d}-{doc_id}-{cand}-p{start}-{end}.pdf"
        method = extract(parent, start, end, out)
        if out.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"invalid extracted PDF: {out}")
        manifest.append({
            "review_rank": idx,
            "container_doc_id": doc_id,
            "candidate_id": cand,
            "heuristic_pages": f"{start}-{end}",
            "record_type_guess": row.get("record_type_guess") or row.get("record_type"),
            "entity_hits": row.get("entity_hits") or row.get("entities") or [],
            "source_pdf": str(out),
            "source_pdf_sha256": sha256(out),
            "extraction_method": method,
            "status": "REVIEW_ONLY_UNCONFIRMED_BOUNDARY",
        })

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"count": len(manifest), "records": manifest}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bundle": str(out_dir), "count": len(manifest), "manifest": str(manifest_path), "records": manifest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
