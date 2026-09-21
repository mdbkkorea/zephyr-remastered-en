# English patcher for macOS / CrossOver and Linux / Proton

This patches the same Windows game resources as the Windows patcher. It does not turn the game into a native Mac/Linux game. Continue launching the game using CrossOver or Steam Proton.

## Run without building

Install Python 3.9 or newer and Tkinter (Tk 8.6+ on macOS). On Fedora 44:

```sh
sudo dnf install python3 python3-pip python3-tkinter
```

Extract the kit, open a terminal in that folder, then run:

```sh
python3 english_app.py
```

On macOS, use a Python installation with working Tcl/Tk (the python.org installer includes it). `Run-Patcher.command` also starts the GUI. Source mode needs no pip packages. All installation operations should run as your normal user, not root/sudo.

If there is no graphical display, use the same engine directly:

```sh
python3 english_engine.py status --game '/absolute/path/to/game copy'
python3 english_engine.py install --game '/absolute/path/to/game copy'
python3 english_engine.py restore --game '/absolute/path/to/game copy'
```

A frozen executable also accepts these actions; on macOS its CLI is `ZephyrEnglishPatcher.app/Contents/MacOS/ZephyrEnglishPatcher`.

## Select the correct folder

Choose the actual directory containing ZephyrRemastered.exe, not a Wine prefix or Proton compatibility-data directory. Custom Steam libraries can be elsewhere.

- CrossOver: use the bottle's Open C: Drive command, then locate Steam/steamapps/common/The Rhapsody of Zephyr Remastered. A typical bottle root is `~/Library/Application Support/CrossOver/Bottles/Steam/drive_c/`.
- Linux Steam: typical library is `~/.local/share/Steam/steamapps/common/`.
- Flatpak Steam: typical library is `~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/`.

For a CrossOver bottle named **Steam**, the typical full game path is:

```text
~/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/The Rhapsody of Zephyr Remastered
```

`~` means your Mac home folder. The Mac patcher displays this example and opens Browse there if it exists. In the folder picker, press **Shift+Command+G** to paste a path. If your bottle has another name or your library is elsewhere, use CrossOver's **Open C: Drive** to find the actual folder. Select the folder containing `ZephyrRemastered.exe`; then click **Check Files**, followed by **Install English** and confirm the folder.

First test with a separate copy of the original Korean game folder. Close the game before installing/restoring; you do not need to stop Steam or the whole Wine server. The patcher refuses unknown resource hashes and checks running game processes. Flatpak/container PID isolation can hide processes from host tools; close the game yourself and run the patcher on the same host as Steam.

Backups:
- macOS: `~/Library/Application Support/ZephyrEnglishPatcher/`
- Linux: `$XDG_STATE_HOME/zephyr-english-patcher/` or `~/.local/state/zephyr-english-patcher/`

Backups are tied to the game directory path. Keep the game path and backup folder unchanged until restored. The optional save converter produces separate copies only. No saves, Wine configuration, Steam settings or game launch options are changed automatically.

## Build a native executable

```sh
bash Build-Native.sh
```

The build installs pinned PyInstaller into a kit-local virtual environment and runs tests. A Mac build produces an app for the Mac's architecture; build/test Intel and Apple Silicon separately. A Fedora build produces a Linux executable targeting that machine's architecture and libc baseline, not every Linux distribution. Building on Fedora 44 does not establish compatibility with older distributions or Steam Deck.

## Fedora 44 test checklist

1. Record `uname -m`, `python3 --version` and `ldd --version`.
2. Run `python3 -m unittest discover -s tests`.
3. Check Files on a separate original game copy; expect original.
4. Install English; expect installed. Backups must exist.
5. Launch the copy using your normal Proton setup, inspect menus/dialogue/battle labels and close it.
6. Restore Original; Check Files should report original. Reinstall and retest.
7. Confirm that launching the patcher while the game runs refuses writes.

Do not treat passing source tests as a completed gameplay test. Report exact errors and whether Steam is native or Flatpak.
