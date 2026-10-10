import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from version_lock import tag_commit, verify_remote, APP, HARDWARE, recipe_info


class RemoteVersionTests(TestCase):
    def test_annotated_tag_is_resolved(self):
        with patch('version_lock.gh_json', side_effect=[
                {'object': {'type': 'tag', 'sha': 'b' * 40}},
                {'object': {'type': 'commit', 'sha': 'a' * 40}}]):
            self.assertEqual(tag_commit(APP, 'v0.1.0'), 'a' * 40)

    def test_moved_tag_blocks_publication(self):
        lock = {'application': {'repository': APP, 'tag': 'v0.1.0', 'commit': 'a' * 40}}
        with patch('version_lock.tag_commit', return_value='b' * 40):
            with self.assertRaisesRegex(ValueError, 'Remote tag moved'):
                verify_remote(lock)

    def test_remote_package_mismatch_blocks_publication(self):
        import base64
        recipe = b'PKG_VERSION:=0.1.0\nPKG_SOURCE_VERSION:=' + b'a' * 40 + b'\nPKG_HASH:=' + b'd' * 64 + b'\nEINK_SOURCE_EPOCH:=1234\n'
        lock = {'application': {'repository': APP, 'tag': 'v0.1.0', 'commit': 'a' * 40},
                'hardware': {'repository': HARDWARE, 'tag': 'einkos-v0.1.0', 'commit': 'b' * 40,
                             'package': recipe_info(recipe)}}
        with patch('version_lock.tag_commit', side_effect=['a' * 40, 'b' * 40]), patch(
                'version_lock.gh_json', return_value={'content': base64.b64encode(recipe.replace(b'0.1.0', b'0.2.0')).decode()}):
            with self.assertRaisesRegex(ValueError, 'Remote hardware package'):
                verify_remote(lock)
