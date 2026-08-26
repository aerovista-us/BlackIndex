#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

python3 "$ROOT/tools/triage-fbi-segmentation.py" --root "$ROOT" --top 30

echo
echo "Top review queue:"
sed -n '1,45p' "$ROOT/local/index/triage/911-fbi-segmentation-priority.md"
