#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"

run_one(){ echo; echo "=== $1 ==="; shift; "$INGEST" "$@"; }

run_one "9/11 Joint Inquiry — declassified Part Four / 28 pages" \
  "https://intelligence.house.gov/UploadedFiles/declasspart4.pdf" \
  --source CONGRESS --collection "9-11 Joint Inquiry 28 Pages" --year 2002 \
  --title "Joint Inquiry into Intelligence Community Activities Before and After 9/11 — Declassified Part Four" \
  --native-id "Declassified Part Four / 28 Pages" \
  --landing-url "https://intelligence.house.gov/2016/07/15/intel-committee-publishes-declassified-28-pages/" \
  --call-id CALL-911-ENCORE --tags "9-11,joint-inquiry,28-pages,saudi-leads,bayoumi,thumairy,foreign-support" --publish

run_one "9/11 Commission Report" \
  "https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT.pdf" \
  --source COMMISSION --collection "9-11 Commission" --year 2004 --document-date "2004-07-22" \
  --title "The 9/11 Commission Report" \
  --native-id "GPO-911REPORT" \
  --landing-url "https://www.govinfo.gov/features/911-commission-report" \
  --call-id CALL-911-ENCORE --tags "9-11,commission,bayoumi,thumairy,hazmi,mihdhar,official-review" --publish

run_one "Operation Encore — closing electronic communication" \
  "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-section-2-b-ii-part-01-of-01" \
  --source FBI --collection "Operation Encore" --year 2021 --document-date "2021-05-27" \
  --title "Operation Encore — Administrative Closing Electronic Communication and Addendum" \
  --native-id "EO14040-000001 through EO14040-000014" \
  --landing-url "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040" \
  --call-id CALL-911-ENCORE --tags "9-11,operation-encore,fbi,bayoumi,thumairy,al-jarrah,negative-finding,closure" --publish

run_one "CIA OIG — 9/11 accountability" \
  "https://www.cia.gov/readingroom/docs/DOC_0006184107.pdf" \
  --source CIAOIG --collection "9-11 Accountability" --year 2005 --document-date "2005-06-01" \
  --title "CIA OIG Report on CIA Accountability Regarding Findings and Conclusions of the Joint Inquiry" \
  --native-id "C06184107 / IG 2003-0005-IN" \
  --landing-url "https://www.cia.gov/stories/story/cia-releases-declassified-documents-related-to-9-11-attacks/" \
  --call-id CALL-911-ENCORE --tags "9-11,cia,oig,accountability,intelligence-sharing,pre-attack,internal-review" --publish

run_one "FBI-CIA joint Saudi-support assessment — executive summary" \
  "https://www.odni.gov/files/documents/Newsroom/Executive_Summary_of_Joint_FBI-CIA_Report_on_Extent_of_Saudi_Government_Support_for_Terrorism.pdf" \
  --source FBICIA --collection "Saudi Government Support Assessment" --year 2005 \
  --title "Executive Summary of the Joint FBI-CIA Assessment on the Extent of Saudi Government Support for Terrorism" \
  --native-id "Joint FBI-CIA Assessment Executive Summary" \
  --landing-url "https://intelligence.house.gov/2016/07/15/intel-committee-publishes-declassified-28-pages/" \
  --call-id CALL-911-ENCORE --tags "9-11,saudi-support,fbi,cia,joint-assessment,official-interpretation" --publish

run_one "9/11 Commission Terrorist Financing Staff Monograph" \
  "https://www.govinfo.gov/content/pkg/GOVPUB-Y3-PURL-LPS53198/pdf/GOVPUB-Y3-PURL-LPS53198.pdf" \
  --source COMMISSION --collection "9-11 Terrorist Financing" --year 2004 \
  --title "Monograph on Terrorist Financing — Staff Report to the 9/11 Commission" \
  --native-id "GOVPUB-Y3-PURL-LPS53198" \
  --landing-url "https://www.govinfo.gov/app/details/GOVPUB-Y3-PURL-LPS53198" \
  --call-id CALL-911-ENCORE --tags "9-11,terrorist-financing,commission,staff-monograph,negative-findings,source-scope" --publish

python3 "$EVIDENCE" --root "$ROOT" bootstrap

# Treat the 2021 closing EC as an attributed investigator finding, never as automatic factual absence.
python3 "$EVIDENCE" --root "$ROOT" investigator-review \
  --report-or-finding "Operation Encore administrative closing EC" \
  --investigator "FBI New York Office / Operation Encore case team" \
  --employer-controller "Federal Bureau of Investigation" \
  --exact-wording "The closing EC states that insufficient evidence existed to prosecute the named subjects for wittingly conspiring to assist the hijackers and that no further logical and reasonable investigative steps were identified at closure." \
  --scope "Operation Encore and associated investigations as summarized in the May 2021 closing EC and September 2021 addendum" \
  --records-reviewed "financial, telecommunications, travel, interview, search-warrant, foreign-partner and case-file material described in the EC" \
  --workpapers-status "underlying serials, FD-302s, ACS legacy files, Sentinel records and foreign-partner material are not all reproduced in the closing EC" \
  --competing-finding "Earlier Joint Inquiry material recorded leads and associations warranting further investigation" \
  --note "The September 2021 addendum corrected the closing EC's interview count from 'hundreds' to approximately 60 for 2007-2016; preserve that correction as a record-integrity issue."

# Explicit public/official-evolution object: early leads vs later closing assessment.
python3 "$EVIDENCE" --root "$ROOT" statement-compare \
  --topic "Evolution of official assessment concerning assistance to Hazmi and Mihdhar in Southern California" \
  --public-source "2002 Joint Inquiry declassified Part Four" \
  --public-statement "The Joint Inquiry recorded leads, relationships, financial and institutional connections requiring additional investigation." \
  --internal-source "2021 Operation Encore closing EC" \
  --internal-content "The FBI later reported that its follow-on investigation did not develop sufficient evidence to prosecute the principal subjects for knowingly conspiring to assist the hijackers." \
  --relationship "in-tension" \
  --note "Different stages, evidentiary thresholds and scopes. Do not interpret the comparison itself as proof for or against any underlying allegation."

# Source genealogy/dependency reminder for overlapping Commission/FBI/CIA conclusions.
python3 "$EVIDENCE" --root "$ROOT" source-dependency \
  --assertion-id "911-support-network-official-assessments" \
  --source-id "9-11-Commission-and-later-federal-reviews" \
  --depends-on "overlapping-FBI-CIA-investigative-records-and-interviews" \
  --dependency-type "shared-underlying-records" \
  --independence "partially-independent" \
  --note "Do not count multiple official reports relying on common FBI/CIA source material as fully independent corroboration without tracing their underlying evidence."

python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify
python3 "$EVIDENCE" --root "$ROOT" publish --push

echo "9/11 Operation Encore evidence-map batch complete."
git -C "$ROOT" status --short
