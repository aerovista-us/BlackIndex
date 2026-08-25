#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
PORT="${1:-8787}"

python3 "$ROOT/tools/evidence_map.py" --root "$ROOT" dashboard

if command -v tailscale >/dev/null 2>&1; then
  BIND="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
else
  BIND=""
fi

if [[ -z "$BIND" ]]; then
  echo "warning: Tailscale IPv4 not found; binding loopback only" >&2
  BIND="127.0.0.1"
fi

echo "BlackIndex dashboard: http://$BIND:$PORT/blackindex-dashboard.html"
echo "Serving only local/dashboard. Ctrl-C to stop."
exec python3 -m http.server "$PORT" --bind "$BIND" --directory "$ROOT/local/dashboard"
