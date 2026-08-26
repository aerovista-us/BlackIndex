#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

echo "== Rebuilding FBI segmentation indexes with tightened identifier parsing =="
bash "$ROOT/tools/segment-911-encore-containers.sh"

echo
echo "== Rebuilding 9/11 FBI review-priority queue =="
bash "$ROOT/tools/triage-911-encore-candidates.sh"

echo
echo "== Building P0 review packets =="
python3 "$ROOT/tools/build-fbi-review-packets.py" --root "$ROOT" --band P0 --limit 0

echo
echo "P0 review preparation complete."
echo "Packets: $ROOT/local/review/911-fbi-p0/"
echo "Manifest: $ROOT/local/review/911-fbi-p0/manifest.json"
