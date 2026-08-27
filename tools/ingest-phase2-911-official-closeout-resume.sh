#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"
CALL_ID="CALL-911-OFFICIAL-CLOSEOUT-RESUME"
REPORT="$ROOT/docs/run-reports/2026-08-27-911-official-closeout-resume.md"

FAILURES=()
SUCCEEDED=0

run_one(){
  local label="$1"
  shift
  echo
  echo "=== $label ==="
  if "$INGEST" "$@"; then
    SUCCEEDED=$((SUCCEEDED + 1))
  else
    local rc=$?
    echo "warning: skipped after acquisition/intake failure (rc=$rc): $label" >&2
    FAILURES+=("$label (rc=$rc)")
  fi
}

# Recovery for the two staff monographs that collided in the shared
# "9/11 Commission Staff Monographs" collection namespace. The immutable raw
# file that already occupies -001 is intentionally left untouched. Each
# monograph now gets a distinct canonical collection namespace so intake can
# assign an unambiguous document ID without overwriting or guessing about the
# prior orphan/local artifact.

run_one "9/11 Commission Staff Monograph — Terrorist Financing (GovInfo preserved)" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-Y3-PURL-LPS53198/pdf/GOVPUB-Y3-PURL-LPS53198.pdf" \
  --source "9/11 Commission" \
  --collection "9/11 Commission Terrorist Financing Staff Monograph" \
  --year 2004 --document-date "2004-08-21" \
  --title "Monograph on Terrorist Financing — Staff Report to the 9/11 Commission" \
  --native-id "GOVPUB-Y3-PURL-LPS53198" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-Y3-PURL-LPS53198" \
  --call-id "$CALL_ID" \
  --tags "9-11,commission,staff-monograph,terrorist-financing,negative-findings,official-interpretation,govinfo" --publish

run_one "9/11 Commission Staff Monograph — 9/11 and Terrorist Travel (GovInfo preserved)" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-Y3-PURL-LPS53197/pdf/GOVPUB-Y3-PURL-LPS53197.pdf" \
  --source "9/11 Commission" \
  --collection "9/11 Commission Terrorist Travel Staff Monograph" \
  --year 2004 --document-date "2004-08-21" \
  --title "9/11 and Terrorist Travel — Staff Report of the National Commission on Terrorist Attacks Upon the United States" \
  --native-id "GOVPUB-Y3-PURL-LPS53197" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-Y3-PURL-LPS53197" \
  --call-id "$CALL_ID" \
  --tags "9-11,commission,staff-monograph,terrorist-travel,hazmi,mihdhar,watchlisting,border-security,official-interpretation,govinfo" --publish

# Refresh local evidence/index/UI state and verify the entire corpus.
python3 -W error::SyntaxWarning -m py_compile "$ROOT/tools/evidence_map.py"
python3 "$EVIDENCE" --root "$ROOT" bootstrap
python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-record-context.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-session.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-export.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-favicon.py" "$ROOT/local/dashboard/blackindex-dashboard.html"

VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
printf '%s\n' "$VERIFY_JSON"

mkdir -p "$(dirname "$REPORT")"
python3 - "$ROOT" "$CALL_ID" "$REPORT" "$SUCCEEDED" "$VERIFY_RC" "$VERIFY_JSON" "${FAILURES[@]}" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
call_id = sys.argv[2]
report = Path(sys.argv[3])
succeeded = int(sys.argv[4])
verify_rc = int(sys.argv[5])
verify = json.loads(sys.argv[6])
failures = sys.argv[7:]

records = []
for path in sorted((root / "metadata").glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue
    if data.get("call_id") == call_id:
        records.append(data)

lines = [
    "# BlackIndex Controlled Ingest Resume — 9/11 Official-Layer Closeout",
    "",
    f"- **Completed UTC:** {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
    f"- **Call ID:** `{call_id}`",
    f"- **Successful/resumed acquisition calls:** **{succeeded} / 2**",
    f"- **Verifier exit code:** `{verify_rc}`",
    f"- **Verifier checked:** `{verify.get('checked')}`",
    f"- **Verifier ok:** `{verify.get('ok')}`",
    f"- **Verifier failures:** `{len(verify.get('failures') or [])}`",
    "",
    "> Recovery note: the original shared collection namespace contained an existing immutable `-001` raw artifact with no usable metadata slot for these retries. This resume deliberately used distinct canonical collection namespaces and did not overwrite or delete that artifact.",
    "",
    "## Durable records produced by this resume",
    "",
]
for data in records:
    lines += [
        f"### {data.get('title')}", "",
        f"- Document ID: `{data.get('doc_id')}`",
        f"- Source: {data.get('source')}",
        f"- Document date: {data.get('document_date') or 'Unknown'}",
        f"- Native ID: `{data.get('native_id') or 'Not recorded'}`",
        f"- SHA-256: `{data.get('sha256')}`",
        f"- Artifact: {data.get('artifact_url') or data.get('source_url')}",
        f"- Evidence status: `{data.get('evidence_status')}`",
        "",
    ]
lines += ["## Acquisition failures", ""]
if failures:
    lines += [f"- {item}" for item in failures]
else:
    lines.append("- None")
lines += [
    "",
    "## Local verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
    "## Stop gate",
    "",
    "Do not treat repeated official statements across the Joint Inquiry, Commission staff work, Commission final report, CIA OIG, and Operation Encore as independent corroboration until their underlying source genealogy is reviewed.",
    "",
]
report.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote durable resume report: {report}")
PY

# Publish only the run report here. Per-document metadata/extractions are
# already published by ingest-url.sh --publish. Record-integrity files remain
# separate durable evidence objects and are not auto-committed by this recovery
# pass merely to make the working tree clean.
if git -C "$ROOT" status --short -- "$REPORT" | grep -q .; then
  git -C "$ROOT" add -- "$REPORT"
  git -C "$ROOT" commit -m "BlackIndex: record 9/11 official closeout resume result"
  git -C "$ROOT" push
  echo "Published durable resume result."
fi

echo
echo "9/11 official closeout resume complete. Successful/resumed artifacts: $SUCCEEDED / 2"
if (( ${#FAILURES[@]} )); then
  echo "Unresolved acquisition failures:"
  printf '  - %s\n' "${FAILURES[@]}"
  echo "These remain acquisition gaps, not evidence gaps."
fi

echo
echo "STOP GATE: source genealogy review comes next. Do not open a new corpus cluster yet."
git -C "$ROOT" status --short
