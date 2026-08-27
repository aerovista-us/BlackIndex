#!/usr/bin/env python3
"""Find candidate occurrences of named 9/11 source records in local normalized text.

This is a recovery aid, not an evidence-promoter. It never edits metadata,
record-integrity objects, extraction state, or source-vault files. Text-page
indices are provisional pdftotext/form-feed positions and MUST NOT be treated as
physical PDF page numbers.
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


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.I | re.S)


TARGETS = [
    {
        "target_id": "THUMAIRY-EC-2002-09-04",
        "label": "FBI EC Fahad Al-Thumairy — 2002-09-04",
        "patterns": [rx(r"fahad\s+al[- ]?thumairy|fahad\s+althumairy"), rx(r"(?:sep(?:t(?:ember)?)?\.?\s*4\s*,?\s*2002|09[/.-]0?4[/.-]2002)")],
    },
    {
        "target_id": "THUMAIRY-EC-2002-10-25",
        "label": "FBI EC Fahad Althumairy — 2002-10-25",
        "patterns": [rx(r"fahad\s+al[- ]?thumairy|fahad\s+althumairy"), rx(r"(?:oct(?:ober)?\.?\s*25\s*,?\s*2002|10[/.-]25[/.-]2002)")],
    },
    {
        "target_id": "THUMAIRY-EC-2002-11-20",
        "label": "FBI EC Fahad Al-Thumairy — 2002-11-20",
        "patterns": [rx(r"fahad\s+al[- ]?thumairy|fahad\s+althumairy"), rx(r"(?:nov(?:ember)?\.?\s*20\s*,?\s*2002|11[/.-]20[/.-]2002)")],
    },
    {
        "target_id": "ABDULLAH-ROI-2002-07-23",
        "label": "FBI ROI/interview Mohdar Abdullah — 2002-07-23",
        "patterns": [rx(r"mohdar\s+abdullah"), rx(r"(?:jul(?:y)?\.?\s*23\s*,?\s*2002|07[/.-]23[/.-]2002)")],
    },
    {
        "target_id": "ABDULLAH-EC-2004-05-19",
        "label": "FBI EC Abdullah investigation — 2004-05-19",
        "patterns": [rx(r"abdullah"), rx(r"(?:may\s*19\s*,?\s*2004|05[/.-]19[/.-]2004)")],
    },
    {
        "target_id": "ABDULLAH-TOMA-2004-05-18",
        "label": "FBI EC interview Charles Sabah Toma — 2004-05-18",
        "patterns": [rx(r"charles\s+sabah\s+toma"), rx(r"(?:may\s*18\s*,?\s*2004|05[/.-]18[/.-]2004)")],
    },
    {
        "target_id": "BAYOUMI-EC-1999-06-07",
        "label": "FBI EC Omar Ahmed Al Bayoumi — 1999-06-07",
        "patterns": [rx(r"omar\s+(?:ahmed\s+)?al[- ]?bayoumi|\bbayoumi\b"), rx(r"(?:jun(?:e)?\.?\s*7\s*,?\s*1999|06[/.-]0?7[/.-]1999)")],
    },
    {
        "target_id": "BAYOUMI-LHM-2002-04-15",
        "label": "FBI LHM investigation of Bayoumi — 2002-04-15",
        "patterns": [rx(r"\bbayoumi\b"), rx(r"(?:apr(?:il)?\.?\s*15\s*,?\s*2002|04[/.-]15[/.-]2002)")],
    },
    {
        "target_id": "BAYOUMI-HOTEL-2002-01-15",
        "label": "FBI recovery of Bayoumi hotel records — 2002-01-15",
        "patterns": [rx(r"\bbayoumi\b"), rx(r"hotel\s+records|recovery\s+of\s+hotel"), rx(r"(?:jan(?:uary)?\.?\s*15\s*,?\s*2002|01[/.-]15[/.-]2002)")],
    },
    {
        "target_id": "BAYOUMI-INTERVIEW-2003-09-17",
        "label": "FBI EC/interview of Bayoumi — 2003-09-17",
        "patterns": [rx(r"\bbayoumi\b"), rx(r"(?:sep(?:t(?:ember)?)?\.?\s*17\s*,?\s*2003|09[/.-]17[/.-]2003)")],
    },
    {
        "target_id": "BAYOUMI-INTERVIEW-2003-10-16-17",
        "label": "Omar al Bayoumi interview — 2003-10-16/17",
        "patterns": [rx(r"\bbayoumi\b"), rx(r"(?:oct(?:ober)?\.?\s*(?:16|17)\s*,?\s*2003|10[/.-](?:16|17)[/.-]2003)")],
    },
    {
        "target_id": "BIN-DON-DYSON-SOURCE-VERSIONS",
        "label": "Caysan Bin Don / Isamu Dyson interview source versions",
        "patterns": [rx(r"caysan\s+bin\s+don|isamu\s+dyson")],
    },
    {
        "target_id": "SAN-DIEGO-PENTTBOM-SAUDI-CONNECTIONS",
        "label": "FBI report Connections of San Diego PENTTBOM Subjects to the Government of Saudi Arabia",
        "patterns": [rx(r"connections\s+of\s+san\s+diego\s+pentt?bom\w*\s+subjects\s+to\s+the\s+government\s+of\s+saudi\s+arabia")],
    },
    {
        "target_id": "CIA-AL-QAIDA-TRAVEL-ISSUES-2003-11-14",
        "label": "CIA analytic report Al-Qa'ida Travel Issues — 2003-11-14",
        "patterns": [rx(r"al[- ]?qa['’]?ida\s+travel\s+issues|ctc\s*2004[- ]40002h"), rx(r"(?:nov(?:ember)?\.?\s*14\s*,?\s*2003|11[/.-]14[/.-]2003)")],
    },
    {
        "target_id": "BENOMRANE-INTERVIEWS-2002",
        "label": "Qualid Moncef Benomrane FBI interviews — 2002",
        "patterns": [rx(r"qualid\s+(?:moncef\s+)?benomrane|\bbenomrane\b")],
    },
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_metadata(root: Path) -> list[dict]:
    records: list[dict] = []
    for path in sorted((root / "metadata").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("doc_id") and data.get("schema_version"):
            records.append(data)
    return records


def preview(text: str, start: int, radius: int = 260) -> str:
    lo = max(0, start - radius)
    hi = min(len(text), start + radius)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


def match_target(page: str, target: dict) -> tuple[bool, list[str], int]:
    matched: list[str] = []
    starts: list[int] = []
    for pattern in target["patterns"]:
        m = pattern.search(page)
        if not m:
            return False, [], -1
        matched.append(m.group(0))
        starts.append(m.start())
    return True, matched, min(starts) if starts else 0


def scan_root(root: Path) -> dict:
    results: dict[str, list[dict]] = {target["target_id"]: [] for target in TARGETS}
    scanned_docs = 0
    scanned_text_pages = 0

    for meta in load_metadata(root):
        text_value = meta.get("normalized_text_path")
        if not text_value:
            continue
        text_path = Path(text_value)
        if not text_path.is_file():
            continue
        scanned_docs += 1
        text = text_path.read_text(encoding="utf-8", errors="replace")
        pages = text.split("\f")
        scanned_text_pages += len(pages)

        for page_index, page in enumerate(pages, start=1):
            if not page.strip():
                continue
            for target in TARGETS:
                ok, matched, start = match_target(page, target)
                if not ok:
                    continue
                results[target["target_id"]].append({
                    "doc_id": meta.get("doc_id"),
                    "source": meta.get("source"),
                    "container_sha256": meta.get("sha256"),
                    "text_page_index": page_index,
                    "physical_page_index": None,
                    "physical_page_verified": False,
                    "matched": matched,
                    "preview": preview(page, start),
                    "review_required": True,
                })

    targets = []
    for target in TARGETS:
        matches = results[target["target_id"]]
        targets.append({
            "target_id": target["target_id"],
            "label": target["label"],
            "candidate_count": len(matches),
            "candidates": matches,
        })

    return {
        "schema_version": 1,
        "object_type": "named_source_recovery_index",
        "generated_at": now(),
        "method": "local normalized-text signature search; candidate recovery only",
        "physical_page_claim": False,
        "scanned_documents": scanned_docs,
        "scanned_text_pages": scanned_text_pages,
        "target_count": len(TARGETS),
        "targets_with_candidates": sum(1 for item in targets if item["candidate_count"]),
        "targets": targets,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# BlackIndex 9/11 Named-Source Recovery Results",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Scanned normalized documents: **{report['scanned_documents']}**",
        f"- Scanned text-page chunks: **{report['scanned_text_pages']}**",
        f"- Recovery targets: **{report['target_count']}**",
        f"- Targets with candidate hits: **{report['targets_with_candidates']}**",
        "",
        "> Candidate hits are review leads only. `text_page_index` is a normalized-text/form-feed position and is **not** a verified physical PDF page number.",
        "",
    ]
    for target in report["targets"]:
        lines += [f"## {target['label']}", "", f"Candidate hits: **{target['candidate_count']}**", ""]
        if not target["candidates"]:
            lines += ["- No local normalized-text candidate found.", ""]
            continue
        for cand in target["candidates"]:
            lines += [
                f"- `{cand['doc_id']}` — text page `{cand['text_page_index']}` — physical page **unverified**",
                f"  - matched: `{'; '.join(cand['matched'])}`",
                f"  - preview: {cand['preview']}",
            ]
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Search local BlackIndex normalized text for named 9/11 source records")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--output", help="JSON output path; defaults to local/index/911-named-source-recovery.json")
    ap.add_argument("--markdown", help="Markdown output path; defaults to local/review/911-named-source-recovery.md")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    report = scan_root(root)
    json_path = Path(args.output) if args.output else root / "local/index/911-named-source-recovery.json"
    md_path = Path(args.markdown) if args.markdown else root / "local/review/911-named-source-recovery.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "json": str(json_path),
        "markdown": str(md_path),
        "scanned_documents": report["scanned_documents"],
        "targets": report["target_count"],
        "targets_with_candidates": report["targets_with_candidates"],
        "physical_page_claim": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
