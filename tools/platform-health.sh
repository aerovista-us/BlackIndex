#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"

echo "== BlackIndex corpus integrity =="
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

echo
echo "== Durable evidence-object validation =="
python3 "$ROOT/tools/validate-evidence-objects.py" --root "$ROOT"

echo
echo "== Source lineage =="
python3 "$ROOT/tools/source-lineage.py" --root "$ROOT"

echo
echo "== Unit tests =="
python3 -m unittest discover -s "$ROOT/tests" -p 'test_*.py'

echo
echo "BlackIndex platform health PASS"
