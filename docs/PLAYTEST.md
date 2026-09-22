# English playtest

The complete translated catalog is built into a separate local game copy at `private/English Playtest`. Your Steam game files are unchanged.

1. Open Steam in CrossOver's **Steam** bottle and sign in normally.
2. Double-click `private/Launch English Playtest.command` in Finder. This starts the copied executable, not Steam's original Play target.
3. Use the existing saves or start a new game. Report untranslated text, awkward wording, missing glyphs or clipped dialogue with the scene and a screenshot where possible.

The copy uses the same save folder as the original. A pre-test backup is in `private/save-backup-before-english-test`. To play the original, close the test copy and launch normally from Steam. No patch uninstall is required.

## Coverage and verification

22,403 resource entries and 30 hard-coded text edits: all 22,149 aligned Korean occurrences, one additional aligned punctuation entry, and 253 supplemental display fields. Story variants, quests, menus, item/skill descriptions, locations and credits are included. Review the [translation sheets](review/README.md).

The resource rebuild passed source hashes, identity/control checks, edited-object readback, unaffected-object preservation, fixed-byte metadata validation and Addressables catalog updates. All 22 unit tests passed. Fourteen particle omissions have binary-specific [static evidence](PARTICLE_REVIEW.md).

This is an experimental playtest build, not a fully runtime-verified release. Initial launch reached Unity startup but stopped because Steam was not running (`k_ESteamAPIInitResult_NoSteamClient`). Visual inspection requires macOS Computer Use permissions. No full playthrough or dialogue-layout pass has been completed.

Original voices and image artwork remain. Supporter display names remain as supplied; internal Korean animation/action identifiers are preserved. Some fallback data and 325 objects without readable type schemas have not been proven unreachable as display text. Proper names without user approval remain provisional. Report any visible Korean outside those attribution/artwork cases so it can be traced and translated.

The upstream Chinese installer must not be used for this English build. All generated game files remain local and ignored under `private/`; nothing has been published.

## Screenshot fixes: playtest 2

The user's September 22 screenshots confirm English journal, skills, field HUD and battle commands working during gameplay. They also reveal overlapping quest headings, a clipped Special Move command, and Korean character names/job titles.

Launch `private/Launch English Playtest 2.command` after closing the first copy. The new folder is `private/English Playtest 2`. Shortened labels: Training 6: Tactics & Gear, Bearer of God's Soul, and Special. These fit more conservatively; the revised layout still needs visual confirmation.

Existing saves contain their own DialogueName, FullName and JobName values. Changing game assets does not replace these saved Korean strings. `scripts/prepare_english_saves.py` prepared separate converted copies under `private/english-save-copies-002`, with a per-file conversion report. No active save was replaced. Other gameplay values are preserved; unknown or conflicting names remain unchanged.

To use a converted save, close the game first, back up the current save folder, and copy the desired converted `.dat` into its corresponding location beneath CrossOver's `Steam/drive_c/users/crossover/AppData/LocalLow/Nine Circles Corporation/ZephyrRemastered` folder. Preserve the relative Steam/account subfolder shown in the conversion directory. Do not copy the report. If you have saved since conversion, regenerate the copies first so progress is not lost. The conversion is optional and not needed for the layout fixes.

## Latest: playtest 3

Close the running game and use `private/Launch English Playtest 3.command`. This includes playtest 2 fixes plus distinct compact attack labels **Slash / W.Slash / S.Slash / Ricochet** (full meanings Weak Slash, Strong Slash, Ricochet Blade), and shorter auto-battle options **Use Special / Heal First**. Previous copies and active saves are unchanged. Rebuilt resources and copied file hashes passed validation; the new labels still need visual confirmation in-game.

## Latest: playtest 4 with ZephyrPassives

Start Steam in CrossOver's **Steam** bottle, close other Zephyr copies, then double-click `private/Launch English Playtest 4.command`. This launches the separate `private/English Playtest 4` copy, containing the latest English catalog (Geyshir, R675 Work Group 12, Aura Slash and compact attacks) and the unmodified ZephyrPassives 2.4.3 mod with its English description profile.

The launcher passes `--dll 'winhttp=n,b'` to CrossOver for this process only. A plain exported WINEDLLOVERRIDES is cleared by this installed CrossOver wrapper. First mod startup may take 1–3 minutes. Check `private/English Playtest 4/BepInEx/LogOutput.log` for `Loading [Zephyr Passives 2.4.3]`; Unity's log is `private/english-playtest-4.log`. It shares your existing saves; a verified pre-test snapshot is at `private/save-backup-before-english-playtest4`. Steam's original game files and earlier playtest copies are unchanged. Build/copy validation passed; actual mod loading and gameplay remain untested until launch.

Fullmap 1.8.0 is now also included unchanged in Playtest 4. CrossOver launch diagnostics are saved in `private/crossover-playtest-4.log`. The corrected loader option has been statically verified; successful startup still requires a user test.

## Latest: playtest 5 with English Fullmap

Close the current game and open `private/Launch English Playtest 5.command` while Steam is running in the Steam bottle. This preserves Playtest 4 as a fallback and adds translated Fullmap names, Interior labels and controller help. See [Fullmap translation](FULLMAP_TRANSLATION.md). Static checks passed; the new translated plugin still needs a runtime/layout test. Saves are shared with earlier playtests.

## Latest: playtest 6 — dialogue spacing

Close the current game and open `private/Launch English Playtest 6.command` with Steam running. Corrects missing word spaces around pause codes in R845, R12204, R13056 and R18396, including “by a woman.” Same translated Fullmap and Passives as Playtest 5; earlier copies preserved. Build checks passed; on-screen verification pending.

## Latest: playtest 7 — settings labels

Use `private/Launch English Playtest 7.command` after closing the game, with Steam running. Shorter Audio/Gameplay tabs and encounter-rate buttons reduce overflow; long settings labels are shortened. Includes all Playtest 6 corrections and both translated mods. Build validated; visual fit awaits user testing.
