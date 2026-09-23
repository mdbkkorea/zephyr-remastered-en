# English patcher for macOS / CrossOver and Linux / Proton

This patches the same Windows game resources as the Windows patcher. It does not turn the game into a native Mac/Linux game. Continue launching the game using CrossOver or Steam Proton.

The maintainer tested the Mac patcher and launcher on Mac mini (2024), Apple M4, 32 GB RAM, macOS Tahoe 26.5.2, CrossOver 26.3 / Windows Steam, including the translated Fullmap overlay. Other Macs are not verified.

The app is not notarized by Apple. If macOS blocks its first opening as an unidentified developer, choose Done/Cancel instead of Move to Trash, then System Settings → Privacy & Security → Open Anyway. Confirm Open. See MAC-GUIDE.md in the Mac ZIP and Apple: https://support.apple.com/en-us/102445

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

### CrossOver mod launcher (beta.5)

The beta.5 Mac ZIP includes **Launch-Zephyr-CrossOver.command** beside the patcher app.
Extract the complete ZIP and keep these together. Double-click the command, check
the detected CrossOver app, bottle folder and game folder, then click **Launch game**.
Use Browse or enter paths for a custom installation; the bottle folder contains
`cxbottle.conf`, and the game folder contains `ZephyrRemastered.exe`.
Selections are remembered locally and can be changed each time. No separate Python
installation is needed for the bundled launcher.

Keep Steam running in that bottle. Clear the Linux/Proton text from Steam Launch
Options and close other Zephyr copies first. The launcher passes
`--dll 'winhttp=n,b'` directly to CrossOver so installed Fullmap/Passives mods can
load. It does not install mods or English, edit the bottle registry, or change
Steam settings. This launcher targets the Steam edition; PURPLE is not verified.

Settings: `~/Library/Application Support/ZephyrEnglishPatcher/crossover-launcher.json`.
Diagnostics: `crossover-launch.log` in the same folder. Source users can run
`python3 english_app.py --launch-crossover` with Tk installed.

### Building

```sh
bash Build-Native.sh
```

The build installs pinned PyInstaller into a kit-local virtual environment and runs tests. A Mac build produces an app for the Mac's architecture; build/test Intel and Apple Silicon separately. A Fedora build produces a Linux executable targeting that machine's architecture and libc baseline, not every Linux distribution. Building on Fedora 44 does not establish compatibility with older distributions or Steam Deck.

On Mac, distribute the generated `dist/Zephyr-English-<version>-macos-<architecture>.zip`.
It contains the app, executable CrossOver command, license and these instructions.
Rebuild the app with the launcher module; the command does not work with beta.3 or
older patcher apps. This addition does not alter already published releases.

## Fedora 44 test checklist

1. Record `uname -m`, `python3 --version` and `ldd --version`.
2. Run `python3 -m unittest discover -s tests`.
3. Check Files on a separate original game copy; expect original.
4. Install English; expect installed. Backups must exist.
5. Launch the copy using your normal Proton setup, inspect menus/dialogue/battle labels and close it.
6. Restore Original; Check Files should report original. Reinstall and retest.
7. Confirm that launching the patcher while the game runs refuses writes.

Do not treat passing source tests as a completed gameplay test. Report exact errors and whether Steam is native or Flatpak.
