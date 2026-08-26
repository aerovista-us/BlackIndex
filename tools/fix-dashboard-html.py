#!/usr/bin/env python3
"""Inject local BlackIndex workflow controls into the generated dashboard.

The dashboard highlighter is emitted correctly by evidence_map.py itself. This
helper only injects local workflow/navigation controls used by the BlackIndex-aware
UI server.
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
    marker = "<!-- BLACKINDEX_WORKFLOW_CONTROLS -->"
    legacy_marker = "<!-- BLACKINDEX_RESUME_FBI_REVIEW -->"
    if marker not in text and legacy_marker not in text:
        control = r'''
<!-- BLACKINDEX_WORKFLOW_CONTROLS -->
<style>
#bi-workflow-controls{position:fixed;right:18px;bottom:18px;z-index:9999;background:#111;border:1px solid #555;border-radius:12px;padding:10px 12px;box-shadow:0 8px 30px rgba(0,0,0,.35);display:flex;gap:8px;align-items:center;flex-wrap:wrap;max-width:650px}
#bi-workflow-controls button,#bi-workflow-controls a{background:#20252b;color:#fff;border:1px solid #68727d;border-radius:8px;padding:10px 14px;font:600 13px system-ui;cursor:pointer;text-decoration:none}
#bi-workflow-controls button:hover,#bi-workflow-controls a:hover{background:#2d353d}
#bi-workflow-controls small{display:block;color:#aaa;width:100%;margin-top:2px}
</style>
<div id="bi-workflow-controls">
  <a href="/work-queue.html" target="_blank">Work Queue</a>
  <a href="/source-lineage.html" target="_blank">Source Lineage</a>
  <a href="/entities.html" target="_blank">Entities</a>
  <form method="post" action="/actions/resume-fbi-review" target="_blank" style="margin:0">
    <button type="submit">Resume FBI Review</button>
  </form>
  <small>Work Queue collects unfinished states. Lineage tracks source genealogy. Entities shows identity/explicit mentions only—association is not culpability.</small>
</div>
'''
        body_end = text.lower().rfind("</body>")
        if body_end >= 0:
            text = text[:body_end] + control + text[body_end:]
        else:
            text += control

    path.write_text(text, encoding="utf-8")
    print(f"Dashboard workflow controls injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
