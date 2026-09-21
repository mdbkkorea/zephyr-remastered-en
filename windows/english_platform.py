"""Host-native backup locations, process checks and operation locks."""
import contextlib
import os
from pathlib import Path
import shlex
import subprocess
import sys


def state_home():
    if sys.platform == 'win32':
        return Path(os.environ['LOCALAPPDATA'])/'ZephyrEnglishPatcher'
    if sys.platform == 'darwin':
        return Path.home()/'Library/Application Support/ZephyrEnglishPatcher'
    configured = os.environ.get('XDG_STATE_HOME')
    base = Path(configured) if configured and Path(configured).is_absolute() else Path.home()/'.local/state'
    return base/'zephyr-english-patcher'


def path_key(path):
    value = str(Path(path).resolve())
    # Linux allows different directories differing only in case.
    return value.casefold() if sys.platform == 'win32' else value


def has_game_process(output):
    for line in output.splitlines():
        try: tokens = shlex.split(line, posix=False)
        except ValueError: tokens = line.split()
        for token in tokens:
            if token.strip("\"'").replace('\\','/').rsplit('/',1)[-1].casefold() == 'zephyrremastered.exe':
                return True
    return False


def require_game_stopped():
    if sys.platform == 'win32':
        result = subprocess.run(['tasklist','/FI','IMAGENAME eq ZephyrRemastered.exe','/FO','CSV','/NH'],capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),check=True)
        running = b'zephyrremastered.exe' in result.stdout.lower()
    else:
        result = subprocess.run(['/bin/ps','-ax','-o','args='],capture_output=True,text=True,check=True)
        running = has_game_process(result.stdout)
    if running:
        raise ValueError('Save and close Zephyr Remastered in Steam, CrossOver, Wine or Proton before patching.')


@contextlib.contextmanager
def operation_lock(home):
    home = Path(home)
    home.mkdir(parents=True,exist_ok=True)
    with (home/'operation.lock').open('a+b') as handle:
        if sys.platform == 'win32':
            import msvcrt
            handle.seek(0);handle.write(b'0');handle.flush();handle.seek(0)
            try: msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc: raise ValueError('Another patch operation is running.') from exc
            try: yield
            finally:
                handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
        else:
            import fcntl
            try: fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError as exc: raise ValueError('Another patch operation is running.') from exc
            try: yield
            finally: fcntl.flock(handle,fcntl.LOCK_UN)
