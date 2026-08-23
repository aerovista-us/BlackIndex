#!/usr/bin/env python3
"""BlackIndex local intake CLI.

Raw source documents and normalized full text stay on NXCore. Git tracks the
system definition plus durable research records: metadata, reviewed extractions,
patterns, controls, detections, training, playbooks, and code.
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
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
BUFFER_SIZE = 1024 * 1024
TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm"}
DOC_METADATA_RE = re.compile(r"^[A-Z0-9_-]+-(?:[0-9]{4}|undated)-[a-z0-9-]+-[0-9]{3,}\.json$")


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
    """Yield only ingested document metadata, never schemas/support JSON."""
    metadata_dir = root / "metadata"
    if not metadata_dir.exists():
        return
    for path in metadata_dir.glob("*.json"):
        if DOC_METADATA_RE.match(path.name):
            yield path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def metadata_path_for(root: Path, doc_id: str) -> Path:
    return root / "metadata" / f"{doc_id}.json"


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


def normalize_text(raw_path: Path, root: Path, doc_id: str) -> tuple[Path | None, str]:
    """Create a plain-text derivative when the format is supported.

    PDFs use system `pdftotext` if installed. OCR is intentionally not automatic;
    image-only PDFs are marked for later review rather than silently transformed.
    """
    out = root / "normalized/text" / f"{doc_id}.txt"
    suffix = raw_path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        try:
            text = raw_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = raw_path.read_text(encoding="utf-8", errors="replace")
        out.write_text(text, encoding="utf-8")
        return out, "native-text"

    if suffix == ".pdf":
        executable = shutil.which("pdftotext")
        if not executable:
            return None, "pdftotext-unavailable"
        result = subprocess.run(
            [executable, "-layout", str(raw_path), str(out)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            if out.exists():
                out.unlink()
            return None, f"pdftotext-error:{result.returncode}"
        if not out.exists() or not out.read_text(encoding="utf-8", errors="ignore").strip():
            if out.exists():
                out.unlink()
            return None, "pdf-no-text-layer"
        return out, "pdftotext"

    return None, "unsupported-format"


def write_extraction_stub(root: Path, metadata: dict) -> Path:
    path = root / "extractions" / f"{metadata['doc_id']}.md"
    if path.exists():
        return path
    provenance = metadata.get("artifact_url") or metadata.get("source_url") or "Local intake; source URL not recorded"
    body = f"""# {metadata['title']}\n\n- **Doc ID:** `{metadata['doc_id']}`\n- **Call ID:** `{metadata.get('call_id') or 'UNASSIGNED'}`\n- **Native ID:** {metadata.get('native_id') or 'Not recorded'}\n- **Source:** {metadata['source']}\n- **Document date:** {metadata.get('document_date') or 'Unknown'}\n- **SHA-256:** `{metadata['sha256']}`\n- **Landing page:** {metadata.get('canonical_landing_url') or 'Not recorded'}\n- **Artifact:** {provenance}\n- **Normalized text:** {metadata.get('normalized_text_path') or 'Unavailable'}\n\n## Evidence established by the document\n\n- TODO\n\n## Corroboration\n\n- TODO\n\n## Inferences\n\n- TODO\n\n## Mechanisms / patterns\n\n- TODO\n\n## Failure modes\n\n- TODO\n\n## Operational analogs\n\n- TODO\n\n## Candidate controls\n\n- TODO\n\n## Candidate detections\n\n- TODO\n\n## Watch-outs / alternative explanations\n\n- TODO\n\n## Confidence / gaps\n\n- TODO\n"""
    path.write_text(body, encoding="utf-8")
    return path


def append_log(root: Path, event: dict) -> None:
    log = root / "local/logs/intake.jsonl"
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def build_manifest(root: Path) -> Path:
    records = []
    for path in sorted(metadata_files(root)):
        data = load_json(path)
        if data:
            records.append(data)
    manifest = root / "local/index/manifest.json"
    write_json(manifest, {"generated_at": utc_now(), "count": len(records), "documents": records})
    return manifest


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_layout(root)
    build_manifest(root)
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

    normalized_path, normalization_status = normalize_text(raw_path, root, doc_id)
    artifact_url = args.artifact_url or args.url
    metadata = {
        "schema_version": 1,
        "doc_id": doc_id,
        "call_id": args.call_id,
        "native_id": args.native_id,
        "record_group": args.record_group,
        "series": args.series,
        "title": args.title or source_path.stem,
        "source": args.source.upper(),
        "collection": args.collection,
        "document_date": args.document_date,
        "year_bucket": year,
        "source_url": artifact_url,
        "canonical_landing_url": args.landing_url,
        "artifact_url": artifact_url,
        "retrieved_at": utc_now(),
        "original_filename": source_path.name,
        "local_raw_path": str(raw_path),
        "normalized_text_path": str(normalized_path) if normalized_path else None,
        "normalization_status": normalization_status,
        "normalized_sha256": sha256_file(normalized_path) if normalized_path else None,
        "mime_hint": ext.lstrip("."),
        "size_bytes": raw_path.stat().st_size,
        "sha256": checksum,
        "tags": [tag.strip() for tag in (args.tags or "").split(",") if tag.strip()],
        "classification_note": args.classification_note,
        "redaction_note": args.redaction_note,
        "evidence_status": "unreviewed",
    }

    metadata_path = metadata_path_for(root, doc_id)
    write_json(metadata_path, metadata)
    extraction_path = write_extraction_stub(root, metadata)
    manifest_path = build_manifest(root)
    append_log(root, {
        "event": "intake",
        "at": utc_now(),
        "doc_id": doc_id,
        "sha256": checksum,
        "normalization_status": normalization_status,
    })

    print(json.dumps({
        "status": "ingested",
        "doc_id": doc_id,
        "sha256": checksum,
        "raw": str(raw_path),
        "normalized": str(normalized_path) if normalized_path else None,
        "normalization_status": normalization_status,
        "metadata": str(metadata_path),
        "extraction": str(extraction_path),
        "manifest": str(manifest_path),
    }, indent=2))
    return 0


def cmd_normalize(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_layout(root)
    metadata_path = metadata_path_for(root, args.doc_id)
    if not metadata_path.is_file():
        print(f"error: metadata not found: {metadata_path}", file=sys.stderr)
        return 2
    data = load_json(metadata_path)
    raw_value = data.get("local_raw_path")
    if not raw_value or not Path(raw_value).is_file():
        print(f"error: raw source missing for {args.doc_id}", file=sys.stderr)
        return 2
    normalized_path, status = normalize_text(Path(raw_value), root, args.doc_id)
    data["normalized_text_path"] = str(normalized_path) if normalized_path else None
    data["normalization_status"] = status
    data["normalized_sha256"] = sha256_file(normalized_path) if normalized_path else None
    data["normalized_at"] = utc_now()
    write_json(metadata_path, data)
    manifest = build_manifest(root)
    append_log(root, {"event": "normalize", "at": utc_now(), "doc_id": args.doc_id, "status": status})
    print(json.dumps({
        "doc_id": args.doc_id,
        "normalization_status": status,
        "normalized": str(normalized_path) if normalized_path else None,
        "normalized_sha256": data.get("normalized_sha256"),
        "manifest": str(manifest),
    }, indent=2))
    return 0 if normalized_path else 1


def cmd_verify(args: argparse.Namespace) -> int:
    root = Path(args.root)
    failures = []
    checked = 0
    for path in metadata_files(root):
        data = load_json(path)
        raw_value = data.get("local_raw_path")
        if not raw_value:
            failures.append({"doc_id": data.get("doc_id"), "error": "metadata_missing_raw_path", "metadata": str(path)})
            continue
        raw = Path(raw_value)
        if not raw.is_file():
            failures.append({"doc_id": data.get("doc_id"), "error": "raw_missing", "path": str(raw)})
            continue
        checked += 1
        actual = sha256_file(raw)
        if actual != data.get("sha256"):
            failures.append({"doc_id": data.get("doc_id"), "error": "hash_mismatch", "expected": data.get("sha256"), "actual": actual})
        normalized_value = data.get("normalized_text_path")
        normalized_hash = data.get("normalized_sha256")
        if normalized_value and normalized_hash:
            normalized = Path(normalized_value)
            if not normalized.is_file():
                failures.append({"doc_id": data.get("doc_id"), "error": "normalized_missing", "path": str(normalized)})
            else:
                actual_normalized = sha256_file(normalized)
                if actual_normalized != normalized_hash:
                    failures.append({"doc_id": data.get("doc_id"), "error": "normalized_hash_mismatch", "expected": normalized_hash, "actual": actual_normalized})
    print(json.dumps({"checked": checked, "failures": failures, "ok": not failures}, indent=2))
    return 1 if failures else 0


def cmd_manifest(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_layout(root)
    path = build_manifest(root)
    print(path)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    root = Path(args.root)
    query = args.query.lower()
    results = []
    for path in sorted(metadata_files(root)):
        data = load_json(path)
        haystack = " ".join([
            str(data.get("doc_id", "")), str(data.get("native_id", "")),
            str(data.get("title", "")), str(data.get("collection", "")),
            str(data.get("source", "")), " ".join(data.get("tags", [])),
        ]).lower()
        text_path = data.get("normalized_text_path")
        snippet = None
        matched = query in haystack
        if text_path and Path(text_path).is_file():
            text = Path(text_path).read_text(encoding="utf-8", errors="ignore")
            lower = text.lower()
            index = lower.find(query)
            if index >= 0:
                matched = True
                start = max(0, index - 120)
                end = min(len(text), index + len(args.query) + 220)
                snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        if matched:
            results.append({
                "doc_id": data.get("doc_id"),
                "native_id": data.get("native_id"),
                "title": data.get("title"),
                "call_id": data.get("call_id"),
                "source": data.get("source"),
                "snippet": snippet,
            })
    print(json.dumps({"query": args.query, "count": len(results), "results": results[: args.limit]}, indent=2))
    return 0


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def cmd_publish(args: argparse.Namespace) -> int:
    """Commit durable research records for one document; optionally push them."""
    root = Path(args.root).resolve()
    if not (root / ".git").exists():
        print(f"error: not a Git checkout: {root}", file=sys.stderr)
        return 2

    metadata = root / "metadata" / f"{args.doc_id}.json"
    extraction = root / "extractions" / f"{args.doc_id}.md"
    missing = [str(p.relative_to(root)) for p in (metadata, extraction) if not p.is_file()]
    if missing:
        print(f"error: missing publish record(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    rel_paths = [str(metadata.relative_to(root)), str(extraction.relative_to(root))]
    add = run_git(root, "add", "--", *rel_paths)
    if add.returncode != 0:
        print(add.stderr, file=sys.stderr)
        return add.returncode

    diff = run_git(root, "diff", "--cached", "--quiet", "--", *rel_paths)
    if diff.returncode == 0:
        print(json.dumps({"status": "no-changes", "doc_id": args.doc_id, "paths": rel_paths}, indent=2))
        return 0

    message = args.message or f"Publish BlackIndex record {args.doc_id}"
    commit = run_git(root, "commit", "-m", message, "--", *rel_paths)
    if commit.returncode != 0:
        print(commit.stdout, file=sys.stderr)
        print(commit.stderr, file=sys.stderr)
        return commit.returncode

    result = {"status": "committed", "doc_id": args.doc_id, "paths": rel_paths}
    if args.push:
        push = run_git(root, "push")
        if push.returncode != 0:
            print(push.stdout, file=sys.stderr)
            print(push.stderr, file=sys.stderr)
            return push.returncode
        result["status"] = "pushed"
    print(json.dumps(result, indent=2))
    return 0


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
    intake.add_argument("--url", help="legacy alias for --artifact-url")
    intake.add_argument("--landing-url", help="canonical collection/report landing page")
    intake.add_argument("--artifact-url", help="direct URL for the exact ingested artifact")
    intake.add_argument("--native-id", help="archive/report/document identifier from the source system")
    intake.add_argument("--record-group")
    intake.add_argument("--series")
    intake.add_argument("--call-id")
    intake.add_argument("--tags", help="comma-separated")
    intake.add_argument("--classification-note")
    intake.add_argument("--redaction-note")
    intake.set_defaults(func=cmd_intake)

    normalize = sub.add_parser("normalize", help="normalize an already-ingested document and update metadata")
    normalize.add_argument("doc_id")
    normalize.set_defaults(func=cmd_normalize)

    verify = sub.add_parser("verify", help="rehash local raw/normalized files and compare to metadata")
    verify.set_defaults(func=cmd_verify)

    manifest = sub.add_parser("manifest", help="rebuild local document manifest")
    manifest.set_defaults(func=cmd_manifest)

    search = sub.add_parser("search", help="search metadata and normalized text")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_search)

    publish = sub.add_parser("publish", help="commit one document's metadata + extraction; optionally push")
    publish.add_argument("doc_id")
    publish.add_argument("--message")
    publish.add_argument("--push", action="store_true", help="push the commit after creating it")
    publish.set_defaults(func=cmd_publish)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
