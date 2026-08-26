#!/usr/bin/env python3
"""Render the conservative local BlackIndex entity index."""
from __future__ import annotations

import argparse, html, json, os
from collections import defaultdict
from pathlib import Path

REPO_ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",REPO_ROOT))

def esc(v): return html.escape("" if v is None else str(v))
def load(p): return json.loads(p.read_text(encoding="utf-8"))

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    src=root/"local/index/entity-index.json"
    if not src.is_file(): raise SystemExit(f"entity index not found: {src}")
    data=load(src); entities=data.get("entities",[]); edges=data.get("edges",[]); counts=data.get("counts",{})
    incoming=defaultdict(list); outgoing=defaultdict(list)
    for e in edges: outgoing[e.get("from")].append(e); incoming[e.get("to")].append(e)
    cards=[]
    for ent in entities:
        eid=ent.get("entity_id"); links=[]
        for e in incoming.get(eid,[]):
            links.append(f"<li><b>{esc(e.get('edge_type'))}</b> ← <code>{esc(e.get('from'))}</code><div class='muted'>{esc(e.get('meaning'))}</div></li>")
        for e in outgoing.get(eid,[]):
            links.append(f"<li><b>{esc(e.get('edge_type'))}</b> → <code>{esc(e.get('to'))}</code><div class='muted'>{esc(e.get('meaning'))}</div></li>")
        aliases=", ".join(ent.get("aliases") or [])
        details=[]
        for key,label in (("birth_year","Born"),("death_year","Died"),("title","Title"),("branch","Branch")):
            if ent.get(key) is not None: details.append(f"{label}: {esc(ent.get(key))}")
        cards.append(f'''<article class="entity" data-search="{esc((ent.get('canonical_name','')+' '+eid+' '+aliases+' '+ent.get('entity_type','')).casefold())}">
<h3>{esc(ent.get('canonical_name'))}</h3><div><code>{esc(eid)}</code> · <b>{esc(ent.get('entity_type'))}</b></div>
<div class="muted">{esc(' · '.join(details))}</div>{f'<div>Aliases: {esc(aliases)}</div>' if aliases else ''}
<details><summary>Relationships / document mentions ({len(links)})</summary><ul>{''.join(links) if links else '<li>None encoded.</li>'}</ul></details>
<div class="sources">Sources: {esc(', '.join(ent.get('sources') or []))}</div></article>''')
    type_counts=counts.get("entity_types",{}); edge_counts=counts.get("edge_types",{})
    body=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlackIndex Entities</title>
<style>:root{{--bg:#0d1014;--p:#151a20;--p2:#1b222a;--t:#e7edf3;--m:#8fa0af;--l:#2a343e;--a:#c8d5df;--warn:#d7b77b}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--t);font:14px/1.45 system-ui,Segoe UI,sans-serif}}header{{padding:18px 20px;border-bottom:1px solid var(--l);position:sticky;top:0;background:#0d1014f2;z-index:2}}h1{{margin:0 0 5px}}a{{color:var(--a)}}main{{max-width:1450px;margin:auto;padding:20px}}input{{width:100%;background:var(--p2);border:1px solid var(--l);color:var(--t);border-radius:8px;padding:10px 12px;margin-top:10px}}.cards{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}.stat,.entity{{background:var(--p);border:1px solid var(--l);border-radius:9px;padding:12px}}.stat strong{{font-size:20px;display:block}}.entities{{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:12px}}.entity h3{{margin:0 0 4px}}.muted,.sources{{color:var(--m)}}.sources{{font-size:12px;margin-top:8px}}code{{color:#bdd0df}}.caution{{border-left:3px solid var(--warn);background:#191814;padding:10px 12px;margin:14px 0}}ul{{padding-left:20px}}summary{{cursor:pointer;margin-top:8px}}</style>
<header><h1>BlackIndex · Entities</h1><div class="muted">Identity and explicit document mentions only. Association is not culpability.</div><div><a href="/blackindex-dashboard.html">Evidence Map</a> · <a href="/work-queue.html">Work Queue</a> · <a href="/source-lineage.html">Source Lineage</a></div><input id="q" placeholder="Filter people, organizations, operations, locations…"></header>
<main><div class="cards"><div class="stat">Entities<strong>{counts.get('entities',0)}</strong></div><div class="stat">Edges<strong>{counts.get('edges',0)}</strong></div>{''.join(f'<div class="stat">{esc(k)}<strong>{v}</strong></div>' for k,v in type_counts.items())}</div>
<div class="caution">Document mention means only that durable metadata explicitly lists the entity. Genealogy edges preserve identity/family structure only. No surname-only linkage, inherited guilt, allegation inference, or conduct scoring is performed.</div>
<div class="muted">Edge types: {esc(', '.join(f'{k}={v}' for k,v in edge_counts.items()))}</div><h2>Entity index</h2><section class="entities" id="entities">{''.join(cards) if cards else '<div class="muted">No explicit entities are currently indexed.</div>'}</section></main>
<script>const q=document.getElementById('q');q.oninput=()=>{{const n=q.value.trim().toLowerCase();document.querySelectorAll('.entity').forEach(x=>x.style.display=!n||x.dataset.search.includes(n)?'block':'none')}};</script>'''
    out=root/"local/dashboard/entities.html"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8")
    print(json.dumps({"output":str(out),"entities":counts.get("entities",0),"edges":counts.get("edges",0),"types":type_counts},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
