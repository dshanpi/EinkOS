#!/usr/bin/env python3
"""Validate a release's actual assets before draft upload or promotion."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import tarfile
from release import BOARD, REQUIRED_CHECKS, sha256

BUILD_CHECKS = ['logic_tests', 'release_tool_tests', 'standalone_source_build',
                'arm_application_build', 'openwrt_image_build', 'firmware_pack',
                'rootfs_application_identity']


def check_assets(directory, channel='draft'):
    root = Path(directory)
    failures = []
    if channel not in ('draft', 'prerelease', 'stable'):
        return ['Unknown release channel']
    try:
        info = json.loads((root / 'build-info.json').read_text())
        report = json.loads((root / 'validation.json').read_text())
        version, commit = info['version'], info['application_commit']
        if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', version):
            return ['Invalid version']
        if not re.fullmatch(r'[a-f0-9]{40}', commit):
            return ['Application commit must be a full SHA-1']
        image_name = f'EinkOS-v{version}-{BOARD}.img.gz'
        source_name = f'EinkOS-v{version}-source.tar.gz'
        required = {image_name, source_name, 'build-info.json', 'validation.json'}
        checksums = {}
        for line in (root / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split(None, 1)
            name = name.lstrip('*')
            if not re.fullmatch(r'[a-f0-9]{64}', digest) or Path(name).name != name or name in checksums:
                return ['Invalid or duplicate SHA256SUMS entry']
            checksums[name] = digest
        if not required <= checksums.keys():
            return ['SHA256SUMS does not cover every required asset']
        for name, expected in checksums.items():
            if (root / name).is_symlink() or sha256(root / name) != expected:
                failures.append(f'Checksum mismatch: {name}')
        if failures:
            return failures
        if checksums[image_name] != info['compressed_sha256'] or checksums[source_name] != info['application_source_sha256']:
            failures.append('Build metadata does not match source/image assets')
        digest = hashlib.sha256()
        with gzip.open(root / image_name, 'rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        if digest.hexdigest() != info['image_sha256'] or report.get('image_sha256') != info['image_sha256']:
            failures.append('Uncompressed image or validation report SHA-256 mismatch')
        with tarfile.open(root / source_name, 'r:gz') as archive:
            prefix = f'EinkOS-v{version}/'
            for name, expected in [('VERSION', version), ('SOURCE_COMMIT', commit)]:
                stream = archive.extractfile(prefix + name)
                if stream is None or stream.read().decode().strip() != expected:
                    failures.append(f'Source archive {name} mismatch')
            archive.getmember(prefix + 'LICENSE')
            archive.getmember(prefix + 'third_party/lvgl/lvgl.h')
        for key in REQUIRED_CHECKS:
            if report.get('checks', {}).get(key) not in ('passed', 'failed', 'not_run'):
                failures.append(f'Missing/invalid hardware result: {key}')
        if info.get('board') != BOARD or not re.fullmatch(r'[a-f0-9]{40}', info.get('hardware', {}).get('commit', '')):
            failures.append('Missing supported board/hardware commit')
        if channel != 'draft':
            for key in BUILD_CHECKS:
                if not re.fullmatch(r'passed(?: \([^\n]*\))?', report.get('build_checks', {}).get(key, '')):
                    failures.append(f'Build check not passed: {key}')
            if any(report['checks'][key] == 'failed' for key in REQUIRED_CHECKS):
                failures.append('Known failed hardware checks prevent publication')
            review = report.get('distribution_review', {})
            if (review.get('status') != 'passed' or not review.get('reviewer')
                    or review.get('image_sha256') != info['image_sha256']
                    or not str(review.get('source_url', '')).startswith('https://')
                    or not str(review.get('vendor_notices_url', '')).startswith('https://')):
                failures.append('Corresponding-source / vendor distribution review missing for this image')
            if not report.get('notes'):
                failures.append('Release validation notes missing')
        if channel == 'stable':
            for key in REQUIRED_CHECKS:
                if report.get('checks', {}).get(key) != 'passed':
                    failures.append(f'Hardware check not passed: {key}')
    except (OSError, ValueError, KeyError, tarfile.TarError, EOFError) as error:
        failures.append(f'Cannot validate assets: {error}')
    return failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--channel', choices=['draft', 'prerelease', 'stable'], default='draft')
    args = parser.parse_args()
    failures = check_assets(args.directory, args.channel)
    if failures:
        for failure in failures:
            print('FAIL:', failure)
        raise SystemExit(1)
    print('PASS:', args.channel, 'release gate')
