#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
REPORT="$ROOT/docs/run-reports/2026-08-29-review-007g-abdullah-official-fbi-bundles.md"
CALL_ID="CALL-911-REVIEW007G-ABDULLAH-FBI-BUNDLES"

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
    FAILURES+=("$label (rc=$rc)")
    echo "warning: $label did not complete (rc=$rc); continuing controlled sprint" >&2
  fi
}

# Review 007G is deliberately limited to two official FBI Vault parent bundles.
# These bundles are recovery containers, not automatic child-record promotions.
# If the same underlying FBI EC/ROI later appears in EO 14040, the releases are
# duplicate release paths, not independent corroboration.

run_one "FBI 9/11 Investigation — April 2002 parent bundle" \
  "https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2002-04-apr/" \
  --source "FBI" \
  --collection "9/11 Commission FBI Monthly Releases April 2002" \
  --year 2002 \
  --title "FBI 9/11 Investigation — April 2002 Release Bundle" \
  --native-id "FBI-911-INV-2002-04-APR" \
  --landing-url "https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2002-04-apr/" \
  --call-id "$CALL_ID" \
  --tags "9-11,fbi,penttbom,mohdar-abdullah,commission-source-files,underlying-records,official-fbi-release" \
  --publish

run_one "FBI 9/11 Investigation — May 2004 parent bundle" \
  "https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2004-05-may" \
  --source "FBI" \
  --collection "9/11 Commission FBI Monthly Releases May 2004" \
  --year 2004 \
  --title "FBI 9/11 Investigation — May 2004 Release Bundle" \
  --native-id "FBI-911-INV-2004-05-MAY" \
  --landing-url "https://vault.fbi.gov/9-11%20Commission%20Report/9-11-investigation-2004-05-may" \
  --call-id "$CALL_ID" \
  --tags "9-11,fbi,mohdar-abdullah,charles-sabah-toma,advance-knowledge,commission-source-files,underlying-records,official-fbi-release" \
  --publish

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

VERIFY_CHECKED="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("checked", ""))' <<<"$VERIFY_JSON" 2>/dev/null || true)"
VERIFY_FAILURE_COUNT="$(python3 -c 'import json,sys; v=json.load(sys.stdin); print(len(v.get("failures") or []))' <<<"$VERIFY_JSON" 2>/dev/null || true)"

FAIL_TEXT=""
if (( ${#FAILURES[@]} )); then
  for failure in "${FAILURES[@]}"; do
    FAIL_TEXT+="- ${failure}"$'\n'
  done
fi
export BLACKINDEX_007G_FAILURES="$FAIL_TEXT"
export BLACKINDEX_007G_VERIFY_JSON="$VERIFY_JSON"

mkdir -p "$(dirname "$REPORT")"
python3 - "$ROOT" "$REPORT" "$CALL_ID" "$SUCCEEDED" "$VERIFY_RC" <<'PY'
from __future__ import annotations
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
report = Path(sys.argv[2])
call_id = sys.argv[3]
succeeded = int(sys.argv[4])
verify_rc = int(sys.argv[5])

verify_raw = os.environ.get("BLACKINDEX_007G_VERIFY_JSON", "{}").strip()
try:
    verify = json.loads(verify_raw)
except Exception:
    verify = {}

records = []
for path in sorted((root / "metadata").glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue
    if data.get("call_id") == call_id:
        records.append(data)


def normalized_text(data: dict) -> str:
    p = data.get("normalized_text_path")
    if not p:
        return ""
    path = Path(p)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def has_any(text: str, needles: list[str]) -> bool:
    low = text.lower()
    return any(n.lower() in low for n in needles)

signature_checks = {}
for data in records:
    native = data.get("native_id") or data.get("doc_id") or "unknown"
    text = normalized_text(data)
    if native == "FBI-911-INV-2004-05-MAY":
        signature_checks[native] = {
            "has_may_18_date": has_any(text, ["05/18/2004", "5/18/2004", "May 18, 2004"]),
            "has_may_17_date": has_any(text, ["05/17/2004", "5/17/2004", "May 17, 2004"]),
            "has_charles_sabah_toma": has_any(text, ["Charles Sabah Toma"]),
            "has_mohdar_abdullah": has_any(text, ["Mohdar Abdullah", "Mohdar M. Abdullah", "Mohdar Mohamed Abdullah"]),
        }
    elif native == "FBI-911-INV-2002-04-APR":
        signature_checks[native] = {
            "has_april_11_date": has_any(text, ["04/11/2002", "4/11/2002", "April 11, 2002"]),
            "has_september_19_abdullah_context": has_any(text, ["September 19, 2001", "09/19/2001", "9/19/2001"]),
            "has_mohdar_abdullah": has_any(text, ["Mohdar Abdullah", "Mohdar M. Abdullah", "Mohdar Mohamed Abdullah"]),
        }

fail_text = os.environ.get("BLACKINDEX_007G_FAILURES", "").strip()
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
lines = [
    "# BlackIndex Controlled Review Run — Review 007G Abdullah Official FBI Parent Bundles",
    "",
    f"- **Completed UTC:** `{now}`",
    f"- **Call ID:** `{call_id}`",
    f"- **Successful/resumed parent bundles:** **{succeeded} / 2**",
    f"- **Verifier exit code:** `{verify_rc}`",
    f"- **Verifier checked:** `{verify.get('checked', 'unknown')}`",
    f"- **Verifier failures:** `{len(verify.get('failures') or []) if isinstance(verify.get('failures'), list) else 'unknown'}`",
    "- **Child-record promotions:** `0`",
    "- **Evidence-state mutations:** `none`",
    "- **OCR performed:** `false`",
    "- **Contains normalized-text previews:** `false`",
    "",
    "> Parent release acquisition does not establish child-record boundaries or independent corroboration. Exact July 23, 2002 and May 19, 2004 source records remain unresolved unless separately demonstrated.",
    "",
    "## Durable parent records",
    "",
]
if records:
    for data in records:
        lines += [
            f"### {data.get('title') or data.get('doc_id')}",
            "",
            f"- Document ID: `{data.get('doc_id') or ''}`",
            f"- Native ID: `{data.get('native_id') or ''}`",
            f"- SHA-256: `{data.get('sha256') or ''}`",
            f"- Normalization status: `{data.get('normalization_status') or 'unknown'}`",
            f"- Source URL: `{data.get('source_url') or ''}`",
            "",
        ]
else:
    lines += ["_No records with the Review 007G call ID were present at report generation time._", ""]

lines += ["## Signature checks", ""]
if signature_checks:
    lines += ["```json", json.dumps(signature_checks, indent=2, sort_keys=True), "```", ""]
else:
    lines += ["_No normalized source text was available for signature checks._", ""]

lines += ["## Acquisition failures", ""]
if fail_text:
    lines += fail_text.splitlines()
else:
    lines += ["_None reported._"]

lines += [
    "",
    "## Interpretation guard",
    "",
    "The May 2004 FBI bundle is expected to contain source material overlapping Commission notes 22-23, including ECs dated May 17 and May 18, 2004. This must be confirmed against the acquired parent artifact before any child promotion.",
    "",
    "The April 2002 FBI bundle is upstream lineage/context and must not be substituted for the still-unrecovered July 23, 2002 Abdullah ROI.",
    "",
    "If either monthly FBI release duplicates a record later released in EO 14040, record a duplicate-release/source-dependency relationship rather than increasing corroboration strength.",
    "",
    "## Verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
]
report.write_text("\n".join(lines), encoding="utf-8")
print(report)
PY

# Publish the sanitized run report before any living-ledger bookkeeping. Existing
# unstaged local integrity files do not block this. Pre-existing staged changes
# do, to avoid mixing unrelated work.
PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving Review 007G report uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007G Abdullah FBI bundle sprint"
    git -C "$ROOT" push
    echo "Published sanitized Review 007G run report."
  else
    echo "Review 007G report unchanged; nothing new to publish."
  fi
fi

# Bookkeeping is intentionally downstream of acquisition, verification, and the
# durable run report. A ledger failure must never hide or invalidate a successful
# corpus operation.
echo
echo "== Reconcile living master ledger =="
RECON_RC=0
if [[ -n "$VERIFY_CHECKED" && -n "$VERIFY_FAILURE_COUNT" ]]; then
  set +e
  python3 "$ROOT/tools/reconcile-review-007-ledger.py" \
    --root "$ROOT" \
    --verifier-checked "$VERIFY_CHECKED" \
    --verifier-failures "$VERIFY_FAILURE_COUNT"
  RECON_RC=$?
  set -e
else
  RECON_RC=4
  echo "warning: verifier JSON could not be summarized for ledger reconciliation." >&2
fi

if [[ "$RECON_RC" -ne 0 ]]; then
  echo "warning: living-ledger reconciliation failed after acquisition/report handling (rc=$RECON_RC)." >&2
  echo "The acquired records, verifier result, and durable run report remain valid." >&2
else
  PRESTAGED_LEDGER="$(git -C "$ROOT" diff --cached --name-only)"
  if [[ -n "$PRESTAGED_LEDGER" ]]; then
    echo "warning: staged changes appeared before ledger publication; leaving the reconciled master uncommitted:" >&2
    printf '%s\n' "$PRESTAGED_LEDGER" >&2
  else
    git -C "$ROOT" add -- "$ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
    if ! git -C "$ROOT" diff --cached --quiet; then
      git -C "$ROOT" commit -m "BlackIndex: reconcile Review 007G living ledger"
      git -C "$ROOT" push
      echo "Published reconciled Review 007G living ledger."
    else
      echo "Living ledger already reconciled; nothing new to publish."
    fi
  fi
fi

echo
echo "Review 007G parent-bundle checkpoint complete."
echo "No child promotion, OCR, or evidence-state mutation was performed."
echo "Durable report: $REPORT"
echo "Living ledger reconciliation exit code: $RECON_RC"
git -C "$ROOT" status --short

# Only corpus verification governs the sprint exit status. Ledger bookkeeping is
# downstream and non-authoritative for corpus integrity.
if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
exit 0
