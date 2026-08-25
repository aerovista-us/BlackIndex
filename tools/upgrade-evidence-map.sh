#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

cd "$ROOT"

echo "[1/5] Bootstrapping Record Integrity objects"
python3 tools/evidence_map.py --root "$ROOT" bootstrap

echo "[2/5] Migrating only auto-generated review stubs to neutral template"
for meta in metadata/*.json; do
  base="$(basename "$meta" .json)"
  [[ "$base" == "schema-v1" ]] && continue
  BLACKINDEX_ROOT="$ROOT" python3 tools/generate-review-template.py "$base"
done

echo "[3/5] Rebuilding evidence-map index"
python3 tools/evidence_map.py --root "$ROOT" index

echo "[4/5] Building self-contained local dashboard"
python3 tools/evidence_map.py --root "$ROOT" dashboard

echo "[5/5] Verifying corpus integrity"
python3 tools/blackindex.py --root "$ROOT" verify

echo
echo "Evidence-map infrastructure bootstrap complete."
echo "Dashboard file: $ROOT/local/dashboard/blackindex-dashboard.html"
echo "Tailscale server: ./tools/serve-dashboard.sh"
echo "Durable object changes are not auto-pushed. Review with: git status --short"
git status --short
