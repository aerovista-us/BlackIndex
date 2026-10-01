#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

run_ingest(){
  bash "$ROOT/tools/ingest-url.sh" "$@" --publish
}

run_ingest \
  "https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2026/FY2026_r1.pdf" \
  --landing-url "https://comptroller.defense.gov/Budget-Materials/" \
  --source DOD --collection "FY 2026 RDT&E Programs R-1" \
  --year 2025 \
  --title "FY 2026 RDT&E Programs (R-1)" --native-id FY2026-R1 \
  --call-id CALL-NC3-PROGRAM-GENEALOGY-001 \
  --tags "nc3,saoc,rdte,budget,program-record,official-dod-budget"
run_ingest \
  "https://www.secnav.navy.mil/fmc/fmb/Documents/26pres/RDTEN_BA1-3_Book.pdf" \
  --landing-url "https://www.secnav.navy.mil/fmc/fmb/Pages/Fiscal-Year-2026.aspx" \
  --source US_NAVY --collection "FY 2026 RDT&E Budget Justification Books" \
  --year 2025 \
  --title "Department of the Navy FY 2026 RDT&E Budget Estimates — BA 1-3 Justification Book" \
  --native-id FY26-RDTEN-BA1-3 \
  --call-id CALL-NC3-PROGRAM-GENEALOGY-001 \
  --tags "nc3,tacamo,e-130j,rdte,budget,program-record,official-navy-budget"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "NC3 program-genealogy parent intake complete."
echo "These budget artifacts document program/funding lineage; they are not operating orders, technical procedures, or proof of operational use."
