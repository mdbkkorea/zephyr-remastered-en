# Validation summary - build 016

- Source publication checkout: 54 tests passed in 0.709 seconds. Full source suite also passed after the Windows path portability correction (54 tests in 0.860 seconds).
- Catalog build: zero audit errors/warnings; edited-object readback and unchanged-original checks passed for standard and Passives stages. Resource count: 22,403; metadata edits: 30.
- Mac Apple Silicon: compiled install, repeat-install and exact-hash restore passed for no mods, Passives only, Fullmap only and both. Unsupported-version fallback preserved plugin hashes. Deep/strict app signature passed; app is not notarized.
- Linux x86-64: Debian 12, glibc 2.36, Python 3.11.2, PyInstaller 6.22.3 under emulation. Compiled installation/restoration and fallback scenarios passed. Initial Tk layout and frozen GUI startup passed. Native Fedora 44 and Proton gameplay remain pending.
- Windows report: Windows 11 x64, Python 3.12.10, Tcl/Tk 8.6.15, PyInstaller 6.22.3. 24 packaged tests: 23 passed, one POSIX-only skip. Eight frozen scenarios passed, including all mod combinations, unsupported versions, independently translated Fullmap and managed mod upgrade. Shipped GUI installation/restoration verified 17 selected files and populated layout at the tested scaling. Windows ZIP/EXE checksums were independently verified on Mac.
- Safety tests cover modified resources, backup validation, recovery, long Windows backup paths, removed/added mods and duplicate/relocated named DLLs. The XDG state test uses a host-absolute temporary path for portability.

All installer tests used separate copies. Steam and active saves were unchanged. These tests do not establish complete gameplay coverage, arbitrary third-party mod compatibility, or real UNC target-folder patching. Original mods loaded in user-reported Windows/CrossOver tests; latest translated map layout remains under review.

## 1.0.0-beta.1 release preparation

Centralized version reporting and manifest version. Translation payload is unchanged from build 016. Source suite: 54 tests passed in 0.899 s. Platform rebuild validation is recorded in the release notes. Windows is the only fully tested release; macOS/Linux are experimental.

Fresh beta.1 Windows report: 24 packaged tests (23 passed, one POSIX-only skip) and direct shipped-EXE GUI Check/Install/Restore with both supported mods; all 17 selected file hashes verified. The eight frozen-harness cases recorded for build016 were not rerun on Windows for beta.1. All application/payload files match the frozen beta kit. The kit reused an older platform test from its base export, so Windows reapplied the already-reviewed test-only host-absolute XDG fix. Automatic export now refreshes all packaged tests from current source. Runtime binaries/payload are unaffected. Fresh Mac/Linux compiled tests passed four supported combinations plus two unsupported fallbacks.

### Safari review suggestions - 2026-09-23

Added per-entry translation suggestions and explanations with separate pending Markdown records. A loopback-only Mac service saves into the mounted review folder. Browser drafts survive navigation; saved entries reload; revisions preserve previous Markdown files. Source/revision checks, idempotent retry and explicit save-failure states prevent silent data loss. No translation or game files are changed automatically. Private suggestion records and deployed service data are excluded from Git.

Validation: six persistence tests; JavaScript search/navigation, draft retention, successful saves/reload and offline failure tests; actual HTTP-to-mounted-storage Markdown save/readback with Unicode, idempotency and origin/token/source rejection. Safari rendering inspected; native Safari typing/save interaction was not established by automation. API and JavaScript paths were independently tested. No compiled release changes.

### Full battle-command names — 2026-09-23

Replaced compact battle labels with full names using nonbreaking spaces within attack suffixes. Updated 199 mirrored occurrences covering 51 Korean labels and ten Stab/stabs occurrences (209 total). Korean source, Chinese references and resource identities preserved. User confirmed both the Cyrano trial and expanded Mac CrossOver test work. Rebuilt bundles passed full-tree readback and unchanged-object checks; catalog CRC/size/hash checks passed. Local full-catalog audit: 22,403 entries, zero errors/warnings. Public catalogs and review sheets updated; distributed release packages have not been rebuilt. No Windows runtime verification of these labels is claimed.

### Windows build kits beta.2 — 2026-09-23

Prepared separate Steam and PURPLE Windows build kits with latest Geysir, full battle names and Stab. Steam automatically handles supported Passives/Fullmap or standard fallback; PURPLE is standard/experimental. New missing-payload instructions distinguish source ZIPs from prepared kits. Included Windows administrator/recovery and PURPLE default-folder guidance. All three 22,403-entry stages passed zero-error/zero-warning rebuild audits. Fullmap rebuild preserved method bodies. Separate-copy install/reinstall/restore passed for Steam standard, Passives, Fullmap, both and unsupported mods, plus PURPLE standard; wrong editions rejected. Global running-game detection was overridden only in the private fixture harness because the user was playing another copy; production checks unchanged. Public suite: 60 tests passed; packaged PURPLE suite: 24 passed. ZIP integrity verified. Windows EXE building/runtime testing remains user-operated and pending. Older published binaries are unchanged.

### English beta.3 release — 2026-09-24

User accepted latest Mac playtest and requested commit, release and separate Windows build kits. Incorporated 13 reviewed dialogue/layout edits, approved skill names, Blade Shot, Killing Blade and Asura's Void Edge. Added hash-locked 2.5x reveal patch for Steam/PURPLE (restorable GameAssembly delta) and six Auto-Advance component font adjustments per edition. Reviewed line-break exceptions require exact original/target hashes; other controls remain checked. Windows ZIP paths are bounded and license notices preserved.

Validation: three 22,403-entry stages passed audits and readback; 66 unit tests passed. Steam standard/Passives/Fullmap/both/unsupported and PURPLE standard passed install/reinstall/exact restore on isolated fixtures; wrong editions rejected. Fixture-only process-guard override allowed tests while a separate user playtest could be running; production guard unchanged. Mac arm64 app built and code signature verified; frozen status check passed. Linux x64 frozen executable passed install/status/restore in Debian 12 emulation; 24 packaged tests passed. Windows EXEs are not built/tested here; user will build ZSteam-b3.zip and ZPurple-b3.zip with Python 3.12. macOS/Linux installers and PURPLE remain experimental; Fedora/Proton gameplay pending. Original installations and saves untouched.

### Beta.4 portable Mac launcher — 2026-09-24

Added the portable CrossOver launcher with local path preferences, safe drive mapping and an older-app compatibility check. Mac packages contain the matching app, command and Apple-sourced first-run instructions. README English/Korean records maintainer testing on Mac mini (2024), M4, 32GB, macOS Tahoe 26.5.2, CrossOver 26.3 / Windows Steam, including translated Fullmap gameplay. Translation data remains identical to beta.3. Existing beta.3 users need no repatching to use the launcher.

Validation: 69 unit tests; 27 packaged Linux tests; Mac signature and frozen launcher protocol checks; Mac/Linux frozen status checks; Steam standard/Passives/Fullmap/both/unsupported and PURPLE standard install/reinstall/exact restore on isolated fixtures; wrong editions rejected. ZIP integrity, short Windows paths, executable launcher permissions and SHA256 sums checked. Windows downloads remain build kits for user-side compilation/testing. Fedora/Proton gameplay remains pending. No Windows PC control or game installation performed.

### English beta.5 — 2026-09-24

User accepted the latest Mac test and requested a release. Includes eight latest reviewed dialogue entries with ten forced breaks removed, two closing-passage corrections and thirteen compact Own shop labels. Preserves 2.5x reveal, smaller Auto-Advance text and the portable CrossOver launcher. Applies shorter user-approved archive filenames, with separate Windows Steam/PURPLE build kits and short internal folder paths.

Validation: all three 22,403-entry translation stages passed full audits with zero errors/warnings and resource readback checks. All 69 unit tests and 27 packaged Linux tests passed. Steam standard/Passives/Fullmap/both/unsupported and PURPLE standard passed install/reinstall/exact restoration on isolated fixtures; wrong editions rejected. Mac signature/launcher handshake and Mac/Linux frozen status checks passed. Windows ZIP paths remain bounded to 39/40 UTF-16 units. Latest Mac playtest accepted by user; beta.5 Windows EXEs await user builds and tests, Fedora/Proton gameplay remains pending. No Windows PC control or original game installation changes.

### Confirmed build recovery and installer filenames — 2026-09-24

User confirmed the updated Windows build works. Build-Windows.ps1 repairs missing pip using bundled ensurepip before dependency installation. It names the EXE from the payload edition and release version, rejecting mismatched versions. New names use ZEnglishSteam/Purple/Macos/Linux_VERSION_betaXX. Mac build/launcher references match the new names; legacy launcher app names remain supported. Published beta.5 archives are unchanged; README links both replacement files required to repair those kits.

Validation: missing-pip reproduction and repeated bootstrap passed on a temporary Mac Python environment; user confirmed Windows build success. Four platform names, beta formatting, invalid input rejection, Windows edition selection, renamed/legacy Mac launcher execution and shell syntax checks passed. No translation or game changes.
