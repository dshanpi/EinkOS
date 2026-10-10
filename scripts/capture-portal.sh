#!/usr/bin/env bash
# Run after `make screenshots`. Requires Node/npm and Playwright Chromium.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p output/playwright
cli=(npx --yes --package @playwright/cli playwright-cli -s=einkos-docs)
python3 -m http.server 8769 --bind 127.0.0.1 --directory build/preview > output/playwright/server.log 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT
# Set PW_CONFIG to use a locally installed browser; no board services are started.
config_args=()
if [[ -n "${PW_CONFIG:-}" ]]; then config_args+=(--config="$PW_CONFIG"); fi
python3 - <<'PY'
import time, urllib.request
for _ in range(30):
    try:
        urllib.request.urlopen('http://127.0.0.1:8769/portal.html', timeout=1).close()
        break
    except OSError:
        time.sleep(.1)
else:
    raise SystemExit('Preview server unavailable')
PY
kill -0 "$server_pid" 2>/dev/null || { echo "Preview port 8769 is already occupied" >&2; exit 1; }
"${cli[@]}" open http://127.0.0.1:8769/portal.html "${config_args[@]}"
"${cli[@]}" resize 390 760
"${cli[@]}" screenshot --filename=output/playwright/27-phone-portal.png --full-page
"${cli[@]}" goto http://127.0.0.1:8769/portal-success.html
"${cli[@]}" screenshot --filename=output/playwright/28-phone-success.png --full-page
"${cli[@]}" goto http://127.0.0.1:8769/portal-failure.html
"${cli[@]}" screenshot --filename=output/playwright/29-phone-failure.png --full-page
"${cli[@]}" close
cp output/playwright/2*-phone-*.png docs/screenshots/
python3 scripts/check_docs.py --record-phone
