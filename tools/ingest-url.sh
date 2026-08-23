#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

usage() {
  cat >&2 <<'EOF'
usage: tools/ingest-url.sh <artifact-url> [--publish] [blackindex intake args...]

Downloads one remote artifact into local/cache, ingests + normalizes it,
verifies the local vault, and optionally publishes only metadata/extraction.

Example:
  tools/ingest-url.sh https://example.gov/doc.pdf \
    --source NARA --collection "Example" --year 1975 \
    --title "Example document" --call-id CALL-999 --publish
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

URL="$1"
shift
PUBLISH=0
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish)
      PUBLISH=1
      shift
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
cleanup() { rm -f "$TMP"; }
trap cleanup EXIT

echo "Downloading: $URL"
curl -fL --retry 3 --retry-delay 2 --connect-timeout 20 \
  -A 'BlackIndex/0.1 (+https://github.com/aerovista-us/BlackIndex)' \
  -o "$TMP" "$URL"

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
