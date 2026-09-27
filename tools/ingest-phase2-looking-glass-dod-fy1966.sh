#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
CALL_ID="CALL-LOOKING-GLASS-DOD-FY1966"

# Contemporaneous DoD annual program report. This is closer to the program-management
# layer than a retrospective history, but it is still not an Emergency War Order or
# nuclear-use authorization.
"$INGEST" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-D-ed021da2d13644089b28ae2bdeffefd8/pdf/GOVPUB-D-ed021da2d13644089b28ae2bdeffefd8.pdf" \
  --source "DOD" \
  --collection "Department of Defense Annual Reports" \
  --year 1967 \
  --title "Department of Defense Annual Report for Fiscal Year 1966, Including the Reports of the Secretary of Defense, Secretary of the Army, Secretary of the Navy, Secretary of the Air Force" \
  --native-id "GOVPUB-D-ed021da2d13644089b28ae2bdeffefd8" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-D-ed021da2d13644089b28ae2bdeffefd8" \
  --call-id "$CALL_ID" \
  --tags "looking-glass,paccs,airborne-launch-control,ec-135,nuclear-command-control,strategic-retaliatory-forces,dod-annual-report,official-government-report" \
  --publish

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "LOOKING GLASS DoD FY1966 program-record sprint complete."
echo "No claim is made that this annual report supplies the complete EWO/SIOP authority chain or operating procedure."
