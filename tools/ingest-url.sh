#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

usage() {
  cat >&2 <<'EOF'
usage: tools/ingest-url.sh <artifact-url> [--publish] [blackindex intake args...]

Downloads one remote artifact into local/cache, ingests + normalizes it,
verifies the local vault, and optionally publishes only metadata/extraction.

The downloader presents a normal browser user-agent and, when --landing-url is
supplied, uses that page as the HTTP Referer. This improves compatibility with
legacy government archives while preserving the supplied provenance metadata.

Example:
  tools/ingest-url.sh https://example.gov/doc.pdf \
    --source NARA --collection "Example" --year 1975 \
    --title "Example document" --landing-url https://example.gov/record \
    --call-id CALL-999 --publish
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

URL="$1"
shift
PUBLISH=0
REFERER=""
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish)
      PUBLISH=1
      shift
      ;;
    --landing-url)
      if [[ $# -lt 2 ]]; then
        echo "error: --landing-url requires a value" >&2
        exit 2
      fi
      REFERER="$2"
      ARGS+=("$1" "$2")
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

command -v curl >/dev/null 2>&1 || { echo "error: curl is required" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "error: python3 is required" >&2; exit 2; }

mkdir -p "$ROOT/local/cache"
TMP="$(mktemp "$ROOT/local/cache/url-ingest.XXXXXX.pdf")"
COOKIE_JAR="$(mktemp "$ROOT/local/cache/url-ingest.cookies.XXXXXX")"
cleanup() { rm -f "$TMP" "$COOKIE_JAR"; }
trap cleanup EXIT

echo "Downloading: $URL"
CURL_ARGS=(
  -fL
  --retry 3
  --retry-delay 2
  --connect-timeout 20
  --max-time 300
  --compressed
  -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/151 Safari/537.36'
  -H 'Accept: application/pdf,application/octet-stream;q=0.9,*/*;q=0.8'
  --cookie-jar "$COOKIE_JAR"
  --cookie "$COOKIE_JAR"
  -o "$TMP"
)
if [[ -n "$REFERER" ]]; then
  CURL_ARGS+=(-e "$REFERER")
fi
curl "${CURL_ARGS[@]}" "$URL"

# Guard against accidentally ingesting an HTML error/landing page as a PDF.
MAGIC="$(head -c 5 "$TMP" || true)"
if [[ "$MAGIC" != "%PDF-" ]]; then
  echo "error: downloaded artifact is not a PDF (magic: ${MAGIC@Q})" >&2
  exit 4
fi

OUT="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" intake "$TMP" \
  --artifact-url "$URL" "${ARGS[@]}")"
printf '%s\n' "$OUT"

DOC_ID="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["doc_id"])')"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

if [[ "$PUBLISH" -eq 1 ]]; then
  "$ROOT/tools/publish-ingest.sh" "$DOC_ID"
fi

echo "One-shot ingest complete: $DOC_ID"
