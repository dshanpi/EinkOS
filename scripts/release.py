#!/usr/bin/env python3
"""Package a freshly built board image, provenance and standalone source."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET
from source_archive import ROOT, archive, git

BOARD = '100ask-t113-pro-240x360'
REQUIRED_CHECKS = ['cold_boot', 'keys', 'display_refresh', 'reader_resume',
                   'wifi_success_and_recovery', 'time_restore_and_sync',
                   'bluetooth_or_unavailable', 'lynx_flash']


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def compress(image, output):
    with Path(image).open('rb') as source, Path(output).open('wb') as dest:
        with gzip.GzipFile(filename='', fileobj=dest, mode='wb', mtime=0, compresslevel=9) as gz:
            shutil.copyfileobj(source, gz)


def validation_complete(report):
    return all(report.get('checks', {}).get(key) == 'passed' for key in REQUIRED_CHECKS)


def repo_info(path):
    def run(*args):
        return subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()
    return {'commit': run('rev-parse', 'HEAD'),
            'tracked_changes': run('status', '--porcelain', '--untracked-files=no').splitlines()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image', required=True, type=Path)
    p.add_argument('--sdk', required=True, type=Path)
    p.add_argument('--hardware', required=True, type=Path)
    p.add_argument('--rootfs', required=True, type=Path)
    p.add_argument('--compiler', required=True)
    p.add_argument('--validation', required=True, type=Path)
    p.add_argument('--output', default=ROOT / 'dist', type=Path)
    args = p.parse_args()
    version = (ROOT / 'VERSION').read_text().strip()
    commit = git('rev-parse', 'HEAD').decode().strip()
    if git('status', '--porcelain', '--untracked-files=normal').strip():
        p.error('Commit the application tree before packaging.')
    if args.image.stat().st_size < 1024 * 1024:
        p.error('Expected a complete board image, not an application binary.')
    installed = args.rootfs / 'usr/share/eink-os'
    if (installed / 'VERSION').read_text().strip() != version:
        p.error('Root filesystem application version does not match this source.')
    installed_commit = (installed / 'SOURCE_COMMIT').read_text().strip()
    if installed_commit != commit:
        p.error('Root filesystem application commit does not match this source.')
    if args.image.stat().st_mtime < (installed / 'SOURCE_COMMIT').stat().st_mtime:
        p.error('Image predates the installed application; rebuild and pack first.')
    report = json.loads(args.validation.read_text())
    if report.get('image_sha256') != sha256(args.image):
        p.error('Validation report must name the exact uncompressed image SHA-256.')
    args.output.mkdir(parents=True, exist_ok=True)
    image = args.output / f'EinkOS-v{version}-{BOARD}.img.gz'
    compress(args.image, image)
    source = archive(args.output)
    projects = []
    manifest = args.sdk / '.repo/manifest.xml'
    for project in ET.parse(manifest).getroot().iter('project'):
        path = project.get('path', project.get('name'))
        try:
            info = repo_info(args.sdk / path)
        except subprocess.CalledProcessError:
            info = {'unavailable': True}
        projects.append({'path': path, **info})
    metadata = {
        'schema_version': 1, 'version': version, 'application_commit': commit,
        'hardware_repository': 'https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5',
        'hardware': repo_info(args.hardware), 'sdk_projects': projects,
        'board': BOARD, 'chip': 't113', 'board_config': 'evb1_auto_nand',
        'kernel': 'linux-5.4', 'rootfs': 'openwrt',
        'toolchain': subprocess.check_output([args.compiler, '--version'], text=True).splitlines()[0],
        'build_commands': ['./build.sh', './build.sh pack'],
        'source_date_epoch': int(git('show', '-s', '--format=%ct', 'HEAD')),
        'image_sha256': sha256(args.image), 'compressed_sha256': sha256(image),
        'application_source_sha256': sha256(source),
        'hardware_validation_complete': validation_complete(report),
        'release_channel': 'stable' if validation_complete(report) else 'prerelease',
    }
    (args.output / 'build-info.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (args.output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    files = [source, image, args.output / 'build-info.json', args.output / 'validation.json']
    (args.output / 'SHA256SUMS').write_text(''.join(f'{sha256(f)}  {f.name}\n' for f in files))
    print(f'Prepared {metadata["release_channel"]} assets in {args.output}')


if __name__ == '__main__':
    main()
