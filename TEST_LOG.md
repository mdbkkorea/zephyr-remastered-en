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
