#!/bin/sh
# Requires GitHub CLI authenticated for dshanpi/EinkOS.
set -eu
cd "$(dirname "$0")/.."
version=$(cat VERSION)
assets=${1:-dist}
python3 - "$assets" <<'PY'
import json, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
info = json.loads((root / 'build-info.json').read_text())
assert info['version'] == pathlib.Path('VERSION').read_text().strip()
assert info['application_commit'] == subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert list(root.glob('*.img.gz')), 'Missing firmware image'
assert list(root.glob('*-source.tar.gz')), 'Missing source bundle'
subprocess.run(['sha256sum', '-c', 'SHA256SUMS'], cwd=root, check=True)
PY
command -v gh >/dev/null
# Always begin as a draft. Publishing is a separate explicit operation.
gh release create "v$version" --repo dshanpi/EinkOS --target "$(git rev-parse HEAD)" \
  --draft --prerelease --title "EinkOS v$version" --notes-file docs/RELEASE_NOTES.md \
  "$assets"/*-source.tar.gz "$assets"/*.img.gz "$assets/SHA256SUMS" \
  "$assets/build-info.json" "$assets/validation.json"
