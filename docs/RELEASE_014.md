# Build 014 — Mac and Linux test packages

The current build uses the latest Playtest 7 English resources: Geyshir/Geyshir Empire, R675 Work Group 12, Aura Slash, distinct battle commands, four dialogue-spacing fixes and compact settings labels. This is the **ZephyrPassives edition**, requiring separately installed ZephyrPassives 2.4.3 with default settings. Fullmap 1.8.0 is compatible; its English DLL is a separate add-on.

Historical build artifacts (not included in this source repository):

- `Zephyr-English-ZephyrPassives-macOS-014.zip`: Apple Silicon app, Python/Tk included. Extract and open ZephyrEnglishPatcher.app. Locally signed, not Apple-notarized.
- `Zephyr-English-ZephyrPassives-Linux-x64-014.tar.gz`: Linux x86-64 executable. Extract, open a terminal in the extracted folder, run `./ZephyrEnglishPatcher`. No Python installation required. Intended for a Linux desktop with glibc 2.36 or newer, including the user's Fedora 44 laptop; native Fedora testing pending.
- `Zephyr-English-ZephyrPassives-Kit-014.zip`: Windows/Linux build source and identical hash-pinned payload. Windows build delegated to the existing Windows task; no new Windows EXE is claimed complete until its report arrives.
- `Zephyr-Fullmap-English-1.8.0.zip`: separate private Fullmap translation add-on, same DLL as Playtests 5–7. Read its backup/replacement instructions; English runtime/layout verification remains pending.
- `SHA256SUMS-014.txt`: checksums for these four packages.

Close the game before patching, select the folder containing ZephyrRemastered.exe, Check Files, then Install English. Start with a separate game copy. Existing English installs managed by this patcher can be updated; unmanaged copies need restoration with their original tool first. Keep the patcher and its backup folder for Restore Original. Saves and Wine/Proton settings are not modified.

Validation: 46 project tests passed on macOS. Native Mac executable installed/restored an isolated resource copy. Linux x86-64 container: 16 packaged tests passed; source GUI layout checked under Xvfb, frozen GUI started and remained open; compiled executable installed/restored all 16 resource files with exact hashes. Both ZIPs, Linux archive permissions/bytes and Mac deep/strict code signature verified. Linux built on Debian 12 (Python 3.11.2, glibc 2.36) under x86-64 emulation on the Mac; this is not a Fedora or Proton gameplay test.

No Steam installation or active save was modified during release tests. No GitHub publication performed. Newer mod versions are not covered by these version-specific compatibility checks.
