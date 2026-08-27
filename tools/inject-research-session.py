#!/usr/bin/env python3
"""Inject browser-local research session helpers into the BlackIndex dashboard.

Pins and recent records live only in browser localStorage. They are convenience
state, never evidence state, and are not committed, published, or synchronized.
"""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_RESEARCH_SESSION -->"
BLOCK = r'''
<!-- BLACKINDEX_RESEARCH_SESSION -->
<style>
#bi-session-toggle{position:fixed;left:16px;bottom:16px;z-index:9997;background:#151a20;color:#e7edf3;border:1px solid #46515c;border-radius:8px;padding:9px 11px;font:600 12px system-ui;cursor:pointer;box-shadow:0 7px 24px #0006}
#bi-session{position:fixed;left:16px;bottom:58px;z-index:9998;width:min(390px,calc(100vw - 32px));max-height:65vh;overflow:auto;background:#101419;border:1px solid var(--line);border-radius:10px;padding:11px;box-shadow:0 10px 35px #0009;display:none}
body.bi-session-open #bi-session{display:block}.bi-session-head{display:flex;justify-content:space-between;gap:8px;align-items:center}.bi-session-head button,.bi-session-actions button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:5px;padding:5px 7px;cursor:pointer}.bi-session-section{margin-top:10px}.bi-session-section b{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.bi-session-list{margin-top:5px}.bi-session-row{display:flex;gap:7px;align-items:flex-start;border-top:1px solid var(--line);padding:7px 0}.bi-session-row:first-child{border-top:0}.bi-session-row a{flex:1;color:var(--accent);text-decoration:none;word-break:break-word}.bi-session-row a:hover{text-decoration:underline}.bi-session-row button{background:transparent;color:var(--muted);border:0;cursor:pointer}.bi-pin-active{border-color:var(--warn)!important;color:var(--warn)!important}
</style>
<script>
(function(){
 const KEY_PINS='blackindex.pins.v1', KEY_RECENT='blackindex.recent.v1';
 const read=k=>{try{return JSON.parse(localStorage.getItem(k)||'[]')}catch(e){return []}};
 const write=(k,v)=>localStorage.setItem(k,JSON.stringify(v));
 const currentId=()=>{try{if(typeof current!=='undefined'&&current&&current.metadata)return current.metadata.doc_id}catch(e){}const p=new URLSearchParams(location.hash.replace(/^#/,''));return p.get('doc')};
 const titleFor=id=>{try{const d=docs.find(x=>x.metadata.doc_id===id);return d?(d.metadata.title||id):id}catch(e){return id}};
 const href=id=>'/blackindex-dashboard.html#doc='+encodeURIComponent(id)+'&tab=extraction';
 function touchRecent(id){if(!id)return;let items=read(KEY_RECENT).filter(x=>x!==id);items.unshift(id);write(KEY_RECENT,items.slice(0,12));render();}
 function togglePin(id){if(!id)return;let items=read(KEY_PINS);items=items.includes(id)?items.filter(x=>x!==id):[id,...items];write(KEY_PINS,items.slice(0,40));render();syncPinButton();}
 function remove(k,id){write(k,read(k).filter(x=>x!==id));render();syncPinButton();}
 function rows(items,k){return items.length?items.map(id=>`<div class="bi-session-row"><a href="${href(id)}">${String(titleFor(id)).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}<div class="sub">${id}</div></a><button type="button" data-rm="${k}" data-id="${id}" title="Remove">×</button></div>`).join(''):'<div class="sub">None yet.</div>'}
 const toggle=document.createElement('button');toggle.id='bi-session-toggle';toggle.type='button';toggle.textContent='Research Session';document.body.appendChild(toggle);
 const panel=document.createElement('aside');panel.id='bi-session';panel.innerHTML='<div class="bi-session-head"><strong>Research Session</strong><button type="button" id="bi-session-close">Close</button></div><div class="sub">Browser-local convenience state only. Pins and history do not change BlackIndex evidence.</div><div id="bi-session-body"></div>';document.body.appendChild(panel);
 toggle.onclick=()=>document.body.classList.toggle('bi-session-open');panel.querySelector('#bi-session-close').onclick=()=>document.body.classList.remove('bi-session-open');
 function render(){const body=panel.querySelector('#bi-session-body');body.innerHTML=`<div class="bi-session-section"><b>Pinned records</b><div class="bi-session-list">${rows(read(KEY_PINS),KEY_PINS)}</div></div><div class="bi-session-section"><b>Recent records</b><div class="bi-session-list">${rows(read(KEY_RECENT),KEY_RECENT)}</div></div>`;body.querySelectorAll('[data-rm]').forEach(b=>b.onclick=()=>remove(b.dataset.rm,b.dataset.id));}
 function syncPinButton(){const id=currentId();const tools=document.querySelector('.bi-record-tools');if(!id||!tools)return;let b=tools.querySelector('[data-bi-pin]');if(!b){b=document.createElement('button');b.type='button';b.dataset.biPin='1';b.onclick=()=>togglePin(currentId());tools.insertBefore(b,tools.firstChild)}const active=read(KEY_PINS).includes(id);b.textContent=active?'Unpin record':'Pin record';b.classList.toggle('bi-pin-active',active)}
 let last=null;function observe(){const id=currentId();if(id&&id!==last){last=id;touchRecent(id)}syncPinButton()}
 const view=document.getElementById('view');if(view)new MutationObserver(observe).observe(view,{childList:true,subtree:true});window.addEventListener('hashchange',()=>setTimeout(observe,0));
 document.addEventListener('keydown',e=>{const tag=(e.target.tagName||'').toLowerCase();if(tag==='input'||tag==='textarea'||tag==='select')return;if(e.key==='p'||e.key==='P'){if(currentId()){e.preventDefault();togglePin(currentId())}}});
 render();observe();
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
        print(f"Research session already injected: {path}")
        return 0
    pos = text.lower().rfind("</body>")
    text = text[:pos] + BLOCK + text[pos:] if pos >= 0 else text + BLOCK
    path.write_text(text, encoding="utf-8")
    print(f"Dashboard browser-local research session injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
