#!/usr/bin/env python3
"""Find BlackIndex document co-occurrences in durable research notes.

Recognition uses explicit document IDs and exact sufficiently-distinct metadata
titles. Outputs a review queue only. Co-occurrence does not imply dependence,
agreement, corroboration, contradiction, or direction of evidence flow.
"""
from __future__ import annotations

import argparse, itertools, json, os, re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT0=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",ROOT0))
DOC_ID_RE=re.compile(r"\b[A-Z][A-Z0-9_-]+-(?:\d{4}|undated)-[a-z0-9-]+-\d{3,}\b")

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load_docs(root):
    docs={}
    for p in (root/"metadata").glob("*.json"):
        try:
            d=json.loads(p.read_text(encoding="utf-8"))
            if d.get("doc_id"): docs[d["doc_id"]]=d
        except Exception: pass
    return docs

def title_index(docs):
    by_title=defaultdict(list)
    for doc_id,d in docs.items():
        title=(d.get("title") or "").strip()
        # Avoid generic labels; title matching is only a recall aid for review.
        if len(title)>=16 and len(title.split())>=3:
            by_title[title.casefold()].append(doc_id)
    return {t:ids[0] for t,ids in by_title.items() if len(ids)==1}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    docs=load_docs(root); valid=set(docs); titles=title_index(docs); files=[]; pairs=Counter(); pair_files=defaultdict(list)
    bases=[root/"docs/reviews",root/"docs/research-clusters"]
    for base in bases:
        if not base.exists(): continue
        for p in sorted(base.rglob("*.md")):
            text=p.read_text(encoding="utf-8",errors="replace"); lower=text.casefold()
            found={x for x in DOC_ID_RE.findall(text) if x in valid}; methods=defaultdict(set)
            for x in found: methods[x].add("explicit_doc_id")
            for title,doc_id in titles.items():
                if title in lower:
                    found.add(doc_id); methods[doc_id].add("exact_metadata_title")
            ids=sorted(found)
            if not ids: continue
            rel=str(p.relative_to(root)); files.append({"path":rel,"doc_ids":ids,"count":len(ids),"recognition":{k:sorted(v) for k,v in methods.items()}})
            for a,b in itertools.combinations(ids,2):
                pairs[(a,b)]+=1; pair_files[(a,b)].append(rel)
    ranked=[]
    for (a,b),count in pairs.most_common():
        ranked.append({"doc_a":a,"doc_b":b,"cooccurrence_files":count,"files":pair_files[(a,b)],"status":"REVIEW_REQUIRED","note":"Research-note co-occurrence only; no evidentiary relationship is asserted."})
    payload={"schema_version":1,"generated_at":now(),"purpose":"research-note cross-reference discovery; no lineage direction or dependency assertion","recognition_methods":["explicit_doc_id","exact_unique_metadata_title"],"files_with_recognized_documents":len(files),"unique_pairs":len(ranked),"files":files,"pairs":ranked}
    out=root/"local/index"; out.mkdir(parents=True,exist_ok=True)
    jp=out/"research-reference-audit.json"; jp.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    lines=["# BlackIndex Research Reference Audit","","> Co-occurrence is not dependence, corroboration, agreement, contradiction, or evidence-flow direction.","",f"Research files with recognized documents: **{len(files)}** · Unique document pairs: **{len(ranked)}**","","| Pair | Research files |","|---|---:|"]
    for r in ranked: lines.append(f"| `{r['doc_a']}` ↔ `{r['doc_b']}` | {r['cooccurrence_files']} |")
    mp=out/"research-reference-audit.md"; mp.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"files":len(files),"pairs":len(ranked),"json":str(jp),"markdown":str(mp)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
