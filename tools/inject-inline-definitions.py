#!/usr/bin/env python3
"""Inject contextual term definitions into generated BlackIndex UI pages."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_INLINE_DEFINITIONS -->"

STYLE = r'''
<!-- BLACKINDEX_INLINE_DEFINITIONS -->
<style>
.bi-defined-label{cursor:help;text-decoration-line:underline;text-decoration-style:dotted;text-decoration-color:#71889a;text-underline-offset:3px}
.bi-defined-control{outline-offset:2px}
.bi-meaning-dot{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;margin-left:5px;padding:0;border:1px solid #536777;border-radius:50%;background:#1b252e;color:#bdd2df;font:700 10px/1 system-ui,Segoe UI,sans-serif;vertical-align:middle;cursor:help}
.bi-meaning-dot:hover,.bi-meaning-dot:focus{background:#2a3b47;border-color:#86a7bd;outline:none}
#bi-meaning-popover{position:fixed;z-index:10030;display:none;width:min(360px,calc(100vw - 24px));background:#10161c;color:#e7edf3;border:1px solid #536777;border-radius:10px;padding:11px 12px;box-shadow:0 14px 44px #000c;font:13px/1.42 system-ui,Segoe UI,sans-serif}
#bi-meaning-popover.bi-visible{display:block}
#bi-meaning-popover strong{display:block;padding-right:24px;font-size:13px}
#bi-meaning-popover .bi-def-cat{margin:2px 0 6px;color:#91a2b1;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
#bi-meaning-popover p{margin:0;color:#d6e0e7}
#bi-meaning-popover .bi-def-close{position:absolute;right:7px;top:6px;border:0;background:transparent;color:#aebfca;cursor:pointer;font-size:16px}
#bi-meaning-popover .bi-def-note{margin-top:7px;padding-top:7px;border-top:1px solid #2c3944;color:#91a2b1;font-size:11px}
.bi-help-glossary .bi-help-card strong{display:flex;align-items:center;gap:5px}
.bi-help-glossary .bi-glossary-cat{font-size:10px;color:#91a2b1;text-transform:uppercase;letter-spacing:.04em;font-weight:500}
@media(max-width:700px){#bi-meaning-popover{width:calc(100vw - 20px)}}
</style>
'''

SCRIPT = r'''
<script>
(()=>{
  if(window.__blackindexInlineDefinitions)return;
  window.__blackindexInlineDefinitions=true;

  const TERMS={
    archive_confidence:{
      label:'Archive confidence',category:'Record integrity',
      definition:'BlackIndex 0–5 measure of the completeness and reconstructability of the accessible archive.',
      note:'It is not a truth score. Missing or destroyed records can lower archive confidence without proving what the missing material contained.'
    },
    completeness:{
      label:'Completeness',category:'Record integrity',
      definition:'BlackIndex 0–5 record-integrity field used to record how complete the accessible documentary record is assessed to be.',
      note:'The project does not assign automatic historical certainty to this number.'
    },
    redaction_concern:{
      label:'Redaction concern',category:'Record integrity',
      definition:'BlackIndex 0–15 record-integrity field for redaction, withholding, or obscured-content concern.',
      note:'A redaction concern is not by itself proof of concealment, wrongdoing, or the content of withheld material.'
    },
    missing_refs:{
      label:'Missing refs',category:'Record integrity',
      definition:'Referenced records or attachments that are not currently mapped or available in the accessible record.',
      note:'A missing reference is an archive/recovery gap, not proof that a record was destroyed, withheld, or contained a particular fact.'
    },
    missing_evidence:{
      label:'Missing evidence',category:'Record integrity',
      definition:'A first-class BlackIndex record of materially absent or unavailable evidence such as referenced documents, attachments, logs, workpapers, or archive gaps.',
      note:'It records the gap and recovery path; it does not invent the missing evidence.'
    },
    unreviewed:{
      label:'Unreviewed',category:'Workflow state',
      definition:'The document metadata has not yet been marked as substantively reviewed.',
      note:'A non-stub extraction may still exist, so “unreviewed” can sometimes represent status lag rather than untouched material.'
    },
    reviewed:{
      label:'Reviewed',category:'Workflow state',
      definition:'A human-reviewed workflow state indicating that the record passed the relevant review step.',
      note:'Reviewed does not mean every claim in the record is true or independently corroborated.'
    },
    evidence_status:{
      label:'Evidence status',category:'Workflow state',
      definition:'Metadata workflow state describing where a document stands in BlackIndex review handling.',
      note:'Evidence status is not a truth score and should not be confused with Canon/Apocrypha research classification.'
    },
    corroborated:{
      label:'Corroborated',category:'Workflow state',
      definition:'Metadata status indicating that review has identified supporting material under the project workflow.',
      note:'Corroboration must still account for source independence; derivative repetition is not independent support.'
    },
    contested:{
      label:'Contested',category:'Workflow state',
      definition:'Metadata status indicating that materially conflicting, disputed, or contrary evidence/context remains relevant.',
      note:'Contested preserves disagreement in the record rather than resolving it automatically.'
    },
    neutral_stub:{
      label:'Neutral review stub',category:'Workflow state',
      definition:'A placeholder extraction/review file with no substantive historical finding yet recorded.',
      note:'Stub status is a workflow condition only.'
    },
    review_state_drift:{
      label:'Review-state drift',category:'Workflow state',
      definition:'Metadata review status and extraction/review activity are out of sync and need reconciliation.',
      note:'Drift does not mean the underlying research conclusion is wrong.'
    },
    promote:{
      label:'PROMOTE',category:'FBI review disposition',
      definition:'Reviewer disposition that a candidate appears eligible to become a distinct child record after required fail-closed provenance and boundary checks.',
      note:'PROMOTE is not self-executing; source-PDF boundary/provenance safeguards still apply.'
    },
    hold:{
      label:'HOLD',category:'FBI review disposition',
      definition:'Potentially useful candidate whose boundary, provenance, content, or source verification still needs work.',
      note:'HOLD is unresolved workflow state, not a negative historical finding.'
    },
    merge:{
      label:'MERGE',category:'FBI review disposition',
      definition:'Reviewer determination that the candidate belongs with another record/candidate rather than standing as a separate child record.',
      note:'This is a record-boundary decision, not a truth judgment.'
    },
    reject_boundary:{
      label:'REJECT-BOUNDARY',category:'FBI review disposition',
      definition:'Reviewer determination that the proposed candidate boundary should not be accepted as a distinct record boundary.',
      note:'This rejects the segmentation boundary, not necessarily the underlying source content.'
    },
    review_required:{
      label:'Review required',category:'Research state',
      definition:'A human review gate remains open before the associated classification, boundary, dependency, or other research state should be treated as settled.',
      note:'BlackIndex uses explicit open gates rather than filling them with inference.'
    },
    dependent:{
      label:'Dependent',category:'Source lineage',
      definition:'The source materially relies on an upstream source, investigation, record, informant, translation, or analytical chain already represented elsewhere.',
      note:'Repeated dependent reporting must not be counted as independent corroboration.'
    },
    partially_independent:{
      label:'Partially independent',category:'Source lineage',
      definition:'The source has some distinct evidentiary basis but also overlaps materially with upstream evidence used by another source.',
      note:'Only the genuinely distinct lineage should contribute independent corroborative weight.'
    },
    independent:{
      label:'Independent',category:'Source lineage',
      definition:'The encoded source lineage is assessed as materially independent of the compared upstream source for the relationship being modeled.',
      note:'Independence is relationship-specific and does not itself establish truth.'
    },
    independence_unknown:{
      label:'Independence unknown',category:'Source lineage',
      definition:'BlackIndex has not established whether the compared sources have independent evidentiary lineage.',
      note:'Unknown must not be silently treated as independent.'
    },
    shared_upstream:{
      label:'Shared upstream family',category:'Source lineage',
      definition:'A group of documents that trace back to common underlying evidence or source lineage.',
      note:'Several documents in one shared family can repeat one evidentiary basis without creating multiple independent proofs.'
    },
    encoded_edge:{
      label:'Encoded dependency edge',category:'Source lineage',
      definition:'A durable BlackIndex relationship recording that one source depends on, derives from, or otherwise traces to another source/container.',
      note:'A missing edge means “not yet encoded,” not automatically “independent.”'
    },
    research_pair:{
      label:'Research pair',category:'Source lineage',
      definition:'Two documents recognized together in research notes and queued for dependency review.',
      note:'Co-occurrence alone does not establish dependence, agreement, contradiction, or corroboration.'
    },
    candidate_hit:{
      label:'Candidate hit',category:'Named-source recovery',
      definition:'A text or source occurrence that may help locate a referenced underlying record.',
      note:'A candidate hit does not prove that the complete cited record or its boundaries have been recovered.'
    },
    citation_only:{
      label:'Citation-only target',category:'Named-source recovery',
      definition:'The named source is localized through a citation or synthesis reference, but no individually mapped release-container record has yet been established.',
      note:'This is localization, not recovery of the underlying record.'
    },
    eo14040_candidate:{
      label:'EO 14040 candidate',category:'Named-source recovery',
      definition:'A candidate occurrence found inside an FBI EO 14040 release container that may help recover the referenced source record.',
      note:'Visual source/boundary verification is still required before child-record promotion.'
    },
    text_page:{
      label:'Text-page index',category:'Named-source recovery',
      definition:'A normalized-text navigation page/index used to localize material during review.',
      note:'It is not automatically the verified physical PDF page number.'
    },
    physical_page:{
      label:'Physical page',category:'Named-source recovery',
      definition:'A page position verified against the original source artifact/PDF image.',
      note:'BlackIndex requires this distinction where page/boundary claims matter.'
    },
    document_mention:{
      label:'Document mention',category:'Entities',
      definition:'The entity is explicitly listed or referenced in durable metadata for a document.',
      note:'A mention does not imply conduct, culpability, ideology, agreement, or relationship beyond what the source actually states.'
    },
    genealogy_edge:{
      label:'Genealogy edge',category:'Entities',
      definition:'An encoded identity/family relationship used to preserve genealogy or identity structure.',
      note:'Relationships do not transfer guilt, conduct, beliefs, or evidentiary weight.'
    },
    alias:{
      label:'Alias',category:'Entities',
      definition:'An alternate name or spelling used to resolve the same entity across sources.',
      note:'Alias matching supports identity resolution; it does not add a substantive claim by itself.'
    },
    ai_sampled:{
      label:'Sampled AI coverage',category:'AI research',
      definition:'Only a subset of the document’s normalized source chunks was supplied to the model for this result.',
      note:'Use sampled output for orientation. It is not an exhaustive review of the entire document.'
    },
    ai_complete:{
      label:'Complete source coverage',category:'AI research',
      definition:'All normalized source chunks for the requested operation were supplied within that AI request’s coverage accounting.',
      note:'Complete input coverage still does not turn AI output into evidence or replace human source review.'
    },
    ai_research_aid:{
      label:'AI-derived research aid',category:'AI research',
      definition:'A local-model explanation, summary, or answer produced from BlackIndex source material for learning/research convenience.',
      note:'It is not evidence and is never automatically promoted into durable BlackIndex evidence state.'
    },
    extractive:{
      label:'Extractive',category:'AI research',
      definition:'The result was produced by deterministic source extraction rather than generative model synthesis.',
      note:'Extractive output is still a navigation/research aid; inspect the cited source lines when the point matters.'
    },
    canon:{
      label:'Canon',category:'Research classification',
      definition:'BlackIndex canonical research state for material accepted into the current working evidentiary model under the project’s review rules.',
      note:'Canon is a research-state decision, not a claim of infallibility. Source history and later transitions remain preserved.'
    },
    field_note:{
      label:'Field note',category:'Research classification',
      definition:'Early or provisional research material preserved for investigation before stronger classification/review is complete.',
      note:'Field notes are not automatically accepted assertions.'
    },
    apocrypha:{
      label:'Apocrypha',category:'Research classification',
      definition:'Preserved material that is disputed, unverified, alternate, or unresolved but still research-relevant.',
      note:'Apocrypha means unresolved/disputed in BlackIndex; it does not mean “false.”'
    },
    pseudepigrapha:{
      label:'Pseudepigrapha',category:'Research classification',
      definition:'Material whose attribution or claimed authorship/source identity is doubtful or unresolved.',
      note:'Attribution confidence is kept separate from whether the underlying content is authentic or accurate.'
    },
    deuterocanon:{
      label:'Deuterocanon',category:'Research classification',
      definition:'Accepted secondary or institutional synthesis retained as useful evidence context while remaining distinct from the underlying primary/source layer.',
      note:'Repeated institutional synthesis must still be checked for shared upstream evidence.'
    },
    fragment:{
      label:'Fragment',category:'Research classification',
      definition:'Partial material preserved because only an incomplete excerpt, portion, or record fragment is available.',
      note:'A fragment should not be silently treated as a complete record.'
    },
    rejected:{
      label:'Rejected',category:'Research classification',
      definition:'Material reviewed and not accepted into the current working evidentiary model for the recorded reason.',
      note:'The preserved source/history remains; rejection is a research-state transition, not deletion.'
    },
    superseded:{
      label:'Superseded',category:'Research classification',
      definition:'A prior research state or target replaced by a newer authoritative representation or workflow state.',
      note:'Superseded material remains historically traceable rather than disappearing.'
    },
    authenticity_status:{
      label:'Authenticity status',category:'Research classification',
      definition:'Assessment of whether the artifact/content itself is authentic or genuine.',
      note:'BlackIndex keeps authenticity separate from attribution so doubtful authorship does not automatically make the content inauthentic.'
    },
    attribution_status:{
      label:'Attribution status',category:'Research classification',
      definition:'Assessment of whether authorship, origin, speaker, creator, or source attribution is correctly identified.',
      note:'Attribution uncertainty is not the same thing as content falsity.'
    },
    provenance_status:{
      label:'Provenance status',category:'Research classification',
      definition:'Assessment of how well the source’s origin, custody, release path, or documentary chain is mapped.',
      note:'Good provenance strengthens traceability; it does not independently prove every claim in the source.'
    },
    corroboration_status:{
      label:'Corroboration status',category:'Research classification',
      definition:'Research note describing how the subject is or is not supported by other evidence.',
      note:'Corroboration must account for source genealogy so derivative repetition is not double-counted.'
    },
    source_independence:{
      label:'Source independence',category:'Research classification',
      definition:'Assessment of whether supporting material comes from genuinely separate evidentiary lineage.',
      note:'Document count is not the same as independent source count.'
    },
    classification_confidence:{
      label:'Classification confidence',category:'Research classification',
      definition:'Optional 0–1 confidence value attached to a BlackIndex research-classification judgment.',
      note:'It expresses confidence in that classification state, not the probability that the historical claim is true.'
    }
  };

  window.BLACKINDEX_GLOSSARY=TERMS;

  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm=s=>String(s??'').trim().replace(/\s+/g,' ').toLowerCase();

  const pop=document.createElement('div');
  pop.id='bi-meaning-popover';
  pop.setAttribute('role','dialog');
  pop.setAttribute('aria-live','polite');
  pop.innerHTML='<button class="bi-def-close" type="button" aria-label="Close definition">×</button><strong></strong><div class="bi-def-cat"></div><p></p><div class="bi-def-note"></div>';
  document.body.appendChild(pop);

  let active=null,pinned=false,hideTimer=null;

  function position(anchor){
    const r=anchor.getBoundingClientRect();
    const width=Math.min(360,window.innerWidth-24);
    let left=Math.max(12,Math.min(window.innerWidth-width-12,r.left));
    let top=r.bottom+8;
    if(top+190>window.innerHeight)top=Math.max(12,r.top-198);
    pop.style.width=width+'px';pop.style.left=left+'px';pop.style.top=top+'px';
  }
  function show(anchor,key,stick=false){
    const d=TERMS[key];if(!d)return;
    clearTimeout(hideTimer);active=anchor;pinned=stick||pinned;
    pop.querySelector('strong').textContent=d.label;
    pop.querySelector('.bi-def-cat').textContent=d.category;
    pop.querySelector('p').textContent=d.definition;
    const note=pop.querySelector('.bi-def-note');note.textContent=d.note||'';note.style.display=d.note?'block':'none';
    pop.classList.add('bi-visible');position(anchor);
  }
  function hide(force=false){
    if(pinned&&!force)return;
    clearTimeout(hideTimer);pop.classList.remove('bi-visible');active=null;
    if(force)pinned=false;
  }
  function scheduleHide(){clearTimeout(hideTimer);hideTimer=setTimeout(()=>hide(false),120)}

  pop.querySelector('.bi-def-close').onclick=()=>hide(true);
  pop.addEventListener('mouseenter',()=>clearTimeout(hideTimer));
  pop.addEventListener('mouseleave',scheduleHide);

  function wireTrigger(trigger,key){
    if(trigger.dataset.biMeaningWired)return;
    trigger.dataset.biMeaningWired='1';
    trigger.dataset.biMeaning=key;
    trigger.addEventListener('mouseenter',()=>show(trigger,key,false));
    trigger.addEventListener('mouseleave',scheduleHide);
    trigger.addEventListener('focus',()=>show(trigger,key,false));
    trigger.addEventListener('blur',scheduleHide);
    trigger.addEventListener('click',e=>{
      e.stopPropagation();
      const same=active===trigger&&pop.classList.contains('bi-visible');
      if(same&&pinned){hide(true);return}
      pinned=true;show(trigger,key,true);
    });
  }

  function addInfo(el,key,direct=false){
    if(!el||!TERMS[key])return;
    if(direct){
      el.classList.add('bi-defined-label','bi-defined-control');
      if(!/^(BUTTON|A|INPUT|SELECT|TEXTAREA)$/.test(el.tagName)){
        if(!el.hasAttribute('tabindex'))el.tabIndex=0;
      }
      wireTrigger(el,key);
      if(!el.getAttribute('aria-label'))el.setAttribute('aria-label',el.textContent.trim()+'. Definition available.');
      return;
    }
    if(el.querySelector(':scope > .bi-meaning-dot[data-bi-term="'+key+'"]'))return;
    el.classList.add('bi-defined-label');
    const b=document.createElement('button');
    b.type='button';b.className='bi-meaning-dot';b.dataset.biTerm=key;b.textContent='i';
    b.setAttribute('aria-label','What does '+TERMS[key].label+' mean?');
    wireTrigger(b,key);el.appendChild(b);
    el.addEventListener('mouseenter',()=>show(b,key,false));
    el.addEventListener('mouseleave',scheduleHide);
  }

  function exactKey(text){
    const n=norm(text);
    const map={
      'archive confidence':'archive_confidence','completeness':'completeness','redaction concern':'redaction_concern',
      'missing refs':'missing_refs','missing references':'missing_refs','missing evidence':'missing_evidence',
      'unreviewed':'unreviewed','reviewed':'reviewed','corroborated':'corroborated','contested':'contested',
      'evidence status':'evidence_status','promote':'promote','hold':'hold','merge':'merge',
      'reject-boundary':'reject_boundary','review required':'review_required','review required.':'review_required',
      'dependent':'dependent','partially-independent':'partially_independent','partially independent':'partially_independent',
      'independent':'independent','unknown':'independence_unknown','shared upstream families':'shared_upstream',
      'shared upstream family':'shared_upstream','encoded edges':'encoded_edge','encoded dependency edges':'encoded_edge',
      'research pairs awaiting review':'research_pair','review-state drift':'review_state_drift',
      'neutral review stubs':'neutral_stub','citation-only target families':'citation_only',
      'eo 14040 target families':'eo14040_candidate'
    };
    return map[n]||null;
  }


  function scanResearchStates(){
    const states={
      'canon':'canon','field note':'field_note','field_note':'field_note','apocrypha':'apocrypha',
      'pseudepigrapha':'pseudepigrapha','deuterocanon':'deuterocanon','fragment':'fragment',
      'rejected':'rejected','superseded':'superseded','authenticity status':'authenticity_status',
      'authenticity_status':'authenticity_status','attribution status':'attribution_status',
      'attribution_status':'attribution_status','provenance status':'provenance_status',
      'provenance_status':'provenance_status','corroboration status':'corroboration_status',
      'corroboration_status':'corroboration_status','source independence':'source_independence',
      'source_independence':'source_independence','classification confidence':'classification_confidence'
    };
    document.querySelectorAll('.bi-pill,.card strong,.card span,td,th,.bi-context-box b').forEach(el=>{
      if(el.closest('pre,#list,.bi-line-text'))return;
      if(el.children.length)return;
      const key=states[norm(el.textContent)];
      if(key)addInfo(el,key);
    });
  }

  function scanEvidence(){
    document.querySelectorAll('#view .cards .card .sub').forEach(el=>{const k=exactKey(el.textContent);if(k)addInfo(el,k)});
    document.querySelectorAll('#bi-utility button').forEach(el=>{const k=exactKey(el.textContent);if(k)addInfo(el,k,true)});
    document.querySelectorAll('#view .bi-context-box > b').forEach(el=>{
      const n=norm(el.textContent);
      if(n==='missing references')addInfo(el,'missing_refs');
      if(n==='depends on'||n==='used by')addInfo(el,'encoded_edge');
      if(n==='research cross-references')addInfo(el,'research_pair');
      if(n==='review state')addInfo(el,'review_required');
      if(n==='explicit entities')addInfo(el,'document_mention');
    });
    document.querySelectorAll('#bi-ai-panel .bi-ai-meta').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('sampled '))addInfo(el,'ai_sampled');
      else if(n.includes('complete source coverage'))addInfo(el,'ai_complete');
      else if(n.includes('research aid'))addInfo(el,'ai_research_aid');
    });
  }

  function scanWork(){
    document.querySelectorAll('.cards .card').forEach(el=>{
      const t=norm(el.childNodes[0]?.textContent||el.textContent);
      const k=exactKey(t);if(k)addInfo(el,k);
    });
    document.querySelectorAll('.queue-section td').forEach(el=>{
      if(el.children.length)return;
      const k=exactKey(el.textContent);if(k)addInfo(el,k,true);
    });
    document.querySelectorAll('.queue-section h2').forEach(el=>{
      const n=norm(el.childNodes[0]?.textContent||'');
      if(n.includes('review-state drift'))addInfo(el,'review_state_drift');
      if(n.includes('fbi p0 review state'))addInfo(el,'review_required');
      if(n.includes('lineage review'))addInfo(el,'research_pair');
      if(n.includes('missing-evidence'))addInfo(el,'missing_evidence');
    });
  }

  function scanNamed(){
    document.querySelectorAll('.cards .card span').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('citation-only')||n.includes('citation/synthesis'))addInfo(el,'citation_only');
      if(n.includes('eo 14040'))addInfo(el,'eo14040_candidate');
      if(n.includes('candidate'))addInfo(el,'candidate_hit');
    });
    document.querySelectorAll('.target h2 span').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('citation_or_synthesis_only'))addInfo(el,'citation_only',true);
      if(n.includes('underlying_container_candidate'))addInfo(el,'eo14040_candidate',true);
    });
    document.querySelectorAll('th').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('text page'))addInfo(el,'text_page');
      if(n.includes('physical page'))addInfo(el,'physical_page');
    });
  }

  function scanLineage(){
    document.querySelectorAll('.card .muted').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('shared upstream'))addInfo(el,'shared_upstream');
      else if(n.includes('dependent edge'))addInfo(el,'dependent');
      else if(n.includes('encoded edge'))addInfo(el,'encoded_edge');
      else if(n.includes('research pair'))addInfo(el,'research_pair');
    });
    document.querySelectorAll('td').forEach(el=>{
      if(el.children.length)return;
      const k=exactKey(el.textContent);if(['dependent','partially_independent','independent','independence_unknown','review_required'].includes(k))addInfo(el,k,true);
    });
  }

  function scanEntities(){
    document.querySelectorAll('.counts span').forEach(el=>{
      const n=norm(el.textContent);
      if(n.includes('doc mention'))addInfo(el,'document_mention',true);
      if(n.includes('genealogy edge'))addInfo(el,'genealogy_edge',true);
    });
    document.querySelectorAll('.entity').forEach(card=>{
      card.querySelectorAll('div').forEach(el=>{
        const n=norm(el.childNodes[0]?.textContent||'');
        if(n.startsWith('aliases:'))addInfo(el,'alias');
      });
    });
  }

  function pageKey(){
    const path=(location.pathname.split('/').pop()||'blackindex-dashboard.html').toLowerCase();
    if(path.includes('work-queue'))return'work';
    if(path.includes('named-source'))return'named';
    if(path.includes('source-lineage'))return'lineage';
    if(path.includes('entities'))return'entities';
    return'evidence';
  }

  function addGlossaryToHelp(){
    const body=document.getElementById('bi-help-body');
    if(!body||document.getElementById('bi-help-glossary'))return;
    const section=document.createElement('section');
    section.className='bi-help-section bi-help-glossary';section.id='bi-help-glossary';
    const cards=Object.entries(TERMS).map(([key,d])=>
      '<div class="bi-help-card" data-help-search="'+esc((d.label+' '+d.category+' '+d.definition+' '+(d.note||'')).toLowerCase())+'">'+
      '<strong>'+esc(d.label)+' <span class="bi-glossary-cat">'+esc(d.category)+'</span></strong>'+
      '<p>'+esc(d.definition)+(d.note?' '+esc(d.note):'')+'</p></div>'
    ).join('');
    section.innerHTML='<h3>Glossary / What does this mean?</h3><div class="bi-help-grid">'+cards+'</div>';
    const note=body.querySelector('.bi-help-note');
    if(note)body.insertBefore(section,note);else body.appendChild(section);
  }

  let scanQueued=false;
  function scan(){
    scanQueued=false;addGlossaryToHelp();
    const key=pageKey();
    if(key==='evidence')scanEvidence();
    else if(key==='work')scanWork();
    else if(key==='named')scanNamed();
    else if(key==='lineage')scanLineage();
    else if(key==='entities')scanEntities();
    scanResearchStates();
  }
  function queueScan(){
    if(scanQueued)return;scanQueued=true;requestAnimationFrame(scan);
  }

  document.addEventListener('click',e=>{
    if(!pop.contains(e.target)&&!e.target.closest('[data-bi-meaning]'))hide(true);
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&pop.classList.contains('bi-visible'))hide(true)});
  window.addEventListener('resize',()=>{if(active&&pop.classList.contains('bi-visible'))position(active)});
  window.addEventListener('scroll',()=>{if(active&&pop.classList.contains('bi-visible'))position(active)},{passive:true});

  new MutationObserver(queueScan).observe(document.body,{childList:true,subtree:true,characterData:true});
  scan();
})();
</script>
'''


def inject(path: Path) -> bool:
    if not path.is_file():
        print(f"skip: not found: {path}", file=sys.stderr)
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Inline definitions already present: {path}")
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
    print(f"Inline definitions injected: {path}")
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
