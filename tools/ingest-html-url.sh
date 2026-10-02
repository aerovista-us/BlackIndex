#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

usage() {
  echo "usage: tools/ingest-html-url.sh <url> [--publish] [blackindex intake args...]" >&2
  exit 2
}
[[ $# -ge 1 ]] || usage
URL="$1"; shift
PUBLISH=0
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish) PUBLISH=1; shift ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

command -v curl >/dev/null
command -v python3 >/dev/null
mkdir -p "$ROOT/local/cache"
TMP="$(mktemp "$ROOT/local/cache/html-ingest.XXXXXX.html")"
trap 'rm -f "$TMP"' EXIT
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/151 Safari/537.36'
ALLOW_BROWSER_FALLBACK=0
case "$URL" in
  https://www.navair.navy.mil/*|https://navair.navy.mil/*|https://www.stratcom.mil/*|https://stratcom.mil/*)
    ALLOW_BROWSER_FALLBACK=1 ;;
esac

html_guard() {
  python3 - "$TMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
if not p.is_file() or p.stat().st_size < 512:
    raise SystemExit(1)
probe=p.read_bytes()[:262144].decode("utf-8", errors="ignore").lower()
s=probe.lstrip()
html_like=s.startswith("<!doctype html") or s.startswith("<html") or "<html" in probe[:16384]
blocked=any(x in probe for x in (
    "attention required! | cloudflare",
    "/cdn-cgi/challenge-platform",
    "cf-error-details",
    "cf-chl-",
))
raise SystemExit(0 if html_like and not blocked else 1)
PY
}
echo "Downloading HTML: $URL"
set +e
curl -fL --http1.1 --retry 2 --retry-delay 2 --connect-timeout 20 --max-time 90 --compressed \
  -A "$UA" -H 'Accept: text/html,application/xhtml+xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.9' -o "$TMP" "$URL"
DOWNLOAD_RC=$?
set -e

if [[ "$DOWNLOAD_RC" -ne 0 ]] || ! html_guard; then
  if [[ "$ALLOW_BROWSER_FALLBACK" -ne 1 ]]; then
    echo "error: direct HTML fetch failed or returned an interstitial; no fallback approved for this host" >&2
    exit 22
  fi
  BROWSER_PY="$ROOT/local/tools/browser-fetch-venv/bin/python"
  [[ -x "$BROWSER_PY" ]] || { echo "error: browser fetch runtime unavailable" >&2; exit 78; }
  rm -f "$TMP"; TMP="$(mktemp "$ROOT/local/cache/html-ingest.XXXXXX.html")"
  echo "Direct fetch did not yield source HTML; retrying approved first-party host with browser TLS..." >&2
  "$BROWSER_PY" "$ROOT/tools/fetch-browser-tls.py" "$URL" "$TMP" --expect html
fi

html_guard || { echo "error: downloaded artifact failed HTML/interstitial guard" >&2; exit 4; }
set +e
OUT="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" intake "$TMP" --artifact-url "$URL" "${ARGS[@]}")"
INTAKE_RC=$?
set -e
printf '%s\n' "$OUT"
[[ "$INTAKE_RC" -eq 0 || "$INTAKE_RC" -eq 3 ]] || exit "$INTAKE_RC"

DOC_ID="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["doc_id"])')"
BLACKINDEX_ROOT="$ROOT" python3 "$ROOT/tools/generate-review-template.py" "$DOC_ID"
python3 "$ROOT/tools/evidence_map.py" --root "$ROOT" integrity "$DOC_ID"
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

if [[ "$PUBLISH" -eq 1 && "$INTAKE_RC" -ne 3 ]]; then
  "$ROOT/tools/publish-ingest.sh" "$DOC_ID"
elif [[ "$PUBLISH" -eq 1 ]]; then
  echo "Resume: durable metadata/extraction for $DOC_ID already present."
fi

echo "One-shot HTML ingest complete: $DOC_ID"
