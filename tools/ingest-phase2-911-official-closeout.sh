#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"

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
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo
echo "9/11 official closeout sprint complete. Successful/resumed artifacts: $SUCCEEDED / 4"
if (( ${#FAILURES[@]} )); then
  echo "Unresolved acquisition failures:"
  printf '  - %s\n' "${FAILURES[@]}"
  echo "These remain acquisition gaps, not evidence gaps."
fi

echo
echo "STOP GATE: do not treat repeated official statements as independent corroboration until Joint Inquiry → Commission staff/final report → CIA OIG → Operation Encore source dependencies are reviewed."
git -C "$ROOT" status --short
