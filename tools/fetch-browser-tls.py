#!/usr/bin/env python3
"""Fetch an artifact with a browser TLS fingerprint.

This is an acquisition fallback for official archives that serve a document to
normal browsers but reject command-line curl clients. It does not use a mirror:
the bytes are fetched directly from the supplied artifact URL.

Requires curl_cffi. Use tools/bootstrap-browser-fetch.sh to create the local
runtime without adding third-party packages to the repository.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

try:
    from curl_cffi import requests
except ImportError:
    print("error: curl_cffi is not installed; run tools/bootstrap-browser-fetch.sh", file=sys.stderr)
    raise SystemExit(78)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("output")
    ap.add_argument("--referer")
    ap.add_argument("--impersonate", default="chrome")
    args = ap.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    headers = {
        "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    if args.referer:
        headers["Referer"] = args.referer

    session = requests.Session(impersonate=args.impersonate)
    if args.referer:
        # Establish same-site cookies/state first. Failure is non-fatal; the
        # artifact request below remains authoritative.
        try:
            session.get(args.referer, timeout=60, allow_redirects=True)
        except Exception as exc:
            print(f"warning: browser-TLS landing preflight failed: {exc}", file=sys.stderr)

    try:
        response = session.get(
            args.url,
            headers=headers,
            timeout=300,
            allow_redirects=True,
            stream=True,
        )
        response.raise_for_status()
        digest = hashlib.sha256()
        size = 0
        with out.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                fh.write(chunk)
                digest.update(chunk)
                size += len(chunk)
    except Exception as exc:
        out.unlink(missing_ok=True)
        print(f"error: browser-TLS fetch failed: {exc}", file=sys.stderr)
        return 22

    magic = out.read_bytes()[:5]
    if magic != b"%PDF-":
        out.unlink(missing_ok=True)
        print(f"error: browser-TLS response is not PDF (magic={magic!r})", file=sys.stderr)
        return 4

    print(f"Browser-TLS fetch complete: {size} bytes sha256={digest.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
