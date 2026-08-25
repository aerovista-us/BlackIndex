#!/usr/bin/env python3
"""Repair the generated BlackIndex dashboard JS highlighter.

The dashboard generator historically emitted a regular-expression escape helper
through a Python f-string. Nested JS/Python escaping could produce an invalid
browser regex. This postprocessor replaces that helper with a literal,
case-insensitive string highlighter that does not construct a RegExp.
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
    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    print(f"Dashboard JS sanitized: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
