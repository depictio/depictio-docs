#!/usr/bin/env bash
#
# Publish the documentation images to a single unversioned location on the
# deploy branch, so mike does not have to copy them into every version.
#
# Pairs with hooks/shared_images.py, which excludes those images from the
# per-version build and points the pages at this copy.
#
# The deploy branch holds several GB, so this never checks it out: it seeds a
# temporary index from the branch tip, writes the blobs directly, and commits
# the resulting tree.
#
# Usage:
#   scripts/publish-shared-images.sh [--dry-run] [--branch gh-pages]
#                                    [--source docs/images] [--dest images]
#                                    [--remote origin]

set -euo pipefail

BRANCH="gh-pages"
SOURCE="docs/images"
DEST="images"
REMOTE="origin"
DRY_RUN=0
FILES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --branch)  BRANCH="$2"; shift 2 ;;
    --source)  SOURCE="$2"; shift 2 ;;
    --dest)    DEST="$2"; shift 2 ;;
    --remote)  REMOTE="$2"; shift 2 ;;
    --file)    FILES+=("$2"); shift 2 ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

# Two modes. Directory mode mirrors a whole tree and prunes the destination
# first, so source deletions propagate. File mode publishes named files only
# and never prunes, for destinations shared with content this script does not
# own (the site-root assets/ directory, for instance).
if [ ${#FILES[@]} -eq 0 ]; then
  [ -d "$SOURCE" ] || { echo "source directory not found: $SOURCE" >&2; exit 1; }
else
  for f in "${FILES[@]}"; do
    [ -f "$f" ] || { echo "file not found: $f" >&2; exit 1; }
  done
fi

git fetch -q "$REMOTE" "$BRANCH"
BASE="$(git rev-parse "${REMOTE}/${BRANCH}")"

GIT_INDEX_FILE="$(mktemp -u)"
export GIT_INDEX_FILE
trap 'rm -f "$GIT_INDEX_FILE"' EXIT

git read-tree "$BASE"

add_file() {
  local file="$1" path="$2" mode=100644 sha
  [ -x "$file" ] && mode=100755
  sha="$(git hash-object -w "$file")"
  git update-index --add --cacheinfo "${mode},${sha},${path}"
}

count=0
if [ ${#FILES[@]} -eq 0 ]; then
  # Clear the destination first so files deleted from the source disappear here
  # too, rather than lingering forever on the deploy branch.
  git ls-tree -r --name-only "$BASE" -- "$DEST" \
    | git update-index --force-remove --stdin

  while IFS= read -r -d '' file; do
    rel="${file#"$SOURCE"/}"
    case "$rel" in .DS_Store|*/.DS_Store) continue ;; esac
    add_file "$file" "${DEST}/${rel}"
    count=$((count + 1))
  done < <(find "$SOURCE" -type f -print0)
else
  for file in "${FILES[@]}"; do
    add_file "$file" "${DEST}/$(basename "$file")"
    count=$((count + 1))
  done
fi

TREE="$(git write-tree)"
if [ "$TREE" = "$(git rev-parse "${BASE}^{tree}")" ]; then
  echo "${DEST}/ already up to date on ${BRANCH} (${count} files)"
  exit 0
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] would publish ${count} files to ${BRANCH}:${DEST}/"
  echo "[dry-run] base=${BASE} tree=${TREE}"
  git diff --stat "$BASE" "$TREE" -- "$DEST" | tail -5
  exit 0
fi

COMMIT="$(git commit-tree "$TREE" -p "$BASE" -m "docs: publish shared image root (${count} files)

Served from one unversioned copy instead of being duplicated into every
mike version directory. See hooks/shared_images.py.")"

git push -q "$REMOTE" "${COMMIT}:refs/heads/${BRANCH}"
echo "published ${count} files to ${BRANCH}:${DEST}/ (${COMMIT})"
