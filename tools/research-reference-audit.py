#!/usr/bin/env python3
"""Find explicit BlackIndex document-ID co-occurrences in durable research notes.

Outputs a review queue only. Co-occurrence does not imply dependence, agreement,
corroboration, contradiction, or direction of evidence flow.
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
def load_doc_ids(root):
    ids=set()
    for p in (root/"metadata").glob("*.json"):
        try:
            d=json.loads(p.read_text(encoding="utf-8"))
            if d.get("doc_id"): ids.add(d["doc_id"])
        except Exception: pass
    return ids

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    valid=load_doc_ids(root); files=[]; pairs=Counter(); pair_files=defaultdict(list)
    bases=[root/"docs/reviews",root/"docs/research-clusters"]
    for base in bases:
        if not base.exists(): continue
        for p in sorted(base.rglob("*.md")):
            text=p.read_text(encoding="utf-8",errors="replace")
            ids=sorted({x for x in DOC_ID_RE.findall(text) if x in valid})
            if not ids: continue
            rel=str(p.relative_to(root)); files.append({"path":rel,"doc_ids":ids,"count":len(ids)})
            for a,b in itertools.combinations(ids,2):
                pairs[(a,b)]+=1; pair_files[(a,b)].append(rel)
    ranked=[]
    for (a,b),count in pairs.most_common():
        ranked.append({"doc_a":a,"doc_b":b,"cooccurrence_files":count,"files":pair_files[(a,b)],"status":"REVIEW_REQUIRED","note":"Research-note co-occurrence only; no evidentiary relationship is asserted."})
    payload={"schema_version":1,"generated_at":now(),"purpose":"research-note cross-reference discovery; no lineage direction or dependency assertion","files_with_doc_ids":len(files),"unique_pairs":len(ranked),"files":files,"pairs":ranked}
    out=root/"local/index"; out.mkdir(parents=True,exist_ok=True)
    jp=out/"research-reference-audit.json"; jp.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    lines=["# BlackIndex Research Reference Audit","","> Co-occurrence is not dependence, corroboration, agreement, contradiction, or evidence-flow direction.","",f"Research files with recognized document IDs: **{len(files)}** · Unique document pairs: **{len(ranked)}**","","| Pair | Research files |","|---|---:|"]
    for r in ranked: lines.append(f"| `{r['doc_a']}` ↔ `{r['doc_b']}` | {r['cooccurrence_files']} |")
    mp=out/"research-reference-audit.md"; mp.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"files":len(files),"pairs":len(ranked),"json":str(jp),"markdown":str(mp)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
