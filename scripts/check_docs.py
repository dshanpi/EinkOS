#!/usr/bin/env python3
"""Check screenshot provenance, route coverage and repository documentation links."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from version_lock import projects_digest

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_phone():
    output = ROOT / 'docs/screenshots'
    inputs = ['platforms/tina/connectd.c', 'scripts/screenshots.py']
    images = sorted(output.glob('2*-phone-*.png'))
    if len(images) != 3:
        raise ValueError('Expected three browser screenshots')
    manifest = {'method': 'Chromium capture of actual connectd.c HTML templates; fictional SSIDs; no network commands',
                'viewport': [390, 760], 'hardware_capture': False,
                'inputs': {name: digest(ROOT / name) for name in inputs},
                'images': [{'file': path.name, 'sha256': digest(path)} for path in images]}
    (output / 'phone-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


def check():
    failures = []
    output = ROOT / 'docs/screenshots'
    readme = (ROOT / 'README.md').read_text()
    for name in ['manifest.json', 'phone-manifest.json']:
        manifest = json.loads((output / name).read_text())
        for path, expected in manifest['inputs'].items():
            if digest(ROOT / path) != expected:
                failures.append(f'{name}: input changed; regenerate screenshots: {path}')
        for item in manifest['images']:
            if digest(output / item['file']) != item['sha256']:
                failures.append(f'Image hash mismatch: {item["file"]}')
            if f'docs/screenshots/{item["file"]}' not in readme:
                failures.append(f'Screenshot missing from README: {item["file"]}')
    enum = re.search(r'enum desktop_screen\s*\{([^}]+)', (ROOT / 'src/ui.h').read_text()).group(1)
    routes = set(re.findall(r'DESKTOP_\w+', enum))
    cases = re.findall(r'CAPTURE\("([^"]+)",\s*(DESKTOP_\w+)', (ROOT / 'tools/ui_capture.c').read_text())
    if routes - {route for _, route in cases}:
        failures.append('Missing desktop route capture: ' + ', '.join(sorted(routes - {route for _, route in cases})))
    for name, _ in cases:
        if not (output / (name + '.png')).is_file():
            failures.append('Missing screenshot: ' + name)
    for record in (ROOT / 'releases').glob('v*.json'):
        if record.stem.endswith('-sdk'):
            continue
        lock = json.loads(record.read_text())
        sdk = json.loads(record.with_name(record.stem + '-sdk.json').read_text())
        if lock['release'] != record.stem or projects_digest(sdk) != lock['sdk']['projects_sha256']:
            failures.append(f'Committed release/SDK record mismatch: {record.name}')
    docs = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'CONTRIBUTING.md']
    docs += list((ROOT / 'docs').rglob('*.md')) + list((ROOT / 'standards').rglob('*.md')) + list((ROOT / 'skills').rglob('SKILL.md'))
    for doc in docs:
        links = re.findall(r'\]\(([^)]+)\)|src="([^"]+)"', doc.read_text())
        for markdown, html in links:
            target = (markdown or html).split('#', 1)[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            if not (doc.parent / target).exists():
                failures.append(f'{doc.relative_to(ROOT)}: broken link {target}')
    return failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record-phone', action='store_true')
    args = parser.parse_args()
    if args.record_phone:
        record_phone()
    else:
        failures = check()
        if failures:
            print('\n'.join(failures))
            raise SystemExit(1)
        print('PASS: screenshot inputs/hashes, desktop route coverage and documentation links')
