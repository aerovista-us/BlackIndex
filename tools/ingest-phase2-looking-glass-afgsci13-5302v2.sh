#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"

URL="https://static.e-publishing.af.mil/production/1/afgsc/publication/afgsci13-5302v2/afgsci13-5302v2.pdf"
LANDING="https://www.e-publishing.af.mil/"

echo "Ingesting official AFGSC ALCS crew Stan/Eval directive..."
"$INGEST" "$URL" \
  --source "USAF" \
  --collection "Air Force Global Strike Command Instructions" \
  --year 2017 \
  --document-date "2017-07-19" \
  --title "Airborne Launch Control System (ALCS) Crew Standardization and Evaluation" \
  --native-id "AFGSCI13-5302V2" \
  --landing-url "$LANDING" \
  --call-id "CALL-LOOKING-GLASS-AFGSCI13-5302V2" \
  --tags "looking-glass,alcs,afgsc,crew-standardization,evaluation,emergency-war-order,nuclear-command-control,official-usaf-directive" \
  --publish
