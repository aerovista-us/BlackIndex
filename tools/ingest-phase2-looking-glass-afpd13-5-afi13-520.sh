#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

run_ingest(){
  bash "$ROOT/tools/ingest-url.sh" "$@" --publish
}

run_ingest \
  "https://static.e-publishing.af.mil/production/1/af_a10/publication/afpd13-5/afpd13-5.pdf" \
  --landing-url "https://www.e-publishing.af.mil/" \
  --source USAF --collection "Air Force Policy Directives" \
  --year 2018 --document-date 2018-07-17 \
  --title "Air Force Nuclear Mission" --native-id AFPD13-5 \
  --call-id CALL-LOOKING-GLASS-AUTHORITY-FAMILY-001 \
  --tags "looking-glass,nuclear-command-control,air-force-nuclear-mission,policy-directive,official-usaf-directive"

run_ingest \
  "https://static.e-publishing.af.mil/production/1/af_a10/publication/afi13-520/afi13-520.pdf" \
  --landing-url "https://www.e-publishing.af.mil/" \
  --source USAF --collection "Air Force Instructions" \
  --year 2018 --document-date 2018-08-22 \
  --title "Aircraft and ICBM Nuclear Operations" --native-id AFI13-520 \
  --call-id CALL-LOOKING-GLASS-AUTHORITY-FAMILY-001 \
  --tags "looking-glass,nuclear-command-control,icbm,nuclear-operations,afi13-530-successor,official-usaf-directive"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "LOOKING GLASS AFPD13-5 / AFI13-520 authority-family sprint complete."
echo "AFI13-530 remains a superseded historical source target; do not treat AFI13-520 as a byte/content substitute."
