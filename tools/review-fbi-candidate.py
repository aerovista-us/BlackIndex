#!/usr/bin/env python3
"""Record a human-reviewed disposition for a local FBI segmentation candidate.

This tool writes only to local/review. It does not promote evidence, modify
metadata, or publish anything. Its purpose is to create a machine-readable audit
trail between heuristic segmentation and any later durable promotion step.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
ALLOWED = {"PROMOTE", "HOLD", "MERGE", "REJECT-BOUNDARY"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Record local review disposition for an FBI segmentation candidate")
    ap.add_argument("container_doc_id")
    ap.add_argument("candidate_id")
    ap.add_argument("disposition", choices=sorted(ALLOWED))
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--confirmed-pages", default="", help="Confirmed inclusive page range, e.g. 154-156")
    ap.add_argument("--record-type", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--serial", default="")
    ap.add_argument("--redactions", default="")
    ap.add_argument("--source-dependency", default="")
    ap.add_argument("--duplicate-of", default="")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    seg_path = root / "local/index/segmentation" / f"{args.container_doc_id}.json"
    if not seg_path.exists():
        raise SystemExit(f"segmentation index not found: {seg_path}")
    seg = load(seg_path, {})
    candidate = next((c for c in seg.get("candidates", []) if c.get("candidate_id") == args.candidate_id), None)
    if not candidate:
        raise SystemExit(f"candidate not found: {args.container_doc_id} / {args.candidate_id}")

    if args.disposition == "PROMOTE" and not args.confirmed_pages:
        raise SystemExit("PROMOTE requires --confirmed-pages after source-PDF boundary review")

    ledger_path = root / "local/review/911-fbi-p0/review-ledger.json"
    ledger = load(ledger_path, {"schema_version": 1, "reviews": []})
    reviews = ledger.setdefault("reviews", [])
    key = (args.container_doc_id, args.candidate_id)
    reviews[:] = [r for r in reviews if (r.get("container_doc_id"), r.get("candidate_id")) != key]
    review = {
        "reviewed_at": now(),
        "container_doc_id": args.container_doc_id,
        "candidate_id": args.candidate_id,
        "heuristic_start_page": candidate.get("start_page"),
        "heuristic_end_page": candidate.get("end_page"),
        "disposition": args.disposition,
        "confirmed_pages": args.confirmed_pages or None,
        "record_type": args.record_type or None,
        "record_date": args.date or None,
        "serial_or_case_id": args.serial or None,
        "redactions": args.redactions or None,
        "source_dependency": args.source_dependency or None,
        "duplicate_of": args.duplicate_of or None,
        "note": args.note or None,
        "promotion_ready": args.disposition == "PROMOTE",
    }
    reviews.append(review)
    reviews.sort(key=lambda r: (r.get("container_doc_id", ""), r.get("candidate_id", "")))
    ledger["updated_at"] = now()
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ledger": str(ledger_path), "review": review}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
