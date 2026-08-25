#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"

run_one(){ echo; echo "=== $1 ==="; shift; "$INGEST" "$@"; }

run_one "TPAJAX — CIA institutional retrospective" \
  "https://www.cia.gov/readingroom/docs/fifty%20years%20of%20the%20cia%5B15465283%5D.pdf" \
  --source CIA --collection "TPAJAX Institutional History" --year 1999 \
  --title "Fifty Years of the CIA — CIA and TPAJAX chapter" \
  --native-id "Fifty Years of the CIA / CIA and TPAJAX" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-TPAJAX-DEEP --tags "tpajax,iran-1953,cia,institutional-history,mossadegh,covert-action" --publish

run_one "TPAJAX — The Battle for Iran" \
  "https://www.cia.gov/readingroom/docs/THE%20BATTLE%20FOR%20IRAN%5B15688467%5D.pdf" \
  --source CIA --collection "TPAJAX Battle for Iran" --year 2019 \
  --title "The Battle for Iran — CIA Historical Review of TPAJAX" \
  --native-id "C01384460" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-TPAJAX-DEEP --tags "tpajax,iran-1953,mossadegh,cia-history,press-accounts,covert-action" --publish

run_one "Iran 1953 — SE-49 Current Outlook" \
  "https://www.cia.gov/readingroom/docs/CIA-RDP79S01011A001100020009-7.pdf" \
  --source CIA --collection "Iran Current Outlook SE49" --year 1953 --document-date "1953-08-21" \
  --title "SE-49: The Current Outlook in Iran" \
  --native-id "CIA-RDP79S01011A001100020009-7" \
  --landing-url "https://www.cia.gov/readingroom/document/cia-rdp79s01011a001100020009-7" \
  --call-id CALL-TPAJAX-DEEP --tags "iran-1953,se-49,post-coup-estimate,mossadegh,zahedi" --publish

run_one "PBSUCCESS — Custody of material" \
  "https://www.cia.gov/readingroom/docs/DOC_0000914015.pdf" \
  --source CIA --collection "PBSUCCESS Record Custody" --year 1954 --document-date "1954-01-02" \
  --title "Custody of PBSUCCESS Material (with attachments)" \
  --native-id "0000914015" \
  --landing-url "https://www.cia.gov/readingroom/document/0000914015" \
  --call-id CALL-PBSUCCESS-DEEP --tags "pbsuccess,guatemala-1954,record-custody,chain-of-custody,covert-action" --publish

run_one "PBSUCCESS — Operational support plan" \
  "https://www.cia.gov/readingroom/docs/DOC_0000923924.pdf" \
  --source CIA --collection "PBSUCCESS Operational Support" --year 1954 --document-date "1954-01-02" \
  --title "The PBSUCCESS Operational Support Plan" \
  --native-id "0000923924" \
  --landing-url "https://www.cia.gov/readingroom/document/0000923924" \
  --call-id CALL-PBSUCCESS-DEEP --tags "pbsuccess,guatemala-1954,logistics,operational-support,covert-action" --publish

run_one "PBSUCCESS — Field historical review" \
  "https://www.cia.gov/readingroom/docs/DOC_0000935207.pdf" \
  --source CIA --collection "PBSUCCESS Historical Review" --year 1954 \
  --title "PBSUCCESS CIA Historical Review — undercover field account" \
  --native-id "0000935207" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-PBSUCCESS-DEEP --tags "pbsuccess,guatemala-1954,historical-review,field-operations,guatemala-city" --publish

run_one "MKSEARCH — DCI testimony on surviving records" \
  "https://www.cia.gov/readingroom/docs/CIA-RDP99-00498R000300020007-3.pdf" \
  --source CIA --collection "MKSEARCH" --year 1977 --document-date "1977-09-21" \
  --title "Statement of Director of Central Intelligence before Subcommittee on Health and Scientific Research — MKSEARCH/OFTEN/CHICKWIT" \
  --native-id "CIA-RDP99-00498R000300020007-3" \
  --landing-url "https://www.cia.gov/readingroom/document/cia-rdp99-00498r000300020007-3" \
  --call-id CALL-MKSEARCH --tags "mksearch,mkultra,often,chickwit,record-gaps,financial-records,drug-research" --publish

run_one "OFTEN/CHICKWIT — later CIA program reconstruction" \
  "https://www.cia.gov/readingroom/docs/influencing%20human%20behavio%5B15132483%5D.pdf" \
  --source CIA --collection "OFTEN CHICKWIT" --year 1977 \
  --title "Influencing Human Behavior — OFTEN and CHICKWIT program discussion" \
  --native-id "Influencing Human Behavior [15132483]" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-MKSEARCH --tags "often,chickwit,mksearch,behavioral-research,edgewood,drug-testing,retrospective" --publish

python3 "$EVIDENCE" --root "$ROOT" bootstrap

# Record that the MKSEARCH documentary base is itself described as fragmentary.
python3 "$EVIDENCE" --root "$ROOT" investigator-review \
  --report-or-finding "DCI testimony concerning MKSEARCH records discovered in 1977" \
  --investigator "Director of Central Intelligence / CIA review staff" \
  --employer-controller "Central Intelligence Agency" \
  --exact-wording "The surviving MKSEARCH material was described as primarily financial papers and the understanding of funded activities as fragmented and incomplete." \
  --scope "records discovered and assembled by CIA staff following the August 1977 MKULTRA hearing" \
  --records-unavailable "substantive project records not present in the financial files" \
  --workpapers-status "requires linkage to the underlying financial records and later program histories" \
  --note "Attributed record-state finding only; not adopted as a final conclusion about every MKSEARCH activity."

# Record a concrete archive-gap object against the MKSEARCH document after ingestion.
MKDOC="$(python3 - "$ROOT" <<'PY'
import json, pathlib, sys
root=pathlib.Path(sys.argv[1])
for p in sorted((root/'metadata').glob('*.json')):
    try:d=json.loads(p.read_text())
    except Exception:continue
    if d.get('collection')=='MKSEARCH':
        print(d['doc_id']); break
PY
)"
if [[ -n "$MKDOC" ]]; then
  python3 "$EVIDENCE" --root "$ROOT" missing-evidence "$MKDOC" \
    --summary "Substantive MKSEARCH project records are not represented by the surviving financial papers described in the 1977 DCI testimony" \
    --referenced-by "DCI testimony, 21 Sep 1977" \
    --stated-reason-missing "not established by this record" \
    --potential-relevance "scope, methods, subjects, approvals, and project-specific outcomes" \
    --alternative-explanation "ordinary records-retention loss or separation into other project files" \
    --recovery-path "link surviving vouchers, grants, project files, OFTEN/CHICKWIT material, and committee workpapers"
fi

python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "Deep covert-action + behavioral-research batch complete."
git -C "$ROOT" status --short
