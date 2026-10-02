#!/usr/bin/env python3
"""Inject shared contextual help, tips, and guided tours into BlackIndex UIs."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_CONTEXT_HELP -->"

STYLE = r'''
<!-- BLACKINDEX_CONTEXT_HELP -->
<style>
:root{--bi-help-bg:#10161c;--bi-help-p:#171f27;--bi-help-p2:#202a34;--bi-help-t:#e7edf3;--bi-help-m:#91a2b1;--bi-help-l:#34414d;--bi-help-a:#bfd3e1;--bi-help-w:#d7b77b}
#bi-help-open,#bi-tip-open{position:fixed;right:18px;z-index:9994;border:1px solid var(--bi-help-l);background:var(--bi-help-p2);color:var(--bi-help-t);border-radius:999px;padding:9px 13px;font:600 12px system-ui,Segoe UI,sans-serif;box-shadow:0 8px 28px #0007;cursor:pointer}
#bi-help-open{bottom:18px}#bi-tip-open{bottom:60px}
body.bi-help-page-evidence #bi-help-open{bottom:112px}
body.bi-help-page-evidence #bi-tip-open{bottom:154px}
#bi-help-open:hover,#bi-tip-open:hover{border-color:#7890a2;background:#293744}
.bi-inline-help{display:inline-flex;align-items:center;justify-content:center;width:21px;height:21px;margin-left:7px;border:1px solid var(--bi-help-l);border-radius:50%;background:transparent;color:var(--bi-help-a);font:700 11px system-ui;cursor:pointer;vertical-align:middle}
.bi-inline-help:hover{background:var(--bi-help-p2)}
#bi-help-overlay{position:fixed;inset:0;z-index:10000;background:#05080cb8;display:none;align-items:center;justify-content:center;padding:18px}
body.bi-help-visible #bi-help-overlay{display:flex}
#bi-help-dialog{width:min(920px,96vw);max-height:90vh;overflow:hidden;background:var(--bi-help-bg);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:14px;box-shadow:0 22px 70px #000c;display:grid;grid-template-rows:auto auto 1fr}
#bi-help-head{display:flex;gap:12px;align-items:flex-start;padding:16px 18px;border-bottom:1px solid var(--bi-help-l)}
#bi-help-head h2{margin:0 0 3px;font-size:19px}#bi-help-head .muted{color:var(--bi-help-m);font-size:12px}
#bi-help-close{margin-left:auto;background:transparent;color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:7px;padding:7px 10px;cursor:pointer}
#bi-help-tools{display:flex;gap:8px;flex-wrap:wrap;padding:11px 18px;border-bottom:1px solid var(--bi-help-l)}
#bi-help-tools input{flex:1;min-width:220px;background:var(--bi-help-p);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:7px;padding:8px 10px}
#bi-help-tools button{background:var(--bi-help-p2);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:7px;padding:8px 10px;cursor:pointer}
#bi-help-body{overflow:auto;padding:16px 18px 24px}
.bi-help-section{margin:0 0 18px}.bi-help-section h3{margin:0 0 8px;font-size:15px}
.bi-help-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:9px}
.bi-help-card{background:var(--bi-help-p);border:1px solid var(--bi-help-l);border-radius:9px;padding:11px}
.bi-help-card strong{display:block;margin-bottom:4px}.bi-help-card p{margin:0;color:var(--bi-help-m)}
.bi-help-card code,.bi-help-kbd{color:#c9dde9}
.bi-help-kbd{display:inline-block;border:1px solid #526270;border-bottom-width:2px;border-radius:4px;padding:1px 5px;background:#222c35;font-size:11px}
.bi-help-note{border-left:3px solid var(--bi-help-w);background:#191914;padding:9px 11px;border-radius:0 7px 7px 0;margin:10px 0;color:#d8d1bb}
#bi-help-hint{position:fixed;left:18px;bottom:18px;z-index:9993;max-width:360px;background:var(--bi-help-bg);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:10px;padding:11px 12px;box-shadow:0 10px 32px #0009;font:13px/1.4 system-ui,Segoe UI,sans-serif}
#bi-help-hint button{margin-left:7px;background:transparent;color:var(--bi-help-a);border:0;cursor:pointer;font-weight:700}
#bi-tip-toast{position:fixed;right:18px;bottom:104px;z-index:9995;width:min(390px,calc(100vw - 36px));background:var(--bi-help-bg);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:10px;padding:12px;box-shadow:0 12px 36px #000a;display:none}
body.bi-tip-visible #bi-tip-toast{display:block}#bi-tip-toast strong{display:block;margin-bottom:4px}#bi-tip-toast .muted{color:var(--bi-help-m)}
#bi-tip-toast button{margin-top:8px;margin-right:5px;background:var(--bi-help-p2);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:6px;padding:6px 8px;cursor:pointer}
#bi-tour-shade{position:fixed;inset:0;z-index:10010;display:none;pointer-events:none;background:#0008}
body.bi-tour-active #bi-tour-shade{display:block}
.bi-tour-target{position:relative!important;z-index:10011!important;box-shadow:0 0 0 4px #a7cbe2,0 0 0 9999px #0008!important;border-radius:8px}
#bi-tour-card{position:fixed;z-index:10012;display:none;width:min(360px,calc(100vw - 30px));background:var(--bi-help-bg);color:var(--bi-help-t);border:1px solid #7890a2;border-radius:11px;padding:12px;box-shadow:0 16px 44px #000c}
body.bi-tour-active #bi-tour-card{display:block}
#bi-tour-card strong{display:block;margin-bottom:5px}#bi-tour-card p{margin:0;color:var(--bi-help-m)}
#bi-tour-card .actions{display:flex;gap:6px;justify-content:flex-end;margin-top:10px}
#bi-tour-card button{background:var(--bi-help-p2);color:var(--bi-help-t);border:1px solid var(--bi-help-l);border-radius:6px;padding:6px 8px;cursor:pointer}
@media(max-width:700px){#bi-help-open,#bi-tip-open{right:10px}#bi-help-open{bottom:10px}#bi-tip-open{bottom:52px}body.bi-help-page-evidence #bi-help-open{bottom:104px}body.bi-help-page-evidence #bi-tip-open{bottom:146px}#bi-help-overlay{padding:7px}#bi-help-dialog{max-height:96vh}.bi-help-grid{grid-template-columns:1fr}#bi-help-hint{left:10px;right:10px;bottom:100px;max-width:none}}
</style>
'''

SCRIPT = r'''
<script>
(()=>{
  if(window.__blackindexContextHelp)return;
  window.__blackindexContextHelp=true;

  const path=(location.pathname.split('/').pop()||'blackindex-dashboard.html').toLowerCase();
  const pageKey=path.includes('work-queue')?'work':
    path.includes('named-source')?'named':
    path.includes('source-lineage')?'lineage':
    path.includes('entities')?'entities':'evidence';

  const common={
    evidence:{
      title:'Evidence Map',
      subtitle:'Find, inspect, learn from, and cite preserved records.',
      steps:[
        ['Find a record','Use search, source filters, or the quick status filters. Press / to jump to search.'],
        ['Inspect the record','Review = extraction/research state. Source Text = normalized source. Metadata = provenance and identifiers.'],
        ['Use AI carefully','Quick Summary and Ask are grounded learning aids. Click a [L…] citation to inspect the exact source lines.'],
        ['Keep evidence separate','AI/extractive help never promotes a claim into Canon or durable evidence automatically.']
      ],
      tips:[
        'Press 1, 2, or 3 to jump between Review, Source Text, and Metadata.',
        'Click an AI [L…] citation to jump directly to the cited normalized source lines.',
        'Timeline and People & Organizations are instant extractive scans in Quick mode; choose Deep for AI synthesis.',
        'Use the URL hash/bookmark behavior to return to a selected record and tab.',
        'Search works across metadata, extraction text, source text, and integrity context.',
        'If a summary says “sampled,” treat it as orientation—not an exhaustive reading of the whole document.'
        'Compare Two Documents: the open record is A; choose B, optionally enter a focus, then use Quick for a focused extractive alignment or Deep for broader multi-window source alignment with A/B citations.',
      ],
      topics:[
        ['Search & filter','Search matches record metadata and text. Source and status controls narrow the corpus without changing evidence state.'],
        ['Review / Text / Metadata','Review shows research/extraction context. Text shows normalized source. Metadata exposes provenance, collection, SHA, dates, and record identifiers.'],
        ['AI Research Assistant','Quick Summary, Deep Summary, Summarize Selection, Ask This Document, Timeline, People & Organizations, Explain Simply, and Compare Two Documents all operate as research aids.'],
        ['Clickable citations','AI citations like [L172-L180] switch to Source Text, scroll to the range, and highlight it. Always inspect the source when a point matters.'],
        ['Research session / export','Browser-local research tools let you collect working context without silently mutating durable evidence objects.'],
        ['Resume FBI Review','This opens the controlled review workflow. It does not auto-promote candidate records.']
      ],
      tour:[
        ['header','Search and navigation','Start here to search the corpus, filter records, and jump to the specialized BlackIndex views.'],
        ['#list','Record list','Select a record here. Search and filters change this list but do not alter evidence.'],
        ['#view','Record workspace','The selected record opens here with Review, Source Text, Metadata, research tools, and AI help.'],
        ['#bi-utility','Quick controls','These controls expose workflow filters, sorting, shortcuts, and the review-resume action.']
      ]
    },
    work:{
      title:'Work Queue',
      subtitle:'See unresolved workflow state without confusing backlog with evidence.',
      steps:[
        ['Filter the queue','Use search plus the section selector to isolate drift, FBI review, lineage, missing evidence, or unreviewed records.'],
        ['Open the underlying record','Document links return you to the Evidence Map with the record selected.'],
        ['Read labels as workflow','Unreviewed, HOLD, missing, drift, and cross-reference are process states—not historical conclusions.'],
        ['Work one queue at a time','Narrow to a section and clear it deliberately instead of treating the whole page as one priority ranking.']
      ],
      tips:[
        'Press / to focus the queue search.',
        'Use the section dropdown before text search when you already know the type of work you want.',
        'Review-state drift means metadata and extraction state disagree; it does not mean the research is wrong.',
        'Missing-evidence objects identify access/recovery gaps, not proof that a record was destroyed or withheld.',
        'FBI PROMOTE still goes through the separate fail-closed child-record promotion workflow.'
      ],
      topics:[
        ['Review-state drift','Shows records where metadata status and extraction/review activity are out of sync.'],
        ['FBI P0 review','Shows local reviewer dispositions such as PROMOTE, HOLD, MERGE, and REJECT-BOUNDARY.'],
        ['Lineage review','Pairs recognized together in research notes that still need an explicit dependency judgment.'],
        ['Missing evidence','Durable gaps or unresolved source references. A gap is represented explicitly rather than filled by inference.'],
        ['Unreviewed metadata','Records still marked unreviewed; use drift context to distinguish untouched records from status lag.']
      ],
      tour:[
        ['header','Filter unresolved work','Search or narrow to one queue section.'],
        ['.cards','Queue counters','These are workflow counts, not importance or truth scores.'],
        ['.caution','Evidence boundary','This reminder explains why queue labels must not be treated as conclusions.'],
        ['.queue-section','Queue sections','Each section represents a different kind of unresolved work.']
      ]
    },
    named:{
      title:'Named Source Recovery',
      subtitle:'Recover referenced records without mistaking a citation hit for the underlying record.',
      steps:[
        ['Choose a named target','Each target corresponds to an upstream record or reference we are trying to recover.'],
        ['Inspect candidate classes','Citation/synthesis hits and release-container hits are different kinds of leads.'],
        ['Verify boundaries visually','Text-page indices guide review; they are not automatically verified physical PDF pages.'],
        ['Promote only after proof','A child record needs provenance, boundary, physical-page, and visual confirmation before promotion.']
      ],
      tips:[
        'Press / to filter named targets and candidate rows.',
        '“Any candidate hit” can be only a citation inside a synthesis document.',
        'EO 14040 container candidates are stronger navigation leads, but still not recovered child records by themselves.',
        'Use this page to find where to inspect next—not to infer missing-record content.'
      ],
      topics:[
        ['Candidate hit','A text/source occurrence that may help locate the referenced material. It is not proof of full record recovery.'],
        ['Citation-only target','The named source is referenced, but no matching release-container occurrence is yet mapped.'],
        ['EO 14040 candidate','A candidate occurrence exists in an FBI release container; visual boundary review is still required.'],
        ['Physical-page verification','Final page/boundary claims come from source-image review, not text indices alone.']
      ],
      tour:[
        ['header','Named-source workspace','Navigate back to Evidence Map, Work Queue, Lineage, or Entities from here.'],
        ['.caution','Recovery rule','This warning is the key methodological boundary for candidate evidence.'],
        ['.cards','Recovery counts','Use these to understand coverage, not to score evidentiary importance.'],
        ['.target','Target sections','Each section groups candidate material for one named upstream source.']
      ]
    },
    lineage:{
      title:'Source Lineage',
      subtitle:'See which documents depend on shared upstream material.',
      steps:[
        ['Start with encoded edges','These are explicit durable dependency or parent-container relationships.'],
        ['Check independence','Dependent and partially-independent labels help prevent double-counting repeated evidence.'],
        ['Inspect shared families','Multiple documents can repeat the same upstream material without becoming independent corroboration.'],
        ['Review candidate pairs separately','Research-note co-occurrence is only a review queue until dependency is explicitly encoded.']
      ],
      tips:[
        'A missing dependency edge means “not yet encoded,” not “independent.”',
        'Two official reports can still be dependent if both summarize the same FBI/CIA records.',
        'Use shared lineage families before counting repeated statements as corroboration.',
        'Research cross-references are candidates for lineage review—not proof of agreement or contradiction.'
      ],
      topics:[
        ['Encoded dependency edge','A durable relationship saying one source depends on another or belongs to a parent-container chain.'],
        ['Dependent','The source relies materially on the same upstream evidence as another source.'],
        ['Partially independent','Some evidentiary basis overlaps, while some source material is distinct.'],
        ['Shared upstream family','A grouped view of sources tracing back to common upstream evidence.'],
        ['Research pair','Two documents recognized together in research notes; dependency still requires human review.']
      ],
      tour:[
        ['header','Lineage purpose','This page is for source genealogy—not judging historical truth.'],
        ['.cards','Lineage counters','See nodes, edges, shared families, dependence, and pending review at a glance.'],
        ['.families','Shared upstream families','Use these to spot repeated evidence traveling through multiple documents.'],
        ['table','Dependency detail','Tables show encoded relationships and candidate review pairs.']
      ]
    },
    entities:{
      title:'Entities',
      subtitle:'Browse explicit people/organization identities and relationships without guilt-by-association.',
      steps:[
        ['Search an entity','Search names, aliases, document IDs, types, or other indexed identity text.'],
        ['Filter by type','Use the entity-type selector to narrow the index.'],
        ['Open relationship details','Each entity card can expose encoded mentions or genealogy relationships.'],
        ['Follow back to source records','Document mentions mean the entity is explicitly listed there—not that a claim about conduct is proven.']
      ],
      tips:[
        'Press / to focus entity search.',
        'A document mention means explicit presence in durable metadata, nothing more.',
        'Genealogy edges preserve identity/family structure only; they do not transfer conduct or culpability.',
        'Use aliases to find the same person/entity across differently named records.'
      ],
      topics:[
        ['Entity card','Shows canonical identity, type, aliases, mention counts, relationships, and source references.'],
        ['Document mention','The entity is explicitly listed in durable metadata for that record.'],
        ['Genealogy edge','An encoded identity/family relationship; it carries no implication of wrongdoing or ideology.'],
        ['Aliases','Alternate names used to resolve identity across records.']
      ],
      tour:[
        ['header','Find an entity','Search or filter the entity index from here.'],
        ['.cards','Index counters','These summarize indexed entities and edge types.'],
        ['.caution','Association boundary','Read this before interpreting document mentions or family relationships.'],
        ['.entities','Entity cards','Open a card to inspect aliases, mentions, and encoded relationships.']
      ]
    }
  };

  const data=common[pageKey];
  document.body.classList.add('bi-help-page-'+pageKey);
  const $=(s,r=document)=>r.querySelector(s);
  const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  function cards(items,cls=''){
    return '<div class="bi-help-grid">'+items.map(([a,b])=>'<div class="bi-help-card '+cls+'" data-help-search="'+esc((a+' '+b).toLowerCase())+'"><strong>'+esc(a)+'</strong><p>'+esc(b)+'</p></div>').join('')+'</div>';
  }

  const helpBtn=document.createElement('button');
  helpBtn.id='bi-help-open'; helpBtn.type='button'; helpBtn.textContent='How to'; helpBtn.title='Open BlackIndex help (H)';
  document.body.appendChild(helpBtn);

  const tipBtn=document.createElement('button');
  tipBtn.id='bi-tip-open'; tipBtn.type='button'; tipBtn.textContent='Tips'; tipBtn.title='Show a quick tip';
  document.body.appendChild(tipBtn);

  const overlay=document.createElement('div');
  overlay.id='bi-help-overlay';
  overlay.innerHTML='<div id="bi-help-dialog" role="dialog" aria-modal="true" aria-labelledby="bi-help-title">'+
    '<div id="bi-help-head"><div><h2 id="bi-help-title">'+esc(data.title)+' · How to</h2><div class="muted">'+esc(data.subtitle)+'</div></div><button id="bi-help-close" type="button">Close</button></div>'+
    '<div id="bi-help-tools"><input id="bi-help-search" placeholder="Search help: AI, citations, missing evidence, shortcuts…"><button type="button" id="bi-help-tour">Show me around</button><button type="button" id="bi-help-tip-from-panel">Quick tip</button></div>'+
    '<div id="bi-help-body">'+
      '<section class="bi-help-section"><h3>Start here</h3>'+cards(data.steps)+'</section>'+
      '<section class="bi-help-section"><h3>How this page works</h3>'+cards(data.topics)+'</section>'+
      '<section class="bi-help-section"><h3>Tips & tricks</h3>'+cards(data.tips.map((x,i)=>['Tip '+(i+1),x]))+'</section>'+
      '<section class="bi-help-section"><h3>Keyboard / fast navigation</h3>'+
        '<div class="bi-help-card" data-help-search="keyboard shortcuts search help escape"><strong>Universal shortcuts</strong><p><span class="bi-help-kbd">H</span> help · <span class="bi-help-kbd">/</span> search when supported · <span class="bi-help-kbd">Esc</span> close help/tips/tour or clear focused search.</p></div>'+
        (pageKey==='evidence'?'<div class="bi-help-card" data-help-search="1 2 3 review text metadata j k"><strong>Evidence Map shortcuts</strong><p><span class="bi-help-kbd">1</span>/<span class="bi-help-kbd">2</span>/<span class="bi-help-kbd">3</span> Review/Text/Metadata · <span class="bi-help-kbd">J</span>/<span class="bi-help-kbd">K</span> next/previous record.</p></div>':'')+
      '</section>'+
      '<div class="bi-help-note">Help text explains workflow and interpretation. It does not change evidence state, source content, or review decisions.</div>'+
    '</div></div>';
  document.body.appendChild(overlay);

  const toast=document.createElement('div');
  toast.id='bi-tip-toast';
  toast.innerHTML='<strong>Tip</strong><div class="muted" id="bi-tip-text"></div><div><button type="button" id="bi-tip-next">Another tip</button><button type="button" id="bi-tip-close">Close</button></div>';
  document.body.appendChild(toast);

  const shade=document.createElement('div'); shade.id='bi-tour-shade'; document.body.appendChild(shade);
  const tour=document.createElement('div'); tour.id='bi-tour-card';
  tour.innerHTML='<strong id="bi-tour-title"></strong><p id="bi-tour-text"></p><div class="actions"><button type="button" id="bi-tour-exit">Exit</button><button type="button" id="bi-tour-prev">Back</button><button type="button" id="bi-tour-next">Next</button></div>';
  document.body.appendChild(tour);

  function openHelp(topic=''){
    document.body.classList.add('bi-help-visible');
    const input=$('#bi-help-search');
    input.value=topic||''; filterHelp();
    setTimeout(()=>input.focus(),0);
  }
  function closeHelp(){document.body.classList.remove('bi-help-visible')}
  function filterHelp(){
    const q=$('#bi-help-search').value.trim().toLowerCase();
    $$('.bi-help-card',$('#bi-help-body')).forEach(card=>{
      card.style.display=!q||card.dataset.helpSearch.includes(q)||card.textContent.toLowerCase().includes(q)?'block':'none';
    });
    $$('.bi-help-section',$('#bi-help-body')).forEach(sec=>{
      const visible=$$('.bi-help-card',sec).some(c=>c.style.display!=='none');
      sec.style.display=visible?'block':'none';
    });
  }

  let tipIndex=Number(localStorage.getItem('blackindex-tip-index-'+pageKey)||0);
  function showTip(){
    const tips=data.tips; if(!tips.length)return;
    $('#bi-tip-text').textContent=tips[tipIndex%tips.length];
    localStorage.setItem('blackindex-tip-index-'+pageKey,String((tipIndex+1)%tips.length));
    tipIndex=(tipIndex+1)%tips.length;
    document.body.classList.add('bi-tip-visible');
  }
  function closeTip(){document.body.classList.remove('bi-tip-visible')}

  let tourIndex=0,tourTarget=null;
  function positionTour(el){
    const r=el.getBoundingClientRect(),card=tour;
    const cw=Math.min(360,window.innerWidth-30), gap=12;
    let top=r.bottom+gap,left=Math.max(15,Math.min(window.innerWidth-cw-15,r.left));
    if(top+220>window.innerHeight)top=Math.max(15,r.top-230);
    card.style.width=cw+'px';card.style.top=top+'px';card.style.left=left+'px';
  }
  function tourStep(index){
    if(tourTarget)tourTarget.classList.remove('bi-tour-target');
    const steps=data.tour.filter(x=>document.querySelector(x[0]));
    if(!steps.length)return stopTour();
    tourIndex=Math.max(0,Math.min(index,steps.length-1));
    const [selector,title,text]=steps[tourIndex],el=document.querySelector(selector);
    if(!el)return tourStep(tourIndex+1);
    tourTarget=el;el.classList.add('bi-tour-target');el.scrollIntoView({block:'center',behavior:'smooth'});
    $('#bi-tour-title').textContent=(tourIndex+1)+' / '+steps.length+' · '+title;
    $('#bi-tour-text').textContent=text;
    $('#bi-tour-prev').disabled=tourIndex===0;
    $('#bi-tour-next').textContent=tourIndex===steps.length-1?'Done':'Next';
    setTimeout(()=>positionTour(el),220);
  }
  function startTour(){closeHelp();closeTip();document.body.classList.add('bi-tour-active');tourStep(0)}
  function stopTour(){if(tourTarget)tourTarget.classList.remove('bi-tour-target');tourTarget=null;document.body.classList.remove('bi-tour-active')}
  function nextTour(){
    const steps=data.tour.filter(x=>document.querySelector(x[0]));
    if(tourIndex>=steps.length-1)stopTour();else tourStep(tourIndex+1);
  }

  helpBtn.onclick=()=>openHelp();
  tipBtn.onclick=showTip;
  $('#bi-help-close').onclick=closeHelp;
  $('#bi-help-search').oninput=filterHelp;
  $('#bi-help-tour').onclick=startTour;
  $('#bi-help-tip-from-panel').onclick=()=>{closeHelp();showTip()};
  $('#bi-tip-next').onclick=showTip;$('#bi-tip-close').onclick=closeTip;
  $('#bi-tour-exit').onclick=stopTour;$('#bi-tour-prev').onclick=()=>tourStep(tourIndex-1);$('#bi-tour-next').onclick=nextTour;
  overlay.addEventListener('click',e=>{if(e.target===overlay)closeHelp()});

  const contextual={
    evidence:[['.bi-ai-title','AI'],['.tabs','Review Text Metadata']],
    work:[['.queue-section h2','queue']],
    named:[['.caution strong','candidate'],['.target h2','candidate']],
    lineage:[['h2','lineage']],
    entities:[['h2','entity']]
  };
  function applyContextualHelp(){
    (contextual[pageKey]||[]).forEach(([selector,topic])=>{
      $$(selector).slice(0,8).forEach(el=>{
        if(el.querySelector&&el.querySelector('.bi-inline-help'))return;
        const b=document.createElement('button');b.type='button';b.className='bi-inline-help';b.textContent='?';b.title='Explain this section';
        b.onclick=e=>{e.preventDefault();e.stopPropagation();openHelp(topic)};
        el.appendChild(b);
      });
    });
  }
  applyContextualHelp();
  if(pageKey==='evidence'){
    const view=$('#view');
    if(view)new MutationObserver(()=>applyContextualHelp()).observe(view,{childList:true,subtree:true});
  }

  const titles={
    'Evidence Map':'Browse all ingested records and their research context.',
    'Work Queue':'See unresolved workflow/review states.',
    'Named Sources':'Recover referenced upstream records without guessing boundaries.',
    'Lineage':'Inspect source dependency and independence.',
    'Source Lineage':'Inspect source dependency and independence.',
    'Entities':'Browse explicitly indexed identities and relationships.',
    'Clear':'Clear the current filter/search.'
  };
  $$('a,button').forEach(el=>{const t=el.textContent.trim();if(titles[t]&&!el.title)el.title=titles[t]});

  if(pageKey==='evidence'){
    const old=$('#bi-help-btn');
    if(old)old.title='Keyboard shortcuts; use How to for the full guide';
  }

  document.addEventListener('keydown',e=>{
    const typing=/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName||'');
    if((e.key==='h'||e.key==='H')&&!typing&&!e.ctrlKey&&!e.metaKey&&!e.altKey){e.preventDefault();openHelp()}
    if(e.key==='Escape'){
      if(document.body.classList.contains('bi-tour-active')){stopTour();return}
      if(document.body.classList.contains('bi-help-visible')){closeHelp();return}
      if(document.body.classList.contains('bi-tip-visible')){closeTip();return}
    }
  });

  if(!localStorage.getItem('blackindex-help-hint-v1')){
    const hint=document.createElement('div');hint.id='bi-help-hint';
    hint.innerHTML='New help is available: <b>How to</b>, contextual <b>?</b> buttons, quick tips, and guided tours. Press <span class="bi-help-kbd">H</span> anytime.<button type="button">Got it</button>';
    hint.querySelector('button').onclick=()=>{localStorage.setItem('blackindex-help-hint-v1','1');hint.remove()};
    document.body.appendChild(hint);
  }
})();
</script>
'''


def inject(path: Path) -> bool:
    if not path.is_file():
        print(f"skip: not found: {path}", file=sys.stderr)
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Context help already present: {path}")
        return True
    head = text.lower().find("</head>")
    if head >= 0:
        text = text[:head] + STYLE + text[head:]
    else:
        style_at = text.lower().find("<style")
        script_at = text.lower().find("<script")
        at = style_at if style_at >= 0 else script_at if script_at >= 0 else len(text)
        text = text[:at] + STYLE + text[at:]
    body = text.lower().rfind("</body>")
    if body >= 0:
        text = text[:body] + SCRIPT + text[body:]
    else:
        text += SCRIPT
    path.write_text(text, encoding="utf-8")
    print(f"Context help injected: {path}")
    return True


def main() -> int:
    paths = [Path(x) for x in sys.argv[1:]]
    if not paths:
        paths = [
            Path("local/dashboard/blackindex-dashboard.html"),
            Path("local/dashboard/work-queue.html"),
            Path("local/dashboard/named-source-recovery.html"),
            Path("local/dashboard/source-lineage.html"),
            Path("local/dashboard/entities.html"),
        ]
    ok = True
    for path in paths:
        ok = inject(path) and ok
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
