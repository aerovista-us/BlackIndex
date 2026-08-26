#!/usr/bin/env python3
"""Repair/enhance the generated BlackIndex dashboard HTML.

Repairs the historical JS highlighter escaping issue and injects local workflow
controls used by the BlackIndex-aware UI server.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("local/dashboard/blackindex-dashboard.html")
    if not path.is_file():
        print(f"error: dashboard not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    start_marker = "function markText(text,q)"
    end_marker = "function renderView()"
    start = text.find(start_marker)
    end = text.find(end_marker, start if start >= 0 else 0)
    if start < 0 or end < 0 or end <= start:
        print("error: dashboard highlighter block not found", file=sys.stderr)
        return 3

    replacement = r'''function markText(text,q){
  const source=String(text??'');
  if(!q)return esc(source);
  const needle=String(q).toLowerCase();
  const lower=source.toLowerCase();
  let out='',pos=0,hit;
  while((hit=lower.indexOf(needle,pos))!==-1){
    out+=esc(source.slice(pos,hit));
    out+='<mark>'+esc(source.slice(hit,hit+needle.length))+'</mark>';
    pos=hit+needle.length;
  }
  return out+esc(source.slice(pos));
}
'''
    text = text[:start] + replacement + text[end:]

    # Inject only once. This form intentionally uses POST so a static file server
    # cannot accidentally execute local workflow actions; serve-dashboard.sh now
    # launches the BlackIndex-aware UI server that handles this route.
    marker = "<!-- BLACKINDEX_RESUME_FBI_REVIEW -->"
    if marker not in text:
        control = r'''
<!-- BLACKINDEX_RESUME_FBI_REVIEW -->
<style>
#bi-resume-review{position:fixed;right:18px;bottom:18px;z-index:9999;background:#111;border:1px solid #555;border-radius:12px;padding:10px 12px;box-shadow:0 8px 30px rgba(0,0,0,.35)}
#bi-resume-review button{background:#20252b;color:#fff;border:1px solid #68727d;border-radius:8px;padding:10px 14px;font:600 13px system-ui;cursor:pointer}
#bi-resume-review button:hover{background:#2d353d}
#bi-resume-review small{display:block;color:#aaa;margin-top:5px;max-width:230px}
</style>
<form id="bi-resume-review" method="post" action="/actions/resume-fbi-review" target="_blank">
  <button type="submit">Resume FBI Review</button>
  <small>Rebuild review state, start the Review Desk, and open it.</small>
</form>
'''
        body_end = text.lower().rfind("</body>")
        if body_end >= 0:
            text = text[:body_end] + control + text[body_end:]
        else:
            text += control

    path.write_text(text, encoding="utf-8")
    print(f"Dashboard JS sanitized + workflow controls injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
