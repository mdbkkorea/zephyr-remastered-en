# macOS / CrossOver and Linux / Proton patcher

The same English playtest-3 payload now has a host-native patcher. It patches the Windows game's files; CrossOver or Proton still runs the game.

## macOS

Local deliverable: `private/Zephyr-English-macOS-AppleSilicon-008.zip`.

Extract it and open **ZephyrEnglishPatcher.app**. This build is for Apple Silicon and includes Python 3.14.7/Tk 9; users do not need to install Python. It is locally ad-hoc signed, not Developer ID signed or notarized. Intel Macs need a separate native build and test.

In CrossOver, use the Steam bottle's **Open C: Drive** command to locate the game folder containing `ZephyrRemastered.exe`. Copy that folder for the first test. Close the game, select the copy in the patcher, check its files, then install English. Restore Original uses the verified backups for that exact path. Save conversion remains optional and creates separate copies.

Backups are under `~/Library/Application Support/ZephyrEnglishPatcher/`. The patcher does not change Wine/CrossOver settings, launch the game or alter active saves.

## Fedora 44

Transfer and extract `private/Zephyr-English-Desktop-Kit-008.zip` on the Fedora laptop. Open a terminal in the extracted folder:

```sh
sudo dnf install python3 python3-pip python3-tkinter
python3 -m unittest discover -s tests
python3 english_app.py
```

Only dependency installation uses sudo; run the patcher as your normal user. Fedora provides Tkinter in the [python3-tkinter package](https://packages.fedoraproject.org/pkgs/python3.14/python3-tkinter/).

Choose the game's actual Steam library folder, not its Proton prefix. Typical libraries are `~/.local/share/Steam/steamapps/common/` or, for Flatpak Steam, `~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/`; custom libraries may differ. Begin with a separate original game copy. Close the game manually before patching, especially with Flatpak/container process isolation.

To build a standalone Linux executable:

```sh
bash Build-Native.sh
```

Output: `dist/ZephyrEnglishPatcher`. The build script installs PyInstaller into a local virtual environment. A Fedora 44 build targets that machine's architecture and library baseline; it is not automatically compatible with older distributions or Steam Deck. [PyInstaller's Linux compatibility guidance](https://www.pyinstaller.org/en/stable/usage.html#making-gnu-linux-apps-forward-compatible).

Linux backups use `$XDG_STATE_HOME/zephyr-english-patcher/`, or `~/.local/state/zephyr-english-patcher/` when unset. The same kit also retains Windows build scripts.

## Verified here / awaiting laptop testing

- Full suite: 38 tests passed on macOS. Packaged tests: 14 passed with Python 3.14.7.
- Real macOS process enumeration and POSIX locking passed the full 16-file install/restore integration test on a separate game copy. Steam originals unchanged.
- Compiled Mac app installed and restored those 16 files successfully through its CLI.
- Rebuilt GUI renders all controls correctly. Computer Use could not reliably enter text into Tk controls, so interactive button/file-picker behavior still needs a manual check.
- First Apple-system-Python/Tk 8.5 GUI rendered blank and was discarded. Modern-runtime build replaces it; the build script rejects Tk older than 8.6 on macOS.
- Fedora runtime, Proton gameplay and Intel Mac builds have not been tested here.

On Fedora, record `uname -m`, `python3 --version`, `ldd --version`, whether Steam is native or Flatpak, the test result, and the install/restore result. Confirm the running-game write guard and inspect the English menus, story and battle labels in-game.

The kit-008 Mac GUI shows the typical full CrossOver Steam path, explains alternate bottles and Shift+Command+G in the folder picker, and expands pasted `~` paths. Rebuilt app layout visually verified; signature and archive integrity passed.
