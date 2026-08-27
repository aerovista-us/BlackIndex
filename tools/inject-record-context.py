#!/usr/bin/env python3
"""Inject a dependency-free selected-record context panel into BlackIndex dashboard.

The panel is generated from already-encoded local indexes. It is navigational only:
entity mentions are not conduct claims, source-lineage edges are not independent
corroboration, and review-state labels are workflow state rather than historical
conclusions.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_RECORD_CONTEXT -->"


def load(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def build_context(root: Path) -> dict:
    entity = load(root / "local/index/entity-index.json", {"entities": [], "edges": []})
    lineage = load(root / "local/index/source-lineage.json", {"edges": []})
    review = load(root / "local/index/review-state-audit.json", {"records": [], "mismatches": []})
    research = load(root / "local/index/research-reference-audit.json", {"pairs": []})

    names = {e.get("entity_id"): e.get("canonical_name") or e.get("entity_id") for e in entity.get("entities", [])}
    by_doc: dict[str, dict] = {}

    def doc(doc_id):
        if not doc_id:
            return None
        return by_doc.setdefault(str(doc_id), {
            "entities": [], "upstream": [], "downstream": [],
            "review_state": None, "review_finding": None,
            "research_cross_references": [],
        })

    for edge in entity.get("edges", []):
        if edge.get("edge_type") != "document_mentions_entity":
            continue
        d = doc(edge.get("from"))
        if d is None:
            continue
        eid = edge.get("to")
        d["entities"].append({
            "entity_id": eid,
            "name": names.get(eid, eid),
            "entity_type": edge.get("entity_type"),
        })

    for edge in lineage.get("edges", []):
        source = edge.get("source_id") or edge.get("source") or edge.get("from")
        parent = edge.get("depends_on") or edge.get("target") or edge.get("to")
        if not source or not parent:
            continue
        ds, dp = doc(source), doc(parent)
        item = {
            "doc_id": str(parent),
            "dependency_type": edge.get("dependency_type"),
            "independence": edge.get("independence"),
        }
        if ds is not None:
            ds["upstream"].append(item)
        if dp is not None:
            dp["downstream"].append({
                "doc_id": str(source),
                "dependency_type": edge.get("dependency_type"),
                "independence": edge.get("independence"),
            })

    review_records = review.get("records") or review.get("documents") or []
    for item in review_records:
        d = doc(item.get("doc_id"))
        if d is not None:
            d["review_state"] = item.get("extraction_state") or item.get("state")
            d["review_finding"] = item.get("finding")
    for item in review.get("mismatches", []):
        d = doc(item.get("doc_id"))
        if d is not None:
            d["review_state"] = item.get("extraction_state") or d.get("review_state")
            d["review_finding"] = item.get("finding") or d.get("review_finding")

    for pair in research.get("pairs", []):
        a, b = pair.get("doc_a"), pair.get("doc_b")
        if a and b:
            da, db = doc(a), doc(b)
            entry_ab = {"doc_id": str(b), "status": pair.get("status") or "REVIEW_REQUIRED", "cooccurrence_files": pair.get("cooccurrence_files")}
            entry_ba = {"doc_id": str(a), "status": pair.get("status") or "REVIEW_REQUIRED", "cooccurrence_files": pair.get("cooccurrence_files")}
            if da is not None: da["research_cross_references"].append(entry_ab)
            if db is not None: db["research_cross_references"].append(entry_ba)

    for d in by_doc.values():
        for key in ("entities", "upstream", "downstream", "research_cross_references"):
            seen = set(); unique = []
            for item in d[key]:
                token = json.dumps(item, sort_keys=True)
                if token not in seen:
                    seen.add(token); unique.append(item)
            d[key] = unique
    return {"schema_version": 1, "documents": by_doc}


def script(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return f'''{MARKER}
<style>
.bi-context{{margin:11px 0;padding:11px 12px;background:var(--panel);border:1px solid var(--line);border-radius:8px}}
.bi-context-head{{display:flex;gap:8px;align-items:center;justify-content:space-between;flex-wrap:wrap}}
.bi-context-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:8px;margin-top:8px}}
.bi-context-box{{background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:8px 9px;min-height:66px}}
.bi-context-box b{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:4px}}
.bi-context a{{color:var(--accent);text-decoration:none}}.bi-context a:hover{{text-decoration:underline}}
.bi-context ul{{margin:4px 0 0;padding-left:17px}}.bi-context li{{margin:2px 0}}
.bi-context-empty{{color:var(--muted);font-size:12px}}
</style>
<script>
(function(){{
 const BI_CONTEXT={data};
 const view=document.getElementById('view');
 if(!view)return;
 const esc2=s=>String(s??'').replace(/[&<>"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[m]));
 const docHref=id=>'/blackindex-dashboard.html#doc='+encodeURIComponent(id)+'&tab=extraction';
 const list=(items,fn)=>items&&items.length?'<ul>'+items.map(x=>'<li>'+fn(x)+'</li>').join('')+'</ul>':'<div class="bi-context-empty">None encoded</div>';
 function currentId(){{
   try{{if(typeof current!=='undefined'&&current&&current.metadata)return current.metadata.doc_id;}}catch(e){{}}
   const p=new URLSearchParams(location.hash.replace(/^#/,''));return p.get('doc');
 }}
 function inject(){{
   if(view.querySelector('.bi-context'))return;
   const id=currentId();if(!id)return;
   const c=(BI_CONTEXT.documents||{{}})[id]||{{entities:[],upstream:[],downstream:[],research_cross_references:[]}};
   const anchor=view.querySelector('.bi-object-strip')||view.querySelector('.bi-record-tools')||view.querySelector('pre');
   if(!anchor)return;
   const panel=document.createElement('section');panel.className='bi-context';
   const status=c.review_state||c.review_finding;
   panel.innerHTML=`<div class="bi-context-head"><strong>Record context</strong><span class="sub">Encoded relationships and workflow context only</span></div>
   <div class="bi-context-grid">
    <div class="bi-context-box"><b>Explicit entities</b>${{list(c.entities,x=>esc2(x.name)+(x.entity_type?' <span class="sub">· '+esc2(x.entity_type)+'</span>':''))}}</div>
    <div class="bi-context-box"><b>Depends on</b>${{list(c.upstream,x=>'<a href="'+docHref(x.doc_id)+'">'+esc2(x.doc_id)+'</a>'+(x.dependency_type?' <span class="sub">· '+esc2(x.dependency_type)+'</span>':''))}}</div>
    <div class="bi-context-box"><b>Used by</b>${{list(c.downstream,x=>'<a href="'+docHref(x.doc_id)+'">'+esc2(x.doc_id)+'</a>'+(x.dependency_type?' <span class="sub">· '+esc2(x.dependency_type)+'</span>':''))}}</div>
    <div class="bi-context-box"><b>Research cross-references</b>${{list(c.research_cross_references,x=>'<a href="'+docHref(x.doc_id)+'">'+esc2(x.doc_id)+'</a> <span class="sub">· '+esc2(String(x.status||'').replaceAll('_',' '))+'</span>')}}</div>
    <div class="bi-context-box"><b>Review state</b>${{status?esc2(c.review_state||'')+(c.review_finding?'<div class="sub">'+esc2(c.review_finding)+'</div>':''):'<div class="bi-context-empty">No audit state encoded</div>'}}</div>
    <div class="bi-context-box"><b>Missing references</b>${{(()=>{{try{{const d=(typeof current!=='undefined'&&current)||null;const a=((d&&d.integrity)||{{}}).missing_referenced_records||[];return a.length?'<ul>'+a.map(x=>'<li>'+esc2(x)+'</li>').join('')+'</ul>':'<div class="bi-context-empty">None encoded</div>'}}catch(e){{return '<div class="bi-context-empty">Unavailable</div>'}}}})()}}</div>
   </div>
   <div class="sub" style="margin-top:7px">Entity mention does not imply conduct. Cross-reference does not imply dependency. Dependency does not create independent corroboration.</div>`;
   anchor.parentNode.insertBefore(panel,anchor.nextSibling);
 }}
 const obs=new MutationObserver(()=>inject());obs.observe(view,{{childList:true,subtree:true}});inject();
 window.addEventListener('hashchange',()=>setTimeout(inject,0));
}})();
</script>'''


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("local/dashboard/blackindex-dashboard.html")
    if not path.is_file():
        print(f"error: dashboard not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Record context already injected: {path}")
        return 0
    root = path.resolve().parents[2]
    payload = build_context(root)
    block = script(payload)
    body_end = text.lower().rfind("</body>")
    text = text[:body_end] + block + text[body_end:] if body_end >= 0 else text + block
    path.write_text(text, encoding="utf-8")
    print(json.dumps({"output": str(path), "context_documents": len(payload["documents"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
