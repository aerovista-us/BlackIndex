#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
LOCAL_JSON="$ROOT/local/index/911-review-007-boundary-diagnostic.json"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-boundary-diagnostic.md"
LEDGER="$ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
mkdir -p "$(dirname "$REPORT")"

echo "== Review 007 structural boundary diagnostic =="
python3 "$ROOT/tools/review-007-boundary-diagnostic.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

python3 - "$LOCAL_JSON" "$REPORT" "$VERIFY_RC" "$VERIFY_JSON" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

local_path = Path(sys.argv[1])
report_path = Path(sys.argv[2])
verify_rc = int(sys.argv[3])
verify = json.loads(sys.argv[4])
payload = json.loads(local_path.read_text(encoding="utf-8")) if local_path.is_file() else {}
generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

lines = [
    "# BlackIndex Controlled Review Run — Review 007 Boundary Diagnostic",
    "",
    f"- **Completed UTC:** `{generated_at}`",
    f"- **Verifier:** `{verify.get('checked')}` checked / `{len(verify.get('failures') or [])}` failures",
    f"- **Targets:** `{payload.get('target_count', 0)}`",
    "- **Source text previews published:** `false`",
    "- **Boundary claims made:** `false`",
    "- **Record promotions:** `none`",
    "- **Evidence-state mutations:** `none`",
    "",
    "> This report contains structural diagnostics only. A heuristic disposition is not a confirmed FBI record boundary and does not promote a child record.",
    "",
    "## Target diagnostics",
    "",
]

for item in payload.get("targets") or []:
    transition = item.get("transition") or {}
    lines += [
        f"### {item.get('target_id')}",
        "",
        f"- Kind: `{item.get('kind')}`",
        f"- Parent: `{item.get('parent_doc_id')}`",
        f"- Parent SHA-256: `{item.get('parent_sha256') or ''}`",
        f"- Proposed range: `{item.get('proposed_start')}-{item.get('proposed_end')}`",
        f"- Diagnostic range: `{item.get('diagnostic_start')}-{item.get('diagnostic_end')}`",
        f"- Status: `{item.get('status')}`",
        f"- All diagnostic pages exact: `{str(bool(item.get('all_diagnostic_pages_exact'))).lower()}`",
        f"- Disposition: `{item.get('disposition')}`",
        f"- Start-record signal: `{str(bool(transition.get('start_record_signal'))).lower()}`",
        f"- Terminal-page signal: `{str(bool(transition.get('terminal_page_signal'))).lower()}`",
        f"- Extends-left signal: `{str(bool(transition.get('extends_left_signal'))).lower()}`",
        f"- Extends-right signal: `{str(bool(transition.get('extends_right_signal'))).lower()}`",
        f"- Left-boundary signal: `{str(bool(transition.get('left_boundary_signal'))).lower()}`",
        f"- Right-boundary signal: `{str(bool(transition.get('right_boundary_signal'))).lower()}`",
        "",
        "#### Page structure",
        "",
    ]
    for page in item.get("diagnostic_pages") or []:
        marker = page.get("page_marker") or {}
        marker_text = f"{marker.get('current')}/{marker.get('total')}" if marker else "none"
        lines += [
            f"- Physical page `{page.get('physical_page')}` · role `{page.get('role')}` · exact `{str(bool(page.get('exact_same_index'))).lower()}`",
            f"  - FBI header: `{str(bool(page.get('fbi_header'))).lower()}`; FD-302: `{str(bool(page.get('fd302_marker'))).lower()}`; EC: `{str(bool(page.get('electronic_communication_marker'))).lower()}`; continuation: `{str(bool(page.get('continuation_marker'))).lower()}`",
            f"  - page marker: `{marker_text}`; case/file label: `{str(bool(page.get('case_or_file_label'))).lower()}`; interview marker: `{str(bool(page.get('interview_language_marker'))).lower()}`",
            f"  - header signature SHA-256: `{page.get('header_signature_sha256') or ''}`",
            f"  - identifier signature SHA-256: `{page.get('identifier_signature_sha256') or ''}`",
        ]
    lines.append("")

lines += [
    "## Interpretation guard",
    "",
    "`STRUCTURALLY_SELF_CONTAINED_CANDIDATE` means the structured text features support both ends of the proposed range without extension signals. It is still not a confirmed source boundary. `LIKELY_EXTENDS_OUTSIDE_PROPOSED_RANGE` means at least one structural continuity signal crosses the proposed range. `SEGMENTATION_GAP_WINDOW_REVIEW` is diagnostic only and must not be promoted as a record.",
    "",
    "## Verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
]
report_path.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({
    "durable_report": str(report_path),
    "contains_text_previews": False,
    "targets": payload.get("target_count", 0),
    "dispositions": {x.get("target_id"): x.get("disposition") for x in payload.get("targets") or []},
}, indent=2))
PY

echo
echo "== Reconcile living master ledger =="
python3 "$ROOT/tools/reconcile-review-007-ledger.py" --root "$ROOT"

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving Review 007 boundary report and ledger uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT" "$LEDGER"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT" "$LEDGER"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 boundary diagnostic" -- "$REPORT" "$LEDGER"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 boundary-diagnostic report and reconciled living ledger."
  else
    echo "Review 007 boundary-diagnostic report/ledger unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 boundary-diagnostic checkpoint complete."
echo "No evidence-state mutation, confirmed boundary claim, or record promotion was performed."
echo "Local diagnostic: $LOCAL_JSON"
echo "Durable sanitized report: $REPORT"
echo "Living ledger: $LEDGER"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
