#!/usr/bin/env python3
"""Build a small standalone BlackIndex work-queue dashboard.

The queue aggregates existing workflow states; it does not infer historical
conclusions or change evidence status. Local-only FBI review state is included
when available. The generated page is dependency-free and links records back to
the local Evidence Map using hash deep links.
"""
from __future__ import annotations

import argparse, html, json, os
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def esc(v): return html.escape("" if v is None else str(v))
def label(v): return str(v or "").replace("_", " ")
def load(path: Path, default):
    if not path.is_file(): return default
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return default

def doc_link(doc_id):
    if not doc_id: return ""
    ident=str(doc_id)
    return f'<a class="doclink" href="/blackindex-dashboard.html#doc={quote(ident)}&tab=extraction"><code>{esc(ident)}</code></a>'

def metadata_docs(root: Path):
    docs=[]
    for p in sorted((root/"metadata").glob("*.json")):
        d=load(p,{})
        if d.get("doc_id"): docs.append(d)
    return docs


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    docs=metadata_docs(root)
    unreviewed=[d for d in docs if d.get("evidence_status") in (None,"unreviewed")]

    missing=[]
    for p in sorted((root/"objects/missing_evidence").glob("*.json")):
        d=load(p,{})
        if d and d.get("status","unresolved") != "resolved": missing.append(d)

    audit=load(root/"local/index/research-reference-audit.json",{"pairs":[]})
    lineage_pairs=audit.get("pairs",[])
    review_audit=load(root/"local/index/review-state-audit.json",{"mismatches":[],"extraction_state_counts":{}})
    review_mismatches=review_audit.get("mismatches",[])
    extraction_counts=review_audit.get("extraction_state_counts",{})

    ledger=load(root/"local/review/911-fbi-p0/review-ledger.json",{"reviews":[]})
    reviews=ledger.get("reviews",[])
    review_counts={"PROMOTE":0,"HOLD":0,"MERGE":0,"REJECT-BOUNDARY":0,"OTHER":0}
    for r in reviews:
        key=r.get("disposition") or "OTHER"; review_counts[key if key in review_counts else "OTHER"]+=1
    p0_manifest=load(root/"local/review/911-fbi-p0/manifest.json",{"packets":[]})
    p0_count=p0_manifest.get("count")
    if p0_count is None: p0_count=len(p0_manifest.get("packets",[]))
    reviewed_keys={(r.get("container_doc_id"),r.get("candidate_id")) for r in reviews}
    pending_fbi=max(0,int(p0_count or 0)-len(reviewed_keys))

    unreviewed_rows="".join(f"<tr>{'<td>'+doc_link(d.get('doc_id'))+'</td>'}<td>{esc(d.get('title'))}</td><td>{esc(d.get('source'))}</td><td>{esc(d.get('collection'))}</td></tr>" for d in unreviewed[:100])
    mismatch_rows="".join(f"<tr><td>{doc_link(d.get('doc_id'))}</td><td>{esc(d.get('metadata_evidence_status'))}</td><td>{esc(d.get('extraction_state'))}</td><td>{esc(d.get('finding'))}</td><td>{esc(label(d.get('status')))}</td></tr>" for d in review_mismatches[:100])
    missing_rows="".join(f"<tr><td><code>{esc(d.get('object_id'))}</code></td><td>{doc_link(d.get('doc_id'))}</td><td>{esc(d.get('category'))}</td><td>{esc(d.get('summary'))}</td></tr>" for d in missing[:100])
    lineage_rows="".join(f"<tr><td>{doc_link(x.get('doc_a'))}</td><td>{doc_link(x.get('doc_b'))}</td><td>{esc(x.get('cooccurrence_files'))}</td><td>{'<br>'.join(esc(f) for f in x.get('files',[]))}</td><td>{esc(label(x.get('status') or 'REVIEW_REQUIRED'))}</td></tr>" for x in lineage_pairs[:100])
    review_rows="".join(f"<tr><td>{doc_link(r.get('container_doc_id'))}</td><td><code>{esc(r.get('candidate_id'))}</code></td><td>{esc(r.get('disposition'))}</td><td>{esc(r.get('confirmed_pages'))}</td><td>{esc(r.get('note'))}</td></tr>" for r in reviews)

    body=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlackIndex Work Queue</title>
<style>:root{{--bg:#0d1014;--p:#151a20;--p2:#1b222a;--t:#e7edf3;--m:#8fa0af;--l:#2a343e;--a:#c8d5df;--warn:#d7b77b}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--t);font:14px/1.45 system-ui,Segoe UI,sans-serif}}header{{padding:18px 20px;border-bottom:1px solid var(--l);position:sticky;top:0;background:#0d1014f5;z-index:3}}h1{{margin:0 0 4px}}a{{color:var(--a)}}main{{max-width:1500px;margin:auto;padding:20px}}.cards{{display:flex;gap:10px;flex-wrap:wrap;margin:15px 0}}.card{{background:var(--p);border:1px solid var(--l);border-radius:10px;padding:12px;min-width:155px;cursor:default}}.card strong{{display:block;font-size:22px}}.muted{{color:var(--m)}}.caution{{border-left:3px solid var(--warn);background:#191814;padding:10px 12px;margin:14px 0}}table{{width:100%;border-collapse:collapse;background:var(--p);margin-bottom:28px}}th,td{{padding:9px 10px;border-bottom:1px solid var(--l);text-align:left;vertical-align:top}}th{{background:var(--p2);position:sticky;top:126px}}code{{color:#bdd0df}}h2{{margin-top:30px}}.nav,.toolbar{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}.nav{{margin-top:6px}}.toolbar{{margin-top:10px;padding-top:10px;border-top:1px solid var(--l)}}.toolbar input,.toolbar select,.toolbar button{{background:var(--p2);color:var(--t);border:1px solid var(--l);border-radius:6px;padding:8px 10px}}.toolbar input{{min-width:280px;flex:1}}.toolbar button{{cursor:pointer}}.toolbar button:hover{{border-color:#687887}}.queue-section[data-hidden="1"]{{display:none}}tr[data-hidden="1"]{{display:none}}.doclink{{text-decoration:none}}.doclink:hover code{{text-decoration:underline}}.section-count{{font-size:12px;color:var(--m);font-weight:400}}#visible-count{{color:var(--m);font-size:12px}}@media(max-width:800px){{th{{position:static}}header{{position:static}}table{{display:block;overflow-x:auto}}.toolbar input{{min-width:100%}}}}</style>
<header><h1>BlackIndex · Work Queue</h1><div class="muted">Unresolved work states only. Queue membership is not evidence of importance, wrongdoing, or truth.</div><div class="nav"><a href="/blackindex-dashboard.html">Evidence Map</a><a href="/source-lineage.html">Source Lineage</a><a href="/entities.html">Entities</a></div><div class="toolbar"><input id="queue-q" placeholder="Filter queue by document, status, category, note…"><select id="queue-section"><option value="">All sections</option><option value="drift">Review-state drift</option><option value="fbi">FBI P0 review</option><option value="lineage">Lineage review</option><option value="missing">Missing evidence</option><option value="unreviewed">Unreviewed metadata</option></select><button id="queue-clear" type="button">Clear</button><span id="visible-count"></span></div></header>
<main><div class="cards"><div class="card"><span class="muted">Git-backed documents</span><strong>{len(docs)}</strong></div><div class="card"><span class="muted">Metadata marked unreviewed</span><strong>{len(unreviewed)}</strong></div><div class="card"><span class="muted">Neutral review stubs</span><strong>{extraction_counts.get('stub',0)}</strong></div><div class="card"><span class="muted">Review-state mismatches</span><strong>{len(review_mismatches)}</strong></div><div class="card"><span class="muted">Unresolved missing-evidence objects</span><strong>{len(missing)}</strong></div><div class="card"><span class="muted">Lineage pairs awaiting review</span><strong>{len(lineage_pairs)}</strong></div><div class="card"><span class="muted">FBI P0 packets</span><strong>{p0_count or 0}</strong></div><div class="card"><span class="muted">FBI P0 without ledger decision</span><strong>{pending_fbi}</strong></div></div>
<div class="caution">This page aggregates workflow state. “Unreviewed,” “missing,” “hold,” “status lag,” and “cross-reference” are process labels, not historical conclusions.</div>
<section class="queue-section" data-section="drift"><h2>Metadata / extraction review-state drift <span class="section-count"></span></h2><p class="muted">A non-stub extraction can indicate review activity while metadata still says unreviewed. This is a synchronization queue only; no evidence status is changed automatically.</p><table><thead><tr><th>Document</th><th>Metadata status</th><th>Extraction state</th><th>Finding</th><th>Status</th></tr></thead><tbody>{mismatch_rows or '<tr><td colspan="5">No review-state mismatches detected.</td></tr>'}</tbody></table></section>
<section class="queue-section" data-section="fbi"><h2>FBI P0 review state <span class="section-count"></span></h2><p class="muted">Local review ledger only. PROMOTE remains subject to the separate fail-closed child-record promoter.</p><div class="cards"><div class="card">PROMOTE<strong>{review_counts['PROMOTE']}</strong></div><div class="card">HOLD<strong>{review_counts['HOLD']}</strong></div><div class="card">MERGE<strong>{review_counts['MERGE']}</strong></div><div class="card">REJECT-BOUNDARY<strong>{review_counts['REJECT-BOUNDARY']}</strong></div></div><table><thead><tr><th>Container</th><th>Candidate</th><th>Disposition</th><th>Confirmed pages</th><th>Note</th></tr></thead><tbody>{review_rows or '<tr><td colspan="5">No FBI review ledger entries currently present.</td></tr>'}</tbody></table></section>
<section class="queue-section" data-section="lineage"><h2>Research cross-references awaiting lineage review <span class="section-count"></span></h2><table><thead><tr><th>Document A</th><th>Document B</th><th>Research files</th><th>Where recognized</th><th>Status</th></tr></thead><tbody>{lineage_rows or '<tr><td colspan="5">No unresolved research cross-reference pairs.</td></tr>'}</tbody></table></section>
<section class="queue-section" data-section="missing"><h2>Unresolved missing-evidence objects <span class="section-count"></span></h2><table><thead><tr><th>Object</th><th>Document</th><th>Category</th><th>Summary</th></tr></thead><tbody>{missing_rows or '<tr><td colspan="4">No unresolved missing-evidence objects.</td></tr>'}</tbody></table></section>
<section class="queue-section" data-section="unreviewed"><h2>Documents still marked unreviewed <span class="section-count"></span></h2><p class="muted">Use the review-state drift table above to distinguish likely status lag from untouched neutral stubs.</p><table><thead><tr><th>Document</th><th>Title</th><th>Source</th><th>Collection</th></tr></thead><tbody>{unreviewed_rows or '<tr><td colspan="4">No metadata records currently marked unreviewed.</td></tr>'}</tbody></table></section>
</main>
<script>
(function(){{
 const q=document.getElementById('queue-q'), section=document.getElementById('queue-section'), clear=document.getElementById('queue-clear'), visible=document.getElementById('visible-count');
 function apply(){{
   const needle=q.value.trim().toLowerCase(), wanted=section.value;let shown=0,total=0;
   document.querySelectorAll('.queue-section').forEach(s=>{{
     const sectionAllowed=!wanted||s.dataset.section===wanted;let rowsShown=0;
     s.querySelectorAll('tbody tr').forEach(r=>{{total++;const ok=sectionAllowed&&(!needle||r.textContent.toLowerCase().includes(needle));r.dataset.hidden=ok?'0':'1';if(ok){{shown++;rowsShown++;}}}});
     const heading=s.querySelector('.section-count');if(heading)heading.textContent=`· ${{rowsShown}} visible`;
     s.dataset.hidden=sectionAllowed&&rowsShown>0?'0':'1';
   }});
   visible.textContent=`${{shown}} visible queue row${{shown===1?'':'s'}}`;
 }}
 q.oninput=apply;section.onchange=apply;clear.onclick=()=>{{q.value='';section.value='';apply();q.focus();}};
 document.addEventListener('keydown',e=>{{if(e.key==='/'&&document.activeElement!==q){{e.preventDefault();q.focus();}}if(e.key==='Escape'&&document.activeElement===q){{q.value='';q.blur();apply();}}}});
 apply();
}})();
</script>'''
    out=root/"local/dashboard/work-queue.html"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8")
    print(json.dumps({"output":str(out),"documents":len(docs),"unreviewed":len(unreviewed),"review_state_mismatches":len(review_mismatches),"neutral_stubs":extraction_counts.get('stub',0),"missing_evidence":len(missing),"lineage_pairs":len(lineage_pairs),"fbi_p0":p0_count or 0,"fbi_pending":pending_fbi},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
