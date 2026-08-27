#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
OUT_DIR="$ROOT/local/review/review-007"
mkdir -p "$OUT_DIR"

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

python3 - "$ROOT" "$OUT_DIR" "$VERIFY_RC" "$VERIFY_JSON" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
verify_rc = int(sys.argv[3])
verify = json.loads(sys.argv[4])
recovery_path = root / "local/index/911-named-source-recovery.json"
recovery = json.loads(recovery_path.read_text(encoding="utf-8")) if recovery_path.is_file() else {}

checkpoint = {
    "schema_version": 1,
    "object_type": "review_007_local_checkpoint",
    "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
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
    "git_mutation_performed": False,
}
(out / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")

lines = [
    "# BlackIndex Review 007 — Local Checkpoint",
    "",
    f"- Generated: `{checkpoint['generated_at']}`",
    f"- Verifier: **{verify.get('checked')} checked / {len(verify.get('failures') or [])} failures**",
    f"- Verifier ok: `{verify.get('ok')}`",
    f"- Recovery targets: **{recovery.get('target_count', 0)}**",
    f"- Targets with candidate hits: **{recovery.get('targets_with_candidates', 0)}**",
    f"- Scanned normalized documents: **{recovery.get('scanned_documents', 0)}**",
    "",
    "> This checkpoint does not promote records, change evidence status, commit files, or claim that text-page indices are physical PDF pages.",
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
(out / "checkpoint.md").write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"checkpoint_json": str(out / 'checkpoint.json'), "checkpoint_markdown": str(out / 'checkpoint.md')}, indent=2))
PY

echo
echo "Review 007 local checkpoint complete."
echo "No Git commit/push and no evidence-state mutation were performed."
echo "Named Source Recovery UI: $ROOT/local/dashboard/named-source-recovery.html"

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
