#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

run_ingest(){
  bash "$ROOT/tools/ingest-url.sh" "$@" --publish
}

run_ingest \
  "https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/374101p.pdf" \
  --landing-url "https://www.esd.whs.mil/Directives/issuances/dodi/" \
  --source DOD --collection "DoD Instructions" \
  --year 2013 --document-date 2013-05-01 \
  --title "National Leadership Command Capabilities (NLCC) Configuration Management (CM)" --native-id DoDI3741.01 \
  --call-id CALL-NC3-GOVERNANCE-001 \
  --tags "nc3,nlcc,configuration-management,governance,dod-instruction,public"
run_ingest \
  "https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/370001p.pdf?ver=2019-06-06-120430-787" \
  --landing-url "https://www.esd.whs.mil/Directives/issuances/dodd/" \
  --source DOD --collection "DoD Directives" \
  --year 2014 --document-date 2014-10-22 \
  --title "DoD Command and Control Enabling Capabilities" --native-id DoDD3700.01 \
  --call-id CALL-NC3-GOVERNANCE-001 \
  --tags "nc3,nlcc,command-control,governance,dod-directive,public"

run_ingest \
  "https://www.jcs.mil/Portals/36/Documents/Library/Instructions/5119_01.pdf" \
  --landing-url "https://www.jcs.mil/Library/CJCS-Instructions/" \
  --source JCS --collection "CJCS Instructions" \
  --year 2007 --document-date 2007-12-14 \
  --title "Charter for the Centralized Direction, Management, Operation, and Technical Support of the Nuclear Command, Control, and Communications System" --native-id CJCSI5119.01C \
  --call-id CALL-NC3-GOVERNANCE-001 \
  --tags "nc3,nuclear-command-control,joint-staff,governance,charter,public"
run_ingest \
  "https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/S-373001_placeholder.pdf?ver=NLAFQ5huSsRUMvJxGNO7bQ%3D%3D" \
  --landing-url "https://www.esd.whs.mil/Directives/issuances/dodi/" \
  --source DOD --collection "DoD Controlled-Issuance Placeholders" \
  --year 2015 --document-date 2015-11-06 \
  --title "DoDI S-3730.01 — Nuclear Command, Control, and Communications (NC3) System — Public Placeholder" --native-id DoDI-S-3730.01-PLACEHOLDER \
  --call-id CALL-NC3-GOVERNANCE-001 \
  --tags "nc3,controlled-document,access-boundary,dod-instruction,public-placeholder"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "NC3 governance baseline ingest complete."
echo "The S-3730.01 corpus record is the public placeholder only; it is not the controlled instruction contents."
