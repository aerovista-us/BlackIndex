#!/usr/bin/env python3
"""Inject the local AI research assistant panel into the BlackIndex dashboard."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_AI_RESEARCH -->"

STYLE = r'''
<!-- BLACKINDEX_AI_RESEARCH -->
<style>
#bi-ai-panel{margin:10px 0 14px;padding:12px;border:1px solid var(--line);border-radius:9px;background:#11171d}
#bi-ai-panel .bi-ai-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}
#bi-ai-panel .bi-ai-title{font-weight:700}
#bi-ai-panel .bi-ai-status{font-size:12px;color:var(--muted)}
#bi-ai-panel .bi-ai-actions{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0}
#bi-ai-panel button,#bi-ai-panel select,#bi-ai-panel input{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:7px 9px}
#bi-ai-panel button{cursor:pointer;font-weight:600}
#bi-ai-panel button:hover{border-color:#687887}
#bi-ai-panel button:disabled{opacity:.5;cursor:wait}
#bi-ai-panel .bi-ai-ask{display:grid;grid-template-columns:1fr auto auto;gap:7px;margin-top:8px}
#bi-ai-panel .bi-ai-ask input{min-width:0;width:100%}
#bi-ai-panel .bi-ai-result{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
#bi-ai-panel .bi-ai-result pre{white-space:pre-wrap;word-break:break-word;max-height:520px;overflow:auto;background:#0c1116;border:1px solid var(--line);border-radius:7px;padding:11px}
#bi-ai-panel .bi-ai-meta{font-size:12px;color:var(--muted);margin:6px 0}
#bi-ai-panel .bi-ai-warning{font-size:12px;color:var(--warn);margin-top:6px}
#bi-ai-panel .bi-ai-copy{margin-top:7px}
@media(max-width:760px){#bi-ai-panel .bi-ai-ask{grid-template-columns:1fr 1fr}.bi-ai-ask input{grid-column:1/-1}}
</style>
'''

SCRIPT = r'''
<script>
(()=>{
  let aiState=null, aiBusy=false;
  async function loadAiStatus(){
    try{
      const r=await fetch('/api/ai/status',{cache:'no-store'});
      aiState=await r.json();
    }catch(e){aiState={available:false,error:String(e)}}
    return aiState;
  }
  function sourceSelection(){
    const sel=window.getSelection();
    if(!sel||!sel.rangeCount)return '';
    const view=document.getElementById('view');
    if(!view||!view.contains(sel.anchorNode)||!view.contains(sel.focusNode))return '';
    return sel.toString().trim();
  }
  function coverageText(c){
    if(!c)return '';
    const ranges=(c.line_ranges||[]).map(x=>`L${x[0]}-L${x[1]}`).join(', ');
    const scope=c.complete?'complete source coverage':`sampled ${c.chunks_used} of ${c.chunks_total} chunks`;
    return [scope,ranges].filter(Boolean).join(' · ');
  }
  function setBusy(panel,on,label='Working…'){
    aiBusy=on;
    panel.querySelectorAll('button').forEach(b=>b.disabled=on);
    const s=panel.querySelector('[data-ai-status]');
    if(on)s.textContent=label;
    else if(aiState&&aiState.available)s.textContent=`Local AI ready · fast ${aiState.fast_model} · deep ${aiState.deep_model}`;
  }
  function renderResult(panel,payload){
    const box=panel.querySelector('[data-ai-result]');
    const pre=box.querySelector('pre');
    const meta=box.querySelector('[data-ai-meta]');
    const warn=box.querySelector('[data-ai-warning]');
    pre.textContent=payload.answer||'';
    const c=payload.citation_check||{};
    meta.textContent=`${payload.notice||'AI-derived research aid — not evidence'} · model ${payload.model||'unknown'} · ${coverageText(payload.coverage)}`;
    const problems=[];
    if(!c.citations_found)problems.push('No source-line citations were produced.');
    if(c.invalid_citations&&c.invalid_citations.length)problems.push('Out-of-range citations: '+c.invalid_citations.join(', '));
    warn.textContent=problems.join(' ');
    box.hidden=false;
    box.querySelector('[data-ai-copy]').onclick=()=>navigator.clipboard.writeText(pre.textContent).catch(()=>{});
  }
  async function runAi(panel,action,depth){
    if(aiBusy||!current)return;
    if(!aiState)await loadAiStatus();
    if(!aiState||!aiState.available){
      panel.querySelector('[data-ai-status]').textContent='Local AI unavailable';
      return;
    }
    const body={action,doc_id:current.metadata.doc_id,depth};
    if(action==='section_summary'){
      if(tab!=='text'){
        panel.querySelector('[data-ai-status]').textContent='Open the Source text tab, select text, then try again.';
        return;
      }
      const selection=sourceSelection();
      if(!selection){
        panel.querySelector('[data-ai-status]').textContent='Select source text first.';
        return;
      }
      body.selection=selection;
    }
    if(action==='ask'){
      const q=panel.querySelector('[data-ai-question]').value.trim();
      if(!q){
        panel.querySelector('[data-ai-status]').textContent='Enter a question first.';
        return;
      }
      body.question=q;
    }
    setBusy(panel,true,action==='summary'?'Summarizing source…':action==='ask'?'Searching source + answering…':'Summarizing selected source…');
    try{
      const r=await fetch('/api/ai/research',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(body),
      });
      const data=await r.json();
      if(!r.ok||!data.ok)throw new Error(data.error||`HTTP ${r.status}`);
      renderResult(panel,data.result);
    }catch(e){
      const box=panel.querySelector('[data-ai-result]');
      box.hidden=false;
      box.querySelector('pre').textContent='AI request failed: '+String(e.message||e);
      box.querySelector('[data-ai-meta]').textContent='No evidence state was changed.';
      box.querySelector('[data-ai-warning]').textContent='';
    }finally{setBusy(panel,false)}
  }
  function injectAiPanel(){
    if(!current)return;
    const view=document.getElementById('view');
    if(!view||view.querySelector('#bi-ai-panel'))return;
    const anchor=view.querySelector('.bi-record-tools')||view.querySelector('pre');
    if(!anchor)return;
    const panel=document.createElement('section');
    panel.id='bi-ai-panel';
    panel.innerHTML=`
      <div class="bi-ai-head">
        <div><div class="bi-ai-title">AI Research Assistant</div><div class="bi-ai-status" data-ai-status>Checking local AI…</div></div>
        <div class="bi-ai-status">Derived learning aid only · never promoted to evidence</div>
      </div>
      <div class="bi-ai-actions">
        <button type="button" data-ai-summary="quick">Quick Summary</button>
        <button type="button" data-ai-summary="deep">Deep Summary</button>
        <button type="button" data-ai-selection>Summarize Selection</button>
      </div>
      <div class="bi-ai-ask">
        <input type="text" data-ai-question maxlength="2000" placeholder="Ask this document…">
        <select data-ai-depth><option value="quick">Quick</option><option value="deep">Deep</option></select>
        <button type="button" data-ai-ask>Ask</button>
      </div>
      <div class="bi-ai-result" data-ai-result hidden>
        <div class="bi-ai-meta" data-ai-meta></div>
        <pre></pre>
        <div class="bi-ai-warning" data-ai-warning></div>
        <button type="button" class="bi-ai-copy" data-ai-copy>Copy result</button>
      </div>`;
    anchor.parentNode.insertBefore(panel,anchor.nextSibling);
    panel.querySelector('[data-ai-summary="quick"]').onclick=()=>runAi(panel,'summary','quick');
    panel.querySelector('[data-ai-summary="deep"]').onclick=()=>runAi(panel,'summary','deep');
    panel.querySelector('[data-ai-selection]').onclick=()=>runAi(panel,'section_summary',panel.querySelector('[data-ai-depth]').value);
    panel.querySelector('[data-ai-ask]').onclick=()=>runAi(panel,'ask',panel.querySelector('[data-ai-depth]').value);
    panel.querySelector('[data-ai-question]').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();panel.querySelector('[data-ai-ask]').click()}});
    loadAiStatus().then(s=>{
      const el=panel.querySelector('[data-ai-status]');
      el.textContent=s&&s.available?`Local AI ready · fast ${s.fast_model} · deep ${s.deep_model}`:'Local AI unavailable';
    });
  }
  const previousRenderView=renderView;
  renderView=function(){previousRenderView();injectAiPanel()};
  setTimeout(injectAiPanel,0);
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
        print(f"AI research layer already present: {path}")
        return 0
    head = text.lower().find("</head>")
    text = text[:head] + STYLE + text[head:] if head >= 0 else STYLE + text
    body = text.lower().rfind("</body>")
    text = text[:body] + SCRIPT + text[body:] if body >= 0 else text + SCRIPT
    path.write_text(text, encoding="utf-8")
    print(f"Dashboard AI research layer injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
