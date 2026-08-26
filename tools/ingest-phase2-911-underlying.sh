#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
EVIDENCE="$ROOT/tools/evidence_map.py"

FAILURES=()
SUCCEEDED=0

run_one(){
  local label="$1"
  shift
  echo
  echo "=== $label ==="
  if "$INGEST" "$@"; then
    SUCCEEDED=$((SUCCEEDED + 1))
  else
    local rc=$?
    echo "warning: skipped after acquisition/intake failure (rc=$rc): $label" >&2
    FAILURES+=("$label (rc=$rc)")
  fi
}

run_one "Operation Encore — April 4, 2016 Electronic Communication" \
  "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/april-4-2016-electronic-communication-part-01-of-01/at_download/file" \
  --source FBI --collection "Operation Encore Underlying Records" --year 2016 --document-date "2016-04-04" \
  --title "April 4, 2016 Electronic Communication — Operation Encore / PENTTBOM follow-on investigation" \
  --native-id "EO14040 April 4 2016 EC" \
  --landing-url "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/april-4-2016-electronic-communication-part-01-of-01/view" \
  --call-id CALL-911-ENCORE-DEEP --tags "9-11,operation-encore,fbi,2016-ec,bayoumi,thumairy,al-jarrah,underlying-record" --publish

run_one "EO 14040 Section 2(b)(i) — Part 1" \
  "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-section-2-b-i-part-01-of-02/at_download/file" \
  --source FBI --collection "EO14040 2(b)(i)" --year 2021 \
  --title "Documents Responsive to Executive Order 14040 Section 2(b)(i) — Part 1 of 2" \
  --native-id "EO14040-2b1-Part01" \
  --landing-url "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-section-2-b-i-part-01-of-02/view" \
  --call-id CALL-911-ENCORE-DEEP --tags "9-11,eo14040,fbi,underlying-records,section-2b1,release-package" --publish

run_one "EO 14040 Section 2(b)(i) — Part 2" \
  "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-section-2-b-i-part-02-of-02/at_download/file" \
  --source FBI --collection "EO14040 2(b)(i)" --year 2021 \
  --title "Documents Responsive to Executive Order 14040 Section 2(b)(i) — Part 2 of 2" \
  --native-id "EO14040-2b1-Part02" \
  --landing-url "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-section-2-b-i-part-02-of-02/view" \
  --call-id CALL-911-ENCORE-DEEP --tags "9-11,eo14040,fbi,underlying-records,section-2b1,release-package" --publish

run_one "EO 14040 Section 2(c) — Part 1" \
  "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-2-c-part-1/at_download/file" \
  --source FBI --collection "EO14040 2(c)" --year 2022 \
  --title "Documents Responsive to Executive Order 14040 Section 2(c) — Part 1" \
  --native-id "EO14040-2c-Part01" \
  --landing-url "https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/9-11-material-released-in-response-to-executive-order-14040/documents-responsive-to-executive-order-14040-2-c-part-1/view" \
  --call-id CALL-911-ENCORE-DEEP --tags "9-11,eo14040,fbi,underlying-records,section-2c,release-package" --publish

# Object/index work should proceed for whichever records are actually present.
python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" bootstrap

ECDOC="$(python3 - "$ROOT" <<'PY'
import json, pathlib, sys
root=pathlib.Path(sys.argv[1])
for p in sorted((root/'metadata').glob('*.json')):
    try:d=json.loads(p.read_text())
    except Exception:continue
    if d.get('collection')=='Operation Encore Underlying Records' and d.get('document_date')=='2016-04-04':
        print(d['doc_id']); break
PY
)"

if [[ -n "$ECDOC" ]]; then
  # Avoid duplicate UNMAPPED object on reruns if one is already linked to this document.
  if ! grep -Rqs 'The April 4, 2016 EC relies on underlying interviews' "$ROOT/objects/missing_evidence" 2>/dev/null; then
    python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" missing-evidence "$ECDOC" \
      --category "UNMAPPED_REFERENCED_EVIDENCE" \
      --summary "The April 4, 2016 EC relies on underlying interviews, serials, analytical products, liaison reporting, and case records that are not yet individually mapped in BlackIndex" \
      --referenced-by "April 4, 2016 FBI Electronic Communication" \
      --stated-reason-missing "Not necessarily absent from the archive; currently not individually mapped to the EC's assertions" \
      --potential-relevance "Reproducibility of factual assertions, source independence, chronology, and later Operation Encore conclusions" \
      --alternative-explanation "Some underlying material may be present inside EO 14040 release packages but not yet segmented as individual records" \
      --recovery-path "segment cited serials/FD-302s/analytical products from EO 14040 packages and link each to the EC assertion it supports"
  fi
fi

if ! grep -Rqs 'operation-encore-2016-ec-source-base' "$ROOT/objects/source_dependencies" 2>/dev/null; then
  python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" source-dependency \
    --assertion-id "operation-encore-2016-ec-source-base" \
    --source-id "April-4-2016-EC" \
    --depends-on "underlying-FBI-serials-interviews-liaison-and-analytical-products" \
    --dependency-type "summary-derived-from-underlying-investigative-records" \
    --independence "dependent" \
    --note "Treat the EC as a synthesis layer; corroboration must be evaluated at the underlying-record level where possible."
fi

python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" index
python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" dashboard
python3 "$ROOT/tools/fix-dashboard-html.py" "$ROOT/local/dashboard/blackindex-dashboard.html"
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify
python3 -W ignore::SyntaxWarning "$EVIDENCE" --root "$ROOT" publish --push

echo
echo "9/11 underlying-record pass complete. Successful/resumed artifacts: $SUCCEEDED / 4"
if (( ${#FAILURES[@]} )); then
  echo "Unresolved acquisition failures:"
  printf '  - %s\n' "${FAILURES[@]}"
  echo "These remain acquisition gaps, not evidence gaps."
fi

git -C "$ROOT" status --short
