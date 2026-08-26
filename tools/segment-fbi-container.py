#!/usr/bin/env python3
"""Generate review-only segmentation candidates for FBI container PDFs.

This tool never promotes evidence automatically. It reads the normalized text for
an ingested BlackIndex document, looks for likely FBI record boundaries and
high-value entity names, and writes a local candidate index under local/index/.

The output is intentionally provisional: every candidate must be reviewed against
the source PDF before it is split or promoted into an individual BlackIndex
record.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))

BOUNDARY_PATTERNS = [
    ("electronic_communication", re.compile(r"\bELECTRONIC COMMUNICATION\b", re.I)),
    ("fd_302", re.compile(r"\bFD[- ]?302\b|\bFEDERAL BUREAU OF INVESTIGATION\b.*\bDate of transcription\b", re.I | re.S)),
    ("fd_1057", re.compile(r"\bFD[- ]?1057\b", re.I)),
    ("fbi_information_report", re.compile(r"\bINFORMATION REPORT\b", re.I)),
    ("memorandum", re.compile(r"\bMEMORANDUM\b", re.I)),
]

ENTITY_PATTERNS = {
    "Omar al-Bayoumi": re.compile(r"\b(?:Omar\s+)?al[- ]?Bayoumi\b|\bBayoumi\b", re.I),
    "Fahad al-Thumairy": re.compile(r"\b(?:Fahad\s+)?al[- ]?Thumairy\b|\bThumairy\b", re.I),
    "Musaed al-Jarrah": re.compile(r"\b(?:Musaed\s+)?al[- ]?Jarrah\b|\bal[- ]?Jarrah\b", re.I),
    "Nawaf al-Hazmi": re.compile(r"\b(?:Nawaf\s+)?al[- ]?Hazmi\b|\bHazmi\b", re.I),
    "Khalid al-Mihdhar": re.compile(r"\b(?:Khalid\s+)?al[- ]?Mihdhar\b|\bMihdhar\b", re.I),
}

# Require an identifier to contain at least one digit. FBI case/file/serial values
# are alphanumeric/punctuation-heavy; plain words such as "and", "agent", "was",
# or "Western" are OCR/parser noise and must not be promoted as identifiers.
SERIAL_PATTERNS = [
    re.compile(r"\b(?:File|Case)\s*(?:No\.?|Number|ID)?\s*[:#]?\s*([A-Z0-9][A-Z0-9./_-]{2,})", re.I),
    re.compile(r"\bSerial\s*(?:No\.?|Number)?\s*[:#]?\s*([A-Z0-9][A-Z0-9./_-]{1,})", re.I),
]

DATE_PATTERNS = [
    re.compile(r"\b(0?[1-9]|1[0-2])[/.-](0?[1-9]|[12]\d|3[01])[/.-]((?:19|20)\d{2})\b"),
    re.compile(r"\b((?:19|20)\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def page_chunks(text: str) -> list[str]:
    pages = text.split("\f")
    if len(pages) == 1:
        return [text]
    return pages


def guess_boundary(page: str) -> tuple[str | None, int]:
    for kind, rx in BOUNDARY_PATTERNS:
        if rx.search(page[:5000]):
            return kind, 3
    score = 0
    upper = page[:3000].upper()
    if "FEDERAL BUREAU OF INVESTIGATION" in upper:
        score += 1
    if "DATE:" in upper or "DATE OF TRANSCRIPTION" in upper:
        score += 1
    if "SUBJECT:" in upper or "TITLE:" in upper:
        score += 1
    return ("possible_fbi_record" if score >= 2 else None, score)


def entity_hits(text: str) -> list[str]:
    return [name for name, rx in ENTITY_PATTERNS.items() if rx.search(text)]


def plausible_identifier(value: str) -> bool:
    value = value.strip(" .,:;()[]{}")
    if not value or not any(ch.isdigit() for ch in value):
        return False
    if len(value) < 3 or len(value) > 80:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9./_-]+", value))


def serial_hits(text: str) -> list[str]:
    hits: list[str] = []
    for rx in SERIAL_PATTERNS:
        for m in rx.finditer(text[:8000]):
            value = m.group(1).strip(" .,:;()[]{}")
            if plausible_identifier(value) and value not in hits:
                hits.append(value)
    return hits[:10]


def date_hits(text: str) -> list[str]:
    out: list[str] = []
    for rx in DATE_PATTERNS:
        for m in rx.finditer(text[:5000]):
            value = m.group(0)
            if value not in out:
                out.append(value)
    return out[:10]


def make_preview(text: str, limit: int = 650) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean[:limit]


def build_candidates(pages: list[str]) -> list[dict]:
    starts: list[tuple[int, str, int]] = []
    for idx, page in enumerate(pages, start=1):
        kind, confidence = guess_boundary(page)
        if kind:
            starts.append((idx, kind, confidence))

    if not starts:
        return []

    candidates: list[dict] = []
    for n, (start, kind, confidence) in enumerate(starts):
        end = starts[n + 1][0] - 1 if n + 1 < len(starts) else len(pages)
        block = "\n".join(pages[start - 1 : end])
        candidates.append({
            "candidate_id": f"CAND-{n+1:04d}",
            "start_page": start,
            "end_page": end,
            "record_type_guess": kind,
            "boundary_confidence": confidence,
            "entity_hits": entity_hits(block),
            "serial_or_case_hits": serial_hits(block),
            "date_hits": date_hits(block),
            "preview": make_preview(block),
            "review_required": True,
            "promoted": False,
        })
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate review-only FBI container segmentation candidates")
    ap.add_argument("doc_id")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--only-key-entities", action="store_true", help="retain only candidates mentioning a priority 9/11 entity")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    meta_path = root / "metadata" / f"{args.doc_id}.json"
    if not meta_path.is_file():
        raise SystemExit(f"metadata not found: {meta_path}")
    meta = load_json(meta_path)
    text_path = meta.get("normalized_text_path")
    if not text_path or not Path(text_path).is_file():
        raise SystemExit(f"normalized text unavailable for {args.doc_id}")

    text = Path(text_path).read_text(encoding="utf-8", errors="replace")
    pages = page_chunks(text)
    candidates = build_candidates(pages)
    if args.only_key_entities:
        candidates = [c for c in candidates if c["entity_hits"]]

    payload = {
        "schema_version": 1,
        "object_type": "segmentation_candidate_index",
        "generated_at": now(),
        "container_doc_id": args.doc_id,
        "container_sha256": meta.get("sha256"),
        "source": meta.get("source"),
        "collection": meta.get("collection"),
        "page_count_text_layer": len(pages),
        "candidate_count": len(candidates),
        "method": "heuristic-boundary-detection; review required",
        "automatic_evidence_status": "none",
        "candidates": candidates,
    }

    out = root / "local/index/segmentation" / f"{args.doc_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "pages": len(pages), "candidates": len(candidates)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
