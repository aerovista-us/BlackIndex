#!/usr/bin/env python3
"""BlackIndex evidence-map infrastructure.

Durable research objects are stored under objects/ and may be committed to Git.
Raw/normalized corpus data and generated dashboards remain under local/ and are
ignored by Git.

This module intentionally records state of the record rather than final historical
verdicts. Assertions, conflicts, gaps, dependencies, and investigator findings may
coexist indefinitely.
"""
from __future__ import annotations

import argparse
import difflib
import html
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))
DOC_METADATA_RE = re.compile(r"^[A-Z0-9_-]+-(?:[0-9]{4}|undated)-[a-z0-9-]+-[0-9]{3,}\.json$")
OBJECT_TYPES = (
    "record_integrity",
    "missing_evidence",
    "version_families",
    "version_comparisons",
    "source_dependencies",
    "statement_comparisons",
    "investigator_reviews",
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return value or "item"


def ensure_layout(root: Path) -> None:
    for kind in OBJECT_TYPES:
        (root / "objects" / kind).mkdir(parents=True, exist_ok=True)
    (root / "local/index").mkdir(parents=True, exist_ok=True)
    (root / "local/dashboard").mkdir(parents=True, exist_ok=True)


def metadata_files(root: Path):
    md = root / "metadata"
    if not md.exists():
        return []
    return sorted(p for p in md.glob("*.json") if DOC_METADATA_RE.match(p.name))


def get_metadata(root: Path, doc_id: str) -> dict:
    p = root / "metadata" / f"{doc_id}.json"
    if not p.is_file():
        raise FileNotFoundError(f"metadata not found: {p}")
    return read_json(p)


def default_record_integrity(meta: dict) -> dict:
    return {
        "schema_version": 1,
        "object_type": "record_integrity",
        "object_id": f"RI-{meta['doc_id']}",
        "doc_id": meta["doc_id"],
        "created_at": now(),
        "updated_at": now(),
        "completeness": None,
        "redaction_concern": None,
        "known_destruction": "unknown",
        "missing_referenced_records": [],
        "custodian_conflicts": [],
        "version_conflicts": [],
        "public_internal_contradictions": [],
        "archive_confidence": None,
        "record_creator": meta.get("record_creator") or meta.get("source"),
        "record_custodian": meta.get("record_custodian"),
        "declassification_authority": meta.get("declassification_authority"),
        "withholding_authority": meta.get("withholding_authority"),
        "artifact_type": meta.get("artifact_type") or meta.get("mime_hint"),
        "chain_of_custody": meta.get("chain_of_custody") or [],
        "alternate_versions": meta.get("alternate_versions") or [],
        "classification_chronology": meta.get("classification_chronology") or [],
        "release_chronology": meta.get("release_chronology") or [],
        "destruction_chronology": meta.get("destruction_chronology") or [],
        "notes": "",
    }


def ensure_integrity(root: Path, doc_id: str) -> Path:
    meta = get_metadata(root, doc_id)
    path = root / "objects/record_integrity" / f"{doc_id}.json"
    if not path.exists():
        write_json(path, default_record_integrity(meta))
    return path


def cmd_bootstrap(args) -> int:
    root = Path(args.root)
    ensure_layout(root)
    made = 0
    for p in metadata_files(root):
        meta = read_json(p)
        target = root / "objects/record_integrity" / f"{meta['doc_id']}.json"
        if not target.exists():
            write_json(target, default_record_integrity(meta))
            made += 1
    index = build_object_index(root)
    print(json.dumps({"documents": len(metadata_files(root)), "record_integrity_created": made, "index": str(index)}, indent=2))
    return 0


def cmd_integrity(args) -> int:
    root = Path(args.root)
    ensure_layout(root)
    path = ensure_integrity(root, args.doc_id)
    data = read_json(path)
    for field, value in (
        ("completeness", args.completeness),
        ("redaction_concern", args.redaction_concern),
        ("archive_confidence", args.archive_confidence),
        ("known_destruction", args.known_destruction),
        ("record_creator", args.record_creator),
        ("record_custodian", args.record_custodian),
        ("declassification_authority", args.declassification_authority),
        ("withholding_authority", args.withholding_authority),
    ):
        if value is not None:
            data[field] = value
    if args.note:
        data["notes"] = (data.get("notes", "") + ("\n" if data.get("notes") else "") + args.note).strip()
    data["updated_at"] = now()
    write_json(path, data)
    build_object_index(root)
    print(path)
    return 0


def next_object_path(root: Path, kind: str, prefix: str) -> Path:
    token = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    return root / "objects" / kind / f"{prefix}-{token}.json"


def cmd_missing(args) -> int:
    root = Path(args.root)
    get_metadata(root, args.doc_id)
    path = next_object_path(root, "missing_evidence", f"ME-{slug(args.doc_id)}")
    obj = {
        "schema_version": 1,
        "object_type": "missing_evidence",
        "object_id": path.stem,
        "doc_id": args.doc_id,
        "created_at": now(),
        "category": args.category,
        "summary": args.summary,
        "referenced_by": args.referenced_by,
        "last_known_location": args.last_known_location,
        "known_creator": args.known_creator,
        "likely_custodian": args.likely_custodian,
        "stated_reason_missing": args.stated_reason_missing,
        "potential_relevance": args.potential_relevance,
        "alternative_explanations": args.alternative_explanation or [],
        "recovery_paths": args.recovery_path or [],
        "status": "unresolved",
    }
    write_json(path, obj)
    integrity = read_json(ensure_integrity(root, args.doc_id))
    integrity.setdefault("missing_referenced_records", []).append(obj["object_id"])
    integrity["updated_at"] = now()
    write_json(root / "objects/record_integrity" / f"{args.doc_id}.json", integrity)
    build_object_index(root)
    print(path)
    return 0


def cmd_version_family(args) -> int:
    root = Path(args.root)
    for doc_id in args.doc_ids:
        get_metadata(root, doc_id)
    path = root / "objects/version_families" / f"{slug(args.family_id)}.json"
    obj = {
        "schema_version": 1,
        "object_type": "version_family",
        "object_id": args.family_id,
        "created_at": now(),
        "updated_at": now(),
        "title": args.title or args.family_id,
        "doc_ids": args.doc_ids,
        "canonical_doc_id": args.canonical_doc_id,
        "notes": args.note or "",
    }
    write_json(path, obj)
    build_object_index(root)
    print(path)
    return 0


def normalized_text(root: Path, doc_id: str) -> tuple[dict, str]:
    meta = get_metadata(root, doc_id)
    value = meta.get("normalized_text_path")
    if not value or not Path(value).is_file():
        raise FileNotFoundError(f"normalized text unavailable for {doc_id}")
    return meta, Path(value).read_text(encoding="utf-8", errors="replace")


def cmd_compare_versions(args) -> int:
    root = Path(args.root)
    left_meta, left = normalized_text(root, args.left_doc_id)
    right_meta, right = normalized_text(root, args.right_doc_id)
    diff = list(difflib.unified_diff(left.splitlines(), right.splitlines(), fromfile=args.left_doc_id, tofile=args.right_doc_id, n=args.context, lineterm=""))
    ratio = difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()
    comparison_id = args.comparison_id or f"VC-{args.left_doc_id}--{args.right_doc_id}"
    path = root / "objects/version_comparisons" / f"{slug(comparison_id)}.json"
    obj = {
        "schema_version": 1,
        "object_type": "version_comparison",
        "object_id": comparison_id,
        "created_at": now(),
        "family_id": args.family_id,
        "left_doc_id": args.left_doc_id,
        "right_doc_id": args.right_doc_id,
        "left_sha256": left_meta.get("sha256"),
        "right_sha256": right_meta.get("sha256"),
        "similarity_ratio": round(ratio, 6),
        "diff_line_count": len(diff),
        "diff_preview": diff[: args.max_diff_lines],
        "notes": args.note or "",
    }
    write_json(path, obj)
    build_object_index(root)
    print(json.dumps({"path": str(path), "similarity_ratio": obj["similarity_ratio"], "diff_line_count": len(diff)}, indent=2))
    return 0


def cmd_dependency(args) -> int:
    root = Path(args.root)
    path = next_object_path(root, "source_dependencies", "SD")
    obj = {
        "schema_version": 1,
        "object_type": "source_dependency",
        "object_id": path.stem,
        "created_at": now(),
        "assertion_id": args.assertion_id,
        "source_id": args.source_id,
        "depends_on": args.depends_on,
        "dependency_type": args.dependency_type,
        "independence": args.independence,
        "notes": args.note or "",
    }
    write_json(path, obj)
    build_object_index(root)
    print(path)
    return 0


def cmd_statement_compare(args) -> int:
    root = Path(args.root)
    path = next_object_path(root, "statement_comparisons", "SC")
    obj = {
        "schema_version": 1,
        "object_type": "statement_comparison",
        "object_id": path.stem,
        "created_at": now(),
        "topic": args.topic,
        "public_source": args.public_source,
        "public_statement": args.public_statement,
        "internal_source": args.internal_source,
        "internal_content": args.internal_content,
        "relationship": args.relationship,
        "notes": args.note or "",
        "judgment": None,
    }
    write_json(path, obj)
    build_object_index(root)
    print(path)
    return 0


def cmd_investigator(args) -> int:
    root = Path(args.root)
    path = next_object_path(root, "investigator_reviews", "IR")
    obj = {
        "schema_version": 1,
        "object_type": "investigator_review",
        "object_id": path.stem,
        "created_at": now(),
        "report_or_finding": args.report_or_finding,
        "investigator": args.investigator,
        "employer_controller": args.employer_controller,
        "exact_wording": args.exact_wording,
        "scope": args.scope,
        "records_reviewed": args.records_reviewed or [],
        "records_unavailable": args.records_unavailable or [],
        "witnesses_omitted": args.witnesses_omitted or [],
        "workpapers_status": args.workpapers_status,
        "competing_findings": args.competing_finding or [],
        "investigator_independence": args.independence,
        "access_to_evidence": args.access,
        "method_transparency": args.transparency,
        "reproducibility": args.reproducibility,
        "conflict_exposure": args.conflict_exposure,
        "notes": args.note or "",
        "conclusion_adopted_as_fact": False,
    }
    write_json(path, obj)
    build_object_index(root)
    print(path)
    return 0


def object_files(root: Path):
    for kind in OBJECT_TYPES:
        base = root / "objects" / kind
        if base.exists():
            yield from sorted(base.glob("*.json"))


def build_object_index(root: Path) -> Path:
    ensure_layout(root)
    grouped = {kind: [] for kind in OBJECT_TYPES}
    for path in object_files(root):
        data = read_json(path)
        kind = data.get("object_type", "")
        directory = path.parent.name
        grouped.setdefault(directory, []).append(data)
    out = root / "local/index/evidence-map.json"
    write_json(out, {"generated_at": now(), "counts": {k: len(v) for k, v in grouped.items()}, "objects": grouped})
    return out


def cmd_index(args) -> int:
    path = build_object_index(Path(args.root))
    print(path)
    return 0


def collect_dashboard_data(root: Path, max_text: int) -> dict:
    docs = []
    for p in metadata_files(root):
        meta = read_json(p)
        doc_id = meta.get("doc_id")
        extraction_path = root / "extractions" / f"{doc_id}.md"
        extraction = extraction_path.read_text(encoding="utf-8", errors="replace") if extraction_path.is_file() else ""
        text = ""
        text_path = meta.get("normalized_text_path")
        if text_path and Path(text_path).is_file():
            text = Path(text_path).read_text(encoding="utf-8", errors="replace")[:max_text]
        integrity_path = root / "objects/record_integrity" / f"{doc_id}.json"
        integrity = read_json(integrity_path) if integrity_path.is_file() else {}
        docs.append({"metadata": meta, "extraction": extraction, "text": text, "integrity": integrity})
    index_path = build_object_index(root)
    obj_index = read_json(index_path)
    return {"generated_at": now(), "documents": docs, "evidence_map": obj_index}


def dashboard_html(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BlackIndex Local Dashboard</title>
<style>
:root{{--bg:#0d1014;--panel:#151a20;--panel2:#1b222a;--text:#e7edf3;--muted:#8fa0af;--line:#2a343e;--accent:#c8d5df;--warn:#d7b77b}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,Segoe UI,sans-serif}}
header{{position:sticky;top:0;z-index:3;background:#0d1014ee;border-bottom:1px solid var(--line);padding:14px 18px;backdrop-filter:blur(8px)}}
h1{{font-size:18px;margin:0 0 8px}} .sub{{color:var(--muted);font-size:12px}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}} input,select,button{{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:8px 10px}} input{{min-width:320px;flex:1}}
main{{display:grid;grid-template-columns:360px 1fr;min-height:calc(100vh - 100px)}}
#list{{border-right:1px solid var(--line);overflow:auto;max-height:calc(100vh - 100px)}} .item{{padding:12px 14px;border-bottom:1px solid var(--line);cursor:pointer}} .item:hover,.item.active{{background:var(--panel2)}}
.item b{{display:block}} .meta{{color:var(--muted);font-size:12px;margin-top:4px}} #view{{padding:20px;overflow:auto;max-height:calc(100vh - 100px)}}
.cards{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}} .card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:9px 11px;min-width:130px}} .card strong{{display:block;font-size:18px}}
pre{{white-space:pre-wrap;word-break:break-word;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;max-height:56vh;overflow:auto}} h2,h3{{margin-top:18px}} a{{color:var(--accent)}} .tabs button.active{{border-color:var(--accent)}} mark{{background:#6d5d2c;color:#fff}} .warn{{color:var(--warn)}}
@media(max-width:850px){{main{{grid-template-columns:1fr}}#list{{max-height:35vh;border-right:0;border-bottom:1px solid var(--line)}}#view{{max-height:none}}}}
</style></head><body>
<header><h1>BlackIndex · Local Evidence Map</h1><div class="sub" id="summary"></div><div class="controls"><input id="q" placeholder="Search title, metadata, extraction, or normalized text…"><select id="source"><option value="">All sources</option></select><button id="clear">Clear</button></div></header>
<main><aside id="list"></aside><section id="view"><div class="sub">Select a record.</div></section></main>
<script>const DATA={payload};
const docs=DATA.documents;let filtered=docs.slice();let current=null;let tab='extraction';
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[m]));
const src=[...new Set(docs.map(d=>d.metadata.source).filter(Boolean))].sort();document.getElementById('source').innerHTML+=""+src.map(s=>`<option>${{esc(s)}}</option>`).join('');
function counts(){{const c=DATA.evidence_map.counts||{{}};document.getElementById('summary').textContent=`${{docs.length}} documents · ${{c.record_integrity||0}} integrity · ${{c.missing_evidence||0}} missing-evidence · ${{c.version_comparisons||0}} version comparisons · generated ${{DATA.generated_at}}`;}}
function searchable(d){{return JSON.stringify(d.metadata)+' '+d.extraction+' '+d.text+' '+JSON.stringify(d.integrity)}}
function apply(){{const q=document.getElementById('q').value.trim().toLowerCase(),s=document.getElementById('source').value;filtered=docs.filter(d=>(!s||d.metadata.source===s)&&(!q||searchable(d).toLowerCase().includes(q)));renderList();}}
function renderList(){{const el=document.getElementById('list');el.innerHTML=filtered.map((d,i)=>`<div class="item ${{current===d?'active':''}}" data-i="${{i}}"><b>${{esc(d.metadata.title||d.metadata.doc_id)}}</b><div class="meta">${{esc(d.metadata.doc_id)}} · ${{esc(d.metadata.source)}} · ${{esc(d.metadata.collection)}}</div></div>`).join('')||'<div class="item">No matches</div>';el.querySelectorAll('[data-i]').forEach(x=>x.onclick=()=>{{current=filtered[+x.dataset.i];tab='extraction';renderList();renderView();}})}}
function markText(text,q){{
  const source=String(text??'');
  if(!q)return esc(source);
  const needle=String(q).toLowerCase();
  const lower=source.toLowerCase();
  let out='',pos=0,hit;
  while((hit=lower.indexOf(needle,pos))!==-1){{
    out+=esc(source.slice(pos,hit));
    out+='<mark>'+esc(source.slice(hit,hit+needle.length))+'</mark>';
    pos=hit+needle.length;
  }}
  return out+esc(source.slice(pos));
}}
function renderView(){{if(!current)return;const d=current,m=d.metadata,r=d.integrity||{{}},q=document.getElementById('q').value.trim();const content=tab==='extraction'?d.extraction:tab==='text'?d.text:JSON.stringify(m,null,2);document.getElementById('view').innerHTML=`<h2>${{esc(m.title||m.doc_id)}}</h2><div class="meta">${{esc(m.doc_id)}} · ${{esc(m.source)}} · ${{esc(m.collection)}} · SHA ${{esc((m.sha256||'').slice(0,12))}}…</div><div class="cards"><div class="card"><span class="sub">Archive confidence</span><strong>${{esc(r.archive_confidence??'—')}}</strong></div><div class="card"><span class="sub">Completeness</span><strong>${{esc(r.completeness??'—')}}</strong></div><div class="card"><span class="sub">Redaction concern</span><strong>${{esc(r.redaction_concern??'—')}}</strong></div><div class="card"><span class="sub">Missing refs</span><strong>${{(r.missing_referenced_records||[]).length}}</strong></div></div><div class="tabs"><button data-t="extraction">Review</button> <button data-t="text">Text chunk</button> <button data-t="metadata">Metadata</button></div><pre>${{markText(content,q)}}</pre>${{m.artifact_url?`<div><a target="_blank" href="${{esc(m.artifact_url)}}">Source artifact</a></div>`:''}}`;document.querySelectorAll('[data-t]').forEach(b=>{{if(b.dataset.t===tab)b.classList.add('active');b.onclick=()=>{{tab=b.dataset.t;renderView()}}}})}}
document.getElementById('q').oninput=()=>{{apply();renderView()}};document.getElementById('source').onchange=apply;document.getElementById('clear').onclick=()=>{{document.getElementById('q').value='';document.getElementById('source').value='';apply();}};counts();apply();
</script></body></html>'''


def cmd_dashboard(args) -> int:
    root = Path(args.root)
    ensure_layout(root)
    data = collect_dashboard_data(root, args.max_text_per_doc)
    out = Path(args.output) if args.output else root / "local/dashboard/blackindex-dashboard.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(dashboard_html(data), encoding="utf-8")
    print(json.dumps({"output": str(out), "documents": len(data["documents"]), "bytes": out.stat().st_size}, indent=2))
    return 0


def cmd_search(args) -> int:
    root = Path(args.root)
    q = args.query.lower()
    hits = []
    for path in object_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        if q in text.lower():
            hits.append({"path": str(path.relative_to(root)), "object": read_json(path)})
    print(json.dumps({"query": args.query, "count": len(hits), "results": hits[:args.limit]}, indent=2))
    return 0


def cmd_publish(args) -> int:
    root = Path(args.root).resolve()
    paths = ["objects"]
    add = subprocess.run(["git", "-C", str(root), "add", "--", *paths], capture_output=True, text=True)
    if add.returncode:
        print(add.stderr, file=sys.stderr); return add.returncode
    diff = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--quiet", "--", *paths])
    if diff.returncode == 0:
        print("No evidence-map object changes to publish"); return 0
    commit = subprocess.run(["git", "-C", str(root), "commit", "-m", args.message or "BlackIndex: update evidence-map objects"], capture_output=True, text=True)
    if commit.returncode:
        print(commit.stdout + commit.stderr, file=sys.stderr); return commit.returncode
    if args.push:
        push = subprocess.run(["git", "-C", str(root), "push"], capture_output=True, text=True)
        if push.returncode:
            print(push.stdout + push.stderr, file=sys.stderr); return push.returncode
    print("Published evidence-map objects" if args.push else "Committed evidence-map objects")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="evidence-map", description="BlackIndex evidence-map objects and local dashboard")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = p.add_subparsers(dest="command", required=True)
    s=sub.add_parser("bootstrap",help="create Record Integrity sidecars for all ingested documents");s.set_defaults(func=cmd_bootstrap)
    s=sub.add_parser("integrity",help="create/update one Record Integrity object");s.add_argument("doc_id");s.add_argument("--completeness",type=int,choices=range(0,6));s.add_argument("--redaction-concern",type=int,choices=range(0,16));s.add_argument("--archive-confidence",type=int,choices=range(0,6));s.add_argument("--known-destruction",choices=["yes","no","unknown"]);s.add_argument("--record-creator");s.add_argument("--record-custodian");s.add_argument("--declassification-authority");s.add_argument("--withholding-authority");s.add_argument("--note");s.set_defaults(func=cmd_integrity)
    s=sub.add_parser("missing-evidence",help="record an explicit missing-evidence object");s.add_argument("doc_id");s.add_argument("--summary",required=True);s.add_argument("--category",default="MISSING_EVIDENCE");s.add_argument("--referenced-by");s.add_argument("--last-known-location");s.add_argument("--known-creator");s.add_argument("--likely-custodian");s.add_argument("--stated-reason-missing");s.add_argument("--potential-relevance");s.add_argument("--alternative-explanation",action="append");s.add_argument("--recovery-path",action="append");s.set_defaults(func=cmd_missing)
    s=sub.add_parser("version-family",help="define documents as versions of the same record");s.add_argument("family_id");s.add_argument("doc_ids",nargs="+");s.add_argument("--title");s.add_argument("--canonical-doc-id");s.add_argument("--note");s.set_defaults(func=cmd_version_family)
    s=sub.add_parser("compare-versions",help="diff normalized text for two versions");s.add_argument("left_doc_id");s.add_argument("right_doc_id");s.add_argument("--family-id");s.add_argument("--comparison-id");s.add_argument("--context",type=int,default=3);s.add_argument("--max-diff-lines",type=int,default=500);s.add_argument("--note");s.set_defaults(func=cmd_compare_versions)
    s=sub.add_parser("source-dependency",help="record whether sources/assertions are genuinely independent");s.add_argument("--assertion-id",required=True);s.add_argument("--source-id",required=True);s.add_argument("--depends-on",required=True);s.add_argument("--dependency-type",default="derived");s.add_argument("--independence",choices=["independent","partially-independent","dependent","unknown"],default="unknown");s.add_argument("--note");s.set_defaults(func=cmd_dependency)
    s=sub.add_parser("statement-compare",help="record public statement vs internal record comparison");s.add_argument("--topic",required=True);s.add_argument("--public-source",required=True);s.add_argument("--public-statement",required=True);s.add_argument("--internal-source",required=True);s.add_argument("--internal-content",required=True);s.add_argument("--relationship",choices=["consistent","partially-consistent","in-tension","contradictory","unclear"],default="unclear");s.add_argument("--note");s.set_defaults(func=cmd_statement_compare)
    s=sub.add_parser("investigator-review",help="record a negative finding or investigator/report reliability context");s.add_argument("--report-or-finding",required=True);s.add_argument("--investigator",required=True);s.add_argument("--employer-controller");s.add_argument("--exact-wording",required=True);s.add_argument("--scope");s.add_argument("--records-reviewed",action="append");s.add_argument("--records-unavailable",action="append");s.add_argument("--witnesses-omitted",action="append");s.add_argument("--workpapers-status");s.add_argument("--competing-finding",action="append");s.add_argument("--independence",type=int,choices=range(0,6));s.add_argument("--access",type=int,choices=range(0,6));s.add_argument("--transparency",type=int,choices=range(0,6));s.add_argument("--reproducibility",type=int,choices=range(0,6));s.add_argument("--conflict-exposure",type=int,choices=range(0,6));s.add_argument("--note");s.set_defaults(func=cmd_investigator)
    s=sub.add_parser("index",help="rebuild local evidence-map index");s.set_defaults(func=cmd_index)
    s=sub.add_parser("search",help="search durable evidence-map objects");s.add_argument("query");s.add_argument("--limit",type=int,default=20);s.set_defaults(func=cmd_search)
    s=sub.add_parser("dashboard",help="build one self-contained local HTML dashboard");s.add_argument("--output");s.add_argument("--max-text-per-doc",type=int,default=250000);s.set_defaults(func=cmd_dashboard)
    s=sub.add_parser("publish",help="commit/push durable objects only");s.add_argument("--message");s.add_argument("--push",action="store_true");s.set_defaults(func=cmd_publish)
    return p


def main():
    args=build_parser().parse_args()
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
