#!/usr/bin/env python3
"""Render BlackIndex source lineage and unresolved lineage-review backlog."""
from __future__ import annotations

import argparse, html, json, os
from pathlib import Path

REPO_ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",REPO_ROOT))

def esc(v): return html.escape("" if v is None else str(v))
def read(p, default=None):
    if not p.is_file(): return {} if default is None else default
    return json.loads(p.read_text(encoding="utf-8"))

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args()
    root=Path(args.root).resolve(); src=root/"local/index/source-lineage.json"
    if not src.is_file(): raise SystemExit(f"source lineage index not found: {src}")
    data=read(src); nodes={n.get("id"):n for n in data.get("nodes",[])}; edges=data.get("edges",[]); fam=data.get("shared_lineage_families",[])
    audit=read(root/"local/index/research-reference-audit.json", {"pairs":[]})
    audit_pairs=audit.get("pairs",[])

    rows=[]
    for e in edges:
        a=nodes.get(e.get("from"),{}); b=nodes.get(e.get("to"),{})
        rows.append(f"<tr><td><code>{esc(e.get('from'))}</code><div>{esc(a.get('title'))}</div></td><td>{esc(e.get('relationship'))}</td><td><code>{esc(e.get('to'))}</code><div>{esc(b.get('title'))}</div></td><td>{esc(e.get('independence') or 'unknown')}</td><td>{esc(e.get('origin'))}</td></tr>")

    family_cards=[]
    for f in fam:
        members="".join(f"<li><code>{esc(x)}</code></li>" for x in f.get("member_sources",[]))
        family_cards.append(f"<section class='family'><h3>{esc(f.get('upstream_source'))}</h3><ul>{members}</ul><p>{esc(f.get('warning'))}</p></section>")

    audit_rows=[]
    for rank,pair in enumerate(audit_pairs[:40], start=1):
        files=pair.get("files") or []
        audit_rows.append(
            f"<tr><td>{rank}</td><td><code>{esc(pair.get('doc_a'))}</code></td>"
            f"<td><code>{esc(pair.get('doc_b'))}</code></td>"
            f"<td>{esc(pair.get('cooccurrence_files',0))}</td>"
            f"<td>{'<br>'.join(esc(x) for x in files)}</td><td>REVIEW REQUIRED</td></tr>"
        )

    counts=data.get("counts",{}); indep=counts.get("independence",{})
    body=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlackIndex Source Lineage</title>
<style>:root{{--bg:#0d1014;--p:#151a20;--p2:#1b222a;--t:#e7edf3;--m:#8fa0af;--l:#2a343e;--a:#c8d5df;--warn:#d7b77b}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--t);font:14px/1.45 system-ui,Segoe UI,sans-serif}}header{{padding:20px;border-bottom:1px solid var(--l);position:sticky;top:0;background:#0d1014f2;z-index:2}}h1{{margin:0 0 5px;font-size:20px}}a{{color:var(--a)}}main{{max-width:1450px;margin:auto;padding:20px}}.cards{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}.card,.family{{background:var(--p);border:1px solid var(--l);border-radius:9px;padding:12px}}.card strong{{font-size:21px;display:block}}.muted{{color:var(--m)}}table{{width:100%;border-collapse:collapse;background:var(--p)}}th,td{{text-align:left;padding:10px;border-bottom:1px solid var(--l);vertical-align:top}}th{{background:var(--p2)}}code{{color:#bdd0df}}.families{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}}.caution{{border-left:3px solid var(--warn);padding:10px 12px;background:#191814;margin:12px 0}}.section-note{{color:var(--m);margin:-8px 0 12px}}</style>
<header><h1>BlackIndex · Source Lineage</h1><div class="muted">Source genealogy only. Repetition through a shared upstream source is not independent corroboration.</div><div><a href="/blackindex-dashboard.html">← Evidence Map</a></div></header>
<main><div class="cards"><div class="card"><span class="muted">Nodes</span><strong>{counts.get('nodes',0)}</strong></div><div class="card"><span class="muted">Encoded edges</span><strong>{counts.get('edges',0)}</strong></div><div class="card"><span class="muted">Shared upstream families</span><strong>{counts.get('shared_lineage_families',0)}</strong></div><div class="card"><span class="muted">Dependent edges</span><strong>{indep.get('dependent',0)}</strong></div><div class="card"><span class="muted">Research pairs awaiting review</span><strong>{len(audit_pairs)}</strong></div></div>
<div class="caution">Encoded lineage and research cross-references are deliberately separate. Missing edges mean “not yet encoded,” not “independent.” A research-note co-occurrence does not establish dependence, agreement, contradiction, or corroboration.</div>
<h2>Shared upstream lineages</h2><div class="families">{''.join(family_cards) if family_cards else '<div class="muted">No multi-source shared upstream lineage is currently encoded.</div>'}</div>
<h2>Encoded dependency edges</h2><div class="section-note">These relationships are durable source-dependency objects or explicit parent-container relationships.</div><table><thead><tr><th>Source</th><th>Relationship</th><th>Depends on</th><th>Independence</th><th>Origin</th></tr></thead><tbody>{''.join(rows) if rows else '<tr><td colspan="5">No encoded edges.</td></tr>'}</tbody></table>
<h2>Research cross-references awaiting lineage review</h2><div class="section-note">Candidate queue only. These pairs were recognized together in durable reviews/research-cluster notes and have not been converted into dependency edges.</div><table><thead><tr><th>#</th><th>Document A</th><th>Document B</th><th>Files</th><th>Research notes</th><th>Status</th></tr></thead><tbody>{''.join(audit_rows) if audit_rows else '<tr><td colspan="6">No research cross-reference candidates currently detected.</td></tr>'}</tbody></table>
<p class="muted">Lineage generated {esc(data.get('generated_at'))} · Research audit generated {esc(audit.get('generated_at'))}</p></main>'''
    out=root/"local/dashboard/source-lineage.html"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8")
    print(json.dumps({"output":str(out),"nodes":counts.get("nodes",0),"edges":counts.get("edges",0),"families":counts.get("shared_lineage_families",0),"research_pairs":len(audit_pairs)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
