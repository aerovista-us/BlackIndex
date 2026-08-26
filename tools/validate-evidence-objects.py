#!/usr/bin/env python3
"""Validate BlackIndex durable evidence-map objects.

Uses jsonschema when installed; otherwise performs a dependency-free structural
validation covering the same required identity and cross-reference invariants.
The fallback is deliberate so validation can run on a minimal NXCore install.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
DIR_TYPES = {
    "record_integrity": "record_integrity",
    "missing_evidence": "missing_evidence",
    "version_families": "version_family",
    "version_comparisons": "version_comparison",
    "source_dependencies": "source_dependency",
    "statement_comparisons": "statement_comparison",
    "investigator_reviews": "investigator_review",
}
REQUIRED = {
    "record_integrity": {"doc_id", "completeness", "redaction_concern", "known_destruction", "missing_referenced_records", "archive_confidence"},
    "missing_evidence": {"doc_id", "category", "summary", "status"},
    "version_family": {"title", "doc_ids"},
    "version_comparison": {"left_doc_id", "right_doc_id", "similarity_ratio", "diff_line_count"},
    "source_dependency": {"assertion_id", "source_id", "depends_on", "dependency_type", "independence"},
    "statement_comparison": {"topic", "public_source", "public_statement", "internal_source", "internal_content", "relationship"},
    "investigator_review": {"report_or_finding", "investigator", "exact_wording", "scope", "conclusion_adopted_as_fact"},
}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def metadata_ids(root: Path) -> set[str]:
    out = set()
    for p in (root / "metadata").glob("*.json"):
        try:
            d = read(p)
        except Exception:
            continue
        if d.get("doc_id"):
            out.add(d["doc_id"])
    return out


def structural(path: Path, data: dict, docs: set[str]) -> list[str]:
    errs = []
    if data.get("schema_version") != 1:
        errs.append("schema_version must be 1")
    if not data.get("object_id"):
        errs.append("object_id is required")
    expected = DIR_TYPES.get(path.parent.name)
    if expected and data.get("object_type") != expected:
        errs.append(f"object_type {data.get('object_type')!r} does not match directory type {expected!r}")
    typ = data.get("object_type")
    missing = sorted(k for k in REQUIRED.get(typ, set()) if k not in data)
    if missing:
        errs.append("missing required fields: " + ", ".join(missing))
    if typ in {"record_integrity", "missing_evidence"} and data.get("doc_id") not in docs:
        errs.append(f"unknown doc_id: {data.get('doc_id')!r}")
    if typ == "version_family":
        unknown = [x for x in data.get("doc_ids", []) if x not in docs]
        if unknown:
            errs.append("unknown version-family doc_ids: " + ", ".join(unknown))
    if typ == "version_comparison":
        for k in ("left_doc_id", "right_doc_id"):
            if data.get(k) not in docs:
                errs.append(f"unknown {k}: {data.get(k)!r}")
    if typ == "investigator_review" and data.get("conclusion_adopted_as_fact") is not False:
        errs.append("investigator_review.conclusion_adopted_as_fact must remain false")
    if typ == "source_dependency" and data.get("independence") not in {"independent", "partially-independent", "dependent", "unknown"}:
        errs.append("invalid independence value")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    schema = read(root / "objects/schema-v1.json")
    docs = metadata_ids(root)
    validator = None
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
    except ImportError:
        pass

    checked = 0
    failures = []
    notices = []
    for directory, expected in DIR_TYPES.items():
        for path in sorted((root / "objects" / directory).glob("*.json")):
            checked += 1
            try:
                data = read(path)
            except Exception as exc:
                failures.append({"path": str(path.relative_to(root)), "errors": [f"invalid JSON: {exc}"]})
                continue
            errs = structural(path, data, docs)
            if validator:
                errs.extend(sorted({e.message for e in validator.iter_errors(data)}))
            if errs:
                failures.append({"path": str(path.relative_to(root)), "errors": sorted(set(errs))})
    if validator is None:
        notices.append("jsonschema package not installed; used structural validation fallback")
    result = {"checked": checked, "failures": failures, "notices": notices, "ok": not failures}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
