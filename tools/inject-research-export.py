#!/usr/bin/env python3
"""Inject browser-local Research Session export helpers into the dashboard.

This layer reads the existing BlackIndex Research Session localStorage keys and
adds convenience export/copy controls. It never writes evidence state, calls a
server, or synchronizes session data.
"""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_RESEARCH_EXPORT -->"
BLOCK = r'''
<!-- BLACKINDEX_RESEARCH_EXPORT -->
<style>
.bi-session-export-actions{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;padding-top:9px;border-top:1px solid var(--line)}
.bi-session-export-actions button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:5px;padding:5px 7px;cursor:pointer;font:600 11px system-ui}
.bi-session-export-note{margin-top:6px;font-size:10px;color:var(--muted);line-height:1.35}
</style>
<script>
(function(){
 const KEY_PINS='blackindex.pins.v1', KEY_RECENT='blackindex.recent.v1';
 const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
 const read=k=>{try{const v=JSON.parse(localStorage.getItem(k)||'[]');return Array.isArray(v)?v:[]}catch(e){return []}};
 const docFor=id=>{try{return docs.find(x=>x?.metadata?.doc_id===id)||null}catch(e){return null}};
 const summary=id=>{const d=docFor(id),m=d?.metadata||{};return {doc_id:id,title:m.title||id,originating_agency:m.originating_agency||m.source||null,document_date:m.document_date||m.date_created||null,document_type:m.document_type||null,source_url:m.source_url||m.canonical_landing_url||null,state_of_record:m.state_of_record||null,inference_dependency:m.inference_dependency||null}};
 function bundle(){const pins=read(KEY_PINS),recent=read(KEY_RECENT);return {schema:'blackindex-research-session-export-v1',exported_at:new Date().toISOString(),notice:'Browser-local convenience state only. This export is not BlackIndex evidence and does not change repository state.',pinned_records:pins.map(summary),recent_record_ids:recent};}
 function download(name,type,text){const blob=new Blob([text],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),0)}
 function markdown(b){const lines=['# BlackIndex Research Session','',`Exported: ${b.exported_at}`,'',`> ${b.notice}`,'','## Pinned records',''];if(!b.pinned_records.length)lines.push('_None._');for(const r of b.pinned_records){lines.push(`### ${r.title}`,'',`- Document ID: \`${r.doc_id}\``);if(r.originating_agency)lines.push(`- Agency/source: ${r.originating_agency}`);if(r.document_date)lines.push(`- Date: ${r.document_date}`);if(r.document_type)lines.push(`- Type: ${r.document_type}`);if(r.state_of_record)lines.push(`- State of record: ${r.state_of_record}`);if(r.inference_dependency)lines.push(`- Inference dependency: ${r.inference_dependency}`);if(r.source_url)lines.push(`- Source: ${r.source_url}`);lines.push('')}lines.push('## Recent record IDs','');if(b.recent_record_ids.length)lines.push(...b.recent_record_ids.map(x=>`- \`${x}\``));else lines.push('_None._');lines.push('');return lines.join('\n')}
 async function copyPinned(){const ids=read(KEY_PINS);const text=ids.join('\n');try{await navigator.clipboard.writeText(text)}catch(e){const ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove()}}
 function attach(){const panel=document.getElementById('bi-session');const body=document.getElementById('bi-session-body');if(!panel||!body||panel.querySelector('[data-bi-export-actions]'))return false;const wrap=document.createElement('div');wrap.className='bi-session-export-actions';wrap.dataset.biExportActions='1';wrap.innerHTML='<button type="button" data-bi-copy-pins>Copy pinned IDs</button><button type="button" data-bi-export-json>Export JSON</button><button type="button" data-bi-export-md>Export Markdown</button><button type="button" data-bi-clear-recent>Clear recent</button><div class="bi-session-export-note">Exports remain local to this browser. They are research convenience artifacts, not evidence objects or reviewed extractions.</div>';body.parentNode.appendChild(wrap);wrap.querySelector('[data-bi-copy-pins]').onclick=copyPinned;wrap.querySelector('[data-bi-export-json]').onclick=()=>download('blackindex-research-session.json','application/json',JSON.stringify(bundle(),null,2)+'\n');wrap.querySelector('[data-bi-export-md]').onclick=()=>{const b=bundle();download('blackindex-research-session.md','text/markdown;charset=utf-8',markdown(b))};wrap.querySelector('[data-bi-clear-recent]').onclick=()=>{localStorage.setItem(KEY_RECENT,'[]');const ev=new Event('hashchange');window.dispatchEvent(ev)};return true}
 if(!attach()){const mo=new MutationObserver(()=>{if(attach())mo.disconnect()});mo.observe(document.documentElement,{childList:true,subtree:true})}
})();
</script>
'''


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("local/dashboard/blackindex-dashboard.html")
    if not path.is_file():
        print(f"error: dashboard not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Research export already injected: {path}")
        return 0
    pos = text.lower().rfind("</body>")
    text = text[:pos] + BLOCK + text[pos:] if pos >= 0 else text + BLOCK
    path.write_text(text, encoding="utf-8")
    print(f"Dashboard browser-local research export injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
