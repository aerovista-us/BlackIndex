#!/usr/bin/env python3
"""Promote human-reviewed FBI segmentation candidates into BlackIndex child records.

Fail-closed rules:
- default is dry-run; --apply is required to modify the corpus;
- only review-ledger entries with disposition=PROMOTE are eligible;
- confirmed page ranges are mandatory;
- the immutable parent raw PDF and its SHA-256 must match metadata;
- page extraction must succeed before intake;
- child metadata preserves parent container, page range, candidate id, review
  timestamp, redactions, source dependency, and promotion disposition.

This tool does not decide whether a candidate should be promoted. That judgment
must already exist in local/review/911-fbi-p0/review-ledger.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
PAGE_RE = re.compile(r"^(\d+)(?:-(\d+))?$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_pages(value: str) -> tuple[int, int]:
    m = PAGE_RE.match(value.strip())
    if not m:
        raise ValueError(f"invalid confirmed page range: {value!r}")
    start = int(m.group(1))
    end = int(m.group(2) or start)
    if start < 1 or end < start:
        raise ValueError(f"invalid confirmed page range: {value!r}")
    return start, end


def extract_pages(parent: Path, start: int, end: int, out: Path) -> str:
    qpdf = shutil.which("qpdf")
    if qpdf:
        cmd = [qpdf, str(parent), "--pages", str(parent), f"{start}-{end}", "--", str(out)]
        subprocess.run(cmd, check=True)
        return "qpdf"

    pdfseparate = shutil.which("pdfseparate")
    pdfunite = shutil.which("pdfunite")
    if pdfseparate and pdfunite:
        with tempfile.TemporaryDirectory(prefix="blackindex-pages-") as td:
            pattern = str(Path(td) / "page-%d.pdf")
            subprocess.run([pdfseparate, "-f", str(start), "-l", str(end), str(parent), pattern], check=True)
            pages = [str(Path(td) / f"page-{n}.pdf") for n in range(start, end + 1)]
            missing = [p for p in pages if not Path(p).exists()]
            if missing:
                raise RuntimeError(f"pdfseparate did not create expected pages: {missing[:3]}")
            subprocess.run([pdfunite, *pages, str(out)], check=True)
        return "pdfseparate+pdfunite"

    raise RuntimeError("page extraction requires qpdf or both pdfseparate and pdfunite")


def intake_child(root: Path, review: dict, parent_meta: dict, child_pdf: Path) -> str:
    record_date = review.get("record_date") or None
    year = record_date[:4] if record_date and len(record_date) >= 4 else parent_meta.get("year_bucket") or "undated"
    record_type = review.get("record_type") or "FBI record"
    serial = review.get("serial_or_case_id")
    candidate_id = review["candidate_id"]
    title = f"{record_type} — segmented from {review['container_doc_id']} {candidate_id}"
    native = serial or f"{review['container_doc_id']}:{candidate_id}"
    parent_artifact = parent_meta.get("artifact_url") or parent_meta.get("source_url")
    landing = parent_meta.get("canonical_landing_url")
    tags = [
        "9-11", "operation-encore", "fbi", "segmented-record",
        review["container_doc_id"].lower(), candidate_id.lower(),
    ]

    cmd = [
        sys.executable, str(root / "tools/blackindex.py"), "--root", str(root), "intake", str(child_pdf),
        "--source", "FBI",
        "--collection", "EO14040 Segmented Records",
        "--year", str(year),
        "--title", title,
        "--native-id", native,
        "--call-id", "CALL-911-ENCORE-SEGMENTED",
        "--tags", ",".join(tags),
    ]
    if record_date:
        cmd += ["--document-date", record_date]
    if parent_artifact:
        cmd += ["--artifact-url", parent_artifact]
    if landing:
        cmd += ["--landing-url", landing]
    if review.get("redactions"):
        cmd += ["--redaction-note", review["redactions"]]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode not in (0, 3):
        raise RuntimeError(f"child intake failed rc={proc.returncode}: {proc.stderr or proc.stdout}")
    data = json.loads(proc.stdout)
    return data["doc_id"]


def enrich_child(root: Path, child_id: str, review: dict, parent_meta: dict, extraction_method: str) -> None:
    path = root / "metadata" / f"{child_id}.json"
    meta = load(path)
    meta.update({
        "artifact_type": review.get("record_type") or "segmented FBI record",
        "document_type": review.get("record_type"),
        "parent_container_doc_id": review["container_doc_id"],
        "parent_container_sha256": parent_meta.get("sha256"),
        "parent_page_range": review.get("confirmed_pages"),
        "segmentation_candidate_id": review["candidate_id"],
        "segmentation_extraction_method": extraction_method,
        "promotion_reviewed_at": review.get("reviewed_at"),
        "promotion_disposition": review.get("disposition"),
        "promotion_note": review.get("note"),
        "source_dependencies": [
            {
                "type": "extracted-from-parent-container",
                "parent_doc_id": review["container_doc_id"],
                "parent_sha256": parent_meta.get("sha256"),
                "page_range": review.get("confirmed_pages"),
                "candidate_id": review["candidate_id"],
            }
        ],
        "related_documents": [review["container_doc_id"]],
        "state_of_record": "R1",
        "evidence_status": "reviewed",
    })
    write(path, meta)


def eligible_reviews(root: Path) -> list[dict]:
    ledger = root / "local/review/911-fbi-p0/review-ledger.json"
    if not ledger.exists():
        return []
    payload = load(ledger)
    return [r for r in payload.get("reviews", []) if r.get("disposition") == "PROMOTE" and r.get("promotion_ready")]


def main() -> int:
    ap = argparse.ArgumentParser(description="Promote reviewed FBI candidates into child BlackIndex records")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--apply", action="store_true", help="Actually extract/intake/publish local child records. Default is dry-run.")
    ap.add_argument("--publish", action="store_true", help="Publish durable metadata/extraction after successful promotion.")
    ap.add_argument("--container", default="", help="Optional container doc_id filter")
    ap.add_argument("--candidate", default="", help="Optional candidate id filter")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    rows = eligible_reviews(root)
    if args.container:
        rows = [r for r in rows if r.get("container_doc_id") == args.container]
    if args.candidate:
        rows = [r for r in rows if r.get("candidate_id") == args.candidate]

    plan = []
    for review in rows:
        parent_id = review["container_doc_id"]
        parent_meta_path = root / "metadata" / f"{parent_id}.json"
        if not parent_meta_path.exists():
            raise SystemExit(f"parent metadata missing: {parent_meta_path}")
        parent_meta = load(parent_meta_path)
        parent_raw = Path(parent_meta["local_raw_path"])
        if not parent_raw.exists():
            raise SystemExit(f"parent raw PDF missing: {parent_raw}")
        actual_parent_sha = sha256(parent_raw)
        if actual_parent_sha != parent_meta.get("sha256"):
            raise SystemExit(f"parent SHA mismatch: {parent_id}")
        start, end = parse_pages(review.get("confirmed_pages") or "")
        plan.append({
            "container_doc_id": parent_id,
            "candidate_id": review["candidate_id"],
            "confirmed_pages": f"{start}-{end}",
            "record_type": review.get("record_type"),
            "record_date": review.get("record_date"),
            "serial_or_case_id": review.get("serial_or_case_id"),
            "parent_sha256": actual_parent_sha,
        })

    if not args.apply:
        print(json.dumps({"mode": "dry-run", "eligible": len(plan), "plan": plan}, indent=2))
        return 0

    if not plan:
        print(json.dumps({"mode": "apply", "promoted": 0, "message": "No reviewed PROMOTE entries are eligible."}, indent=2))
        return 0

    promoted = []
    cache = root / "local/cache/promoted-segments"
    cache.mkdir(parents=True, exist_ok=True)
    for review in rows:
        parent_id = review["container_doc_id"]
        parent_meta = load(root / "metadata" / f"{parent_id}.json")
        parent_raw = Path(parent_meta["local_raw_path"])
        start, end = parse_pages(review["confirmed_pages"])
        out = cache / f"{parent_id}-{review['candidate_id']}-p{start}-{end}.pdf"
        method = extract_pages(parent_raw, start, end, out)
        if out.stat().st_size == 0 or out.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"invalid extracted PDF: {out}")
        child_id = intake_child(root, review, parent_meta, out)
        enrich_child(root, child_id, review, parent_meta, method)

        subprocess.run([sys.executable, str(root / "tools/generate-review-template.py"), child_id], env={**os.environ, "BLACKINDEX_ROOT": str(root)}, check=True)
        subprocess.run([sys.executable, "-W", "ignore::SyntaxWarning", str(root / "tools/evidence_map.py"), "--root", str(root), "integrity", child_id], check=True)
        subprocess.run([sys.executable, str(root / "tools/blackindex.py"), "--root", str(root), "verify"], check=True)
        if args.publish:
            subprocess.run([str(root / "tools/publish-ingest.sh"), child_id], check=True)
        promoted.append({"child_doc_id": child_id, "parent_doc_id": parent_id, "candidate_id": review["candidate_id"], "pages": review["confirmed_pages"]})

    print(json.dumps({"mode": "apply", "promoted": len(promoted), "records": promoted}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
