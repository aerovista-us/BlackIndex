#!/usr/bin/env python3
"""Audit BlackIndex metadata review status against durable extraction state.

This tool never changes metadata. It identifies workflow drift only:
- metadata says unreviewed while the extraction is no longer a neutral TODO stub;
- metadata says reviewed/corroborated/contested while extraction is missing/stub.

A non-stub extraction is *candidate evidence of review activity*, not proof that a
specific evidence_status value is correct. Any status change remains explicit.
"""
from __future__ import annotations

import argparse, json, os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT=Path(__file__).resolve().parents[1]
DEFAULT_ROOT=Path(os.environ.get("BLACKINDEX_ROOT",REPO_ROOT))


def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def load(p):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {}
def is_stub(text):
    return "TODO" in text and ("## DOCUMENT CONTENT" in text or "## Evidence established by the document" in text or "## DOCUMENT SAYS" in text) and ("R0" in text or "substantive review pending" in text)


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(DEFAULT_ROOT)); args=ap.parse_args(); root=Path(args.root).resolve()
    rows=[]; states=Counter(); extraction_states=Counter()
    for p in sorted((root/"metadata").glob("*.json")):
        m=load(p); doc_id=m.get("doc_id")
        if not doc_id: continue
        status=m.get("evidence_status") or "unset"; states[status]+=1
        xp=root/"extractions"/f"{doc_id}.md"
        if not xp.is_file():
            xstate="missing"
        else:
            text=xp.read_text(encoding="utf-8",errors="replace")
            xstate="stub" if is_stub(text) else ("empty" if not text.strip() else "non_stub")
        extraction_states[xstate]+=1
        finding=None
        if status in ("unreviewed","unset") and xstate=="non_stub":
            finding="STATUS_LAG_NON_STUB_EXTRACTION"
        elif status in ("reviewed","corroborated","contested") and xstate in ("missing","empty","stub"):
            finding="STATUS_AHEAD_OF_EXTRACTION"
        if finding:
            rows.append({
                "doc_id":doc_id,"title":m.get("title"),"metadata_evidence_status":status,
                "extraction_state":xstate,"finding":finding,"status":"REVIEW_REQUIRED",
                "note":"Workflow-state mismatch only. Do not change evidence status without substantive review of the extraction and source record."
            })
    payload={
        "schema_version":1,"generated_at":now(),
        "purpose":"workflow-state drift audit; no evidence status is changed automatically",
        "metadata_status_counts":dict(sorted(states.items())),
        "extraction_state_counts":dict(sorted(extraction_states.items())),
        "mismatch_count":len(rows),"mismatches":rows
    }
    out=root/"local/index"; out.mkdir(parents=True,exist_ok=True)
    jp=out/"review-state-audit.json"; jp.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# BlackIndex Review-State Audit","","> Workflow-state audit only. A non-stub extraction does not automatically justify changing metadata evidence status.","",f"Mismatches requiring review: **{len(rows)}**","","| Document | Metadata status | Extraction state | Finding |","|---|---|---|---|"]
    for r in rows: lines.append(f"| `{r['doc_id']}` | {r['metadata_evidence_status']} | {r['extraction_state']} | {r['finding']} |")
    mp=out/"review-state-audit.md"; mp.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"mismatches":len(rows),"metadata_status_counts":payload["metadata_status_counts"],"extraction_state_counts":payload["extraction_state_counts"],"json":str(jp),"markdown":str(mp)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
