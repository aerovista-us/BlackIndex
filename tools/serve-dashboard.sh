#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
START_PORT="${1:-8787}"
REVIEW_PORT="${BLACKINDEX_REVIEW_PORT:-8811}"

python3 "$ROOT/tools/source-lineage.py" --root "$ROOT"
python3 "$ROOT/tools/dependency-audit.py" --root "$ROOT"
python3 "$ROOT/tools/research-reference-audit.py" --root "$ROOT"
python3 "$ROOT/tools/review-state-audit.py" --root "$ROOT"
python3 "$ROOT/tools/entity-index.py" --root "$ROOT"
python3 "$ROOT/tools/source-lineage-ui.py" --root "$ROOT"
python3 "$ROOT/tools/entity-ui.py" --root "$ROOT"
python3 "$ROOT/tools/work-queue-ui.py" --root "$ROOT"
python3 "$ROOT/tools/evidence_map.py" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-record-context.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-session.py" "$ROOT/local/dashboard/blackindex-dashboard.html"

if command -v tailscale >/dev/null 2>&1; then
  BIND="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
else
  BIND=""
fi

if [[ -z "$BIND" ]]; then
  echo "warning: Tailscale IPv4 not found; binding loopback only" >&2
  BIND="127.0.0.1"
fi

find_free_port() {
  local host="$1"
  local start="$2"
  python3 - "$host" "$start" <<'PY'
import socket, sys
host = sys.argv[1]
start = int(sys.argv[2])
for port in range(start, min(start + 200, 65536)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except OSError:
        s.close()
        continue
    else:
        s.close()
        print(port)
        raise SystemExit(0)
raise SystemExit(1)
PY
}

if ! PORT="$(find_free_port "$BIND" "$START_PORT")"; then
  echo "error: no free TCP port found from $START_PORT through $((START_PORT + 199)) on $BIND" >&2
  exit 3
fi

if [[ "$PORT" != "$START_PORT" ]]; then
  echo "Port $START_PORT is in use; selected free port $PORT instead."
fi

echo "BlackIndex dashboard: http://$BIND:$PORT/blackindex-dashboard.html"
echo "Work queue: http://$BIND:$PORT/work-queue.html"
echo "Source lineage: http://$BIND:$PORT/source-lineage.html"
echo "Entities: http://$BIND:$PORT/entities.html"
echo "Resume FBI Review button will prepare/open the review desk on port $REVIEW_PORT."
echo "Serving local/dashboard with BlackIndex local workflow actions. Ctrl-C to stop."
exec python3 "$ROOT/tools/blackindex-ui-server.py" \
  --root "$ROOT" \
  --bind "$BIND" \
  --port "$PORT" \
  --review-port "$REVIEW_PORT"
