#!/usr/bin/env python3
"""Create a deterministic standalone source archive from a committed revision."""
import argparse
import gzip
import io
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def archive(output, revision='HEAD'):
    commit = git('rev-parse', revision + '^{commit}').decode().strip()
    version = git('show', commit + ':VERSION').decode().strip()
    epoch = int(git('show', '-s', '--format=%ct', commit))
    prefix = f'EinkOS-v{version}'
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    target = output / f'{prefix}-source.tar.gz'
    source = git('archive', '--format=tar', f'--prefix={prefix}/', commit)
    with target.open('wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=io.BytesIO(source)) as old, tarfile.open(fileobj=gz, mode='w|') as new:
            for member in old:
                new.addfile(member, old.extractfile(member) if member.isfile() else None)
            for name, text in [('SOURCE_COMMIT', commit + '\n'), ('SOURCE_DATE_EPOCH', str(epoch) + '\n')]:
                content = text.encode()
                info = tarfile.TarInfo(f'{prefix}/{name}')
                info.size = len(content)
                info.mtime = epoch
                info.mode = 0o644
                new.addfile(info, io.BytesIO(content))
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='dist')
    parser.add_argument('--revision', default='HEAD')
    args = parser.parse_args()
    print(archive(args.output, args.revision))
