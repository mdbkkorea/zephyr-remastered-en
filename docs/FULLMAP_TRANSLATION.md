# Fullmap English playtest

The user confirmed Fullmap working in CrossOver with the corrected `--dll 'winhttp=n,b'` launcher. Playtest 5 adds an English display-text variant of **ZephyrFullmap 1.8.0**, alongside the existing English game and ZephyrPassives translations.

Start Steam in CrossOver's Steam bottle, close the running game, then open `private/Launch English Playtest 5.command`. The separate `private/English Playtest 5` copy contains the translated plugin. Playtest 4 and Steam's plugin are unchanged. Saves use the same location as earlier playtests.

Translated 109 unique JSON labels in 869 occurrences: region names, destinations, room titles and Interior labels. Existing Korean-based English place spellings are reused, including Geyshir, Cyrups and Ruben. Unapproved names remain provisional. Controller help reads `R: Pan  LT+R: Zoom  R3: Center` (R means right stick). The Korean direction suffix is omitted because the exit already displays the destination name. Mod log/config text remains Korean.

Review F001–F111 under **ZephyrFullmap 1.8.0 English** on the NAS review page. These are separate from base-game R entries and passive-profile P entries.

The private builder `scripts/translate_fullmap.py` requires dnfile and dncil (available in `private/mod-inspection-deps`), and accepts only the exact original 1.8.0 DLL SHA256 `9c891825ed28212df42a97512c2e6b522304009e2e7dca669a7615f30b199334`. It changes embedded JSON display strings and two fixed-size UI literals, preserving executable method bodies, metadata tables, IDs, coordinates and map geometry. The resource is relocated into an expanded readable final PE section. It produces a separate private DLL, never edits its input, and rejects different/signed images. Original game/mod assets and generated DLLs are not committed.

Static parsing/readback and method-body comparison passed. English rendering, label width and the translated DLL's runtime loading remain unverified until user testing. New diagnostics: `private/crossover-playtest-5.log`, `private/english-playtest-5.log`, and the playtest copy's `BepInEx/LogOutput.log`.
