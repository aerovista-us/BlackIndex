#!/usr/bin/env bash
set -euo pipefail

# BlackIndex location-relative bootstrap.
# The directory containing this script is expected to be <APP_ROOT>/bootstrap.
# Therefore the parent of this script directory becomes the BlackIndex app root.
#
# Example:
#   /srv/Collab/mini.shops/blackindex/bootstrap/deploy.sh
# resolves:
#   APP_ROOT=/srv/Collab/mini.shops/blackindex

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
APP_ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
REPO_URL="${BLACKINDEX_REPO_URL:-https://github.com/aerovista-us/BlackIndex.git}"

if [[ $EUID -eq 0 ]]; then
  echo "Run this as the intended BlackIndex owner, not root." >&2
  exit 2
fi

# Guard against accidentally treating / or an unexpected shallow path as the app root.
if [[ -z "$APP_ROOT" || "$APP_ROOT" == "/" ]]; then
  echo "Refusing unsafe BlackIndex app root: '$APP_ROOT'" >&2
  exit 2
fi

mkdir -p \
  "$APP_ROOT/source-vault/raw" \
  "$APP_ROOT/normalized/text" \
  "$APP_ROOT/local/index" \
  "$APP_ROOT/local/cache" \
  "$APP_ROOT/local/logs" \
  "$APP_ROOT/metadata" \
  "$APP_ROOT/extractions"

# The repository itself is the application root. No nested system/ checkout.
# When bootstrap/deploy.sh is being executed from a cloned repository, use it in-place.
if [[ ! -d "$APP_ROOT/.git" ]]; then
  echo "BlackIndex repository was not found at: $APP_ROOT" >&2
  echo "Expected layout: <app-root>/.git and <app-root>/bootstrap/deploy.sh" >&2
  echo "Clone first, for example:" >&2
  echo "  git clone $REPO_URL $APP_ROOT" >&2
  exit 2
fi

# Only fast-forward the current checkout when explicitly requested. This avoids
# surprising source changes merely from running a deployment/bootstrap script.
if [[ "${BLACKINDEX_UPDATE:-0}" == "1" ]]; then
  git -C "$APP_ROOT" pull --ff-only
fi

chmod 750 "$APP_ROOT/source-vault" "$APP_ROOT/source-vault/raw" || true

python3 "$APP_ROOT/tools/blackindex.py" --root "$APP_ROOT" init
python3 -m unittest discover -s "$APP_ROOT/tests" -v

cat <<EOF

BlackIndex bootstrap complete.
App root: $APP_ROOT
Repository: $APP_ROOT
Raw vault: $APP_ROOT/source-vault/raw

Next:
  python3 "$APP_ROOT/tools/blackindex.py" --root "$APP_ROOT" intake /path/to/document.pdf \\
    --source CIA --collection "Family Jewels" --year 1973 --call-id CALL-003

Optional update before bootstrap:
  BLACKINDEX_UPDATE=1 "$SCRIPT_DIR/deploy.sh"
EOF
