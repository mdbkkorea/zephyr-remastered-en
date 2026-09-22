import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'windows'))
import english_platform as platform

class PlatformTests(unittest.TestCase):
    def test_wine_proton_process_forms(self):
        examples=['wine64 "Z:\\Users\\name\\Game Folder\\ZephyrRemastered.exe"', '/games/ZephyrRemastered.exe', 'wine /games/ZephyrRemastered.exe', '"/games/Game Folder/ZephyrRemastered.exe"']
        for command in examples:
            self.assertTrue(platform.has_game_process(command),command)
        self.assertFalse(platform.has_game_process('python english_engine.py status --game /games/Zephyr\n/usr/bin/wineserver'))

    def test_linux_state_and_case_sensitive_paths(self):
        absolute_state = Path(tempfile.gettempdir()).resolve()/'zephyr-state-test'
        with patch.object(platform.sys,'platform','linux'),patch.dict(os.environ,{'XDG_STATE_HOME':str(absolute_state)}):
            self.assertEqual(platform.state_home(),absolute_state/'zephyr-english-patcher')
            self.assertNotEqual(platform.path_key('/tmp/Game'),platform.path_key('/tmp/game'))
        with patch.object(platform.sys,'platform','linux'),patch.dict(os.environ,{'XDG_STATE_HOME':'relative'}):
            self.assertTrue(platform.state_home().is_absolute())

    def test_mac_and_windows_state(self):
        with patch.object(platform.sys,'platform','darwin'):
            self.assertEqual(platform.state_home(),Path.home()/'Library/Application Support/ZephyrEnglishPatcher')
        with patch.object(platform.sys,'platform','win32'),patch.dict(os.environ,{'LOCALAPPDATA':'/tmp/localappdata'}):
            self.assertEqual(platform.state_home(),Path('/tmp/localappdata/ZephyrEnglishPatcher'))

    def test_running_game_and_failed_scan_block(self):
        with patch.object(platform.sys,'platform','linux'),patch.object(platform.subprocess,'run',return_value=subprocess.CompletedProcess([],0,stdout='wine /games/ZephyrRemastered.exe')):
            with self.assertRaises(ValueError):platform.require_game_stopped()
        with patch.object(platform.sys,'platform','darwin'),patch.object(platform.subprocess,'run',side_effect=subprocess.CalledProcessError(1,'ps')):
            with self.assertRaises(subprocess.CalledProcessError):platform.require_game_stopped()

    @unittest.skipIf(sys.platform=='win32','POSIX lock test')
    def test_real_posix_lock_contention_and_release(self):
        with tempfile.TemporaryDirectory() as home:
            with platform.operation_lock(home):
                with self.assertRaises(ValueError):
                    with platform.operation_lock(home):pass
            with platform.operation_lock(home):pass
