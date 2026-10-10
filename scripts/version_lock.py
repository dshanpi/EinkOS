#!/usr/bin/env python3
"""Bind a release to immutable application, hardware, SDK and image identities."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess

APP = 'https://github.com/dshanpi/EinkOS'
HARDWARE = 'https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5'
BRANCH = 'einkos-240x360'
RECIPE = 'openwrt/package/thirdparty/gui/eink-dashboard/Makefile'
SDK_BASELINE = 'TinaSDK 5.0 v1.2'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def projects_digest(projects):
    return digest(json.dumps(projects, sort_keys=True, separators=(',', ':')).encode())


def recipe_info(content):
    text = content.decode()
    def field(name):
        values = re.findall(r'^' + name + r'\s*:=\s*(\S+)\s*$', text, re.M)
        if len(values) != 1:
            raise ValueError('Missing/ambiguous package field: ' + name)
        return values[0]
    return {'path': RECIPE, 'sha256': digest(content),
            'application_version': field('PKG_VERSION'),
            'application_commit': field('PKG_SOURCE_VERSION'),
            'github_archive_sha256': field('PKG_HASH'),
            'source_date_epoch': int(field('EINK_SOURCE_EPOCH'))}


def make_lock(info, build_info_bytes, recipe):
    version = info['version']
    projects = info['sdk_projects']
    lock = {
        'schema_version': 1, 'release': 'v' + version,
        'application': {'repository': APP, 'tag': 'v' + version, 'commit': info['application_commit']},
        'hardware': {'repository': HARDWARE, 'branch': BRANCH, 'tag': 'einkos-v' + version,
                     'commit': info['hardware']['commit'], 'package': recipe_info(recipe)},
        'sdk': {'baseline': SDK_BASELINE, 'projects_file': 'build-info.json',
                'projects_field': 'sdk_projects', 'project_count': len(projects),
                'projects_sha256': projects_digest(projects),
                'modified_project_count': sum(bool(p.get('tracked_changes')) for p in projects)},
        'build': {key: info[key] for key in ('board', 'chip', 'board_config', 'kernel', 'rootfs')},
        'build_info_sha256': digest(build_info_bytes),
        'image': {'file': f'EinkOS-v{version}-{info["board"]}.img.gz',
                  'sha256': info['compressed_sha256'], 'uncompressed_sha256': info['image_sha256']},
        'source': {'file': f'EinkOS-v{version}-source.tar.gz', 'sha256': info['application_source_sha256']},
    }
    errors = validate_lock(lock, info, build_info_bytes)
    if errors:
        raise ValueError('; '.join(errors))
    return lock


def validate_lock(lock, info, build_info_bytes):
    errors = []
    def same(actual, expected, label):
        if actual != expected:
            errors.append('Version lock mismatch: ' + label)
    version = info['version']
    same(lock['schema_version'], 1, 'schema')
    same(lock['release'], 'v' + version, 'release')
    same(lock['application'], {'repository': APP, 'tag': 'v' + version,
                              'commit': info['application_commit']}, 'application')
    hw = lock['hardware']
    same(hw['repository'], info['hardware_repository'], 'hardware repository')
    same(hw['repository'], HARDWARE, 'supported hardware repository')
    same(hw['branch'], BRANCH, 'hardware development branch')
    same(hw['tag'], 'einkos-v' + version, 'hardware tag')
    same(hw['commit'], info['hardware']['commit'], 'hardware commit')
    same(info['hardware'].get('tracked_changes'), [], 'uncommitted hardware changes')
    package = hw['package']
    same(package['path'], RECIPE, 'package path')
    same(package['application_version'], version, 'package application version')
    same(package['application_commit'], info['application_commit'], 'package application commit')
    same(package['source_date_epoch'], info['source_date_epoch'], 'package source date')
    for key in ('sha256', 'github_archive_sha256'):
        if not re.fullmatch('[a-f0-9]{64}', package[key]):
            errors.append('Invalid package hash: ' + key)
    projects = info['sdk_projects']
    if not projects or len({p['path'] for p in projects}) != len(projects):
        errors.append('SDK project list is empty or has duplicates')
    for project in projects:
        if not re.fullmatch('[a-f0-9]{40}', project.get('commit', '')) or project.get('unavailable'):
            errors.append('SDK project has no immutable revision: ' + project['path'])
    same(lock['sdk'], {'baseline': SDK_BASELINE, 'projects_file': 'build-info.json',
                       'projects_field': 'sdk_projects', 'project_count': len(projects),
                       'projects_sha256': projects_digest(projects),
                       'modified_project_count': sum(bool(p.get('tracked_changes')) for p in projects)}, 'SDK projects')
    same(lock['build'], {k: info[k] for k in ('board', 'chip', 'board_config', 'kernel', 'rootfs')}, 'board configuration')
    same(lock['build_info_sha256'], digest(build_info_bytes), 'build-info checksum')
    same(lock['image'], {'file': f'EinkOS-v{version}-{info["board"]}.img.gz',
                        'sha256': info['compressed_sha256'], 'uncompressed_sha256': info['image_sha256']}, 'image')
    same(lock['source'], {'file': f'EinkOS-v{version}-source.tar.gz',
                         'sha256': info['application_source_sha256']}, 'source archive')
    return errors


def write_lock(directory, hardware):
    directory = Path(directory)
    raw = (directory / 'build-info.json').read_bytes()
    info = json.loads(raw)
    recipe = subprocess.check_output(['git', '-C', str(hardware), 'show', info['hardware']['commit'] + ':' + RECIPE])
    lock = make_lock(info, raw, recipe)
    target = directory / 'release-lock.json'
    target.write_text(json.dumps(lock, indent=2) + '\n')
    return target


def gh_json(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint]))


def tag_commit(repository, tag):
    repo = repository[len('https://github.com/'):]
    obj = gh_json(f'repos/{repo}/git/ref/tags/{tag}')['object']
    for _ in range(8):
        if obj['type'] == 'commit':
            return obj['sha']
        if obj['type'] != 'tag':
            break
        obj = gh_json(f'repos/{repo}/git/tags/{obj["sha"]}')['object']
    raise ValueError('Tag does not resolve to a commit: ' + tag)


def verify_remote(lock):
    for key in ('application', 'hardware'):
        item = lock[key]
        if tag_commit(item['repository'], item['tag']) != item['commit']:
            raise ValueError('Remote tag moved or points to the wrong commit: ' + item['tag'])
    hw = lock['hardware']
    repo = hw['repository'][len('https://github.com/'):]
    response = gh_json(f'repos/{repo}/contents/{RECIPE}?ref={hw["commit"]}')
    if recipe_info(base64.b64decode(response['content'])) != hw['package']:
        raise ValueError('Remote hardware package does not match the version lock')


def notes(lock):
    app, hw, sdk = lock['application'], lock['hardware'], lock['sdk']
    return f'''## 版本对应关系（以提交和哈希为准）

| 项目 | 此镜像使用的版本 |
| --- | --- |
| EinkOS | `{lock['release']}` · [{app['commit']}]({app['repository']}/tree/{app['commit']}) |
| 硬件开发分支 | [`{hw['branch']}`]({hw['repository']}/tree/{hw['branch']})（会继续更新） |
| 硬件固定版本 | [`{hw['tag']}`]({hw['repository']}/tree/{hw['tag']}) · [{hw['commit']}]({hw['repository']}/tree/{hw['commit']}) |
| SDK | {sdk['baseline']}；{sdk['project_count']} 个组件的精确提交见 `build-info.json` 的 `sdk_projects` |
| 构建配置 | `{lock['build']['chip']}` / `{lock['build']['board_config']}` / `{lock['build']['kernel']}` / `{lock['build']['rootfs']}` |
| 镜像 SHA-256（解压后） | `{lock['image']['uncompressed_sha256']}` |

附件 `release-lock.json` 将应用、硬件包配方、SDK 组件清单和镜像哈希绑定；
`SHA256SUMS` 包含该文件。硬件包配方固定同一应用提交，禁止用分支最新代码代替此版本。
SDK 有 {sdk['modified_project_count']} 个组件记录了本地修改；提交清单不是完整源码或补丁包，
仍须补齐对应源码/修改内容及分发审核后才能公开镜像。安装工具统一使用 [LYNX](https://github.com/dshanpi/lynx-releases)。
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--hardware', type=Path, help='Generate lock from recorded hardware commit')
    parser.add_argument('--verify-remote', action='store_true')
    parser.add_argument('--notes', action='store_true')
    args = parser.parse_args()
    if args.hardware:
        write_lock(args.directory, args.hardware)
    lock = json.loads((args.directory / 'release-lock.json').read_text())
    raw = (args.directory / 'build-info.json').read_bytes()
    errors = validate_lock(lock, json.loads(raw), raw)
    if errors:
        raise SystemExit('\n'.join(errors))
    if args.verify_remote:
        verify_remote(lock)
    if args.notes:
        print(notes(lock))
    else:
        print('PASS: release version lock' + (' and remote tags/package' if args.verify_remote else ''))


if __name__ == '__main__':
    main()
