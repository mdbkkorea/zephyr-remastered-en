import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'windows'))
import english_crossover as launcher


@unittest.skipIf(sys.platform == 'win32', 'CrossOver drive mappings require POSIX symlinks')
class CrossOverLauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.app = self.root / 'Custom Apps/CrossOver.app'
        self.bottle = self.root / 'My bottle'
        self.game = self.bottle / launcher.GAME_REL
        self.game.mkdir(parents=True)
        (self.game / 'ZephyrRemastered.exe').touch()
        wine = self.app / launcher.WINE
        wine.parent.mkdir(parents=True)
        wine.touch()
        wine.chmod(0o755)
        for name in ('system.reg', 'cxbottle.conf'):
            (self.bottle / name).touch()
        drives = self.bottle / 'dosdevices'
        drives.mkdir()
        (drives / 'c:').symlink_to(self.bottle / 'drive_c', target_is_directory=True)
        (drives / 'z:').symlink_to('/', target_is_directory=True)
        self.settings = dict(app=str(self.app), bottle=str(self.bottle), game=str(self.game))

    def test_nondefault_paths_and_c_drive(self):
        args = launcher.launch_args(self.settings)
        self.assertEqual(args[args.index('--bottle') + 1], str(self.bottle))
        self.assertEqual(args[args.index('--dll') + 1], 'winhttp=n,b')
        self.assertEqual(args[-1], 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\'
                         'The Rhapsody of Zephyr Remastered\\ZephyrRemastered.exe')

    def test_external_library_shell_characters_stay_literal(self):
        game = self.root / 'External Library/$(touch SHOULD_NOT_EXIST); Game'
        game.mkdir(parents=True)
        (game / 'ZephyrRemastered.exe').touch()
        self.settings['game'] = str(game)
        args = launcher.launch_args(self.settings)
        self.assertEqual(args[-2], str(game))
        self.assertTrue(args[-1].startswith('Z:\\'))
        self.assertIn('$(touch SHOULD_NOT_EXIST); Game', args[-1])
        (self.bottle / 'dosdevices/z:').unlink()
        with self.assertRaisesRegex(ValueError, 'not accessible'):
            launcher.launch_args(self.settings)

    def test_missing_bottle_rejected_and_corrupt_settings_recovered(self):
        (self.bottle / 'cxbottle.conf').unlink()
        with self.assertRaisesRegex(ValueError, 'Required file'):
            launcher.launch_args(self.settings)
        config = self.root / 'settings.json'
        for content in ('invalid', '[]', '{"app": 42}'):
            config.write_text(content)
            self.assertEqual(launcher.load_settings(config, self.settings), self.settings)
        config.write_text(json.dumps(self.settings))
        self.assertEqual(launcher.load_settings(config, {}), {})
        self.assertEqual(launcher.load_settings(config, self.settings), self.settings)


if __name__ == '__main__':
    unittest.main()
