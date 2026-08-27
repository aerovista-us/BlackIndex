#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"
REPORT="$ROOT/docs/run-reports/2026-08-27-911-official-closeout.md"

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

# Controlled closeout sprint for the 9/11 official-interpretation layer.
#
# The Joint Inquiry final report is already present in Git-backed metadata as
# US CONGRESS-2002-9-11-joint-inquiry-001. This sprint fills the remaining
# official-baseline gaps using stable government-preserved sources and adds
# the CIA OIG accountability review. These records are interpretation/review
# layers; repeated statements must not be counted as independent corroboration
# until their underlying source genealogy is mapped.

run_one "9/11 Commission Final Report — official U.S. Government edition" \
  "https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Final Report" --year 2004 --document-date "2004-07-22" \
  --title "The 9/11 Commission Report — Final Report of the National Commission on Terrorist Attacks Upon the United States" \
  --native-id "GPO-911REPORT" \
  --landing-url "https://www.govinfo.gov/app/details/GPO-911REPORT" \
  --call-id CALL-911-OFFICIAL-CLOSEOUT \
  --tags "9-11,commission,final-report,official-government-edition,hazmi,mihdhar,bayoumi,thumairy,official-interpretation" --publish

run_one "9/11 Commission Staff Monograph — Terrorist Financing (GovInfo preserved)" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-Y3-PURL-LPS53198/pdf/GOVPUB-Y3-PURL-LPS53198.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Staff Monographs" --year 2004 --document-date "2004-08-21" \
  --title "Monograph on Terrorist Financing — Staff Report to the 9/11 Commission" \
  --native-id "GOVPUB-Y3-PURL-LPS53198" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-Y3-PURL-LPS53198" \
  --call-id CALL-911-OFFICIAL-CLOSEOUT \
  --tags "9-11,commission,staff-monograph,terrorist-financing,negative-findings,official-interpretation,govinfo" --publish

run_one "9/11 Commission Staff Monograph — 9/11 and Terrorist Travel (GovInfo preserved)" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-Y3-PURL-LPS53197/pdf/GOVPUB-Y3-PURL-LPS53197.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Staff Monographs" --year 2004 --document-date "2004-08-21" \
  --title "9/11 and Terrorist Travel — Staff Report of the National Commission on Terrorist Attacks Upon the United States" \
  --native-id "GOVPUB-Y3-PURL-LPS53197" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-Y3-PURL-LPS53197" \
  --call-id CALL-911-OFFICIAL-CLOSEOUT \
  --tags "9-11,commission,staff-monograph,terrorist-travel,hazmi,mihdhar,watchlisting,border-security,official-interpretation,govinfo" --publish

run_one "CIA OIG — Report on CIA Accountability With Respect to the 9/11 Attacks" \
  "https://www.cia.gov/readingroom/docs/DOC_0006184107.pdf" \
  --source "CIA" --collection "9/11 CIA Accountability" --year 2005 \
  --title "OIG Report on CIA Accountability With Respect to the 9/11 Attacks" \
  --native-id "C06184107" \
  --landing-url "https://www.cia.gov/stories/story/cia-releases-declassified-documents-related-to-9-11-attacks/" \
  --call-id CALL-911-OFFICIAL-CLOSEOUT \
  --tags "9-11,cia,oig,accountability,joint-inquiry,intelligence-sharing,analytic-failures,negative-findings,official-review" --publish

# Refresh durable indexes and generated research surfaces for whichever records
# actually acquired. Acquisition failure is an acquisition gap, not evidence
# that the underlying document does not exist.
python3 -W error::SyntaxWarning -m py_compile "$ROOT/tools/evidence_map.py"
python3 "$EVIDENCE" --root "$ROOT" bootstrap
python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-record-context.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-session.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-export.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-favicon.py" "$ROOT/local/dashboard/blackindex-dashboard.html"

# Capture the authoritative local verifier output instead of requiring the
# operator to copy it back into chat. The durable run report below is safe to
# publish because it contains only status/provenance metadata, never raw source
# bytes or normalized corpus text.
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

echo
echo "9/11 official closeout sprint complete. Successful/resumed artifacts: $SUCCEEDED / 4"
if (( ${#FAILURES[@]} )); then
  echo "Unresolved acquisition failures:"
  printf '  - %s\n' "${FAILURES[@]}"
  echo "These remain acquisition gaps, not evidence gaps."
fi

echo
echo "STOP GATE: do not treat repeated official statements as independent corroboration until Joint Inquiry → Commission staff/final report → CIA OIG → Operation Encore source dependencies are reviewed."

mkdir -p "$(dirname "$REPORT")"
FAIL_TEXT=""
if (( ${#FAILURES[@]} )); then
  for failure in "${FAILURES[@]}"; do
    FAIL_TEXT+="- ${failure}"$'\n'
  done
fi
export BLACKINDEX_SPRINT_FAILURES="$FAIL_TEXT"
export BLACKINDEX_SPRINT_VERIFY_JSON="$VERIFY_JSON"
python3 - "$ROOT" "$REPORT" "$SUCCEEDED" "$VERIFY_RC" <<'PY'
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import sys

root = Path(sys.argv[1])
report = Path(sys.argv[2])
succeeded = int(sys.argv[3])
verify_rc = int(sys.argv[4])

records = []
for path in sorted((root / "metadata").glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue
    if data.get("call_id") == "CALL-911-OFFICIAL-CLOSEOUT":
        records.append(data)

verify_raw = os.environ.get("BLACKINDEX_SPRINT_VERIFY_JSON", "").strip()
try:
    verify = json.loads(verify_raw) if verify_raw else None
except Exception:
    verify = None

fail_text = os.environ.get("BLACKINDEX_SPRINT_FAILURES", "").strip()
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
lines = [
    "# BlackIndex Controlled Ingest Run — 9/11 Official-Layer Closeout",
    "",
    f"- **Completed UTC:** {now}",
    "- **Call ID:** `CALL-911-OFFICIAL-CLOSEOUT`",
    f"- **Successful/resumed acquisition calls:** **{succeeded} / 4**",
    f"- **Verifier exit code:** `{verify_rc}`",
]
if isinstance(verify, dict):
    lines += [
        f"- **Verifier checked:** `{verify.get('checked', 'unknown')}`",
        f"- **Verifier ok:** `{verify.get('ok', 'unknown')}`",
        f"- **Verifier failures:** `{len(verify.get('failures', [])) if isinstance(verify.get('failures'), list) else 'unknown'}`",
    ]
lines += [
    "",
    "> This is an acquisition/provenance run record, not a historical conclusion. Acquisition failures remain acquisition gaps, not evidence gaps.",
    "",
    "## Durable records produced by this sprint",
    "",
]
if records:
    for data in records:
        lines += [
            f"### {data.get('title') or data.get('doc_id')}",
            "",
            f"- Document ID: `{data.get('doc_id', '')}`",
            f"- Source: {data.get('source', '')}",
            f"- Document date: {data.get('document_date') or data.get('year_bucket') or ''}",
            f"- Native ID: `{data.get('native_id') or ''}`",
            f"- SHA-256: `{data.get('sha256') or ''}`",
            f"- Artifact: {data.get('artifact_url') or data.get('source_url') or ''}",
            f"- Evidence status: `{data.get('evidence_status') or 'unknown'}`",
            "",
        ]
else:
    lines += ["_No metadata records with this call ID were present at report generation time._", ""]

lines += ["## Acquisition failures", ""]
if fail_text:
    lines += fail_text.splitlines()
else:
    lines += ["_None reported by the sprint._"]

lines += [
    "",
    "## Local verifier output",
    "",
    "```json",
    verify_raw or "{}",
    "```",
    "",
    "## Stop gate",
    "",
    "Do not treat repeated official statements across the Joint Inquiry, Commission staff work, Commission final report, CIA OIG, and Operation Encore as independent corroboration until their underlying source genealogy is reviewed.",
    "",
]
report.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote durable sprint report: {report}")
PY

# Publish only the generated run report, and only when there was no unrelated
# content already staged. Each successful document was already published by
# publish-ingest.sh with its own integrity gate.
PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving sprint report uncommitted to avoid mixing unrelated work:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet; then
    git -C "$ROOT" commit -m "BlackIndex: record 9/11 official closeout sprint result"
    git -C "$ROOT" push
    echo "Published durable sprint result."
  else
    echo "Sprint report unchanged; nothing new to publish."
  fi
fi

git -C "$ROOT" status --short

# Preserve verifier failure as the overall sprint exit status after the report
# has been written/published, so automation can still detect an integrity gate
# failure without losing the diagnostic record.
if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
