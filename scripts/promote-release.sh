#!/bin/sh
# Validate the downloaded release, not a potentially different local copy.
set -eu
cd "$(dirname "$0")/.."
tag=${1:?usage: promote-release.sh vVERSION prerelease-or-stable}
channel=${2:?usage: promote-release.sh vVERSION prerelease-or-stable}
case "$channel" in prerelease|stable) ;; *) echo 'Expected prerelease or stable' >&2; exit 2 ;; esac
case "$tag" in v[0-9]*) ;; *) echo 'Expected vVERSION' >&2; exit 2 ;; esac
command -v gh >/dev/null
release_tmp=$(mktemp -d)
trap 'rm -rf "$release_tmp"' EXIT HUP INT TERM
gh release download "$tag" --repo dshanpi/EinkOS --dir "$release_tmp"
python3 scripts/check_release.py "$release_tmp" --channel "$channel"
version=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$release_tmp/build-info.json")
[ "$tag" = "v$version" ] || { echo 'Tag does not match assets' >&2; exit 1; }
if [ "$channel" = stable ]; then
  gh release edit "$tag" --repo dshanpi/EinkOS --draft=false --prerelease=false
else
  gh release edit "$tag" --repo dshanpi/EinkOS --draft=false --prerelease=true
fi
