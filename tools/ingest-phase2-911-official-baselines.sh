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

# These are official interpretation / inquiry baselines for the existing
# Operation Encore cluster. They do not replace underlying FBI records and
# must not be counted as independent corroboration when they rely on the same
# underlying interviews, serials, intelligence reporting, or liaison material.

run_one "Joint Inquiry Final Report — declassified public version" \
  "https://www.govinfo.gov/content/pkg/CRPT-107hrpt792/pdf/CRPT-107hrpt792.pdf" \
  --source "US Congress" --collection "9/11 Joint Inquiry" --year 2002 --document-date "2002-12-20" \
  --title "Joint Inquiry into Intelligence Community Activities Before and After the Terrorist Attacks of September 11, 2001 — Declassified Final Report" \
  --native-id "S.Rept.107-351-H.Rept.107-792" \
  --landing-url "https://www.govinfo.gov/app/details/CRPT-107hrpt792/CRPT-107hrpt792" \
  --call-id CALL-911-OFFICIAL-BASELINES \
  --tags "9-11,joint-inquiry,congress,foreign-support,bayoumi,hazmi,mihdhar,official-interpretation,declassified-report" --publish

run_one "9/11 Commission Report — Chapter 7: The Attack Looms" \
  "https://www.9-11commission.gov/report/911Report_Ch7.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Official Baselines" --year 2004 --document-date "2004-07-22" \
  --title "The 9/11 Commission Report — Chapter 7: The Attack Looms" \
  --native-id "911Report-Ch7" \
  --landing-url "https://www.9-11commission.gov/report/" \
  --call-id CALL-911-OFFICIAL-BASELINES \
  --tags "9-11,commission,chapter-7,hazmi,mihdhar,bayoumi,thumairy,abdullah,official-interpretation" --publish

run_one "9/11 Commission Staff Monograph — Terrorist Financing" \
  "https://www.9-11commission.gov/staff_statements/911_TerrFin_Monograph.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Staff Monographs" --year 2004 --document-date "2004-08-21" \
  --title "9/11 Commission Staff Monograph on Terrorist Financing" \
  --native-id "911-TerrFin-Monograph" \
  --landing-url "https://www.9-11commission.gov/staff_statements/" \
  --call-id CALL-911-OFFICIAL-BASELINES \
  --tags "9-11,commission,staff-monograph,terrorist-financing,negative-findings,official-interpretation" --publish

run_one "9/11 Commission Staff Monograph — 9/11 and Terrorist Travel" \
  "https://www.9-11commission.gov/staff_statements/911_TerrTrav_Monograph.pdf" \
  --source "9/11 Commission" --collection "9/11 Commission Staff Monographs" --year 2004 --document-date "2004-08-21" \
  --title "9/11 and Terrorist Travel — Staff Report of the National Commission on Terrorist Attacks Upon the United States" \
  --native-id "911-TerrTrav-Monograph" \
  --landing-url "https://www.9-11commission.gov/staff_statements/" \
  --call-id CALL-911-OFFICIAL-BASELINES \
  --tags "9-11,commission,staff-monograph,terrorist-travel,hazmi,mihdhar,watchlisting,official-interpretation" --publish

# Refresh durable indexes and generated local research surfaces for whichever
# documents actually acquired. Acquisition failure is recorded as an
# acquisition gap; it is not evidence that the underlying record is absent.
python3 -W error::SyntaxWarning -m py_compile "$ROOT/tools/evidence_map.py"
python3 "$EVIDENCE" --root "$ROOT" bootstrap
python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-record-context.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-session.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/inject-research-export.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo
echo "9/11 official-baseline pass complete. Successful/resumed artifacts: $SUCCEEDED / 4"
if (( ${#FAILURES[@]} )); then
  echo "Unresolved acquisition failures:"
  printf '  - %s\n' "${FAILURES[@]}"
  echo "These remain acquisition gaps, not evidence gaps."
fi

echo
echo "Review requirement: classify these records as official inquiry/interpretation layers and map their source dependencies before treating repeated assertions as corroboration."
git -C "$ROOT" status --short
