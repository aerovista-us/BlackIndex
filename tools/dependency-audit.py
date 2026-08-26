#!/usr/bin/env python3
"""Audit BlackIndex for document references that are not yet encoded as source-dependency edges.

This tool is intentionally conservative: it does not create dependency objects.
It finds explicit document references in durable metadata/extractions and reports
candidate lineage work for human or later substantive review.
"""
from __future__ import annotations

import argparse, json, os, re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
DOC_ID_RE = re.compile(r"\b[A-Z][A-Z0-9_-]+-(?:\d{4}|undated)-[a-z0-9-]+-\d{3,}\b")


def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def read_json(p): return json.loads(p.read_text(encoding="utf-8"))

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    args=ap.parse_args(); root=Path(args.root).resolve()
    docs={}
    for p in sorted((root/"metadata").glob("*.json")):
        try: d=read_json(p)
        except Exception: continue
        if d.get("doc_id"): docs[d["doc_id"]]=d

    encoded=set()
    for p in sorted((root/"objects/source_dependencies").glob("*.json")):
        try: d=read_json(p)
        except Exception: continue
        a=d.get("source_id"); b=d.get("depends_on")
        if a and b: encoded.add((a,b))
    for doc_id,m in docs.items():
        parent=m.get("parent_container_doc_id")
        if parent: encoded.add((doc_id,parent))
        for dep in m.get("source_dependencies") or []:
            if isinstance(dep,dict):
                target=dep.get("parent_doc_id") or dep.get("source_id") or dep.get("depends_on")
                if target: encoded.add((doc_id,target))

    candidates=[]
    for doc_id,m in docs.items():
        refs=defaultdict(set)
        for target in m.get("related_documents") or []:
            if isinstance(target,str) and target in docs and target!=doc_id:
                refs[target].add("metadata.related_documents")
        extraction=root/"extractions"/f"{doc_id}.md"
        if extraction.is_file():
            text=extraction.read_text(encoding="utf-8",errors="replace")
            for target in DOC_ID_RE.findall(text):
                if target in docs and target!=doc_id:
                    refs[target].add("extraction.explicit_doc_id")
        for target,origins in sorted(refs.items()):
            if (doc_id,target) in encoded: continue
            candidates.append({
                "source_doc_id":doc_id,
                "referenced_doc_id":target,
                "reference_origins":sorted(origins),
                "status":"REVIEW_REQUIRED",
                "note":"Explicit cross-document reference only. This is not yet a source-dependency assertion."
            })

    by_source=defaultdict(int)
    for c in candidates: by_source[c["source_doc_id"]]+=1
    payload={
        "schema_version":1,
        "generated_at":now(),
        "purpose":"candidate lineage backfill queue; no dependency is asserted by this report",
        "document_count":len(docs),
        "encoded_dependency_edges":len(encoded),
        "candidate_count":len(candidates),
        "candidates":candidates,
        "candidate_counts_by_source":dict(sorted(by_source.items(), key=lambda kv:(-kv[1],kv[0])))
    }
    out=root/"local/index"; out.mkdir(parents=True,exist_ok=True)
    jp=out/"dependency-audit.json"; jp.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    lines=["# BlackIndex Dependency Audit","","> Candidate lineage work only. An explicit cross-document reference does not by itself establish source dependence.","",f"Documents: **{len(docs)}** · Encoded edges: **{len(encoded)}** · Review candidates: **{len(candidates)}**","","| Source document | References | Origin |","|---|---|---|"]
    for c in candidates:
        lines.append(f"| `{c['source_doc_id']}` | `{c['referenced_doc_id']}` | {', '.join(c['reference_origins'])} |")
    mp=out/"dependency-audit.md"; mp.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"documents":len(docs),"encoded_edges":len(encoded),"candidates":len(candidates),"json":str(jp),"markdown":str(mp)},indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
