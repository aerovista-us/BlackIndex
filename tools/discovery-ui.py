#!/usr/bin/env python3
"""Render the local BlackIndex Discovery Inbox.

Discovery objects are research leads and workflow state. They are not evidence
objects promoted into historical conclusions merely by appearing here.
"""
from __future__ import annotations

import argparse, html, json, os
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def esc(value):
    return html.escape("" if value is None else str(value))


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def doc_link(doc_id):
    ident = str(doc_id or "")
    return f'<a href="/blackindex-dashboard.html#doc={quote(ident)}&tab=extraction"><code>{esc(ident)}</code></a>' if ident else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    items = [load(p) for p in sorted((root / "objects/discoveries").glob("*.json"))]
    items = [x for x in items if x.get("object_type") == "discovery"]
    open_items = [x for x in items if x.get("status") not in {"promoted", "resolved", "rejected"}]

    rows = []
    for item in items:
        docs = "<br>".join(doc_link(x) for x in item.get("linked_doc_ids", [])) or "—"
        sources = "<br>".join(esc(x) for x in item.get("source_refs", [])) or "—"
        rows.append(
            f'<tr data-search="{esc(json.dumps(item).lower())}">'
            f'<td><code>{esc(item.get("object_id"))}</code></td>'
            f'<td><b>{esc(item.get("title"))}</b><br><span class="muted">{esc(item.get("summary"))}</span></td>'
            f'<td>{esc(item.get("discovery_type"))}</td><td>{esc(item.get("status"))}</td>'
            f'<td>{esc(item.get("discovered_at"))}</td><td>{docs}</td><td>{sources}</td>'
            f'<td>{esc(item.get("evidence_boundary"))}</td></tr>'
        )

    body = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BlackIndex Discovery Inbox</title>
<style>body{{margin:0;background:#0d1014;color:#e7edf3;font:14px/1.45 system-ui}}header,main{{padding:18px 20px}}header{{border-bottom:1px solid #2a343e}}a{{color:#c8d5df}}.muted{{color:#8fa0af}}.warn{{border-left:3px solid #d7b77b;background:#191814;padding:10px;margin:14px 0}}input{{width:100%;padding:9px;background:#1b222a;color:#e7edf3;border:1px solid #2a343e;border-radius:6px}}table{{width:100%;border-collapse:collapse;margin-top:16px}}th,td{{padding:9px;border-bottom:1px solid #2a343e;text-align:left;vertical-align:top}}th{{background:#1b222a}}code{{color:#bdd0df}}tr[data-hidden="1"]{{display:none}}</style>
<header><h1>BlackIndex · Discovery Inbox</h1><div class="muted">{len(items)} discoveries · {len(open_items)} open workflow items</div>
<div><a href="/work-queue.html">Work Queue</a> · <a href="/capability-registry.html">Capability Registry</a> · <a href="/blackindex-dashboard.html">Evidence Map</a></div></header>
<main><div class="warn">Discoveries are leads, questions, artifacts, or observations awaiting research disposition. Presence here does not promote a claim to evidence or fact.</div>
<input id="q" placeholder="Filter discoveries…">
<table><thead><tr><th>ID</th><th>Discovery</th><th>Type</th><th>Status</th><th>Observed</th><th>Documents</th><th>Sources</th><th>Evidence boundary</th></tr></thead>
<tbody>{''.join(rows) or '<tr><td colspan="8">No discovery objects yet.</td></tr>'}</tbody></table></main>
<script>const q=document.getElementById('q');q.oninput=()=>document.querySelectorAll('tbody tr[data-search]').forEach(r=>r.dataset.hidden=r.dataset.search.includes(q.value.toLowerCase())?'0':'1');</script>'''
    out = root / "local/dashboard/discovery-inbox.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(json.dumps({"output": str(out), "discoveries": len(items), "open": len(open_items)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
