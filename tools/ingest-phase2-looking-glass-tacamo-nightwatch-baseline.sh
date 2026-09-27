#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

run_ingest(){
  bash "$ROOT/tools/ingest-url.sh" "$@" --publish
}

run_ingest \
  "https://www.stratcom.mil/Portals/8/Documents/2024%20USSTRATCOM%20Congressional%20Posture%20Statement.pdf" \
  --landing-url "https://www.stratcom.mil/" \
  --source USSTRATCOM --collection "Congressional Posture Statements" \
  --year 2024 --document-date 2024-02-29 \
  --title "Statement of Anthony J. Cotton, Commander, United States Strategic Command, Before the Senate Committee on Armed Services" \
  --native-id 2024-USSTRATCOM-SASC-POSTURE \
  --call-id CALL-LOOKING-GLASS-TACAMO-NIGHTWATCH-001 \
  --tags "looking-glass,tacamo,nightwatch,naoc,e-6b,e-4b,nc3,usstratcom,official-government-report"

run_ingest \
  "https://media.defense.gov/2020/May/18/2002302043/-1/-1/1/NPG17.PDF" \
  --landing-url "https://www.navy.mil/" \
  --source "US NAVY" --collection "Program Guides" \
  --year 2017 \
  --title "U.S. Navy Program Guide 2017" \
  --native-id NPG17 \
  --call-id CALL-LOOKING-GLASS-TACAMO-NIGHTWATCH-001 \
  --tags "looking-glass,tacamo,e-6b,airborne-command-post,nc3,navy-program-guide,official-government-report"

run_ingest \
  "https://static.e-publishing.af.mil/production/1/af_a3/publication/afman11-2e-4bv3/afman11-2e-4v3.pdf" \
  --landing-url "https://www.e-publishing.af.mil/" \
  --source USAF --collection "Air Force Manuals" \
  --year 2019 --document-date 2019-07-09 \
  --title "E-4B Operations Procedures" --native-id AFMAN11-2E-4BV3 \
  --call-id CALL-LOOKING-GLASS-TACAMO-NIGHTWATCH-001 \
  --tags "looking-glass,nightwatch,naoc,e-4b,nc3,command-control,official-usaf-manual"

python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "LOOKING GLASS TACAMO / NIGHTWATCH baseline complete."
echo "This sprint preserves mission/command-source records only; it does not promote detailed operating procedures into analytical conclusions."
