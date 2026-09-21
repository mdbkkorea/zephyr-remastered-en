# Zephyr English translation — 2026-09-22

## Authoritative context

Recovered from cloud task `Fork and Translate Repo` (6ab0ab4f-8418-83ee-937f-ef054eaacb04). The user requires Korean to override Chinese in every conflict. Translation and Tempest rebuild are separate projects.

Local repository: `/Users/timmoon/Documents/Codex/zephyr-english`.
Remote: `https://github.com/mdbkkorea/zephyr-remastered-en.git`.
Branch: `english-localization`; downloaded baseline `8dcb9a8`.

Original game (READ ONLY):
`/Users/timmoon/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/The Rhapsody of Zephyr Remastered`

## Approved terminology

User-approved 2026-09-22: 주신교 → High Church; deity 주신 → High God; 주신들 → High Gods; 게이시르 → Gaysir. Check Chinese 主神敎/主神教 and 主神 alongside Korean, distinguishing ordinary verbal 주신 (given/provided, etc.). See `docs/GLOSSARY.md`. Seven existing targets corrected (one High Church, six Gaysir); source fields and review numbers preserved. No standalone deity 주신/주신들 occurs in the current translated batches.

Additional user approvals: 사이럽스 → Cyrups; 루벤 → Ruben; 학술원 → Academy; 이스카리옷 → Iscariot (a name); 악마재판장 → Inquisition; 창세전쟁의 비록 → Secret Chronicles of the War of Genesis; 기쉬네 → Gishne. Updated 16 targets (12 Ruben, 2 Cyrups, 2 Inquisition) and resolved matching terminology notes across variants. Namu Wiki is a supporting name-research source, but this lookup was inaccessible and supplied no verification.

Deimos (데이모스) is also user-approved. Updated 26 batch-005 name notes and its review sheet; translation text and review IDs unchanged.

## Current checkpoint: complete catalog and local playtest build

- Batches 001–095 contain 22,150 entries, including all 22,149 aligned Korean occurrences. `supplemental-display.jsonl` adds 253 display fields: 22,403 resource entries total. Thirty fixed-slot hard-coded text edits are in `metadata-drafts.json`.
- Full audit: zero errors, zero warnings, zero aligned Korean occurrences remaining. Fourteen particle omissions are resolved by binary-specific static investigation and exact source/target hashes; see `docs/PARTICLE_REVIEW.md`. Runtime triggering of those messages remains untested.
- All 22 tests passed in 0.450 seconds. Full resource stage `private/english-stage-complete-001` passed edited-object and metadata readback; originals unchanged. Fourteen edited files plus two Addressables catalog files. Catalog hash `a1068c40dd8b3d5132013a4f61f245f0`.
- Separate full copy: `private/English Playtest`; all 16 overlay files verified. Launcher: `private/Launch English Playtest.command`. Save/settings backup: `private/save-backup-before-english-test`.
- Actual launch reached Unity initialization, then failed Steam initialization because no Steam client was running. First launch attempt with a native path failed path resolution; Windows Z: path worked. Visual test could not proceed: Computer Use permissions remained pending, then its server timed out. No gameplay or visual layout validation claimed.
- Expanded inventory inspected 196,715 objects in 38 bundles, three asset files and level0. Preserved internal animation/action keys and 4,210 supporter display-name occurrences. Some fallback data and 325 unreadable-schema objects remain a coverage limitation. The 204 upstream structural operations concerned fonts/materials/appearance rather than missing text. English punctuation was normalized to existing ASCII glyph coverage.
- Korean is authoritative; Chinese was supporting context. Source contradictions between classic/remastered routes remain intentional. Unapproved names remain provisional. Namu Wiki did not provide accessible verification.
- Review sheets regenerated through all 22,403 entries. Original Chinese-derived menu drafts remain separate and unchanged.

## Next work

Start Steam in the CrossOver Steam bottle, then launch the separate English copy using `docs/PLAYTEST.md`. Check title menus, a loaded save, dialogue, inventory and particle-bearing messages. Investigate any visible Korean or clipping. This is a complete catalog playtest candidate, not a fully runtime-tested release or proof that every possible on-screen string is translated.

Steam installation has not been edited. No commit, publication or push. No agents used. Generated assets, source catalogs and backups remain ignored under `private/`.

## Screenshot follow-up — playtest 2

User screenshots confirm gameplay in English (journal, field, character skills and battle). Identified journal/HUD overflow and clipped Special Move. Shortened 16 catalog occurrences; stage `private/english-stage-layout-002` rebuilt all 22,403 resource entries and 30 metadata edits with zero errors/warnings, unchanged originals and successful readback. Catalog hash `28d2bfe4a64bb39ddbff521401f0a9cb`.

Second separate copy `private/English Playtest 2` and `private/Launch English Playtest 2.command` are ready; 16 overlay files verified. First copy untouched. Revised layout awaits screenshots.

Korean character names/job titles are embedded in existing gzip JSON saves as DialogueName/FullName/JobName. Prepared seven converted copies under `private/english-save-copies-002`; active saves untouched. Converter changes only these display fields, preserves unknown names and gameplay data, and refuses overwriting outputs. All 24 tests passed in 0.576 seconds. Save conversion must be applied with the game closed; regenerate first if newer progress exists. See `docs/PLAYTEST.md`.

## Attack selector follow-up — playtest 3

User corrected attacks to Slash, Weak Slash, Strong Slash, Ricochet Blade. Compact selector suffixes are Slash, W.Slash, S.Slash and Ricochet. Korean 약베기/강베기/탄검 and Chinese supporting labels were checked; unrelated bolt spells unchanged. Updated 48 attack-name occurrences and 28 auto-battle options (Use Special / Heal First) to avoid screenshot overlap. Glossary and review sheets updated.

Stage `private/english-stage-combat-003`: 22,403 resource entries plus 30 metadata edits, zero audit errors/warnings, all readbacks passed, originals unchanged. Catalog hash `b4f16a2deebd9d2292c8cb66c803a2d4`. New `private/English Playtest 3` and launcher ready, all 16 overlay files hash-verified. Prior copies and saves untouched. Actual revised selector rendering awaits runtime confirmation.

## Standalone Windows build kit

Prepared `private/Zephyr-English-Windows-Build-003.zip` (about 24 MB) with English playtest-3 deltas, English Tkinter interface, reused journaled engine, original/version hashes including GameAssembly, optional save-copy conversion, and Windows build scripts. Produces one self-contained `ZephyrEnglishPatcher.exe` using Python 3.12 x64 + PyInstaller 6.22.3; no .NET SDK required. Upstream Chinese installer files remain separate. No updater/network code in the English patcher.

33 local tests passed in 0.469 seconds; nine packaged tests passed in 0.048 seconds. Full 16-file install/restore passed on a separate local game copy with matching hashes and unchanged Steam originals. Windows process/lock APIs were overridden only in the local integration subclass, so Windows behavior and the frozen UI remain untested. ZIP integrity and source syntax checks pass. See `docs/WINDOWS_PATCHER.md`.

User now requests installing build prerequisites on their connected Windows laptop. Computer Use inventory currently exposes only the Mac; asked which remote-access app/session or SSH host connects the laptop. No Windows install or EXE compilation has happened yet. No publication or push.

Connection clarification: laptop is connected via ChatGPT app. Current task tools still expose only local Mac projects and Mac Computer Use. Official Remote docs confirm host-specific tools; Windows-side task/run location is needed. Prepared build ZIP can be copied to Windows and continued there. No Windows installation claimed.

## Review file and bilingual GitHub README

Generated `private/Zephyr-Translation-Review.html`: searchable offline Korean/English side-by-side review, batch filters, Chinese supporting text, notes and stable R001–R22403 plus M001–M030 IDs (22,433 entries). Refreshed Markdown review sheets, including previously stale batches 001–007. Generator: `scripts/render_offline_review.py`.

Published only README.md and README.en.md to GitHub main at user request, via GitHub connector commits 0b76d1930ec3034fdb56663c8da11d1443eb3345 and d493e1a6473ece3319df01924f3b90fe62d29cc2. Text distinguishes upstream Chinese localization from this fork's initial Chinese-derived English drafts and current direct Korean translation, describes review corrections, credits upstream and states release limitations. Main README is bilingual English/Korean. Local development branch remains separate; no catalogs/assets/build kits published.

## Native macOS / Linux patcher — desktop kit 005

Shared engine now uses native backup paths, macOS/Linux process checks and POSIX flock; Linux directory keys preserve case. Added unified GUI/CLI entry point, source launcher, native build script and Fedora 44 instructions. Source remains under historical windows/ directory but now supports all three platforms.

Deliverables: `private/Zephyr-English-macOS-AppleSilicon.zip` (37,793,858 bytes, SHA256 3c15712a42b9582076aa37ee97a55e5ad5e10fdcbe19a83df03090c5900bfac8) and `private/Zephyr-English-Desktop-Kit-005.zip` (24,924,509 bytes, SHA256 1b1ee6126d580c86c1829dec963afaab20846e954e7138be4601c1c0d05fb7f9). Mac app embeds Python 3.14.7/Tk 9, is arm64 and ad-hoc signed, not notarized. Linux kit includes source-mode launcher and native executable build script; Fedora gameplay/build awaits the user's laptop. No GitHub publication this turn.

38 tests passed in 0.564 seconds; 14 packaged tests with Python 3.14.7 passed in 0.043 seconds. Actual macOS process/lock checks and full 16-file install/restore passed on the private test copy. Compiled modern Mac app install/restore also passed through CLI; final build status/signature/archive checks passed. Steam originals unchanged. GUI renders correctly, but Computer Use could not reliably type into its Tk controls, so manual interaction is still needed. See `docs/MACOS_LINUX_PATCHER.md`.

## Windows handoff integrated — desktop kit 006

Read user-supplied MAC-HANDOFF.md and verified all four SHA256 entries in the ZIP. Ported only the Windows-tested fixes into current shared code: extended-length local/UNC path helper used by safe() and backup state paths; journal rollback paths now use as_posix(). Preserved macOS/Linux state paths, process checks and file locks. Added handoff long-backup install/restore regression. 39 local tests passed in 0.507 seconds.

New `private/Zephyr-English-Desktop-Kit-006.zip` includes the merged fixes; ZIP integrity checked and all 18 payload files byte-identical to kit 005. Requires a new Windows build/test. Handoff reports prior kit-003 Windows build, 10 tests, GUI startup and frozen diagnostic copy-only install/restore passed; no full gameplay. Prior failed backslash journals are not migrated automatically; UNC behavior untested. No game files, saves, commits or GitHub changes made this turn.

## Windows folder guidance and published testing environments

Windows GUI now displays the usual Steam game directory, explains Steam Manage / Browse local files for alternate libraries, opens Browse at the usual directory when present, and gives numbered Check Files / Install English steps. User still selects the target; no game directory is selected or patched automatically. Windows window enlarged for guidance. Build kit 007 contains this change and all prior handoff fixes; existing compiled EXEs require rebuilding.

README.md now lists tested Mac mini M4 / 32 GB / macOS 26.5.2 / CrossOver 26.3 / Windows Steam, tested Windows 11 / Steam on Samsung Galaxy Book Pro2 360 i5-1240P, and pending Fedora 44 / Steam-Proton on the same laptop. Mac details read locally; Windows/Fedora hardware and status supplied by user. Scope remains selected gameplay screens and patcher copy-only install/restore, not a full playthrough. Published only README.md to GitHub main at user request (443c26599e712c4c43a636eed64e4dd0fced0c14); remote content verified exact.

39 tests passed in 0.502 seconds. GUI syntax, kit ZIP integrity, packaged source identity and unchanged payload checks passed. New Windows GUI rendering remains untested on Windows. No Steam files or saves changed.

### Mac folder guidance — desktop kit 008

Added the full typical CrossOver Steam bottle game path to the Mac GUI, alternate-bottle Open C: Drive instructions and Shift+Command+G folder-picker help. Browse starts at the example directory if present; target remains user-selected. Pasted home-relative paths expand before confirmation. Enlarged window accommodates the guidance. Native README updated.

Rebuilt Apple Silicon app with Python 3.14.7 / Tk 9 / PyInstaller 6.22.3. Actual compiled app screenshot confirms the complete path/help and all controls fit without overlap. GUI syntax, kit ZIP integrity and byte-identical payload against kit 007 passed. codesign --verify --deep --strict and app ZIP integrity passed. Deliverables: private/Zephyr-English-macOS-AppleSilicon-008.zip and private/Zephyr-English-Desktop-Kit-008.zip. Ad-hoc signed, not notarized. No install/restore repeated for this UI change; previous engine tests remain recorded separately. No game/save changes or GitHub publication.

### Source publication requested

User authorized pushing the current work to GitHub. Publication includes Korean-based translation batches/review sheets, shared desktop patcher source (Windows long-path fixes and Windows/Mac folder guidance), build/export tooling, tests and documentation. Private game assets, extracted source catalogs, compiled builds, saves and .DS_Store are excluded. CLI HTTPS push has no configured credentials; use the authenticated GitHub connector with current main as parent and a non-forced ref update.

Pre-publication checks: 39 tests passed in 0.502 seconds; complete catalog audit reports 22,403 entries, zero errors/warnings and zero remaining aligned Korean occurrences. Existing runtime limits remain as recorded. No installer release is created by this source publication.
