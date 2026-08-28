#!/usr/bin/env python3
"""Serve the BlackIndex dashboard with local workflow actions.

This is intentionally a local/Tailscale operational helper, not a public API.
It serves local/dashboard and exposes a small POST action that resumes the FBI
review workflow, prepares missing review artifacts, starts the FBI Review Desk
if needed, and redirects the browser there.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path(os.environ.get("BLACKINDEX_ROOT", REPO_ROOT))


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.4):
            return True
    except OSError:
        return False


def run_step(root: Path, cmd: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, output[-12000:]


def ensure_review_state(root: Path) -> tuple[bool, str]:
    logs: list[str] = []
    steps: list[list[str]] = [
        ["bash", str(root / "tools/prepare-911-p0-review.sh")],
        [sys.executable, str(root / "tools/build-fbi-source-review-bundle.py"), "--root", str(root), "--band", "P0", "--record-type", "fd_302", "--limit", "8"],
        [sys.executable, str(root / "tools/inspect-fbi-source-review-bundle.py"), "--root", str(root)],
    ]
    for cmd in steps:
        ok, out = run_step(root, cmd)
        logs.append("$ " + " ".join(cmd) + "\n" + out)
        if not ok:
            return False, "\n\n".join(logs)
    return True, "\n\n".join(logs)


def start_review_desk(root: Path, bind: str, port: int) -> tuple[bool, str]:
    if port_open(bind, port):
        return True, "Review Desk already running."
    log_path = root / "local/logs/fbi-review-desk.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = log_path.open("ab")
    subprocess.Popen(
        [sys.executable, str(root / "tools/fbi-review-desk.py"), "--root", str(root), "--bind", bind, "--port", str(port)],
        cwd=root,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(30):
        if port_open(bind, port):
            return True, f"Review Desk started; log: {log_path}"
        time.sleep(0.15)
    return False, f"Review Desk did not start on {bind}:{port}; see {log_path}"


class Handler(SimpleHTTPRequestHandler):
    root: Path
    dashboard_dir: Path
    bind_host: str
    review_port: int

    def translate_path(self, path: str) -> str:
        rel = urllib.parse.urlparse(path).path.lstrip("/")
        if not rel:
            rel = "blackindex-dashboard.html"
        candidate = (self.dashboard_dir / rel).resolve()
        try:
            candidate.relative_to(self.dashboard_dir.resolve())
        except ValueError:
            return str(self.dashboard_dir / "__blocked__")
        return str(candidate)

    def do_GET(self):
        if urllib.parse.urlparse(self.path).path == "/__blackindex_health":
            payload = {
                "ok": True,
                "service": "blackindex-dashboard",
                "schema_version": 1,
            }
            body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/actions/resume-fbi-review":
            self.send_error(404)
            return
        ok, prep_log = ensure_review_state(self.root)
        if not ok:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(("BlackIndex FBI review preparation failed.\n\n" + prep_log).encode())
            return
        started, message = start_review_desk(self.root, self.bind_host, self.review_port)
        if not started:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write((message + "\n\n" + prep_log).encode())
            return
        self.send_response(303)
        self.send_header("Location", f"http://{self.bind_host}:{self.review_port}/")
        self.end_headers()

    def log_message(self, fmt, *args):
        super().log_message(fmt, *args)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--review-port", type=int, default=8811)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    dashboard_dir = root / "local/dashboard"
    Handler.root = root
    Handler.dashboard_dir = dashboard_dir
    Handler.bind_host = args.bind
    Handler.review_port = args.review_port

    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    print(f"BlackIndex dashboard: http://{args.bind}:{args.port}/blackindex-dashboard.html")
    print(f"Health: http://{args.bind}:{args.port}/__blackindex_health")
    print(f"Resume FBI Review action: POST /actions/resume-fbi-review -> review desk :{args.review_port}")
    print("Serving local/dashboard with BlackIndex local actions. Ctrl-C to stop.")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
