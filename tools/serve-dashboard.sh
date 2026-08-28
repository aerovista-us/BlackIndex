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
python3 "$ROOT/tools/named-source-recovery-ui.py" --root "$ROOT"
python3 "$ROOT/tools/evidence_map.py" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-record-context.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-session.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-export.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-favicon.py" "$ROOT/local/dashboard/blackindex-dashboard.html"

if command -v tailscale >/dev/null 2>&1; then
  BIND="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
else
  BIND=""
fi

if [[ -z "$BIND" ]]; then
  echo "warning: Tailscale IPv4 not found; binding loopback only" >&2
  BIND="127.0.0.1"
fi

blackindex_health() {
  local host="$1"
  local port="$2"
  python3 - "$host" "$port" <<'PY'
import json, sys, urllib.request
host, port = sys.argv[1], int(sys.argv[2])
try:
    with urllib.request.urlopen(f"http://{host}:{port}/__blackindex_health", timeout=0.5) as r:
        payload = json.loads(r.read().decode("utf-8", "replace"))
    if payload.get("ok") is True and payload.get("service") == "blackindex-dashboard":
        raise SystemExit(0)
except Exception:
    pass
raise SystemExit(1)
PY
}

legacy_blackindex_process() {
  local port="$1"
  if ! command -v lsof >/dev/null 2>&1; then
    return 1
  fi
  local pid args
  while IFS= read -r pid; do
    [[ -n "$pid" ]] || continue
    args="$(ps -p "$pid" -o args= 2>/dev/null || true)"
    if [[ "$args" == *"blackindex-ui-server.py"* ]]; then
      return 0
    fi
  done < <(lsof -nP -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null | sort -u)
  return 1
}

port_is_free() {
  local host="$1"
  local port="$2"
  python3 - "$host" "$port" <<'PY'
import socket, sys
host, port = sys.argv[1], int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except OSError:
    raise SystemExit(1)
finally:
    s.close()
raise SystemExit(0)
PY
}

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

print_urls() {
  local port="$1"
  echo "BlackIndex dashboard: http://$BIND:$port/blackindex-dashboard.html"
  echo "Work queue: http://$BIND:$port/work-queue.html"
  echo "Named source recovery: http://$BIND:$port/named-source-recovery.html"
  echo "Source lineage: http://$BIND:$port/source-lineage.html"
  echo "Entities: http://$BIND:$port/entities.html"
}

# Re-generating the dashboard above updates files on disk. A running BlackIndex
# server serves those files directly, so do not create a second dashboard server
# merely because the preferred port is already occupied.
if ! port_is_free "$BIND" "$START_PORT"; then
  if blackindex_health "$BIND" "$START_PORT" || legacy_blackindex_process "$START_PORT"; then
    echo "Existing BlackIndex dashboard detected on port $START_PORT; reusing it."
    print_urls "$START_PORT"
    echo "Resume FBI Review button uses review desk port $REVIEW_PORT."
    exit 0
  fi
fi

if ! PORT="$(find_free_port "$BIND" "$START_PORT")"; then
  echo "error: no free TCP port found from $START_PORT through $((START_PORT + 199)) on $BIND" >&2
  exit 3
fi

if [[ "$PORT" != "$START_PORT" ]]; then
  echo "Port $START_PORT is in use by a non-BlackIndex service; selected free port $PORT instead."
fi

print_urls "$PORT"
echo "Resume FBI Review button will prepare/open the review desk on port $REVIEW_PORT."
echo "Serving local/dashboard with BlackIndex local workflow actions. Ctrl-C to stop."
exec python3 "$ROOT/tools/blackindex-ui-server.py" \
  --root "$ROOT" \
  --bind "$BIND" \
  --port "$PORT" \
  --review-port "$REVIEW_PORT"
