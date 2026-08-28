#!/usr/bin/env bash
set -u -o pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
INGEST="$ROOT/tools/ingest-url.sh"
REPORT="$ROOT/docs/run-reports/2026-08-28-review-007c-cia-oig-executive-summary.md"
CALL_ID="CALL-911-CIA-OIG-EXEC-SUMMARY"
PURL="https://purl.fdlp.gov/GPO/LPS93679"
ACQ_STATUS="ACQUISITION_GAP"
ACQ_RC=0

mkdir -p "$(dirname "$REPORT")"

echo "== Review 007C — official CIA OIG Executive Summary companion check =="
echo "Government persistent identifier: $PURL"
echo

set +e
"$INGEST" "$PURL" \
  --source "CIA" \
  --collection "9/11 CIA Accountability Executive Summary" \
  --year 2005 \
  --title "Executive Summary — OIG Report on CIA Accountability With Respect to the 9/11 Attacks" \
  --native-id "GPO-LPS93679" \
  --landing-url "$PURL" \
  --call-id "$CALL_ID" \
  --tags "9-11,cia,oig,accountability,executive-summary,2007-release,companion-release,official-review" \
  --publish
ACQ_RC=$?
set -e
if [[ "$ACQ_RC" -eq 0 ]]; then
  ACQ_STATUS="ACQUIRED_OR_RESUMED"
else
  echo "warning: official executive-summary acquisition did not complete (rc=$ACQ_RC)." >&2
  echo "This remains an acquisition gap; no third-party substitution will be attempted." >&2
fi

echo
echo "== Reconcile living master ledger =="
python3 "$ROOT/tools/reconcile-review-007-ledger.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

export BLACKINDEX_007C_VERIFY_JSON="$VERIFY_JSON"
python3 - "$ROOT" "$REPORT" "$CALL_ID" "$PURL" "$ACQ_STATUS" "$ACQ_RC" <<'PY'
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
report = Path(sys.argv[2])
call_id = sys.argv[3]
purl = sys.argv[4]
acq_status = sys.argv[5]
acq_rc = int(sys.argv[6])
verify = json.loads(os.environ.get("BLACKINDEX_007C_VERIFY_JSON", "{}"))

records = []
for path in sorted((root / "metadata").glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue
    if data.get("call_id") == call_id or data.get("native_id") == "GPO-LPS93679":
        records.append(data)

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
lines = [
    "# BlackIndex Controlled Review Run — Review 007C CIA OIG Executive Summary Companion",
    "",
    f"- **Completed UTC:** `{now}`",
    f"- **Call ID:** `{call_id}`",
    f"- **Government persistent identifier:** `{purl}`",
    f"- **Acquisition status:** `{acq_status}`",
    f"- **Acquisition exit code:** `{acq_rc}`",
    f"- **Verifier:** `{verify.get('checked', 'unknown')}` checked / `{len(verify.get('failures') or []) if isinstance(verify.get('failures'), list) else 'unknown'}` failures",
    "- **Third-party source substitution:** `false`",
    "- **OCR performed by this checkpoint:** `false`",
    "- **Evidence-state mutations:** `none`",
    "",
    "> The 2007 Executive Summary is a companion/release artifact, not a replacement for the full CIA OIG report already held by BlackIndex. Acquisition failure is an acquisition gap, not evidence that the document does not exist.",
    "",
    "## Companion record result",
    "",
]
if records:
    for data in records:
        norm_status = data.get("normalization_status") or "unknown"
        text_path = data.get("normalized_text_path")
        lines += [
            f"### {data.get('title') or data.get('doc_id')}",
            "",
            f"- Document ID: `{data.get('doc_id') or ''}`",
            f"- Native ID: `{data.get('native_id') or ''}`",
            f"- SHA-256: `{data.get('sha256') or ''}`",
            f"- Source: `{data.get('source') or ''}`",
            f"- Normalization status: `{norm_status}`",
            f"- Native text derivative available: `{str(bool(text_path)).lower()}`",
            f"- Artifact URL: `{data.get('artifact_url') or data.get('source_url') or ''}`",
            "",
        ]
else:
    lines += [
        "_No durable metadata record for `GPO-LPS93679` was present at report generation time._",
        "",
        "Status remains an official-source acquisition gap. Do not fill it with a third-party transcription.",
        "",
    ]

lines += [
    "## Interpretation guard",
    "",
    "If acquired, this Executive Summary is a subset/summary release in the same CIA OIG source lineage. It must not be counted as independent corroboration of the full report or Joint Inquiry propositions.",
    "",
    "Public search/index text associated with the full CIA PDF remains navigation-only until exact wording is verified against an official page image.",
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

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving 007C report/ledger uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT" "$ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
  if ! git -C "$ROOT" diff --cached --quiet; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007C executive-summary checkpoint"
    git -C "$ROOT" push
    echo "Published sanitized Review 007C report and reconciled living ledger."
  else
    echo "Review 007C report/ledger unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007C executive-summary checkpoint complete."
echo "No OCR, evidence-state mutation, or historical conclusion was performed."
echo "Durable report: $REPORT"
echo "Living ledger: $ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
exit 0
