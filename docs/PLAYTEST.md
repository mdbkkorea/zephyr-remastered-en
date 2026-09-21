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
