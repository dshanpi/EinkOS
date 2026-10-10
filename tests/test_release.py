import gzip
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from release import compress, sha256, validation_complete, REQUIRED_CHECKS


class ReleaseTest(unittest.TestCase):
    def test_image_roundtrip_and_reproducible_gzip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            image = root / 'test.img'
            image.write_bytes(bytes(range(256)) * 100)
            a, b = root / 'a.gz', root / 'b.gz'
            compress(image, a)
            compress(image, b)
            self.assertEqual(sha256(a), sha256(b))
            self.assertEqual(gzip.decompress(a.read_bytes()), image.read_bytes())
            self.assertEqual(a.read_bytes()[4:8], bytes(4))

    def test_stable_requires_all_hardware_checks(self):
        self.assertFalse(validation_complete({}))
        checks = dict.fromkeys(REQUIRED_CHECKS, 'passed')
        self.assertTrue(validation_complete({'checks': checks}))
        for status in ['failed', 'not_run']:
            checks['lynx_flash'] = status
            self.assertFalse(validation_complete({'checks': checks}))
