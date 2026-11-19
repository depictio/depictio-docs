#!/usr/bin/env bash
#
# Publish the GitHub Pages redirect shell (redirects/github-pages/) to its own
# branch. Once GitHub Pages serves that branch, every old URL under
# depictio.github.io/depictio-docs/ lands on the same path on the new host.
#
# This script only writes the branch. GitHub Pages keeps serving gh-pages until
# its source is switched, which is the one user-visible step of the cut-over:
#
#   gh api -X PUT repos/depictio/depictio-docs/pages \
#     -f "source[branch]=pages-redirect" -f "source[path]=/"
#
# Rolling back is the same call with source[branch]=gh-pages. gh-pages itself is
# never touched: mike keeps deploying to it and Kubernetes keeps serving it.
#
# Usage:
#   scripts/publish-pages-redirect.sh [--dry-run] [--origin https://docs.depictio.embl.org]
#                                     [--branch pages-redirect] [--source redirects/github-pages]
#                                     [--remote origin]

set -euo pipefail

ORIGIN="https://docs.depictio.embl.org"
BRANCH="pages-redirect"
SOURCE="redirects/github-pages"
REMOTE="origin"
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --origin)  ORIGIN="${2%/}"; shift 2 ;;
    --branch)  BRANCH="$2"; shift 2 ;;
    --source)  SOURCE="$2"; shift 2 ;;
    --remote)  REMOTE="$2"; shift 2 ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

case "$ORIGIN" in
  https://*) ;;
  *) echo "--origin must be an https:// URL: $ORIGIN" >&2; exit 2 ;;
esac
[ -f "$SOURCE/404.html" ] || { echo "missing $SOURCE/404.html" >&2; exit 1; }

STAGE="$(mktemp -d)"
GIT_INDEX_FILE="$(mktemp -u)"
export GIT_INDEX_FILE
trap 'rm -rf "$STAGE"; rm -f "$GIT_INDEX_FILE"' EXIT

cp -R "$SOURCE"/. "$STAGE"/
find "$STAGE" -name .DS_Store -delete
for page in "$STAGE"/*.html; do
  sed "s#__DOCS_ORIGIN__#${ORIGIN}#g" "$page" > "$page.tmp" && mv "$page.tmp" "$page"
done
if grep -rq "__DOCS_ORIGIN__" "$STAGE"; then
  echo "placeholder left in the staged pages" >&2
  exit 1
fi

# The branch only ever holds this shell, so each publish is built from scratch
# rather than on top of the branch's previous tree.
git --work-tree="$STAGE" add -A .
TREE="$(git write-tree)"

PARENT=""
if git ls-remote --exit-code --heads "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
  git fetch -q "$REMOTE" "$BRANCH"
  PARENT="$(git rev-parse FETCH_HEAD)"
  if [ "$TREE" = "$(git rev-parse "${PARENT}^{tree}")" ]; then
    echo "${BRANCH} already up to date (${ORIGIN})"
    exit 0
  fi
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] would publish to ${REMOTE}/${BRANCH}, redirecting to ${ORIGIN}:"
  git ls-tree -r --name-only "$TREE" | sed 's/^/  /'
  exit 0
fi

COMMIT="$(git commit-tree "$TREE" ${PARENT:+-p "$PARENT"} -m "docs: redirect GitHub Pages to ${ORIGIN}")"
git push -q "$REMOTE" "${COMMIT}:refs/heads/${BRANCH}"
echo "published ${BRANCH} (${COMMIT}), redirecting to ${ORIGIN}"
echo "GitHub Pages still serves its current source until it is switched (see the header of this script)."
