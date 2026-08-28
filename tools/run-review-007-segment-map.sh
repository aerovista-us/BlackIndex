#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
OUT_DIR="$ROOT/local/review/review-007"
REPORT="$ROOT/docs/run-reports/2026-08-27-review-007-segment-map.md"
mkdir -p "$OUT_DIR" "$(dirname "$REPORT")"

echo "== Refresh Review 007 named-source recovery =="
python3 "$ROOT/tools/recover-911-named-sources.py" --root "$ROOT"

echo
echo "== Map EO 14040 recovery hits to segmentation candidates =="
python3 "$ROOT/tools/map-911-recovery-to-segments.py" --root "$ROOT"

echo
echo "== Refresh Named Source Recovery UI =="
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
map_path = root / "local/index/911-named-source-segment-map.json"
segment_map = json.loads(map_path.read_text(encoding="utf-8")) if map_path.is_file() else {}
generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

checkpoint = {
    "schema_version": 1,
    "object_type": "review_007_segment_map_checkpoint",
    "generated_at": generated_at,
    "verifier": verify,
    "verifier_exit_code": verify_rc,
    "segment_map": {
        "target_family_count": segment_map.get("target_family_count", 0),
        "candidate_position_count": segment_map.get("candidate_position_count", 0),
        "positions_with_segment_match": segment_map.get("positions_with_segment_match", 0),
        "positions_without_segment_match": segment_map.get("positions_without_segment_match", 0),
        "physical_page_claim": False,
        "boundary_claim": False,
    },
    "evidence_state_mutated": False,
    "record_promotion_performed": False,
}
(out / "segment-map-checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")

lines = [
    "# BlackIndex Controlled Review Run — Review 007 Segment Map",
    "",
    f"- **Completed UTC:** `{generated_at}`",
    f"- **Verifier:** `{verify.get('checked')}` checked / `{len(verify.get('failures') or [])}` failures",
    f"- **EO 14040 target families:** `{segment_map.get('target_family_count', 0)}`",
    f"- **EO 14040 candidate positions:** `{segment_map.get('candidate_position_count', 0)}`",
    f"- **Positions mapped to heuristic segments:** `{segment_map.get('positions_with_segment_match', 0)}`",
    f"- **Positions without heuristic segment match:** `{segment_map.get('positions_without_segment_match', 0)}`",
    "- **Physical-page claims made:** `false`",
    "- **Boundary claims made:** `false`",
    "- **Record promotions:** `none`",
    "- **Evidence-state mutations:** `none`",
    "",
    "> This report maps normalized-text recovery positions to existing heuristic segmentation candidates. It does not establish record boundaries or physical PDF pages.",
    "",
    "## Segment mapping",
    "",
]

for target in segment_map.get("targets") or []:
    lines += [f"### {target.get('label') or target.get('target_id')}", ""]
    for pos in target.get("eo14040_candidate_positions") or []:
        lines += [
            f"- Parent: `{pos.get('parent_doc_id')}`",
            f"  - Parent SHA-256: `{pos.get('parent_sha256') or ''}`",
            f"  - Normalized text page: `{pos.get('text_page_index')}`",
            "  - Physical page: `UNVERIFIED`",
            f"  - Matching segments: `{pos.get('segment_match_count', 0)}`",
        ]
        for seg in pos.get("segments") or []:
            lines += [
                f"  - Segment: `{seg.get('candidate_id')}`",
                f"    - Heuristic range: `{seg.get('start_page')}–{seg.get('end_page')}`",
                f"    - Record type guess: `{seg.get('record_type_guess')}`",
                f"    - Priority band: `{seg.get('priority_band')}`",
                f"    - Priority score: `{seg.get('priority_score')}`",
                f"    - P0 review packet present: `{bool(seg.get('p0_packet'))}`",
                f"    - Existing promotion state: `{seg.get('p0_promotion_state')}`",
                "    - Boundary verified: `false`",
                "    - Physical page verified: `false`",
            ]
        lines.append("")

lines += [
    "## Interpretation guard",
    "",
    "A segment match means the recovered text-page position falls inside an existing heuristic candidate range. It does not prove that the named source is the candidate's complete record, that the candidate boundary is correct, or that the text-page number equals the physical PDF page. Review the original parent PDF before promotion.",
    "",
]
report_path.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"durable_report": str(report_path), "contains_raw_previews": False}, indent=2))
PY

PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -n "$PRESTAGED" ]]; then
  echo "warning: pre-existing staged changes detected; leaving segment-map report uncommitted:" >&2
  printf '%s\n' "$PRESTAGED" >&2
else
  git -C "$ROOT" add -- "$REPORT"
  if ! git -C "$ROOT" diff --cached --quiet -- "$REPORT"; then
    git -C "$ROOT" commit -m "BlackIndex: record Review 007 segment map" -- "$REPORT"
    git -C "$ROOT" push
    echo "Published sanitized Review 007 segment-map report."
  else
    echo "Review 007 segment-map report unchanged; nothing new to publish."
  fi
fi

echo
echo "Review 007 segment-map checkpoint complete."
echo "No evidence-state mutation or record promotion was performed."
echo "Local map: $ROOT/local/review/911-named-source-segment-map.md"
echo "Durable sanitized report: $REPORT"
git -C "$ROOT" status --short

if [[ "$VERIFY_RC" -ne 0 ]]; then
  exit "$VERIFY_RC"
fi
