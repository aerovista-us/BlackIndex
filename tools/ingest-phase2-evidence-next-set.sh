#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
MAP="$ROOT/tools/evidence_map.py"

[[ -x "$INGEST" ]] || { echo "error: $INGEST is not executable" >&2; exit 2; }

run_one() {
  local label="$1"; shift
  echo
  echo "============================================================"
  echo "BlackIndex evidence-map batch: $label"
  echo "============================================================"
  "$INGEST" "$@"
}

run_one "Gulf of Tonkin — NSA cryptologic reconstruction" \
  "https://media.defense.gov/2021/Jun/29/2002751691/-1/-1/0/SKUNKS.PDF" \
  --source NSA \
  --collection "Gulf of Tonkin" \
  --year 2001 \
  --title "Skunks, Bogies, Silent Hounds, and the Flying Fish: The Gulf of Tonkin Mystery, 2–4 August 1964" \
  --native-id "SKUNKS.PDF / Cryptologic Quarterly Vols. 19-20" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Internal-Periodicals-Publications/Legacy-Periodicals-Lists/igphoto/2002751691/" \
  --call-id CALL-GULF-TONKIN \
  --tags "gulf-of-tonkin,nsa,sigint,vietnam,august-4-1964,retrospective-analysis,source-selection" \
  --classification-note "NSA historical/cryptologic retrospective based on declassified SIGINT holdings; not a contemporaneous 1964 operational report" \
  --redaction-note "Preserve distinctions among contemporaneous SIGINT products, later reconstruction, omitted material, and retrospective interpretation" \
  --publish

run_one "MHCHAOS — Rockefeller Commission report / official investigative layer" \
  "https://www.cia.gov/readingroom/docs/REPORT%20TO%20THE%20PRESIDENT%20B%5B15890372%5D.pdf" \
  --source CIA \
  --collection "MHCHAOS" \
  --year 1975 \
  --document-date "1975-06-01" \
  --title "Report to the President by the Commission on CIA Activities Within the United States — Operation CHAOS sections" \
  --native-id "C02330017" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-MHCHAOS \
  --tags "mhchaos,operation-chaos,cia,domestic-intelligence,antiwar,rockefeller-commission,oversight" \
  --classification-note "Official investigative/retrospective layer; underlying operational files remain separate research targets" \
  --redaction-note "Treat commission characterizations as attributed findings. Track underlying records cited, omitted material, investigative scope, and later/earlier conflicting accounts separately" \
  --publish

run_one "TPAJAX — CIA retrospective history layer" \
  "https://www.cia.gov/readingroom/docs/DOC_0005654141.pdf" \
  --source CIA \
  --collection "TPAJAX" \
  --year 2014 \
  --title "The Road to Covert Action in Iran, 1953" \
  --native-id "0005654141" \
  --landing-url "https://www.cia.gov/readingroom/document/0005654141" \
  --call-id CALL-TPAJAX \
  --tags "tpajax,iran,1953,mossadegh,cia,retrospective-history,official-interpretation" \
  --classification-note "CIA Studies in Intelligence retrospective; analysis layer distinct from contemporaneous TPAJAX records" \
  --redaction-note "Use for chronology, source leads, and official retrospective framing; do not substitute it for underlying operational records" \
  --publish

run_one "PBSUCCESS — contemporaneous operational support plan" \
  "https://www.cia.gov/readingroom/docs/DOC_0000923924.pdf" \
  --source CIA \
  --collection "PBSUCCESS" \
  --year 1954 \
  --document-date "1954-01-02" \
  --title "The PBSUCCESS Operational Support Plan" \
  --native-id "0000923924" \
  --landing-url "https://www.cia.gov/readingroom/document/0000923924" \
  --call-id CALL-PBSUCCESS \
  --tags "pbsuccess,guatemala,arbenz,cia,covert-action,operational-support,planning" \
  --redaction-note "Separate planned support architecture, authorization, implementation, execution, and outcome. Preserve sanitized identities and missing attachments as record-integrity issues" \
  --publish

run_one "MKSEARCH / OFTEN / CHICKWIT — CIA R&D/testing review" \
  "https://www.cia.gov/readingroom/docs/cia%20r%26d%20and%20testing%20of%20be%5B15132315%5D.pdf" \
  --source CIA \
  --collection "MKSEARCH OFTEN CHICKWIT" \
  --year 1977 \
  --title "CIA R&D and Testing of Behavioral Drugs — MKSEARCH / OFTEN / CHICKWIT" \
  --native-id "C01434878" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-MKSEARCH \
  --tags "mksearch,often,chickwit,mkultra,cia,behavioral-research,drug-testing,record-destruction" \
  --redaction-note "Track surviving financial/review records separately from destroyed project records; preserve volunteer/unwitting-subject distinctions and unresolved scope" \
  --publish

echo
echo "Evidence-map corpus batch complete."
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify
python3 "$MAP" --root "$ROOT" bootstrap
python3 "$MAP" --root "$ROOT" index
python3 "$MAP" --root "$ROOT" dashboard

echo "Dashboard rebuilt: $ROOT/local/dashboard/blackindex-dashboard.html"
git -C "$ROOT" status --short
