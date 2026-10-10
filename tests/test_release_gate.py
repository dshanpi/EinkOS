import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_release import check_assets, BUILD_CHECKS
from release import BOARD, REQUIRED_CHECKS, sha256


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.image = self.root / f'EinkOS-v0.1.0-{BOARD}.img.gz'
        self.source = self.root / 'EinkOS-v0.1.0-source.tar.gz'
        payload = b'fixture firmware image\n' * 100
        self.image.write_bytes(gzip.compress(payload))
        with tarfile.open(self.source, 'w:gz') as archive:
            for name, value in [('VERSION', '0.1.0'), ('SOURCE_COMMIT', 'a' * 40), ('LICENSE', 'fixture'), ('third_party/lvgl/lvgl.h', 'fixture')]:
                member = tarfile.TarInfo('EinkOS-v0.1.0/' + name)
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value.encode()))
        self.info = {'version': '0.1.0', 'application_commit': 'a' * 40, 'board': BOARD,
                     'hardware': {'commit': 'b' * 40}, 'image_sha256': hashlib.sha256(payload).hexdigest(),
                     'compressed_sha256': sha256(self.image), 'application_source_sha256': sha256(self.source)}
        self.report = {'image_sha256': self.info['image_sha256'], 'checks': dict.fromkeys(REQUIRED_CHECKS, 'not_run'),
                       'build_checks': dict.fromkeys(BUILD_CHECKS, 'passed'), 'notes': 'Synthetic unit-test fixture'}
        self.save()

    def save(self):
        (self.root / 'build-info.json').write_text(json.dumps(self.info))
        (self.root / 'validation.json').write_text(json.dumps(self.report))
        files = [self.image, self.source, self.root / 'build-info.json', self.root / 'validation.json']
        (self.root / 'SHA256SUMS').write_text(''.join(f'{sha256(p)}  {p.name}\n' for p in files))

    def review(self):
        self.report['distribution_review'] = {'status': 'passed', 'reviewer': 'fixture reviewer',
            'image_sha256': self.info['image_sha256'], 'source_url': 'https://example.test/source',
            'vendor_notices_url': 'https://example.test/notices'}
        self.save()

    def test_draft_accepts_unrun_hardware_but_publication_requires_review(self):
        self.assertEqual(check_assets(self.root), [])
        self.assertTrue(check_assets(self.root, 'prerelease'))
        self.review()
        self.assertEqual(check_assets(self.root, 'prerelease'), [])
        self.assertTrue(check_assets(self.root, 'stable'))

    def test_stable_requires_every_hardware_result(self):
        self.review()
        self.report['checks'] = dict.fromkeys(REQUIRED_CHECKS, 'passed')
        self.save()
        self.assertEqual(check_assets(self.root, 'stable'), [])
        self.report['checks']['lynx_flash'] = 'failed'
        self.save()
        self.assertTrue(check_assets(self.root, 'stable'))
        self.assertTrue(check_assets(self.root, 'prerelease'))

    def test_tampered_image_rejected(self):
        self.image.write_bytes(b'tampered')
        self.assertTrue(check_assets(self.root))

    def test_old_validation_cannot_approve_different_image(self):
        self.report['image_sha256'] = '0' * 64
        self.save()
        self.assertTrue(check_assets(self.root))

    def test_source_commit_must_match_metadata(self):
        self.info['application_commit'] = 'c' * 40
        self.save()
        self.assertTrue(check_assets(self.root))

    def test_missing_checksum_entry_rejected(self):
        p = self.root / 'SHA256SUMS'
        p.write_text('\n'.join(p.read_text().splitlines()[:-1]) + '\n')
        self.assertTrue(check_assets(self.root))

    def test_distribution_review_is_bound_to_image(self):
        self.review()
        self.report['distribution_review']['image_sha256'] = '0' * 64
        self.save()
        self.assertTrue(check_assets(self.root, 'prerelease'))
