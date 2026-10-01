#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

bash "$ROOT/tools/ingest-url.sh" \
  "https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/S-510092_placeholder.pdf" \
  --landing-url "https://www.esd.whs.mil/Directives/issuances/dodi/" \
  --source DOD --collection "DoD Controlled-Issuance Placeholders" \
  --year 2009 --document-date 2009-05-11 \
  --title "DoDI S-5100.92 — Defense and National Leadership Command Capability (DNLCC) Governance — Public Placeholder" \
  --native-id DoDI-S-5100.92-PLACEHOLDER \
  --call-id CALL-NC3-GOVERNANCE-CURRENCY-001 \
  --tags "nc3,nlcc,dnlcc,governance,controlled-document,access-boundary,public-placeholder" \
  --publish

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "NC3 governance currency supplement complete."
echo "The S-5100.92 record is the public placeholder only; controlled contents remain unavailable."
