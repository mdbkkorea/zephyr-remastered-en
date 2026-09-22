# Build the standalone Windows English patcher

Use the private `Zephyr-English-Desktop-Kit-011.zip` kit. Extract the complete ZIP on Windows, install **64-bit Python 3.12** with the Python launcher and Tcl/Tk, and double-click **Build-Windows.cmd**. The script creates a local virtual environment, installs pinned PyInstaller, runs the patcher tests and builds **dist/ZephyrEnglishPatcher.exe**. Neither the .NET SDK nor the ChatGPT app is needed.

The EXE contains Python, the English interface and the patch payload. Recipients do not need Python or a network connection. This uses a new English interface with the existing journaled transaction logic, keeping the upstream Chinese build intact. There is no updater or network code in the patcher. The build wrapper's PowerShell execution-policy override applies only to that process.

## Scope

The payload reconstructs the exact 16 files from English playtest 3 using compressed XOR differences against the user's original files. Original executable, GameAssembly and resource hashes must match; supported Steam build is 25418345. Thirty fixed-slot metadata edits and 22,403 resource entries are already included in those validated files. The kit contains no full playable game and stays under ignored `private/`.

Check Files, Install English, Restore Original and Recover are available. Backups live under `%LOCALAPPDATA%\ZephyrEnglishPatcher`, keyed by the selected installation path. Recovery refuses to overwrite files changed after an interruption. No force-restore control is exposed in the GUI. The game must be closed. Keep the executable and backup directory for restoration; moving the game changes its backup lookup key.

Optional save-name conversion produces separate copies and never installs them automatically. It changes only DialogueName, FullName and JobName using unambiguous catalog mappings and explicit approved overrides. Unknown names remain unchanged. Back up active saves, close the game and preserve relative paths when copying converted saves manually; regenerate if newer progress exists.

## Validation and remaining Windows check

Local tests cover install/restore, idempotence, modified-file rejection, tampered payload rejection, interruption rollback, explicit recovery, protection of newer changes, path traversal and save-field preservation. A full 16-file install/restore against a separate game copy passed on macOS with exact output hashes and unchanged Steam originals. Windows process enumeration and file locking are explicitly overridden for this local integration test; they are not claimed as verified on Windows.

The kit is source plus payload, **not a compiled Windows EXE yet**. On Windows, first test a separate original Korean game copy: Check Files → Install English → launch with Steam running → close game → Restore Original → Check Files. Then reinstall. Check the UI, font layout and optional save copies. The EXE will be unsigned; no code-signing identity or publication has been configured.

## Rebuilding the kit

Run `scripts/prepare_windows_package.py` with `--game` pointing to read-only originals, `--stage` pointing to a validated English stage and `--output` naming a new directory beneath `private/`. The exporter verifies source hashes and stage results, generates embedded payload hashes, and creates a ZIP. Do not run the upstream `scripts/build.ps1` for English: it still packages Chinese.

## Windows handoff incorporated

The September 22 Windows handoff reports a successful kit-003 EXE build, 10 tests, GUI launch and frozen diagnostic install/restore on separate copied game files. Its EXE SHA256 is `6e62d9627631b6a4154501b72428c8aee7957a7b3fd99cf58c0b9df7bdfbedcb`; that binary was not included in the handoff. No Windows gameplay was tested.

Kit 006 merges its Windows extended-length backup paths and forward-slash recovery journals with the newer macOS/Linux support. All 39 local tests pass; a new Windows build/test is still required for the merged code. Previously failed backslash journals are not migrated automatically; keep their backups and diagnose them before retrying. Real UNC/network-share operation remains unverified.

## Compatible user mods

The installer lists **ZephyrFullmap 1.8.0** (Full Map) and **ZephyrPassives 2.4.3** (Passives). Install the mods separately. The Passives translation edition requires version 2.4.3 and describes its default settings. Fullmap English labels are a separate add-on; the resource installer does not install or translate the Fullmap DLL. The original mods have user-reported Windows/CrossOver success; the translated Fullmap add-on still awaits runtime confirmation. Other mod versions are not covered by this compatibility note.
