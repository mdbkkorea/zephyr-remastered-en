# The Rhapsody of Zephyr Remastered — English localization work

**Translation work in progress. This is not an installable English patch.**

Based on [wanjizheng/zephyr-remastered-zh-cn](https://github.com/wanjizheng/zephyr-remastered-zh-cn), commit `151d854e3cf23bbe5730d8716c5e1df81dbba428` (v0.2.0). Credit for the Chinese translation and patching tools belongs to the upstream contributors. Their MIT notice remains intact; it covers original tool code and documentation, not rights to the game or its story.

## Current work

- Extracted 22,502 occurrences into 12,637 distinct Chinese source strings with resource names, object IDs, and exact JSON paths.
- Added 333 draft English translations, covering all 332 distinct Chinese strings found in the remastered UI bundle and the additional startup-menu string.
- The other 12,304 distinct strings remain untranslated. No text has received in-game English verification.
- Preserved the Chinese release payload, its hashes, original backup behavior, and signatures. Running the existing patcher still installs Chinese.
- The original README, patcher interface, developer documentation, and history remain in Chinese. This English document describes the new work; it is not a full translation of those documents.

Counts describe strings present in this patch, not proof of coverage of the entire game. Some are sample labels and layout placeholders. The original project explicitly excludes video subtitles and preserves certain graphic menus/logos. Those need a separate inventory for an all-English release.

## Editing the translation

First run `python scripts/english_catalog.py extract` to generate the working catalog from the upstream payload and the included English drafts. The generated 9 MB catalog is omitted from this initial GitHub commit; the starter ZIP includes a generated copy.

`localization/en-US/catalog.jsonl` has one JSON object per unique Chinese string:

- `source`: original Chinese text; do not edit.
- `target`: English translation; empty means untranslated.
- `status`: `untranslated`, `draft`, or `reviewed`.
- `references`: every occurrence in the upstream payload.

Use `python scripts/english_catalog.py check` to check source identity, completeness, references, status, rich-text tags, and common format placeholders. It does not verify meaning, English wrapping, glyph coverage, or game compatibility. `menu-drafts.json` records the initial English drafts; subsequent translation work belongs in `catalog.jsonl`. The extractor refuses to overwrite an existing catalog.

Strings are deduplicated by exact source text. Review every reference before accepting a shared translation: short labels can have different meanings in different contexts. Names and setting terminology are provisional until checked against Korean text and Latin names in the game. For example, `关闭` may need either “Off” or “Close” depending on its control. A future exporter must support per-reference overrides for such cases.

## Requirements before a playable release

1. Finish dialogue, item, ability, quest, and remaining interface translations, with a consistent glossary and contextual review. Cross-check ambiguous Chinese relay translations against the Korean original.
2. Rebuild from a legitimate local Windows game installation matching the upstream resource hashes. The payload identifies Steam App `5099430`, Build `25418345`; that is the supported upstream baseline, not a claim about the latest Steam build. No game resources are included here.
3. Implement an English export/rebuild workflow. Upstream documents say their private generation workspace is not included. New text changes bundle hashes, CRCs and the Addressables catalog. Fixed-length edits in `global-metadata.dat` also require explicit byte-length handling. Simply changing `trusted_payload.py` hashes is not a valid rebuild.
4. Verify English glyph coverage and layout in both game modes, menus, subtitles, and story branches. Review the original Chinese-specific typography changes before retaining them.
5. Translate the patcher and remaining documentation; configure the fork's own release destination and signing identity. The current updater points to the Chinese upstream release and must not ship as an English updater.
6. Validate installation, restoration, interrupted-operation recovery, supported-version checks, and in-game results before publishing an English installer.

The English fork is https://github.com/mdbkkorea/zephyr-remastered-en. Translation work is maintained on the `english-localization` branch.

## Source overlay archive

If reading this in `zephyr-english-starter.zip`, extract its files into a checkout of the upstream commit above. This archive contains the added translation work and validation script, not the upstream payload or a game installer. It can be committed to your fork after GitHub access is available.
