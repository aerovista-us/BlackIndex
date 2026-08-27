#!/usr/bin/env python3
"""Render the local 9/11 named-source recovery scan as a standalone HTML page."""
from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
EO14040_RE = re.compile(r"^FBI-(?:2021|2022)-eo14040-")


def esc(value) -> str:
    return html.escape("" if value is None else str(value))


def load(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def hit_class(candidate: dict) -> tuple[str, str]:
    doc_id = str(candidate.get("doc_id") or "")
    source = str(candidate.get("source") or "").upper()
    if EO14040_RE.match(doc_id):
        return "EO14040_CONTAINER_CANDIDATE", "EO 14040 container candidate"
    if source == "COMMISSION":
        return "CITATION_OR_SYNTHESIS", "Commission citation/synthesis"
    if doc_id.startswith("FBI-2016-operation-encore"):
        return "LATER_FBI_SYNTHESIS", "Later FBI synthesis"
    return "OTHER_REFERENCE_CANDIDATE", "Other reference candidate"


def target_classification(target: dict) -> str:
    kinds = {hit_class(c)[0] for c in target.get("candidates", [])}
    if "EO14040_CONTAINER_CANDIDATE" in kinds:
        return "UNDERLYING_CONTAINER_CANDIDATE"
    if kinds:
        return "CITATION_OR_SYNTHESIS_ONLY"
    return "NO_LOCAL_CANDIDATE"


def main() -> int:
    ap = argparse.ArgumentParser(description="Render BlackIndex named-source recovery results")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    report_path = root / "local/index/911-named-source-recovery.json"
    report = load(report_path, None)

    if report:
        targets = report.get("targets", [])
        eo14040_targets = sum(1 for t in targets if target_classification(t) == "UNDERLYING_CONTAINER_CANDIDATE")
        citation_only_targets = sum(1 for t in targets if target_classification(t) == "CITATION_OR_SYNTHESIS_ONLY")
        cards = [
            ("Targets", report.get("target_count", 0)),
            ("Any candidate hit", report.get("targets_with_candidates", 0)),
            ("EO 14040 target families", eo14040_targets),
            ("Citation/synthesis only", citation_only_targets),
            ("Scanned documents", report.get("scanned_documents", 0)),
            ("Text-page chunks", report.get("scanned_text_pages", 0)),
        ]
        sections = []
        for target in targets:
            rows = []
            target_kind = target_classification(target)
            for cand in target.get("candidates", []):
                _, kind_label = hit_class(cand)
                rows.append(
                    "<tr>"
                    f"<td>{esc(kind_label)}</td>"
                    f"<td><code>{esc(cand.get('doc_id'))}</code></td>"
                    f"<td>{esc(cand.get('source'))}</td>"
                    f"<td>{esc(cand.get('text_page_index'))}</td>"
                    "<td>unverified</td>"
                    f"<td>{esc('; '.join(cand.get('matched') or []))}</td>"
                    f"<td>{esc(cand.get('preview'))}</td>"
                    "</tr>"
                )
            body_rows = "".join(rows) or '<tr><td colspan="7">No local candidate hit.</td></tr>'
            sections.append(
                f'<section class="target" data-target="{esc(target.get("target_id"))}">'
                f'<h2>{esc(target.get("label"))} <span>{esc(target.get("candidate_count", 0))} candidate(s) · {esc(target_kind)}</span></h2>'
                '<table><thead><tr><th>Hit class</th><th>Parent document</th><th>Source</th><th>Text page</th><th>Physical page</th><th>Matched signature</th><th>Preview</th></tr></thead>'
                f'<tbody>{body_rows}</tbody></table></section>'
            )
        empty_note = ""
    else:
        cards = [("Targets", 0), ("Any candidate hit", 0), ("EO 14040 target families", 0), ("Citation/synthesis only", 0), ("Scanned documents", 0), ("Text-page chunks", 0)]
        sections = []
        empty_note = (
            '<div class="notice">No named-source recovery scan exists yet. Run '
            '<code>python3 tools/recover-911-named-sources.py</code> or the controlled Review 007 local checkpoint command. '
            'This page will populate from the local result without changing evidence state.</div>'
        )

    card_html = "".join(f'<div class="card"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in cards)
    section_html = "".join(sections)
    generated = esc(report.get("generated_at")) if report else "not run"

    page = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlackIndex Named Source Recovery</title>
<style>:root{{--bg:#0d1014;--panel:#151a20;--panel2:#1b222a;--text:#e7edf3;--muted:#8fa0af;--line:#2a343e;--link:#c8d5df;--warn:#d7b77b}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,Segoe UI,sans-serif}}header{{padding:18px 20px;border-bottom:1px solid var(--line);position:sticky;top:0;background:#0d1014f5;z-index:3}}h1{{margin:0 0 4px}}a{{color:var(--link)}}nav{{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}}main{{max-width:1600px;margin:auto;padding:20px}}.cards{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;min-width:170px}}.card span{{color:var(--muted);display:block}}.card strong{{font-size:22px}}.notice,.caution{{padding:12px;border-left:3px solid var(--warn);background:#191814;margin:14px 0}}.toolbar{{display:flex;gap:8px;align-items:center;margin:16px 0}}.toolbar input{{flex:1;min-width:260px;background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:9px 10px}}table{{width:100%;border-collapse:collapse;background:var(--panel);margin-bottom:26px}}th,td{{padding:9px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:var(--panel2)}}h2{{margin:28px 0 8px}}h2 span{{color:var(--muted);font-size:12px;font-weight:400}}code{{color:#bdd0df}}.muted{{color:var(--muted)}}.target[data-hidden="1"],tr[data-hidden="1"]{{display:none}}@media(max-width:900px){{header{{position:static}}table{{display:block;overflow-x:auto}}}}</style></head>
<body><header><h1>BlackIndex · Named Source Recovery</h1><div class="muted">Review 007A · generated {generated}</div><nav><a href="/blackindex-dashboard.html">Evidence Map</a><a href="/work-queue.html">Work Queue</a><a href="/source-lineage.html">Source Lineage</a><a href="/entities.html">Entities</a></nav></header>
<main><div class="caution"><strong>Candidate recovery only.</strong> “Any candidate hit” includes citations inside synthesis documents. Only the separate EO 14040 count identifies target families with a candidate occurrence inside an FBI release container. Neither class proves that the full underlying record boundary has been recovered, and text-page indices are not verified physical PDF page numbers.</div>{empty_note}<div class="cards">{card_html}</div><div class="toolbar"><input id="q" placeholder="Filter target, hit class, document, matched text, preview…"><span id="count" class="muted"></span></div>{section_html}</main>
<script>(function(){{const q=document.getElementById('q'),count=document.getElementById('count');function apply(){{const needle=q.value.trim().toLowerCase();let shown=0;document.querySelectorAll('.target').forEach(s=>{{let sectionShown=0;s.querySelectorAll('tbody tr').forEach(r=>{{const ok=!needle||r.textContent.toLowerCase().includes(needle)||s.querySelector('h2').textContent.toLowerCase().includes(needle);r.dataset.hidden=ok?'0':'1';if(ok){{shown++;sectionShown++;}}}});s.dataset.hidden=sectionShown?'0':'1';}});count.textContent=`${{shown}} visible candidate row${{shown===1?'':'s'}}`;}}q.oninput=apply;document.addEventListener('keydown',e=>{{if(e.key==='/'&&document.activeElement!==q){{e.preventDefault();q.focus();}}if(e.key==='Escape'&&document.activeElement===q){{q.value='';q.blur();apply();}}}});apply();}})();</script></body></html>'''

    out = root / "local/dashboard/named-source-recovery.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "scan_present": bool(report),
        "targets": report.get("target_count", 0) if report else 0,
        "targets_with_candidates": report.get("targets_with_candidates", 0) if report else 0,
        "eo14040_target_families": eo14040_targets if report else 0,
        "citation_only_target_families": citation_only_targets if report else 0,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
