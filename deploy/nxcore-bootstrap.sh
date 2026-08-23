#!/usr/bin/env bash
set -euo pipefail

ROOT="${BLACKINDEX_ROOT:-/srv/NXDrive/BlackIndex}"
REPO_URL="${BLACKINDEX_REPO_URL:-https://github.com/aerovista-us/BlackIndex.git}"
CODE_DIR="${BLACKINDEX_CODE_DIR:-$ROOT/system}"

if [[ $EUID -eq 0 ]]; then
  echo "Run this as the intended BlackIndex owner, not root." >&2
  exit 2
fi

mkdir -p "$ROOT"

if [[ ! -d "$CODE_DIR/.git" ]]; then
  git clone "$REPO_URL" "$CODE_DIR"
else
  git -C "$CODE_DIR" pull --ff-only
fi

mkdir -p \
  "$ROOT/source-vault/raw" \
  "$ROOT/normalized/text" \
  "$ROOT/local/index" \
  "$ROOT/local/cache" \
  "$ROOT/local/logs" \
  "$ROOT/metadata" \
  "$ROOT/extractions"

chmod 750 "$ROOT" "$ROOT/source-vault" "$ROOT/source-vault/raw" || true

python3 "$CODE_DIR/tools/blackindex.py" --root "$ROOT" init
python3 -m unittest discover -s "$CODE_DIR/tests" -v

cat <<EOF

BlackIndex bootstrap complete.
Root: $ROOT
Code: $CODE_DIR

Next:
  python3 $CODE_DIR/tools/blackindex.py --root $ROOT intake /path/to/document.pdf \\
    --source CIA --collection "Family Jewels" --year 1973 --call-id CALL-003
EOF
