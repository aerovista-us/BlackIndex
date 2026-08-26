#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
VENV="$ROOT/local/tools/browser-fetch-venv"

mkdir -p "$ROOT/local/tools"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating local browser-fetch virtualenv: $VENV"
  python3 -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install 'curl_cffi>=0.7,<1'

echo "Browser-fetch runtime ready: $VENV/bin/python"
