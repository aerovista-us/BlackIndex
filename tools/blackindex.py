#!/usr/bin/env python3
"""BlackIndex local intake CLI.

Standard-library-only foundation for NXCore. Raw source documents are stored locally;
Git tracks the system definition and research outputs, not the source corpus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path("/srv/NXDrive/BlackIndex")
BUFFER_SIZE = 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "document"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(BUFFER_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_layout(root: Path) -> None:
    for relative in (
        "source-vault/raw",
        "normalized/text",
        "local/index",
        "local/cache",
        "local/logs",
        "metadata",
        "extractions",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)


def metadata_files(root: Path):
    yield from (root / "metadata").glob("*.json")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def find_duplicate(root: Path, checksum: str) -> dict | None:
    for path in metadata_files(root):
        data = load_json(path)
        if data.get("sha256") == checksum:
            return data
    return None


def next_sequence(root: Path, source: str, year: str, collection: str) -> int:
    prefix = f"{source.upper()}-{year}-{slugify(collection)}-"
    highest = 0
    for path in metadata_files(root):
        doc_id = path.stem
        if doc_id.startswith(prefix):
            try:
                highest = max(highest, int(doc_id.rsplit("-", 1)[1]))
            except ValueError:
                pass
    return highest + 1


def make_doc_id(root: Path, source: str, year: str, collection: str) -> str:
    seq = next_sequence(root, source, year, collection)
    return f"{source.upper()}-{year}-{slugify(collection)}-{seq:03d}"


def safe_copy_immutable(source: Path, destination: Path) -> None:
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing raw file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    destination.chmod(0o444)


def write_extraction_stub(root: Path, metadata: dict) -> Path:
    path = root / "extractions" / f"{metadata['doc_id']}.md"
    if path.exists():
        return path
    body = f"""# {metadata['title']}\n\n- **Doc ID:** `{metadata['doc_id']}`\n- **Call ID:** `{metadata.get('call_id') or 'UNASSIGNED'}`\n- **Source:** {metadata['source']}\n- **Document date:** {metadata.get('document_date') or 'Unknown'}\n- **SHA-256:** `{metadata['sha256']}`\n- **Provenance:** {metadata.get('source_url') or 'Local intake; source URL not recorded'}\n\n## Evidence established by the document\n\n- TODO\n\n## Corroboration\n\n- TODO\n\n## Inferences\n\n- TODO\n\n## Mechanisms / patterns\n\n- TODO\n\n## Failure modes\n\n- TODO\n\n## Operational analogs\n\n- TODO\n\n## Candidate controls\n\n- TODO\n\n## Candidate detections\n\n- TODO\n\n## Watch-outs / alternative explanations\n\n- TODO\n\n## Confidence / gaps\n\n- TODO\n"""
    path.write_text(body, encoding="utf-8")
    return path


def append_log(root: Path, event: dict) -> None:
    log = root / "local/logs/intake.jsonl"
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_layout(root)
    print(f"BlackIndex initialized: {root}")
    return 0


def cmd_intake(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_layout(root)
    source_path = Path(args.file).expanduser().resolve()
    if not source_path.is_file():
        print(f"error: not a file: {source_path}", file=sys.stderr)
        return 2

    checksum = sha256_file(source_path)
    duplicate = find_duplicate(root, checksum)
    if duplicate:
        print(json.dumps({"status": "duplicate", "doc_id": duplicate.get("doc_id"), "sha256": checksum}, indent=2))
        return 3

    year = str(args.year or "undated")
    doc_id = make_doc_id(root, args.source, year, args.collection)
    ext = source_path.suffix.lower()
    raw_dir = root / "source-vault/raw" / args.source.lower() / slugify(args.collection)
    raw_path = raw_dir / f"{doc_id}{ext}"
    safe_copy_immutable(source_path, raw_path)

    metadata = {
        "schema_version": 1,
        "doc_id": doc_id,
        "call_id": args.call_id,
        "title": args.title or source_path.stem,
        "source": args.source.upper(),
        "collection": args.collection,
        "document_date": args.document_date,
        "year_bucket": year,
        "source_url": args.url,
        "retrieved_at": utc_now(),
        "original_filename": source_path.name,
        "local_raw_path": str(raw_path),
        "mime_hint": ext.lstrip("."),
        "size_bytes": raw_path.stat().st_size,
        "sha256": checksum,
        "tags": [tag.strip() for tag in (args.tags or "").split(",") if tag.strip()],
        "classification_note": args.classification_note,
        "redaction_note": args.redaction_note,
        "evidence_status": "unreviewed",
    }

    metadata_path = root / "metadata" / f"{doc_id}.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    extraction_path = write_extraction_stub(root, metadata)
    append_log(root, {"event": "intake", "at": utc_now(), "doc_id": doc_id, "sha256": checksum})

    print(json.dumps({
        "status": "ingested",
        "doc_id": doc_id,
        "sha256": checksum,
        "raw": str(raw_path),
        "metadata": str(metadata_path),
        "extraction": str(extraction_path),
    }, indent=2))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    root = Path(args.root)
    failures = []
    checked = 0
    for path in metadata_files(root):
        data = load_json(path)
        raw = Path(data.get("local_raw_path", ""))
        if not raw.is_file():
            failures.append({"doc_id": data.get("doc_id"), "error": "raw_missing", "path": str(raw)})
            continue
        checked += 1
        actual = sha256_file(raw)
        if actual != data.get("sha256"):
            failures.append({"doc_id": data.get("doc_id"), "error": "hash_mismatch", "expected": data.get("sha256"), "actual": actual})
    print(json.dumps({"checked": checked, "failures": failures, "ok": not failures}, indent=2))
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="blackindex", description="BlackIndex local intake utility")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help=f"vault root (default: {DEFAULT_ROOT})")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create the local vault layout")
    init.set_defaults(func=cmd_init)

    intake = sub.add_parser("intake", help="ingest one source document")
    intake.add_argument("file")
    intake.add_argument("--source", required=True, help="CIA, FBI, NSA, NARA, SENATE, NSARCHIVE, etc.")
    intake.add_argument("--collection", required=True)
    intake.add_argument("--year", help="year bucket used in Doc ID; use document year where known")
    intake.add_argument("--title")
    intake.add_argument("--document-date")
    intake.add_argument("--url")
    intake.add_argument("--call-id")
    intake.add_argument("--tags", help="comma-separated")
    intake.add_argument("--classification-note")
    intake.add_argument("--redaction-note")
    intake.set_defaults(func=cmd_intake)

    verify = sub.add_parser("verify", help="rehash local raw files and compare to metadata")
    verify.set_defaults(func=cmd_verify)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
