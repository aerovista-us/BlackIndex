#!/usr/bin/env python3
"""Local review desk for FBI source-review bundles.

Serves a localhost/Tailscale-only HTML interface for reviewing source-slice PDFs
and recording dispositions through the existing review-fbi-candidate.py CLI.

This tool does NOT promote evidence. It only writes the local review ledger.
Actual promotion still requires promote-reviewed-fbi-candidates.py --apply.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(v):
    return html.escape("" if v is None else str(v))


class ReviewHandler(SimpleHTTPRequestHandler):
    root: Path
    bundle: Path

    def translate_path(self, path):
        rel = urllib.parse.urlparse(path).path.lstrip("/")
        if not rel or rel == "index.html":
            return str(self.bundle / "review-desk.html")
        candidate = (self.bundle / rel).resolve()
        try:
            candidate.relative_to(self.bundle.resolve())
        except ValueError:
            return str(self.bundle / "__blocked__")
        return str(candidate)

    def do_POST(self):
        if self.path != "/review":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        data = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        one = lambda k: (data.get(k) or [""])[0]
        disposition = one("disposition")
        if disposition not in {"PROMOTE", "HOLD", "MERGE", "REJECT-BOUNDARY"}:
            self.send_error(400, "invalid disposition")
            return
        cmd = [
            "python3", str(self.root / "tools/review-fbi-candidate.py"),
            one("container_doc_id"), one("candidate_id"), disposition,
            "--root", str(self.root),
        ]
        opts = {
            "confirmed_pages": "--confirmed-pages",
            "record_type": "--record-type",
            "date": "--date",
            "serial": "--serial",
            "redactions": "--redactions",
            "source_dependency": "--source-dependency",
            "duplicate_of": "--duplicate-of",
            "note": "--note",
        }
        for key, flag in opts.items():
            value = one(key).strip()
            if value:
                cmd += [flag, value]
        if one("source_checked") == "1":
            cmd.append("--source-checked")
        if one("boundary_override") == "1":
            cmd.append("--boundary-override")
        result = subprocess.run(cmd, cwd=self.root, text=True, capture_output=True)
        if result.returncode != 0:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write((result.stderr or result.stdout).encode())
            return
        build_review_page(self.root, self.bundle)
        self.send_response(303)
        self.send_header("Location", "/index.html")
        self.end_headers()


def checked(v):
    return " checked" if v else ""


def build_review_page(root: Path, bundle: Path):
    manifest = load_json(bundle / "manifest.json", {"records": []})
    inspection = load_json(bundle / "inspection.json", {})
    ledger = load_json(root / "local/review/911-fbi-p0/review-ledger.json", {"reviews": []})

    inspect_rows = inspection.get("records") or inspection.get("items") or inspection.get("inspections") or []
    by_key = {(r.get("container_doc_id"), r.get("candidate_id")): r for r in inspect_rows}
    review_by_key = {(r.get("container_doc_id"), r.get("candidate_id")): r for r in ledger.get("reviews", [])}

    cards = []
    for rec in manifest.get("records", []):
        key = (rec.get("container_doc_id"), rec.get("candidate_id"))
        ins = by_key.get(key, {})
        prior = review_by_key.get(key, {})
        pdf_name = Path(rec.get("source_pdf", "")).name
        recommendation = ins.get("recommendation", "UNINSPECTED")
        date_hints = ins.get("date_hints") or []
        serials = ins.get("serial_or_case_hits") or ins.get("serial_case") or []
        if isinstance(date_hints, str): date_hints = [date_hints]
        if isinstance(serials, str): serials = [serials]
        heuristic = rec.get("heuristic_pages", "")
        cards.append(f'''
<section class="card">
  <div class="head">
    <div><strong>#{esc(rec.get('review_rank'))} {esc(rec.get('candidate_id'))}</strong><br>
    <code>{esc(rec.get('container_doc_id'))}</code></div>
    <span class="badge">{esc(recommendation)}</span>
  </div>
  <div class="meta">Heuristic pages: <b>{esc(heuristic)}</b> · Type: <b>{esc(rec.get('record_type_guess'))}</b> · Entities: {esc(', '.join(rec.get('entity_hits') or []))}</div>
  <object data="/{esc(pdf_name)}" type="application/pdf" class="pdf"><a href="/{esc(pdf_name)}">Open PDF</a></object>
  <form method="post" action="/review">
    <input type="hidden" name="container_doc_id" value="{esc(rec.get('container_doc_id'))}">
    <input type="hidden" name="candidate_id" value="{esc(rec.get('candidate_id'))}">
    <div class="grid">
      <label>Confirmed pages<input name="confirmed_pages" value="{esc(prior.get('confirmed_pages') or heuristic)}"></label>
      <label>Record type<input name="record_type" value="{esc(prior.get('record_type') or rec.get('record_type_guess') or '')}"></label>
      <label>Date<input name="date" value="{esc(prior.get('record_date') or (date_hints[0] if date_hints else ''))}"></label>
      <label>Serial/case<input name="serial" value="{esc(prior.get('serial_or_case_id') or (serials[0] if serials else ''))}"></label>
      <label>Redactions<input name="redactions" value="{esc(prior.get('redactions') or '')}"></label>
      <label>Source dependency<input name="source_dependency" value="{esc(prior.get('source_dependency') or 'FBI interview/investigative record within EO 14040 release container')}"></label>
      <label>Duplicate of<input name="duplicate_of" value="{esc(prior.get('duplicate_of') or '')}"></label>
      <label class="wide">Note<input name="note" value="{esc(prior.get('note') or '')}"></label>
    </div>
    <div class="checks">
      <label class="check"><input type="checkbox" name="source_checked" value="1"{checked(prior.get('source_pdf_checked'))}> I visually checked the original source PDF and confirmed these metadata/boundaries.</label>
      <label class="check"><input type="checkbox" name="boundary_override" value="1"{checked(prior.get('boundary_override'))}> Confirmed pages intentionally extend beyond the heuristic range (requires explanatory note).</label>
    </div>
    <div class="actions">
      <button name="disposition" value="PROMOTE">PROMOTE</button>
      <button name="disposition" value="HOLD">HOLD</button>
      <button name="disposition" value="MERGE">MERGE</button>
      <button name="disposition" value="REJECT-BOUNDARY">REJECT BOUNDARY</button>
      <span>Current: <b>{esc(prior.get('disposition') or 'UNREVIEWED')}</b></span>
    </div>
  </form>
</section>''')

    body = f'''<!doctype html><meta charset="utf-8"><title>BlackIndex FBI Review Desk</title>
<style>
body{{font:15px system-ui;margin:0;background:#111;color:#eee}} main{{max-width:1300px;margin:auto;padding:24px}}
h1{{margin:0 0 6px}} .note{{color:#bbb;margin-bottom:24px}} .card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:18px;margin:18px 0}}
.head{{display:flex;justify-content:space-between;gap:12px}} .badge{{background:#333;padding:6px 10px;border-radius:999px;height:max-content}} .meta{{margin:10px 0;color:#ccc}}
.pdf{{width:100%;height:620px;background:white;border:0;margin:8px 0 14px}} .grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}} label{{display:flex;flex-direction:column;gap:4px;color:#bbb}} input{{background:#111;color:#eee;border:1px solid #444;border-radius:6px;padding:8px}} .wide{{grid-column:1/-1}} .checks{{display:grid;gap:8px;margin-top:12px}} .check{{display:flex;flex-direction:row;align-items:center;gap:8px;color:#ddd}} .actions{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}} button{{padding:9px 12px;border:1px solid #555;background:#292929;color:#fff;border-radius:7px;cursor:pointer}} button:hover{{background:#3a3a3a}} code{{color:#bcd}} @media(max-width:800px){{.grid{{grid-template-columns:1fr}}.pdf{{height:500px}}}}
</style><main><h1>BlackIndex — FBI Review Desk</h1>
<div class="note">Review ledger only. PROMOTE requires the source-PDF confirmation checkbox. If confirmed pages extend beyond the heuristic range, boundary override plus an explanatory note are required. Actual corpus promotion remains a separate fail-closed step.</div>
{''.join(cards)}</main>'''
    (bundle / "review-desk.html").write_text(body, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--bundle", default="local/review/source-bundles/911-fbi-first-promotion")
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8811)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    bundle = Path(args.bundle)
    if not bundle.is_absolute(): bundle = root / bundle
    if not (bundle / "manifest.json").exists():
        raise SystemExit(f"bundle manifest not found: {bundle / 'manifest.json'}")
    build_review_page(root, bundle)
    ReviewHandler.root = root
    ReviewHandler.bundle = bundle
    server = ThreadingHTTPServer((args.bind, args.port), ReviewHandler)
    print(f"BlackIndex FBI review desk: http://{args.bind}:{args.port}/")
    print("Ledger only; no evidence promotion occurs from this server. Ctrl-C to stop.")
    server.serve_forever()

if __name__ == "__main__":
    main()
