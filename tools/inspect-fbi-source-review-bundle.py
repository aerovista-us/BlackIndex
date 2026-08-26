#!/usr/bin/env python3
"""Inspect review-only FBI source slices for likely record boundaries.

This tool is advisory only. It does not modify BlackIndex metadata, evidence
objects, or the human review ledger. It reads the review-bundle manifest and the
small extracted PDFs, runs pdftotext, and reports structural signals that help a
reviewer confirm whether each heuristic slice is a complete FBI record.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))

FD302_RE = re.compile(r"\bFD[- ]?302\b|FEDERAL BUREAU OF INVESTIGATION", re.I)
TRANSCRIPTION_RE = re.compile(r"Date of transcription\s*[:\-]?\s*([^\n]+)", re.I)
DATE_RE = re.compile(r"\b(?:0?[1-9]|1[0-2])[/.-](?:0?[1-9]|[12]\d|3[01])[/.-](?:19|20)\d{2}\b")
SERIAL_RE = re.compile(r"\b(?:File|Case|Serial)\s*(?:No\.?|Number|ID)?\s*[:#]?\s*([A-Z0-9-]*\d[A-Z0-9-]*)", re.I)
CONT_RE = re.compile(r"\b(?:Continuation|continued|page\s+\d+\s+of\s+\d+)\b", re.I)
RED_RE = re.compile(r"\b(?:PII|FGJ|FBI Classified|USG|FBI Personnel)\b", re.I)


def run_pdftotext(pdf: Path) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise RuntimeError("pdftotext is required")
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        out = Path(tmp.name)
    try:
        proc = subprocess.run([exe, "-layout", str(pdf), str(out)], capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or f"pdftotext rc={proc.returncode}")
        return out.read_text(encoding="utf-8", errors="replace")
    finally:
        out.unlink(missing_ok=True)


def uniq(values):
    out=[]
    for v in values:
        v=v.strip()
        if v and v not in out:
            out.append(v)
    return out


def inspect_text(text: str, page_count: int) -> dict:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    first = pages[0] if pages else text
    last = pages[-1] if pages else text
    header_fd302 = bool(FD302_RE.search(first[:5000]))
    continuation_first = bool(CONT_RE.search(first[:3000])) and not header_fd302
    continuation_last = bool(CONT_RE.search(last[:3000]))
    transcription = uniq(m.group(1)[:80] for m in TRANSCRIPTION_RE.finditer(text))[:10]
    dates = uniq(m.group(0) for m in DATE_RE.finditer(text))[:15]
    serials = uniq(m.group(1) for m in SERIAL_RE.finditer(text))[:15]
    redactions = uniq(m.group(0) for m in RED_RE.finditer(text))

    first_nonblank = " ".join(first.strip().split())[:320]
    last_nonblank = " ".join(last.strip().split())[-320:]

    if continuation_first:
        recommendation = "LIKELY_CONTINUATION"
        reason = "first page appears to continue an earlier record"
    elif not header_fd302:
        recommendation = "BOUNDARY_NEEDS_REVIEW"
        reason = "first page lacks a clear FD-302/FBI header signal"
    elif page_count == 1 and continuation_last:
        recommendation = "BOUNDARY_NEEDS_REVIEW"
        reason = "single-page slice contains continuation language"
    else:
        recommendation = "LIKELY_COMPLETE"
        reason = "first page has a strong FBI/FD-302 header signal and no obvious leading continuation"

    return {
        "recommendation": recommendation,
        "reason": reason,
        "fd302_header_on_first_page": header_fd302,
        "leading_continuation_signal": continuation_first,
        "trailing_continuation_signal": continuation_last,
        "date_of_transcription_hits": transcription,
        "date_hits": dates,
        "serial_or_case_hits": serials,
        "redaction_label_hits": redactions,
        "first_page_preview": first_nonblank,
        "last_page_preview": last_nonblank,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Inspect FBI review-bundle PDFs for boundary signals")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--manifest", default="local/review/source-bundles/911-fbi-first-promotion/manifest.json")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = root / manifest
    data = json.loads(manifest.read_text(encoding="utf-8"))

    results=[]
    counts={"LIKELY_COMPLETE":0,"LIKELY_CONTINUATION":0,"BOUNDARY_NEEDS_REVIEW":0}
    for rec in data.get("records", []):
        pdf = Path(rec["source_pdf"])
        text = run_pdftotext(pdf)
        page_count = max(1, text.count("\f"))
        inspection = inspect_text(text, page_count)
        counts[inspection["recommendation"]] = counts.get(inspection["recommendation"],0)+1
        results.append({
            "review_rank": rec.get("review_rank"),
            "container_doc_id": rec.get("container_doc_id"),
            "candidate_id": rec.get("candidate_id"),
            "heuristic_pages": rec.get("heuristic_pages"),
            "source_pdf": str(pdf),
            **inspection,
        })

    out_dir = manifest.parent
    out_json = out_dir / "inspection.json"
    out_md = out_dir / "inspection.md"
    out_json.write_text(json.dumps({"count":len(results),"recommendation_counts":counts,"records":results}, indent=2)+"\n", encoding="utf-8")

    lines=["# FBI source-review bundle inspection","","> Advisory boundary inspection only. No candidate is promoted by this report.","",f"Records: **{len(results)}** · Likely complete={counts.get('LIKELY_COMPLETE',0)} · Continuation={counts.get('LIKELY_CONTINUATION',0)} · Needs review={counts.get('BOUNDARY_NEEDS_REVIEW',0)}","","| Rank | Candidate | Pages | Recommendation | Date hints | Serial/case |","|---:|---|---|---|---|---|"]
    for r in results:
        dates=", ".join(r["date_of_transcription_hits"] or r["date_hits"][:3]) or "—"
        serials=", ".join(r["serial_or_case_hits"][:3]) or "—"
        lines.append(f"| {r['review_rank']} | `{r['candidate_id']}` | {r['heuristic_pages']} | **{r['recommendation']}** | {dates} | {serials} |")
    lines += ["","## Review notes",""]
    for r in results:
        lines += [f"### {r['candidate_id']} — {r['heuristic_pages']}",f"- Recommendation: **{r['recommendation']}** — {r['reason']}",f"- First-page preview: {r['first_page_preview'] or '—'}",f"- Last-page preview: {r['last_page_preview'] or '—'}",f"- Redaction labels: {', '.join(r['redaction_label_hits']) or 'None detected in text layer'}",""]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"records":len(results),"recommendation_counts":counts,"json":str(out_json),"markdown":str(out_md)}, indent=2))
    print("\n" + "\n".join(lines[:12]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
