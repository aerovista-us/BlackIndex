#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
SEG="$ROOT/tools/segment-fbi-container.py"

python3 - "$ROOT" <<'PY' | while IFS= read -r doc_id; do
import json, pathlib, sys
root=pathlib.Path(sys.argv[1])
wanted={
    'Operation Encore Underlying Records',
    'EO14040 2(b)(i)',
    'EO14040 2(c)',
}
rows=[]
for p in (root/'metadata').glob('*.json'):
    try:d=json.loads(p.read_text())
    except Exception:continue
    if d.get('collection') in wanted and d.get('source')=='FBI':
        rows.append((d.get('document_date') or '', d.get('doc_id') or ''))
for _, doc_id in sorted(rows):
    if doc_id:
        print(doc_id)
PY
  echo
  echo "=== Segmenting $doc_id ==="
  python3 "$SEG" --root "$ROOT" "$doc_id"
done

echo
echo "Segmentation candidate indexes:"
find "$ROOT/local/index/segmentation" -maxdepth 1 -type f -name '*.json' -printf '%f\n' 2>/dev/null | sort || true
