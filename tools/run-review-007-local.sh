#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
OUT_DIR="$ROOT/local/review/review-007"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-named-source-recovery.md"
mkdir -p "$OUT_DIR" "$(dirname "$REPORT")"

echo "== Review 007 named-source recovery scan =="
python3 "$ROOT/tools/recover-911-named-sources.py" --root "$ROOT"

echo
echo "== Dependency audit =="
python3 "$ROOT/tools/dependency-audit.py" --root "$ROOT"

echo
echo "== Review-state audit =="
python3 "$ROOT/tools/review-state-audit.py" --root "$ROOT"

echo
echo "== Named Source Recovery UI =="
python3 "$ROOT/tools/named-source-recovery-ui.py" --root "$ROOT"

echo
echo "== Corpus verifier =="
set +e
VERIFY_JSON="$(python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify)"
VERIFY_RC=$?
set -e
printf '%s\n' "$VERIFY_JSON"

python3 - "$ROOT" "$OUT_DIR" "$REPORT" "$VERIFY_RC" "$VERIFY_JSON" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
report_path = Path(sys.argv[3])
verify_rc = int(sys.argv[4])
verify = json.loads(sys.argv[5])
recovery_path = root / "local/index/911-named-source-recovery.json"
recovery = json.loads(recovery_path.read_text(encoding="utf-8")) if recovery_path.is_file() else {}
generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

checkpoint = {
    "schema_version": 1,
    "object_type": "review_007_local_checkpoint",
    "generated_at": generated_at,
    "verifier": verify,
    "verifier_exit_code": verify_rc,
    "named_source_recovery": {
        "target_count": recovery.get("target_count", 0),
        "targets_with_candidates": recovery.get("targets_with_candidates", 0),
        "scanned_documents": recovery.get("scanned_documents", 0),
        "scanned_text_pages": recovery.get("scanned_text_pages", 0),
        "physical_page_claim": False,
    },
    "evidence_state_mutated": False,
    "git_report_publication_requested": True,
}
(out / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")

local_lines = [
    "# BlackIndex Review 007 — Local Checkpoint",
    "",
    f"- Generated: `{generated_at}`",
    f"- Verifier: **{verify.get('checked')} checked / {len(verify.get('failures') or [])} failures**",
    f"- Verifier ok: `{verify.get('ok')}`",
    f"- Recovery targets: **{recovery.get('target_count', 0)}**",
    f"- Targets with candidate hits: **{recovery.get('targets_with_candidates', 0)}**",
    f"- Scanned normalized documents: **{recovery.get('scanned_documents', 0)}**",
    "",
    "> This checkpoint does not promote records, change evidence status, or claim that text-page indices are physical PDF pages.",
    "",
    "## Recovery outputs",
    "",
    "- `local/index/911-named-source-recovery.json`",
    "- `local/review/911-named-source-recovery.md`",
    "- `local/dashboard/named-source-recovery.html`",
    "- `local/index/dependency-audit.json`",
    "- `local/index/review-state-audit.json`",
    "",
    "## Next gate",
    "",
    "Review candidate hits against source boundaries and physical pages before promoting any named record. A no-hit target remains UNMAPPED_REFERENCED_EVIDENCE, not proof that the record is absent.",
    "",
]
(out / "checkpoint.md").write_text("\n".join(local_lines), encoding="utf-8")

# Durable report is intentionally sanitized. It contains target labels and
# parent-document/text-page coordinates, but never normalized-text previews.
report_lines = [
    "# BlackIndex Controlled Review Run — Review 007 Named-Source Recovery",
    "",
    f"- **Completed UTC:** `{generated_at}`",
    f"- **Verifier exit code:** `{verify_rc}`",
    f"- **Verifier checked:** `{verify.get('checked')}`",
    f"- **Verifier ok:** `{verify.get('ok')}`",
    f"- **Verifier failures:** `{len(verify.get('failures') or [])}`",
    f"- **Normalized documents scanned:** `{recovery.get('scanned_documents', 0)}`",
    f"- **Text-page chunks scanned:** `{recovery.get('scanned_text_pages', 0)}`",
    f"- **Recovery targets:** `{recovery.get('target_count', 0)}`",
    f"- **Targets with candidate hits:** `{recovery.get('targets_with_candidates', 0)}`",
    "- **Physical-page claims made:** `false`",
    "- **Evidence-state mutations:** `none`",
    "",
    "> This is a recovery/run record, not a historical finding. Candidate hits are navigation leads only. Text-page indices are normalized-text/form-feed positions, not verified physical PDF pages.",
    "",
    "## Candidate recovery summary",
    "",
]

for target in recovery.get("targets", []):
    label = target.get("label") or target.get("target_id") or "Unnamed target"
    candidates = target.get("candidates") or []
    report_lines += [f"### {label}", "", f"- Candidate count: **{len(candidates)}**"]
    if not candidates:
        report_lines += ["- Status: `NO_LOCAL_CANDIDATE_FOUND`", ""]
        continue
    report_lines.append("- Status: `CANDIDATE_RECOVERY_REVIEW_REQUIRED`")
    for cand in candidates:
        report_lines += [
            f"- Parent document: `{cand.get('doc_id')}`",
            f"  - Source: `{cand.get('source') or ''}`",
            f"  - Parent SHA-256: `{cand.get('container_sha256') or ''}`",
            f"  - Text-page index: `{cand.get('text_page_index')}`",
            "  - Physical page: `UNVERIFIED`",
        ]
    report_lines.append("")

report_lines += [
    "## Verifier output",
    "",
    "```json",
    json.dumps(verify, indent=2),
    "```",
    "",
    "## Interpretation guard",
    "",
    "A candidate hit does not establish that the complete cited record boundary was recovered. A no-hit result does not establish that the record is absent, destroyed, or withheld. Child promotion remains blocked until parent hash, source boundary, title/date/type, and physical-page evidence are reviewed under the existing FBI source safeguards.",
    "",
]
report_path.write_text("\n".join(report_lines), encoding="utf-8")

print(json.dumps({
    "checkpoint_json": str(out / "checkpoint.json"),
    "checkpoint_markdown": str(out / "checkpoint.md"),
    "durable_report": str(report_path),
    "durable_report_contains_previews": False,
}, indent=2))
PY

# Publish only the sanitized run report. Existing unstaged local evidence-object
# work is left untouched. If something is already staged, fail safe and leave
# the report local rather than mixing unrelated staged work into this commit.
PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving Review 007 run report uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 named-source recovery" -- "$REPORT"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 recovery report."
  else
    echo "Review 007 recovery report unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 local checkpoint complete."
echo "No evidence-state mutation or record promotion was performed."
echo "Named Source Recovery UI: $ROOT/local/dashboard/named-source-recovery.html"
echo "Durable sanitized report: $REPORT"

git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
