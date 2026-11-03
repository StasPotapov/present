import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('present', ROOT / 'scripts/present.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.mock_home = patch.object(Path, 'home', return_value=self.home)
        self.mock_home.start()

    def tearDown(self):
        self.mock_home.stop()
        self.tmp.cleanup()

    def test_preview_does_not_write(self):
        result = cli.setup('codex', False)
        self.assertEqual(len(result['planned']), 2)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_repeat_and_client_isolation(self):
        self.assertEqual(len(cli.setup('codex', True)['installed']), 2)
        self.assertFalse((self.home / '.claude').exists())
        self.assertEqual(cli.setup('codex', True)['installed'], [])
        cli.setup('claude-code', True)
        for native in ['.agents', '.claude']:
            root = self.home / native / 'skills'
            self.assertEqual((root / 'present').resolve(), ROOT)
            self.assertEqual((root / 'present-setup').resolve(), ROOT / 'setup')
            self.assertTrue((root / 'present/assets/kernel.html').is_file())

    def test_foreign_second_target_prevents_first_write(self):
        folder = self.home / '.agents/skills'
        folder.mkdir(parents=True)
        (folder / 'present-setup').write_text('user content')
        with self.assertRaisesRegex(ValueError, 'foreign'):
            cli.setup('codex', True)
        self.assertFalse((folder / 'present').exists())
        self.assertEqual((folder / 'present-setup').read_text(), 'user content')

    def test_foreign_and_dangling_links_preserved(self):
        folder = self.home / '.agents/skills'
        folder.mkdir(parents=True)
        target = folder / 'present'
        target.symlink_to(self.home / 'missing')
        with self.assertRaises(ValueError):
            cli.setup('codex', True)
        self.assertEqual(os.readlink(target), str(self.home / 'missing'))
        self.assertFalse((folder / 'present-setup').exists())

    def test_partial_failure_rolls_back_links(self):
        original = Path.symlink_to
        def fail_second(path, *args, **kwargs):
            if path.name == 'present-setup':
                raise OSError('injected write failure')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'symlink_to', fail_second):
            with self.assertRaises(OSError):
                cli.setup('codex', True)
        self.assertFalse(os.path.lexists(self.home / '.agents/skills/present'))

    def test_no_ai_cli_needed(self):
        for args in [['--help'], ['--version'], ['doctor']]:
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/present.py'), *args],
                                    env={**os.environ, 'PATH': ''}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = json.loads(result.stdout)
        self.assertIsNone(result['node'])
        self.assertFalse(result['ai_client_cli_required'])

    def test_incomplete_package_refuses_install(self):
        with patch.object(cli, 'ROOT', self.home / 'missing'):
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                cli.setup('codex', True)
        self.assertFalse((self.home / '.agents').exists())

    def test_partially_damaged_package_refuses_install(self):
        package = self.home / 'package'
        for name in cli.RESOURCES:
            file = package / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text('fixture')
        broken = package / 'stages/build.md'
        broken.unlink()
        broken.mkdir()  # A directory at a required file path is also invalid.
        (package / 'assets/cookbook.md').unlink()
        with patch.object(cli, 'ROOT', package):
            self.assertEqual(set(cli.doctor()['missing_resources']),
                             {'stages/build.md', 'assets/cookbook.md'})
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                cli.setup('codex', True)
        self.assertFalse((self.home / '.agents').exists())

    def test_cli_rejects_unknown_client(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/present.py'),
                                 'setup', '--client', 'unknown'], capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
