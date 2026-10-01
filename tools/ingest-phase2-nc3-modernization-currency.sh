#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

run_ingest(){
  bash "$ROOT/tools/ingest-url.sh" "$@" --publish
}

run_ingest \
  "https://media.defense.gov/2022/Oct/27/2003103845/-1/-1/1/2022-NUCLEAR-POSTURE-REVIEW.PDF" \
  --landing-url "https://www.defense.gov/News/Releases/Release/Article/3201683/department-of-defense-releases-its-2022-strategic-reviews-national-defense-stra/" \
  --source DOD --collection "National Defense Strategy and Nuclear Posture Reviews" \
  --year 2022 --document-date 2022-10-27 \
  --title "2022 National Defense Strategy, Nuclear Posture Review, and Missile Defense Review" \
  --native-id 2022-NDS-NPR-MDR \
  --call-id CALL-NC3-MODERNIZATION-CURRENCY-001 \
  --tags "nc3,nuclear-posture-review,nuclear-modernization,national-defense-strategy,official-dod-strategy"
run_ingest \
  "https://www.stratcom.mil/Portals/8/Documents/2025%20USSTRATCOM%20Congressional%20Posture%20Statement.pdf?ver=CxQgRM89pGjF2tuITb4GMQ%3D%3D" \
  --landing-url "https://www.stratcom.mil/" \
  --source USSTRATCOM --collection "Congressional Posture Statements" \
  --year 2025 --document-date 2025-03-26 \
  --title "Statement of Anthony J. Cotton, Commander, United States Strategic Command, Before the Senate Armed Services Committee on Strategic Forces" \
  --native-id 2025-USSTRATCOM-SASC-POSTURE \
  --call-id CALL-NC3-MODERNIZATION-CURRENCY-001 \
  --tags "nc3,nuclear-modernization,usstratcom,posture-statement,official-government-report"

run_ingest \
  "https://www.stratcom.mil/Portals/8/Documents/Posture%20Statements/2026%20USSTRATCOM%20Congressional%20Posture%20Statement.pdf?ver=Hb98LGT3_5gb01-f_KLHhQ%3D%3D" \
  --landing-url "https://www.stratcom.mil/" \
  --source USSTRATCOM --collection "Congressional Posture Statements" \
  --year 2026 --document-date 2026-03-17 \
  --title "Statement of Richard A. Correll, Commander, United States Strategic Command, Before the House Armed Services Committee on Strategic Forces" \
  --native-id 2026-USSTRATCOM-HASC-POSTURE \
  --call-id CALL-NC3-MODERNIZATION-CURRENCY-001 \
  --tags "nc3,nuclear-modernization,usstratcom,posture-statement,official-government-report"
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "NC3 modernization/currency baseline ingest complete."
echo "USSTRATCOM posture statements are institutional version layers, not independent corroboration of underlying NC3 program records."
