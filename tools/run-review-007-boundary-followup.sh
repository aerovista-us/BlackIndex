#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
LOCAL_JSON="$ROOT/local/index/911-review-007-boundary-followup.json"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-boundary-followup.md"
LEDGER="$ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
mkdir -p "$(dirname "$REPORT")"

echo "== Review 007 boundary hypotheses + Benomrane expansion =="
python3 "$ROOT/tools/review-007-boundary-followup.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

python3 - "$LOCAL_JSON" "$REPORT" "$LEDGER" "$VERIFY_JSON" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

local_path = Path(sys.argv[1])
report_path = Path(sys.argv[2])
ledger_path = Path(sys.argv[3])
verify = json.loads(sys.argv[4])
payload = json.loads(local_path.read_text(encoding="utf-8"))
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

lines = [
    "# BlackIndex Controlled Review Run — Review 007 Boundary Follow-up",
    "",
    f"- **Completed UTC:** `{now}`",
    f"- **Verifier:** `{verify.get('checked')}` checked / `{len(verify.get('failures') or [])}` failures",
    "- **Source text previews published:** `false`",
    "- **Confirmed boundary claims:** `none`",
    "- **Record promotions:** `none`",
    "- **Evidence-state mutations:** `none`",
    "",
    "> Boundary hypotheses are review aids. A bracketed range is not a confirmed child record and remains subject to visual/source-image confirmation.",
    "",
    "## Existing P0 candidate hypotheses",
    "",
]
for item in payload.get("candidate_boundary_hypotheses") or []:
    lines += [
        f"### {item.get('target_id')}",
        "",
        f"- Parent: `{item.get('parent_doc_id')}`",
        f"- Parent SHA-256: `{item.get('parent_sha256') or ''}`",
        f"- Proposed range: `{item.get('proposed_start')}-{item.get('proposed_end')}`",
        f"- Hypothesis: `{item.get('hypothesis_status')}`",
        f"- Start-page record signal: `{str(bool(item.get('start_page_has_record_start_signal'))).lower()}`",
        f"- Next-page strong new-record signal: `{str(bool(item.get('page_after_has_strong_new_record_signal'))).lower()}`",
        f"- Extends left: `{str(bool(item.get('extends_left_signal'))).lower()}`",
        f"- Extends right: `{str(bool(item.get('extends_right_signal'))).lower()}`",
        f"- Boundary confirmed: `false`",
        f"- Visual confirmation required: `true`",
        "",
    ]

ben = payload.get("benomrane_expansion") or {}
lines += [
    "## Benomrane widened structural search",
    "",
    f"- Parent: `{ben.get('parent_doc_id') or ''}`",
    f"- Parent SHA-256: `{ben.get('parent_sha256') or ''}`",
    f"- Anchor pages: `{', '.join(map(str, ben.get('anchor_pages') or []))}`",
    f"- Search range: `{ben.get('search_start')}-{ben.get('search_end')}`",
    f"- All search pages exact: `{str(bool(ben.get('all_search_pages_exact'))).lower()}`",
    f"- Strong start pages: `{', '.join(map(str, ben.get('strong_record_start_pages') or [])) or 'none'}`",
    f"- Nearest strong start at/before anchors: `{ben.get('nearest_strong_start_at_or_before_anchors') or 'none'}`",
    f"- Nearest strong start after anchors: `{ben.get('nearest_strong_start_after_anchors') or 'none'}`",
    f"- Proposed review range: `{ben.get('proposed_review_start') or 'none'}-{ben.get('proposed_review_end') or 'none'}`",
    f"- Proposed span pages: `{ben.get('proposed_review_span_pages') or 'none'}`",
    f"- Status: `{ben.get('status')}`",
    "- Proposed range is a confirmed boundary: `false`",
    "- Visual confirmation required: `true`",
    "",
    "## Interpretation guard",
    "",
    "`BRACKETED_BY_NEXT_RECORD_START_PENDING_VISUAL_CONFIRMATION` records a structural hypothesis only. `BRACKETED_GAP_CANDIDATE_REVIEW` likewise creates a segmentation-review target, not a child record. No substantive claim gains corroboration weight from this pass.",
    "",
    "## Verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
]
report_path.write_text("\n".join(lines), encoding="utf-8")

text = ledger_path.read_text(encoding="utf-8")
text = text.replace(
    "| Review 007 boundary diagnostic | `PREPARED` | structural before/range/after diagnostic ready; publishes no source text and cannot promote records |",
    "| Review 007 boundary diagnostic | `COMPLETE` | executed at 36/0; CAND-0005 and CAND-0013 require visual confirmation; Benomrane remains a segmentation-gap review |",
)
anchor = "| Review 007 boundary diagnostic | `COMPLETE` | executed at 36/0; CAND-0005 and CAND-0013 require visual confirmation; Benomrane remains a segmentation-gap review |"
addition = "\n| Review 007F boundary hypotheses | `ACTIVE` | CAND-0005 and CAND-0013 may be bracketed by a next-record start but remain unconfirmed pending visual/source-image review |\n| Review 007F Benomrane expansion | `ACTIVE` | widened exact-page structural search seeks nearest strong record starts around pages 173/175; any emitted range is review-only |"
if anchor in text and "| Review 007F boundary hypotheses |" not in text:
    text = text.replace(anchor, anchor + addition)
ledger_path.write_text(text, encoding="utf-8")
print(json.dumps({
    "durable_report": str(report_path),
    "living_ledger": str(ledger_path),
    "contains_text_previews": False,
    "candidate_hypotheses": {x.get('target_id'): x.get('hypothesis_status') for x in payload.get('candidate_boundary_hypotheses') or []},
    "benomrane_status": ben.get('status'),
    "benomrane_proposed_range": [ben.get('proposed_review_start'), ben.get('proposed_review_end')],
}, indent=2))
PY

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving Review 007 follow-up outputs uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT" "$LEDGER"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT" "$LEDGER"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 boundary follow-up" -- "$REPORT" "$LEDGER"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 boundary-follow-up report and reconciled living ledger."
  else
    echo "Review 007 boundary-follow-up outputs unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 boundary-follow-up checkpoint complete."
echo "No evidence-state mutation, confirmed boundary claim, or record promotion was performed."
echo "Local follow-up: $LOCAL_JSON"
echo "Durable sanitized report: $REPORT"
echo "Living ledger: $LEDGER"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
