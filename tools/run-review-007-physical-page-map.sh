#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-physical-page-map.md"
LOCAL_JSON="$ROOT/local/index/911-review-007-physical-page-map.json"
mkdir -p "$(dirname "$REPORT")"

echo "== Review 007 physical-page verification =="
python3 "$ROOT/tools/map-review-007-physical-pages.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

python3 - "$LOCAL_JSON" "$REPORT" "$VERIFY_JSON" "$VERIFY_RC" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

local_path = Path(sys.argv[1])
report_path = Path(sys.argv[2])
verify = json.loads(sys.argv[3])
verify_rc = int(sys.argv[4])
result = json.loads(local_path.read_text(encoding="utf-8"))
completed = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

lines = [
    "# BlackIndex Controlled Review Run — Review 007 Physical Page Map",
    "",
    f"- **Completed UTC:** `{completed}`",
    f"- **Verifier:** `{verify.get('checked')}` checked / `{len(verify.get('failures') or [])}` failures",
    f"- **Positions checked:** `{result.get('position_count', 0)}`",
    f"- **Positions verified:** `{result.get('verified_position_count', 0)}`",
    f"- **Positions unresolved:** `{result.get('unresolved_position_count', 0)}`",
    "- **OCR used:** `false`",
    "- **Fuzzy matching used:** `false`",
    "- **Evidence-state mutations:** `none`",
    "- **Record promotions:** `none`",
    "",
    "> Physical pages are reported as verified only for unique exact canonical-text matches produced with the same `pdftotext -layout` method used during normalization. No text previews are published here.",
    "",
    "## Mapping summary",
    "",
]
for target in result.get("targets") or []:
    lines += [f"### {target.get('label') or target.get('target_id')}", ""]
    for pos in target.get("positions") or []:
        lines += [
            f"- Parent: `{pos.get('parent_doc_id')}`",
            f"  - Parent SHA-256: `{pos.get('parent_sha256') or ''}`",
            f"  - Normalized text page: `{pos.get('text_page_index')}`",
            f"  - Mapping status: `{pos.get('mapping_status')}`",
            f"  - Physical page: `{pos.get('physical_page_index') if pos.get('physical_page_verified') else 'UNVERIFIED'}`",
            f"  - Physical page verified: `{str(bool(pos.get('physical_page_verified'))).lower()}`",
        ]
        if pos.get("exact_match_pages"):
            lines.append(f"  - Exact match page(s): `{', '.join(map(str, pos.get('exact_match_pages') or []))}`")
    lines.append("")

lines += [
    "## Interpretation guard",
    "",
    "A verified text-page↔physical-page correspondence does not itself establish the start/end boundary of a child record. Candidate boundary confirmation and source review remain separate gates before any promotion.",
    "",
    "## Verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
]
report_path.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"durable_report": str(report_path), "contains_text_previews": False}, indent=2))
PY

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving physical-page report uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 physical page map" -- "$REPORT"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 physical-page report."
  else
    echo "Review 007 physical-page report unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 physical-page checkpoint complete."
echo "No evidence-state mutation or record promotion was performed."
echo "Local map: $LOCAL_JSON"
echo "Durable sanitized report: $REPORT"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
