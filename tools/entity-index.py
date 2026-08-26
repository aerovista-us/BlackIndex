#!/usr/bin/env python3
"""Compile a conservative local BlackIndex entity index.

Sources:
- explicit metadata people/organizations/operations/locations fields;
- curated genealogy baselines under entities/**/genealogy-baseline.json.

No free-text NER, surname matching, allegation inference, or culpability scoring is
performed. A document/entity edge means only that the durable metadata explicitly
lists that entity. Genealogy edges mean only the curated baseline relationship.
"""
from __future__ import annotations

import argparse, json, os, re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",REPO_ROOT))
FIELDS={"people":"person","organizations":"organization","operations":"operation","locations":"location"}


def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def load(p, default=None):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {} if default is None else default

def slug(v):
    return re.sub(r"[^a-z0-9]+","-",str(v).casefold()).strip("-") or "entity"

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    entities={}; edges=[]; aliases=defaultdict(set)

    def ensure(entity_id, name, kind, source, **extra):
        e=entities.setdefault(entity_id,{"entity_id":entity_id,"canonical_name":name,"entity_type":kind,"sources":[],"aliases":[]})
        if source not in e["sources"]: e["sources"].append(source)
        for k,v in extra.items():
            if v is not None and k not in e: e[k]=v
        return e

    docs=[]
    for p in sorted((root/"metadata").glob("*.json")):
        d=load(p,{}); doc_id=d.get("doc_id")
        if not doc_id: continue
        docs.append(doc_id)
        for field,kind in FIELDS.items():
            values=d.get(field) or []
            if isinstance(values,str): values=[values]
            for value in values:
                if not isinstance(value,str) or not value.strip(): continue
                name=value.strip(); eid=f"{kind}:{slug(name)}"
                ensure(eid,name,kind,f"metadata:{doc_id}")
                edges.append({
                    "edge_type":"document_mentions_entity",
                    "from":doc_id,"to":eid,"entity_type":kind,
                    "source":f"metadata/{doc_id}.json",
                    "meaning":"durable metadata explicitly lists this entity; no conduct or culpability is implied"
                })

    genealogy_files=[]
    for p in sorted((root/"entities").rglob("genealogy-baseline.json")) if (root/"entities").exists() else []:
        data=load(p,{}); genealogy_files.append(str(p.relative_to(root)))
        people=[]
        founder=data.get("founder")
        if isinstance(founder,dict): people.append(founder)
        for key in ("five_branches","london_branch_path_to_victor"):
            vals=data.get(key) or []
            if isinstance(vals,list): people.extend(x for x in vals if isinstance(x,dict))
        seen=set()
        for person in people:
            pid=person.get("person_id"); name=person.get("canonical_name")
            if not pid or not name: continue
            eid=f"person:{pid}"; seen.add(eid)
            ensure(eid,name,"person",str(p.relative_to(root)),birth_year=person.get("birth_year"),death_year=person.get("death_year"),title=person.get("title"),branch=person.get("branch"))
            pref=person.get("preferred_name")
            if pref: aliases[eid].add(pref)
            parent=person.get("parent_id")
            if parent:
                parent_eid=f"person:{parent}"
                edges.append({
                    "edge_type":"genealogy_parent_child","from":parent_eid,"to":eid,
                    "source":str(p.relative_to(root)),
                    "meaning":"curated genealogical parent-child relationship only; no inherited culpability or association is implied"
                })
        # The path array is ordered ancestry even where parent_id is omitted.
        path_people=[x for x in (data.get("london_branch_path_to_victor") or []) if isinstance(x,dict) and x.get("person_id")]
        for a,b in zip(path_people,path_people[1:]):
            ae=f"person:{a['person_id']}"; be=f"person:{b['person_id']}"
            if not any(e.get("edge_type")=="genealogy_parent_child" and e.get("from")==ae and e.get("to")==be for e in edges):
                edges.append({
                    "edge_type":"genealogy_ancestry_path","from":ae,"to":be,
                    "source":str(p.relative_to(root)),
                    "meaning":"ordered curated ancestry path; exact relationship level should be checked in the cited genealogy source before reuse"
                })

    for eid,vals in aliases.items():
        if eid in entities: entities[eid]["aliases"]=sorted(vals)
    # Deduplicate edges deterministically.
    unique=[]; seen=set()
    for e in edges:
        key=(e.get("edge_type"),e.get("from"),e.get("to"),e.get("source"))
        if key not in seen: seen.add(key); unique.append(e)
    type_counts=defaultdict(int)
    for e in entities.values(): type_counts[e["entity_type"]]+=1
    edge_counts=defaultdict(int)
    for e in unique: edge_counts[e["edge_type"]]+=1
    payload={
        "schema_version":1,"generated_at":now(),
        "rules":{
            "free_text_ner":False,"surname_only_matching":False,"association_implies_culpability":False,
            "genealogy_implies_conduct":False,"document_mention_implies_claim":False,
            "non_identity_relationships_require_separate_sourced_evidence":True
        },
        "document_count":len(docs),"genealogy_files":genealogy_files,
        "counts":{"entities":len(entities),"edges":len(unique),"entity_types":dict(sorted(type_counts.items())),"edge_types":dict(sorted(edge_counts.items()))},
        "entities":sorted(entities.values(),key=lambda x:(x["entity_type"],x["canonical_name"].casefold(),x["entity_id"])),
        "edges":unique
    }
    out=root/"local/index/entity-index.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out),**payload["counts"],"genealogy_files":len(genealogy_files)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
