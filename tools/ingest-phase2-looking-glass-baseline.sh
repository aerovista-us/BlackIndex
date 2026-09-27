#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
CALL_ID="CALL-LOOKING-GLASS-OFFICIAL-BASELINE"
FAILURES=()
SUCCEEDED=0

run_one(){
  local label="$1"; shift
  echo
  echo "=== $label ==="
  if "$INGEST" "$@"; then
    SUCCEEDED=$((SUCCEEDED + 1))
  else
    local rc=$?
    FAILURES+=("$label (rc=$rc)")
    echo "warning: $label did not complete (rc=$rc); continuing bounded baseline" >&2
  fi
}

# Baseline 1: Headquarters Strategic Air Command institutional history.
# This is an official historical synthesis, not an operational order or nuclear-use authority.
run_one "SAC Alert Operations, 1957-1991" \
  "https://www.afgsc.af.mil/Portals/51/Docs/SAC%20Alert%20Operations%20Lo-Res.pdf" \
  --source "USAF" \
  --collection "Strategic Air Command Historical Studies" \
  --year 1991 \
  --title "Peace Is Our Profession: Alert Operations and the Strategic Air Command, 1957-1991" \
  --native-id "SAC-HIST-ALERT-OPS-1957-1991" \
  --call-id "$CALL_ID" \
  --tags "looking-glass,sac,post-attack-command-control,paccs,ec-135,nuclear-command-control,alert-operations,official-usaf-history" \
  --publish

# Baseline 2: broader Air Force institutional history for chronology/context.
# It may repeat SAC history and must not be counted as independent corroboration by document count alone.
run_one "Winged Shield, Winged Sword — Volume II" \
  "https://media.defense.gov/2010/Nov/05/2001329896/-1/-1/0/AFD-101105-002.pdf" \
  --source "USAF" \
  --collection "Air Force History and Museums Program" \
  --year 1997 \
  --title "Winged Shield, Winged Sword: A History of the United States Air Force, Volume II, 1950-1997" \
  --native-id "AFHMP-WINGED-SHIELD-WINGED-SWORD-VOL-II" \
  --call-id "$CALL_ID" \
  --tags "looking-glass,sac,air-force-history,nuclear-command-control,paccs,cold-war,official-usaf-history" \
  --publish

echo
echo "== Corpus verifier =="
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
printf '%s\n' "$VERIFY_JSON"

echo
echo "Baseline result: $SUCCEEDED / 2 official USAF documents ingested/resumed."
if (( ${#FAILURES[@]} )); then
  printf 'Acquisition failures:\n' >&2
  printf ' - %s\n' "${FAILURES[@]}" >&2
fi

echo "No claim is made that these histories establish nuclear-use authority, complete emergency procedures, or independent corroboration of each other."
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
if (( SUCCEEDED != 2 )); then
  exit 5
fi
exit 0
