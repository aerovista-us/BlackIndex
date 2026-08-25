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

The downloader presents a normal browser user-agent and, when --landing-url is
supplied, first visits that landing page to establish cookies/session state and
uses it as the HTTP Referer. This improves compatibility with government
archives that reject direct hot-link downloads.

Duplicate-by-hash intake is treated as a successful resume condition: the
existing doc_id is reused and the integrity/verification steps continue.

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

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'

# Establish the same cookie/session context a normal browser gets before
# following a document download link. Failure here is non-fatal because many
# archives do not require a landing-page session.
if [[ -n "$REFERER" ]]; then
  echo "Preflighting landing page: $REFERER"
  curl -sSL --http1.1 \
    --connect-timeout 20 --max-time 60 \
    -A "$UA" \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Accept-Language: en-US,en;q=0.9' \
    --cookie-jar "$COOKIE_JAR" --cookie "$COOKIE_JAR" \
    -o /dev/null "$REFERER" || true
fi

echo "Downloading: $URL"
CURL_ARGS=(
  -fL
  --http1.1
  --retry 3
  --retry-delay 2
  --connect-timeout 20
  --max-time 300
  --compressed
  -A "$UA"
  -H 'Accept: application/pdf,application/octet-stream;q=0.9,*/*;q=0.8'
  -H 'Accept-Language: en-US,en;q=0.9'
  --cookie-jar "$COOKIE_JAR"
  --cookie "$COOKIE_JAR"
  -o "$TMP"
)
if [[ -n "$REFERER" ]]; then
  CURL_ARGS+=(-e "$REFERER")
fi

set +e
curl "${CURL_ARGS[@]}" "$URL"
DOWNLOAD_RC=$?
set -e

# FBI Vault currently serves these PDFs to browsers while sometimes rejecting
# direct CLI hot-links. Retry once with browser navigation headers after the
# landing-page cookie preflight. This remains a direct FBI download; no mirror
# is substituted and provenance stays on the FBI artifact URL.
if [[ "$DOWNLOAD_RC" -ne 0 && "$URL" == https://vault.fbi.gov/* ]]; then
  echo "FBI Vault direct download rejected; retrying with browser-navigation headers..." >&2
  rm -f "$TMP"
  TMP="$(mktemp "$ROOT/local/cache/url-ingest.XXXXXX.pdf")"
  set +e
  curl -fL --http1.1 --retry 2 --retry-delay 2 \
    --connect-timeout 20 --max-time 300 --compressed \
    -A "$UA" \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf;q=0.8,*/*;q=0.7' \
    -H 'Accept-Language: en-US,en;q=0.9' \
    -H 'Cache-Control: no-cache' \
    -H 'Pragma: no-cache' \
    -H 'Sec-Fetch-Dest: document' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Upgrade-Insecure-Requests: 1' \
    --cookie-jar "$COOKIE_JAR" --cookie "$COOKIE_JAR" \
    ${REFERER:+-e "$REFERER"} \
    -o "$TMP" "$URL"
  DOWNLOAD_RC=$?
  set -e
fi

if [[ "$DOWNLOAD_RC" -ne 0 ]]; then
  echo "error: download failed after browser-session retry (curl rc=$DOWNLOAD_RC): $URL" >&2
  echo "landing page: ${REFERER:-not supplied}" >&2
  exit "$DOWNLOAD_RC"
fi

# Guard against accidentally ingesting an HTML error/landing page as a PDF.
MAGIC="$(head -c 5 "$TMP" || true)"
if [[ "$MAGIC" != "%PDF-" ]]; then
  echo "error: downloaded artifact is not a PDF (magic: ${MAGIC@Q})" >&2
  exit 4
fi

# Intake returns rc=3 for an artifact whose SHA-256 is already present. In a
# resumable batch that is success, not failure: reuse the existing doc_id and
# continue with review/integrity/verification without creating a second record.
set +e
OUT="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" intake "$TMP" \
  --artifact-url "$URL" "${ARGS[@]}")"
INTAKE_RC=$?
set -e
printf '%s\n' "$OUT"

if [[ "$INTAKE_RC" -ne 0 && "$INTAKE_RC" -ne 3 ]]; then
  echo "error: BlackIndex intake failed (rc=$INTAKE_RC)" >&2
  exit "$INTAKE_RC"
fi

DOC_ID="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["doc_id"])')"
if [[ "$INTAKE_RC" -eq 3 ]]; then
  echo "Resume: artifact already exists as $DOC_ID; skipping duplicate raw intake."
fi

# Replace only legacy auto-generated TODO stubs. Existing substantive reviews
# are intentionally preserved.
BLACKINDEX_ROOT="$ROOT" python3 "$ROOT/tools/generate-review-template.py" "$DOC_ID"

# Ensure the first-class Record Integrity sidecar exists for every new intake.
python3 -W ignore::SyntaxWarning "$ROOT/tools/evidence_map.py" --root "$ROOT" integrity "$DOC_ID"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

if [[ "$PUBLISH" -eq 1 && "$INTAKE_RC" -ne 3 ]]; then
  "$ROOT/tools/publish-ingest.sh" "$DOC_ID"
elif [[ "$PUBLISH" -eq 1 ]]; then
  echo "Resume: durable metadata/extraction for $DOC_ID already published or locally present."
fi

echo "One-shot ingest complete: $DOC_ID"
