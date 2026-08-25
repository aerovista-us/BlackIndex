#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"

[[ -x "$INGEST" ]] || { echo "error: $INGEST is not executable" >&2; exit 2; }

run_one() {
  local label="$1"; shift
  echo
  echo "============================================================"
  echo "BlackIndex Phase 2: $label"
  echo "============================================================"
  "$INGEST" "$@"
}

# 1) VENONA program history / release guide. This is the corpus map before
# ingesting individual message translations.
run_one "VENONA — The Venona Story" \
  "https://www.nsa.gov/Portals/70/documents/about/cryptologic-heritage/historical-figures-publications/publications/coldwar/venona_story.pdf" \
  --source NSA \
  --collection "VENONA" \
  --year 1995 \
  --title "The Venona Story" \
  --native-id "NSA Center for Cryptologic History - The Venona Story" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/Venona/" \
  --call-id CALL-007 \
  --tags "venona,nsa,signals-intelligence,cryptanalysis,soviet-espionage,release-guide" \
  --redaction-note "Some identities were withheld for privacy in early releases; later releases restored some names. Preserve translation confidence and covername-identification uncertainty." \
  --publish

# 2) Pentagon Papers index. This is intentionally the small NARA map before
# selecting multi-hundred-MB substantive volumes.
run_one "Pentagon Papers — Index" \
  "https://nara-media-001.s3.amazonaws.com/arcmedia/research/pentagon-papers/Pentagon-Papers-Index.pdf" \
  --source NARA \
  --collection "Pentagon Papers" \
  --year 1969 \
  --title "Report of the Office of the Secretary of Defense Vietnam Task Force — Index" \
  --native-id "NARA 5890484" \
  --landing-url "https://www.archives.gov/research/pentagon-papers" \
  --call-id CALL-004 \
  --tags "pentagon-papers,vietnam,nara,index,decision-history,public-statements,internal-documents" \
  --redaction-note "NARA states the 2011 complete release is unredacted; retain version/release provenance because earlier public editions were incomplete." \
  --publish

# 3) Iran-Contra Diversion Memo — connects the Iran arms/hostage channel to
# support for the Nicaraguan resistance.
run_one "Iran-Contra — Diversion Memo" \
  "https://nsarchive.gwu.edu/sites/default/files/documents/4463972/Document-05-NSC-Memorandum-from-Oliver-North.pdf" \
  --source NSC \
  --collection "Iran-Contra" \
  --year 1986 \
  --document-date "1986-04-04" \
  --title "Release of American Hostages in Beirut" \
  --native-id "Oliver North memorandum, 1986-04-04 (Diversion Memo)" \
  --landing-url "https://nsarchive.gwu.edu/document/16593-document-05-nsc-memorandum-oliver-north" \
  --call-id CALL-005 \
  --tags "iran-contra,nsc,oliver-north,iran,hostages,contras,diversion,covert-action" \
  --redaction-note "Review blacked-out identities/contacts and distinguish proposal, approval, transaction, diversion, and outcome states." \
  --publish

# 4) Iran-Contra Fallback Plan — includes original and altered versions in the
# same archival packet, making it a high-value record-integrity case.
run_one "Iran-Contra — Fallback Plan original/altered" \
  "https://nsarchive.gwu.edu/sites/default/files/documents/3224973/04-NSC-Memorandum-from-Oliver-L-North-to-Robert.pdf" \
  --source NSC \
  --collection "Iran-Contra" \
  --year 1985 \
  --document-date "1985-03-16" \
  --title "Fallback Plan for the Nicaraguan Resistance — original and altered versions" \
  --native-id "NSC System IV 400246" \
  --landing-url "https://nsarchive.gwu.edu/document/22305-04-nsc-memorandum-oliver-l-north-robert" \
  --call-id CALL-005 \
  --tags "iran-contra,nsc,oliver-north,nicaragua,contras,system-iv,record-integrity,altered-record" \
  --redaction-note "Packet contains original and altered versions. Preserve version identity and do not merge differing language into a single record." \
  --publish

echo
echo "Phase 2 next-set batch ingest complete."
echo "Run: python3 tools/blackindex.py verify"
echo "Run: git status --short"
