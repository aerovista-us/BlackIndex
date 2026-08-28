#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-verified-source-bundle.md"
MANIFEST="$ROOT/local/review/source-bundles/review-007-verified/manifest.json"
mkdir -p "$(dirname "$REPORT")"

echo "== Review 007 verified source-image bundle =="
python3 "$ROOT/tools/build-review-007-verified-source-bundle.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

python3 - "$MANIFEST" "$REPORT" "$VERIFY_RC" "$VERIFY_JSON" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

manifest_path = Path(sys.argv[1])
report_path = Path(sys.argv[2])
verify_rc = int(sys.argv[3])
verify = json.loads(sys.argv[4])
manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

lines = [
    "# BlackIndex Controlled Review Run — Review 007 Verified Source Bundle",
    "",
    f"- **Completed UTC:** `{generated_at}`",
    f"- **Verifier:** `{verify.get('checked')}` checked / `{len(verify.get('failures') or [])}` failures",
    f"- **Targets:** `{manifest.get('target_count', 0)}`",
    f"- **Review slices ready:** `{manifest.get('ready_count', 0)}`",
    "- **Record promotions:** `none`",
    "- **Evidence-state mutations:** `none`",
    "- **Boundary claims:** `none`",
    "- **Source PDF bytes published to Git:** `false`",
    "",
    "> A review slice is created only after every page in its proposed range exact-matches the corresponding physical PDF page using `pdftotext -layout`. A ready slice is still a review artifact, not a confirmed child-record boundary.",
    "",
    "## Target results",
    "",
]

for item in manifest.get("targets") or []:
    lines += [
        f"### {item.get('target_id')}",
        "",
        f"- Kind: `{item.get('kind')}`",
        f"- Parent: `{item.get('parent_doc_id')}`",
        f"- Parent SHA-256: `{item.get('parent_sha256') or ''}`",
        f"- Proposed range: `{item.get('start')}-{item.get('end')}`",
        f"- Status: `{item.get('status')}`",
        f"- Full range verified: `{str(bool(item.get('range_verified'))).lower()}`",
        f"- Boundary verified: `false`",
    ]
    verification = item.get("range_verification") or {}
    if verification:
        lines += [
            f"- Range pages verified: `{verification.get('verified_count', 0)}/{verification.get('page_count', 0)}`",
        ]
    if item.get("status") == "REVIEW_SLICE_READY":
        lines += [
            f"- Physical review range: `{item.get('physical_range')}`",
            f"- Local review-slice SHA-256: `{item.get('source_pdf_sha256')}`",
            f"- Extraction method: `{item.get('extraction_method')}`",
        ]
    if item.get("anchor_pages"):
        lines.append(f"- Recovery anchor pages: `{', '.join(map(str, item.get('anchor_pages') or []))}`")
    lines.append("")

lines += [
    "## Interpretation guard",
    "",
    "`REVIEW_SLICE_READY` means the requested physical page range was safely extracted after exact page correspondence was established for every page in that range. It does not establish that the slice is one complete FBI record, that its first/last pages are true record boundaries, or that it is independent evidence. Boundary review remains mandatory before any promotion.",
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
    "contains_source_bytes": False,
    "contains_text_previews": False,
    "ready": manifest.get("ready_count", 0),
    "targets": manifest.get("target_count", 0),
}, indent=2))
PY

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving Review 007 source-bundle report uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 verified source bundle" -- "$REPORT"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 verified source-bundle report."
  else
    echo "Review 007 verified source-bundle report unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 verified source-bundle checkpoint complete."
echo "No evidence-state mutation, boundary claim, or record promotion was performed."
echo "Local bundle: $ROOT/local/review/source-bundles/review-007-verified"
echo "Durable sanitized report: $REPORT"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
