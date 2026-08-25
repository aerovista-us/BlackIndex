#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"

run_one(){ echo; echo "=== $1 ==="; shift; "$INGEST" "$@"; }

run_one "Gulf of Tonkin — President Johnson address, 4 Aug 1964" \
  "https://www.nsa.gov/Portals/70/documents/resources/everyone/digital-media-center/video-audio/historical-audio/nsa-60th/nsa-60th-1960s/19640804_PresAddresstoNation.pdf" \
  --source WHITEHOUSE --collection "Gulf of Tonkin Public Statement" --year 1964 --document-date "1964-08-04" \
  --title "President Johnson Address to the Nation Regarding North Vietnam's Attack on U.S. Ships" \
  --native-id "NSA 60th Timeline / 19640804_PresAddresstoNation" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/NSA-60th-Timeline/smdpage14701/9/" \
  --call-id CALL-GULF-TONKIN --tags "gulf-of-tonkin,lbj,public-statement,august-4-1964,vietnam" --publish

run_one "Gulf of Tonkin — JCS Proof of Attack message" \
  "https://media.defense.gov/2021/Jul/20/2002806531/-1/-1/0/19640807_1960_DOC_JOHNSONLIBRARY_JCS.PDF" \
  --source JCS --collection "Gulf of Tonkin" --year 1964 --document-date "1964-08-07" \
  --title "Proof of Attack — JCS Incoming Message Regarding Gulf of Tonkin" \
  --native-id "19640807_1960_DOC_JOHNSONLIBRARY_JCS" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/NSA-60th-Timeline/smdpage14701/9/" \
  --call-id CALL-GULF-TONKIN --tags "gulf-of-tonkin,jcs,proof-of-attack,august-4-1964,operational-reporting" --publish

run_one "Gulf of Tonkin — NSA cryptologic reconstruction" \
  "https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/gulf-of-tonkin/articles/release-1/rel1_skunks_bogies.pdf" \
  --source NSA --collection "Gulf of Tonkin" --year 2001 \
  --title "Skunks, Bogies, Silent Hounds, and the Flying Fish: The Gulf of Tonkin Mystery, 2-4 August 1964" \
  --native-id "Cryptologic Quarterly Vols. 19/20 Nos. 4-1" \
  --landing-url "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Internal-Periodicals-Publications/Legacy-Periodicals-Lists/igphoto/2002751691/" \
  --call-id CALL-GULF-TONKIN --tags "gulf-of-tonkin,nsa,sigint,cryptologic-history,august-4-1964,retrospective-analysis" --publish

run_one "MHCHAOS — CIA institutional history" \
  "https://www.cia.gov/readingroom/docs/DOC_0001342704.pdf" \
  --source CIA --collection "MHCHAOS" --year 1993 \
  --title "Richard Helms as Director of Central Intelligence — MHCHAOS: CIA and the Antiwar Movement" \
  --native-id "DOC_0001342704" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-MHCHAOS --tags "mhchaos,operation-chaos,cia,antiwar,domestic-intelligence,foreign-influence" --publish

run_one "Operation CHAOS — Rockefeller Commission Report to the President" \
  "https://www.cia.gov/readingroom/docs/REPORT%20TO%20THE%20PRESIDENT%20B%5B15890372%5D.pdf" \
  --source ROCKEFELLER --collection "Operation CHAOS" --year 1975 --document-date "1975-06-01" \
  --title "Report to the President by the Commission on CIA Activities Within the United States — Operation CHAOS sections" \
  --native-id "C02330017 / Rockefeller Commission Report" \
  --landing-url "https://www.cia.gov/readingroom/" \
  --call-id CALL-MHCHAOS --tags "operation-chaos,mhchaos,rockefeller-commission,cia,domestic-intelligence,oversight" --publish

# Create/update neutral integrity sidecars for the expected first records in these new collections.
python3 "$EVIDENCE" --root "$ROOT" bootstrap

# Public statement vs later NSA reconstruction. Record relationship only; no final verdict.
python3 "$EVIDENCE" --root "$ROOT" statement-compare \
  --topic "Whether an attack occurred on the night of 4 August 1964" \
  --public-source "President Johnson address to the nation, 4 Aug 1964" \
  --public-statement "The President publicly described renewed hostile action against U.S. ships and announced a military response." \
  --internal-source "NSA Cryptologic Quarterly retrospective, Skunks/Bogies/Silent Hounds/Flying Fish" \
  --internal-content "The later NSA reconstruction reports major SIGINT problems and material inconsistent with the contemporaneous attack narrative." \
  --relationship "in-tension" \
  --note "This comparison records divergence in the surviving record; it is not a BlackIndex final determination."

# Later official investigator/technical finding remains attributed.
python3 "$EVIDENCE" --root "$ROOT" investigator-review \
  --report-or-finding "NSA retrospective review of Gulf of Tonkin SIGINT" \
  --investigator "NSA historical/cryptologic review author" \
  --employer-controller "National Security Agency" \
  --exact-wording "Retrospective review concluded that SIGINT evidence used to support the second attack was seriously flawed and identified intercepted material pointing the other way." \
  --scope "Released SIGINT reporting, summaries, message traffic, and later reconstruction described in the review" \
  --workpapers-status "Underlying released documents should be linked individually as the corpus expands" \
  --note "Stored as an attributed later investigative/analytic finding; BlackIndex does not adopt it as final fact."

python3 "$EVIDENCE" --root "$ROOT" index
python3 "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo "Tonkin + CHAOS batch complete."
git -C "$ROOT" status --short
