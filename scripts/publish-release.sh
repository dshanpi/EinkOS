#!/bin/sh
# Upload immutable build assets as a draft; documentation HEAD may be newer.
set -eu
cd "$(dirname "$0")/.."
assets=${1:-dist}
python3 scripts/check_release.py "$assets" --channel draft
version=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$assets/build-info.json")
commit=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["application_commit"])' "$assets/build-info.json")
command -v gh >/dev/null
gh release create "v$version" --repo dshanpi/EinkOS --target "$commit" \
  --draft --prerelease --title "EinkOS v$version" --notes-file docs/RELEASE_NOTES.md \
  "$assets"/*-source.tar.gz "$assets"/*.img.gz "$assets/SHA256SUMS" \
  "$assets/build-info.json" "$assets/validation.json"
