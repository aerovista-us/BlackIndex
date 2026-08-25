#!/usr/bin/env bash
set -euo pipefail

# Publish one BlackIndex document's durable research record to GitHub.
# Raw source bytes, normalized text, cache, indexes, and logs remain local-only.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${BLACKINDEX_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd -P)}"
DOC_ID="${1:-}"

if [[ -z "$DOC_ID" ]]; then
  echo "usage: $0 <DOC_ID> [commit message]" >&2
  exit 2
fi

META="$ROOT/metadata/$DOC_ID.json"
EXTRACT="$ROOT/extractions/$DOC_ID.md"
MESSAGE="${2:-BlackIndex: publish $DOC_ID}"

if [[ ! -d "$ROOT/.git" ]]; then
  echo "error: not a Git checkout: $ROOT" >&2
  exit 2
fi

if [[ ! -f "$META" ]]; then
  echo "error: metadata record missing: $META" >&2
  exit 2
fi

if [[ ! -f "$EXTRACT" ]]; then
  echo "error: extraction record missing: $EXTRACT" >&2
  exit 2
fi

# Integrity is a hard gate before publication.
python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify

# Only stage durable, reviewable research records for this document.
git -C "$ROOT" add -- "$META" "$EXTRACT"

STAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -z "$STAGED" ]]; then
  echo "Nothing new to publish for $DOC_ID"
  exit 0
fi

# Defense in depth: never permit local corpus/runtime material into a publish commit.
if printf '%s\n' "$STAGED" | grep -Eq '^(source-vault/|normalized/|local/|raw/)|\.(pdf|zip|7z|tar|gz)$'; then
  echo "error: local-only corpus/runtime path was staged; aborting" >&2
  git -C "$ROOT" reset --quiet
  exit 3
fi

printf 'Publishing durable record:\n%s\n' "$STAGED"
git -C "$ROOT" commit -m "$MESSAGE"
git -C "$ROOT" push

echo "Published $DOC_ID"
