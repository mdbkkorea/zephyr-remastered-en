# Project status - build 016

The Korean-authoritative English catalog contains 22,403 resource translations and 30 hard-coded text edits. Chinese is supporting context. Reviewed terminology includes Geyshir, Cyrups, Ruben, Gishne, Deimos, High Church, High God and Aura Slash. Dialogue spacing and compact UI labels have been corrected from playtest feedback.

The shared Windows/macOS/Linux installer automatically detects ZephyrPassives 2.4.3 and ZephyrFullmap 1.8.0. Supported mods receive matching translations. An unsupported version selects standard resource translation and preserves all mod files. Missing mods are not installed. Passives descriptions assume default settings. Backups, restoration and interrupted-operation recovery are implemented.

Windows x64, macOS Apple Silicon and Linux x64 installers have been built and tested separately from Steam installations. This repository update publishes source and review documents, not compiled installers or original game assets. See README.md, docs/RELEASE_016.md and TEST_LOG.md.

Pending: native Fedora 44/Proton gameplay, wider story coverage and translated map layout checks. Existing screenshots verify selected CrossOver gameplay screens, not a complete playthrough. Names without approval remain provisional. Tempest restoration remains separate.

## 1.0.0-beta.1 release preparation

Centralized version reporting and manifest version. Translation payload is unchanged from build 016. Source suite: 54 tests passed in 0.899 s. Platform rebuild validation is recorded in the release notes. Windows is the only fully tested release; macOS/Linux are experimental.

Windows beta.1 rebuild and direct GUI install/restore passed. All three beta.1 packages are ready, with Windows the only fully tested installer release and macOS/Linux experimental. Automatic export now refreshes packaged tests when combining older resource kits.

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

### Beta.5 archive refresh — 2026-09-24

User requested refreshed published archives. Repacked Steam/PURPLE build kits with the confirmed pip bootstrap repair and version/edition-based ZEnglish executable names. Rebuilt Mac/Linux executables with matching names and updated the bundled Mac launcher. Archive names are ZEnglishSteam, ZEnglishPurple, ZEnglishMacos and ZEnglishLinux followed by _1.0.0_beta05. Translation payloads remain byte-for-byte identical to initial beta.5; no game repatching is needed for this packaging update.

Checks: both Windows ZIPs contain exact current build/version files, all payload bytes match prior kits, archive integrity and 39/40-unit internal path limits pass. Mac signature/launcher protocol and both native frozen status checks pass; 27 packaged Linux tests pass. User previously confirmed repaired Windows build works. Original beta.5 checksums superseded by refreshed SHA256SUMS. No Windows control, game modification or translation re-audit.

### Quest text sizing integrated for next build — 2026-09-26

Integrated shared tracker/journal auto-sizing into the release builder for Steam and PURPLE, including three layout-only chapter headings. Each edition must apply exactly 97 checked fields: 85 quest fields across 28 components and 12 Auto-Advance fields. Short text retains its normal maximum size; long labels stay on one line and journal descriptions retain wrapping. No translation wording changed.

Validation: four focused regression tests passed. Separate Steam and PURPLE rebuilds each staged 22,403 occurrences with zero errors/warnings and 97 layout fields. Exact changed-object readback, unchanged-object preservation, original file hashes and catalog CRC/size/hash checks passed. Initial integration checks caught the edition-specific bundle aliases; corrected profiles passed both rebuilds. Visual runtime verification remains pending. Existing beta.5 release archives are unchanged; this source update is for the next build. No original game installation or Windows PC was modified.
