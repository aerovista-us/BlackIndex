#!/usr/bin/env python3
"""Inject a dependency-free embedded favicon into generated BlackIndex HTML."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "<!-- BLACKINDEX_FAVICON -->"
ICON = '''<!-- BLACKINDEX_FAVICON -->
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%23101419'/%3E%3Cpath d='M14 13h18c11 0 18 5 18 14 0 5-3 9-8 11 6 2 9 6 9 12 0 10-7 15-20 15H14V13zm12 9v12h7c5 0 8-2 8-6s-3-6-8-6h-7zm0 21v13h8c6 0 9-2 9-7s-3-6-9-6h-8z' fill='%23e7edf3'/%3E%3C/svg%3E">
'''


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("local/dashboard/blackindex-dashboard.html")
    if not path.is_file():
        print(f"error: dashboard not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Favicon already injected: {path}")
        return 0
    pos = text.lower().find("</head>")
    text = text[:pos] + ICON + text[pos:] if pos >= 0 else ICON + text
    path.write_text(text, encoding="utf-8")
    print(f"BlackIndex favicon injected: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
