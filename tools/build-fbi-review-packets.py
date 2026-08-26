#!/usr/bin/env python3
"""Build local review packets for triaged FBI segmentation candidates.

This tool does not promote evidence. It combines triage metadata with the
normalized parent-container text and writes review packets under local/review/.
Each packet preserves parent doc_id, page range, candidate id, entity hits,
identifier/date hints, and the extracted text for that page span.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pages_for(root: Path, doc_id: str) -> list[str]:
    meta = load_json(root / "metadata" / f"{doc_id}.json")
    text_path = meta.get("normalized_text_path")
    if not text_path:
        raise RuntimeError(f"normalized text unavailable: {doc_id}")
    return Path(text_path).read_text(encoding="utf-8", errors="replace").split("\f")


def candidate_rows(payload: dict) -> list[dict]:
    # triage JSON uses all_candidates / top_candidates; older keys kept as fallbacks.
    for key in ("all_candidates", "top_candidates", "ranked", "candidates", "queue", "items"):
        rows = payload.get(key)
        if isinstance(rows, list):
            return rows
    raise RuntimeError("triage JSON has no candidate list")


def val(row: dict, *keys, default=None):
    for key in keys:
        if key in row:
            return row[key]
    return default


def main() -> int:
    ap = argparse.ArgumentParser(description="Build review-only packets from FBI triage output")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--triage", default="local/index/triage/911-fbi-segmentation-priority.json")
    ap.add_argument("--band", default="P0")
    ap.add_argument("--limit", type=int, default=0, help="Max packets to write. 0 means all rows in the band.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    triage_path = Path(args.triage)
    if not triage_path.is_absolute():
        triage_path = root / triage_path
    payload = load_json(triage_path)
    rows = candidate_rows(payload)

    selected = []
    for row in rows:
        band = val(row, "review_priority_band", "priority_band", "priority", "band")
        if band == args.band:
            selected.append(row)
        if args.limit and len(selected) >= args.limit:
            break

    out_dir = root / "local/review/911-fbi-p0"
    out_dir.mkdir(parents=True, exist_ok=True)
    page_cache: dict[str, list[str]] = {}
    manifest = []

    for rank, row in enumerate(selected, start=1):
        doc_id = val(row, "container_doc_id", "container", "doc_id")
        cand_id = val(row, "candidate_id", "candidate")
        start = int(val(row, "start_page", "page_start", default=0) or 0)
        end = int(val(row, "end_page", "page_end", default=start) or start)
        if not doc_id or not cand_id or start < 1 or end < start:
            continue
        if doc_id not in page_cache:
            page_cache[doc_id] = pages_for(root, doc_id)
        pages = page_cache[doc_id]
        text = "\n\f\n".join(pages[start-1:end])
        entities = val(row, "entity_hits", "entities", default=[]) or []
        serials = val(row, "serial_or_case_hits", "serials", "serial_case", default=[]) or []
        dates = val(row, "date_hits", "dates", default=[]) or []
        record_type = val(row, "record_type_guess", "record_type", "type", default="unknown")
        score = val(row, "review_priority_score", "review_score", "score", default="")

        safe = f"{rank:02d}-{doc_id}-{cand_id}.md"
        path = out_dir / safe
        body = f"""# FBI candidate review packet — {cand_id}

- **Review rank:** {rank}
- **Priority band:** {args.band}
- **Review score:** {score}
- **Parent container:** `{doc_id}`
- **Candidate:** `{cand_id}`
- **Container pages:** {start}–{end}
- **Record type guess:** `{record_type}`
- **Entity hits:** {', '.join(entities) if entities else 'None'}
- **Serial/case hints:** {', '.join(serials) if serials else 'None'}
- **Date hints:** {', '.join(dates) if dates else 'None'}

> REVIEW-ONLY. The page range is heuristic until checked against the source PDF.
> Do not cite or promote this packet as an independent record.

## Boundary review

- [ ] Confirm true first page of record
- [ ] Confirm true last page of record
- [ ] Confirm record type
- [ ] Confirm date
- [ ] Confirm FBI file/serial/case identifiers
- [ ] Record redaction markings
- [ ] Identify referenced attachments/serials/interviews
- [ ] Check whether this record is reused in the 2016 EC or 2021 closing EC

## Extracted parent-container text

```text
{text}
```
"""
        path.write_text(body, encoding="utf-8")
        manifest.append({
            "rank": rank,
            "priority_band": args.band,
            "container_doc_id": doc_id,
            "candidate_id": cand_id,
            "start_page": start,
            "end_page": end,
            "record_type_guess": record_type,
            "entities": entities,
            "packet": str(path),
        })

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"count": len(manifest), "packets": manifest}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"band": args.band, "packets": len(manifest), "output": str(out_dir), "manifest": str(manifest_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
