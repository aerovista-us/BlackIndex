#!/usr/bin/env python3
"""Render the conservative local BlackIndex entity index as a standalone browser."""
from __future__ import annotations

import argparse, html, json, os
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

REPO_ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",REPO_ROOT))

def esc(v): return html.escape("" if v is None else str(v))
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def doc_link(doc_id): return f'<a href="/blackindex-dashboard.html#doc={quote(str(doc_id))}&tab=extraction"><code>{esc(doc_id)}</code></a>'
def entity_link(entity_id): return f'<a href="#{quote(str(entity_id))}"><code>{esc(entity_id)}</code></a>'

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    src=root/"local/index/entity-index.json"
    if not src.is_file(): raise SystemExit(f"entity index not found: {src}")
    data=load(src); entities=data.get("entities",[]); edges=data.get("edges",[]); counts=data.get("counts",{})
    incoming=defaultdict(list); outgoing=defaultdict(list)
    for e in edges: outgoing[e.get("from")].append(e); incoming[e.get("to")].append(e)
    entity_ids={e.get("entity_id") for e in entities}
    cards=[]
    for ent in entities:
        eid=ent.get("entity_id"); links=[]; mention_docs=[]; genealogy=[]
        for e in incoming.get(eid,[]):
            if e.get("edge_type")=="document_mentions_entity":
                mention_docs.append(e.get("from")); links.append(f"<li><b>document mention</b> ← {doc_link(e.get('from'))}<div class='muted'>{esc(e.get('meaning'))}</div></li>")
            else:
                genealogy.append(e); src_link=entity_link(e.get('from')) if e.get('from') in entity_ids else f"<code>{esc(e.get('from'))}</code>"
                links.append(f"<li><b>{esc(e.get('edge_type'))}</b> ← {src_link}<div class='muted'>{esc(e.get('meaning'))}</div></li>")
        for e in outgoing.get(eid,[]):
            if e.get("edge_type")=="document_mentions_entity":
                links.append(f"<li><b>document mention</b> → {doc_link(e.get('to'))}<div class='muted'>{esc(e.get('meaning'))}</div></li>")
            else:
                genealogy.append(e); dst_link=entity_link(e.get('to')) if e.get('to') in entity_ids else f"<code>{esc(e.get('to'))}</code>"
                links.append(f"<li><b>{esc(e.get('edge_type'))}</b> → {dst_link}<div class='muted'>{esc(e.get('meaning'))}</div></li>")
        aliases=", ".join(ent.get("aliases") or [])
        details=[]
        for key,label in (("birth_year","Born"),("death_year","Died"),("title","Title"),("branch","Branch")):
            if ent.get(key) is not None: details.append(f"{label}: {esc(ent.get(key))}")
        searchable=(ent.get('canonical_name','')+' '+eid+' '+aliases+' '+ent.get('entity_type','')+' '+' '.join(str(x) for x in mention_docs)).casefold()
        cards.append(f'''<article class="entity" id="{esc(eid)}" data-type="{esc(ent.get('entity_type'))}" data-search="{esc(searchable)}">
<div class="entity-head"><div><h3>{esc(ent.get('canonical_name'))}</h3><div><code>{esc(eid)}</code> · <b>{esc(ent.get('entity_type'))}</b></div></div><div class="counts"><span>{len(mention_docs)} doc mention{'' if len(mention_docs)==1 else 's'}</span><span>{len(genealogy)} genealogy edge{'' if len(genealogy)==1 else 's'}</span></div></div>
<div class="muted">{esc(' · '.join(details))}</div>{f'<div>Aliases: {esc(aliases)}</div>' if aliases else ''}
<details><summary>Encoded relationships / mentions ({len(links)})</summary><ul>{''.join(links) if links else '<li>None encoded.</li>'}</ul></details>
<div class="sources">Sources: {esc(', '.join(ent.get('sources') or []))}</div></article>''')
    type_counts=counts.get("entity_types",{}); edge_counts=counts.get("edge_types",{})
    options=''.join(f'<option value="{esc(k)}">{esc(k)} ({v})</option>' for k,v in sorted(type_counts.items()))
    body=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlackIndex Entities</title>
<style>:root{{--bg:#0d1014;--p:#151a20;--p2:#1b222a;--t:#e7edf3;--m:#8fa0af;--l:#2a343e;--a:#c8d5df;--warn:#d7b77b}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--t);font:14px/1.45 system-ui,Segoe UI,sans-serif}}header{{padding:18px 20px;border-bottom:1px solid var(--l);position:sticky;top:0;background:#0d1014f5;z-index:2}}h1{{margin:0 0 5px}}a{{color:var(--a)}}main{{max-width:1450px;margin:auto;padding:20px}}.toolbar{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}input,select,button{{background:var(--p2);border:1px solid var(--l);color:var(--t);border-radius:8px;padding:9px 11px}}input{{min-width:300px;flex:1}}button{{cursor:pointer}}.cards{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}.stat,.entity{{background:var(--p);border:1px solid var(--l);border-radius:9px;padding:12px}}.stat strong{{font-size:20px;display:block}}.entities{{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:12px}}.entity{{scroll-margin-top:160px}}.entity:target{{border-color:#7f93a5;box-shadow:0 0 0 1px #7f93a555}}.entity h3{{margin:0 0 4px}}.entity-head{{display:flex;justify-content:space-between;gap:12px}}.counts{{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end;align-content:flex-start}}.counts span{{font-size:10px;border:1px solid var(--l);border-radius:999px;padding:3px 6px;color:var(--m);white-space:nowrap}}.muted,.sources{{color:var(--m)}}.sources{{font-size:12px;margin-top:8px}}code{{color:#bdd0df}}.caution{{border-left:3px solid var(--warn);background:#191814;padding:10px 12px;margin:14px 0}}ul{{padding-left:20px}}summary{{cursor:pointer;margin-top:8px}}#result-count{{color:var(--m);font-size:12px;align-self:center}}@media(max-width:700px){{header{{position:static}}.entities{{grid-template-columns:1fr}}input{{min-width:100%}}.entity-head{{display:block}}.counts{{justify-content:flex-start;margin-top:8px}}}}</style>
<header><h1>BlackIndex · Entities</h1><div class="muted">Identity and explicit document mentions only. Association is not culpability.</div><div><a href="/blackindex-dashboard.html">Evidence Map</a> · <a href="/work-queue.html">Work Queue</a> · <a href="/source-lineage.html">Source Lineage</a></div><div class="toolbar"><input id="q" placeholder="Filter people, organizations, operations, locations, document IDs…"><select id="type"><option value="">All entity types</option>{options}</select><button id="clear" type="button">Clear</button><span id="result-count"></span></div></header>
<main><div class="cards"><div class="stat">Entities<strong>{counts.get('entities',0)}</strong></div><div class="stat">Edges<strong>{counts.get('edges',0)}</strong></div>{''.join(f'<div class="stat">{esc(k)}<strong>{v}</strong></div>' for k,v in type_counts.items())}</div>
<div class="caution">Document mention means only that durable metadata explicitly lists the entity. Genealogy edges preserve identity/family structure only. No surname-only linkage, inherited guilt, allegation inference, or conduct scoring is performed.</div>
<div class="muted">Edge types: {esc(', '.join(f'{k}={v}' for k,v in edge_counts.items()))}</div><h2>Entity index</h2><section class="entities" id="entities">{''.join(cards) if cards else '<div class="muted">No explicit entities are currently indexed.</div>'}</section></main>
<script>(function(){{const q=document.getElementById('q'),t=document.getElementById('type'),c=document.getElementById('clear'),count=document.getElementById('result-count');function apply(){{const n=q.value.trim().toLowerCase(),type=t.value;let shown=0;document.querySelectorAll('.entity').forEach(x=>{{const ok=(!n||x.dataset.search.includes(n))&&(!type||x.dataset.type===type);x.style.display=ok?'block':'none';if(ok)shown++;}});count.textContent=`${{shown}} / ${{document.querySelectorAll('.entity').length}} entities`;}}q.oninput=apply;t.onchange=apply;c.onclick=()=>{{q.value='';t.value='';apply();q.focus();}};document.addEventListener('keydown',e=>{{if(e.key==='/'&&document.activeElement!==q){{e.preventDefault();q.focus();}}if(e.key==='Escape'&&document.activeElement===q){{q.value='';q.blur();apply();}}}});apply();}})();</script>'''
    out=root/"local/dashboard/entities.html"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8")
    print(json.dumps({"output":str(out),"entities":counts.get("entities",0),"edges":counts.get("edges",0),"types":type_counts},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
