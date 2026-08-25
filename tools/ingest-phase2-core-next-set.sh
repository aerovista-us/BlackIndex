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
  echo "BlackIndex P0 core: $label"
  echo "============================================================"
  "$INGEST" "$@"
}

run_one "MKULTRA — 1977 Senate joint hearing" \
  "https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-hearings-95mkultra.pdf" \
  --source SENATE \
  --collection "MKULTRA" \
  --year 1977 \
  --document-date "1977-08-03" \
  --title "Project MKULTRA, the CIA's Program of Research in Behavioral Modification — Joint Hearing" \
  --native-id "95th Congress joint hearing, 1977-08-03" \
  --landing-url "https://www.intelligence.senate.gov/1977/08/03/hearings-joint-hearing-subcommittee-health-and-scientific-research-committee-human-resources-project/" \
  --call-id CALL-MKULTRA \
  --tags "mkultra,mksearch,cia,human-experimentation,behavioral-modification,lsd,record-destruction,oversight" \
  --redaction-note "Treat destroyed records and later-discovered financial files as archive-integrity issues. Separate established experimentation from claims not supported by surviving records." \
  --publish

run_one "MINARET — Lew Allen testimony / watch-list activity" \
  "https://media.defense.gov/2021/Jul/20/2002806877/-1/-1/0/19751029_1970_DOC_FORDLIBRARY_GEN.PDF" \
  --source NSA \
  --collection "MINARET" \
  --year 1975 \
  --document-date "1975-10-29" \
  --title "Statement of Lt. General Lew Allen, Jr. before the Senate Select Committee on Intelligence — Watch List Activity" \
  --native-id "Ford Library / NSA 19751029_1970_DOC_FORDLIBRARY_GEN" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/NSA-60th-Timeline/smdpage14701/7/" \
  --call-id CALL-MINARET \
  --tags "minaret,nsa,watch-list,domestic-surveillance,communications-intelligence,americans,oversight" \
  --redaction-note "Preserve classified/withheld sections and distinguish foreign-intelligence collection from U.S.-person watch-list selection and dissemination." \
  --publish

run_one "SHAMROCK — Allen/Abzug correspondence" \
  "https://media.defense.gov/2021/Jul/20/2002806876/-1/-1/0/19751000_1970_DOC_FORDLIBRARY_SHAMROCK.PDF" \
  --source NSA \
  --collection "SHAMROCK" \
  --year 1975 \
  --document-date "1975-10-23" \
  --title "SHAMROCK — NSA Version and Lew Allen / Bella Abzug Correspondence" \
  --native-id "Ford Library / NSA 19751000_1970_DOC_FORDLIBRARY_SHAMROCK" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/NSA-60th-Timeline/smdpage14701/7/" \
  --call-id CALL-SHAMROCK \
  --tags "shamrock,nsa,telegraph,cable,telex,communications-intelligence,private-companies,oversight" \
  --redaction-note "Distinguish company provision of traffic from NSA downstream selection/use; preserve the agency's own legal/national-security characterization and later oversight findings separately." \
  --publish

run_one "TPAJAX — Iran 1953 implementation/finance memo" \
  "https://www.cia.gov/readingroom/docs/CIA-RDP78-04913A000100030035-4.pdf" \
  --source CIA \
  --collection "TPAJAX" \
  --year 1953 \
  --document-date "1953-09-02" \
  --title "TPAJAX — Finance Division memorandum concerning project implementation and obligations" \
  --native-id "CIA-RDP78-04913A000100030035-4" \
  --landing-url "https://www.cia.gov/readingroom/document/cia-rdp78-04913a000100030035-4" \
  --call-id CALL-TPAJAX \
  --tags "tpajax,iran,1953,mossadegh,cia,covert-action,finance,implementation" \
  --classification-note "Originally Secret; CREST release record" \
  --redaction-note "Substantial names/amounts are sanitized. Use this record to establish project implementation/financial administration, not the full coup narrative by itself." \
  --publish

run_one "PBSUCCESS — Stage Two political/psychological program" \
  "https://www.cia.gov/readingroom/docs/DOC_0000914052.pdf" \
  --source CIA \
  --collection "PBSUCCESS" \
  --year 1954 \
  --document-date "1954-01-25" \
  --title "Proposed PP Program, Stage Two, PBSUCCESS" \
  --native-id "CIA Historical Review Program DOC_0000914052" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-PBSUCCESS \
  --tags "pbsuccess,guatemala,arbenz,cia,covert-action,psychological-operations,regime-change" \
  --classification-note "Originally Secret / RYBAT / PBSUCCESS; CIA Historical Review Program release" \
  --redaction-note "Preserve sanitized operational identities and distinguish stated objectives/plans from actions later executed." \
  --publish

echo
echo "P0 core next-set batch ingest complete."
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

git -C "$ROOT" status --short
