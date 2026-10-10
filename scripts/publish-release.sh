#!/bin/sh
# Upload immutable build assets as a draft; documentation HEAD may be newer.
set -eu
cd "$(dirname "$0")/.."
assets=${1:-dist}
python3 scripts/check_release.py "$assets" --channel draft
version=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$assets/build-info.json")
commit=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["application_commit"])' "$assets/build-info.json")
command -v gh >/dev/null
python3 scripts/version_lock.py "$assets" --verify-remote
release_notes=$(mktemp)
trap 'rm -f "$release_notes"' EXIT HUP INT TERM
cat docs/RELEASE_NOTES.md > "$release_notes"
python3 scripts/version_lock.py "$assets" --notes >> "$release_notes"
gh release create "v$version" --repo dshanpi/EinkOS --target "$commit" \
  --verify-tag --draft --prerelease --title "EinkOS v$version" --notes-file "$release_notes" \
  "$assets"/*-source.tar.gz "$assets"/*.img.gz "$assets/SHA256SUMS" \
  "$assets/build-info.json" "$assets/validation.json" "$assets/release-lock.json"
