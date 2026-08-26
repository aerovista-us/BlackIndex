#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

usage() {
  cat >&2 <<'EOF'
usage: tools/ingest-url.sh <artifact-url> [--publish] [blackindex intake args...]

Downloads one remote artifact into local/cache, ingests + normalizes it,
creates/preserves the neutral evidence-map review record, verifies the local
vault, and optionally publishes only durable metadata/extraction.

Downloader tiers:
1. normal curl + browser UA
2. landing-page cookie preflight + browser-navigation curl
3. browser-TLS impersonation via local curl_cffi runtime when available

Duplicate-by-hash intake is treated as a successful resume condition.
EOF
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi
URL="$1"; shift
PUBLISH=0
REFERER=""
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish) PUBLISH=1; shift ;;
    --landing-url)
      [[ $# -ge 2 ]] || { echo "error: --landing-url requires a value" >&2; exit 2; }
      REFERER="$2"; ARGS+=("$1" "$2"); shift 2 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

command -v curl >/dev/null 2>&1 || { echo "error: curl is required" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "error: python3 is required" >&2; exit 2; }

mkdir -p "$ROOT/local/cache"
TMP="$(mktemp "$ROOT/local/cache/url-ingest.XXXXXX.pdf")"
COOKIE_JAR="$(mktemp "$ROOT/local/cache/url-ingest.cookies.XXXXXX")"
cleanup(){ rm -f "$TMP" "$COOKIE_JAR"; }
trap cleanup EXIT
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'

if [[ -n "$REFERER" ]]; then
  echo "Preflighting landing page: $REFERER"
  curl -sSL --http1.1 --connect-timeout 20 --max-time 60 \
    -A "$UA" \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Accept-Language: en-US,en;q=0.9' \
    --cookie-jar "$COOKIE_JAR" --cookie "$COOKIE_JAR" \
    -o /dev/null "$REFERER" || true
fi

echo "Downloading: $URL"
CURL_ARGS=(
  -fL --http1.1 --retry 3 --retry-delay 2 --connect-timeout 20 --max-time 300 --compressed
  -A "$UA"
  -H 'Accept: application/pdf,application/octet-stream;q=0.9,*/*;q=0.8'
  -H 'Accept-Language: en-US,en;q=0.9'
  --cookie-jar "$COOKIE_JAR" --cookie "$COOKIE_JAR" -o "$TMP"
)
[[ -z "$REFERER" ]] || CURL_ARGS+=(-e "$REFERER")
set +e
curl "${CURL_ARGS[@]}" "$URL"
DOWNLOAD_RC=$?
set -e

if [[ "$DOWNLOAD_RC" -ne 0 && "$URL" == https://vault.fbi.gov/* ]]; then
  echo "FBI Vault direct download rejected; retrying with browser-navigation headers..." >&2
  rm -f "$TMP"; TMP="$(mktemp "$ROOT/local/cache/url-ingest.XXXXXX.pdf")"
  FBI_ARGS=(
    -fL --http1.1 --retry 2 --retry-delay 2 --connect-timeout 20 --max-time 300 --compressed
    -A "$UA"
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf;q=0.8,*/*;q=0.7'
    -H 'Accept-Language: en-US,en;q=0.9'
    -H 'Cache-Control: no-cache' -H 'Pragma: no-cache'
    -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin'
    -H 'Upgrade-Insecure-Requests: 1'
    --cookie-jar "$COOKIE_JAR" --cookie "$COOKIE_JAR" -o "$TMP"
  )
  [[ -z "$REFERER" ]] || FBI_ARGS+=(-e "$REFERER")
  set +e
  curl "${FBI_ARGS[@]}" "$URL"
  DOWNLOAD_RC=$?
  set -e
fi

# Final direct-source fallback: use a real browser TLS fingerprint. This does
# not proxy or mirror the document; bytes still come directly from URL.
if [[ "$DOWNLOAD_RC" -ne 0 && "$URL" == https://vault.fbi.gov/* ]]; then
  BROWSER_PY="$ROOT/local/tools/browser-fetch-venv/bin/python"
  if [[ -x "$BROWSER_PY" ]]; then
    echo "FBI Vault curl retries rejected; trying browser-TLS impersonation..." >&2
    rm -f "$TMP"; TMP="$(mktemp "$ROOT/local/cache/url-ingest.XXXXXX.pdf")"
    BROWSER_ARGS=("$ROOT/tools/fetch-browser-tls.py" "$URL" "$TMP")
    [[ -z "$REFERER" ]] || BROWSER_ARGS+=(--referer "$REFERER")
    set +e
    "$BROWSER_PY" "${BROWSER_ARGS[@]}"
    DOWNLOAD_RC=$?
    set -e
  else
    echo "Browser-TLS fallback is not bootstrapped. Run: bash tools/bootstrap-browser-fetch.sh" >&2
  fi
fi

if [[ "$DOWNLOAD_RC" -ne 0 ]]; then
  echo "error: download failed after all configured acquisition tiers (rc=$DOWNLOAD_RC): $URL" >&2
  echo "landing page: ${REFERER:-not supplied}" >&2
  exit "$DOWNLOAD_RC"
fi

MAGIC="$(head -c 5 "$TMP" || true)"
[[ "$MAGIC" == "%PDF-" ]] || { echo "error: downloaded artifact is not a PDF (magic: ${MAGIC@Q})" >&2; exit 4; }

set +e
OUT="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" intake "$TMP" --artifact-url "$URL" "${ARGS[@]}")"
INTAKE_RC=$?
set -e
printf '%s\n' "$OUT"
[[ "$INTAKE_RC" -eq 0 || "$INTAKE_RC" -eq 3 ]] || { echo "error: BlackIndex intake failed (rc=$INTAKE_RC)" >&2; exit "$INTAKE_RC"; }

DOC_ID="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["doc_id"])')"
if [[ "$INTAKE_RC" -eq 3 ]]; then echo "Resume: artifact already exists as $DOC_ID; skipping duplicate raw intake."; fi

BLACKINDEX_ROOT="$ROOT" python3 "$ROOT/tools/generate-review-template.py" "$DOC_ID"
python3 -W ignore::SyntaxWarning "$ROOT/tools/evidence_map.py" --root "$ROOT" integrity "$DOC_ID"
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

if [[ "$PUBLISH" -eq 1 && "$INTAKE_RC" -ne 3 ]]; then
  "$ROOT/tools/publish-ingest.sh" "$DOC_ID"
elif [[ "$PUBLISH" -eq 1 ]]; then
  echo "Resume: durable metadata/extraction for $DOC_ID already published or locally present."
fi

echo "One-shot ingest complete: $DOC_ID"
