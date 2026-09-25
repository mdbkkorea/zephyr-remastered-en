# Quest text sizing — next build

Screenshots showed quest titles and objectives wrapping across fixed-height rows
in the field tracker and journal. The profile in `localization/quest-layout.json`
changes 85 layout fields on 28 shared text components across the two UI bundles.
It does not change quest wording or progress.

- Tracker titles/objectives: auto-size 10–24 points, one line. The game measures
  each displayed string, so later quests use the same rules. Existing short text
  stays at the original maximum size. The smallest estimated current label is
  11.23 points, including a 5% glyph-advance allowance; inspect readability in-game.
- Journal list: auto-size 16 points up to the original 28/30/32-point maximum,
  one line. Quest title labels gain an 80-unit right margin to fit their banners.
- Journal descriptions: retain wrapping, auto-size 18–32 points within the page.

All 215 quest labels and 282 descriptions were estimated using the shipped
Dotum/Batang font metrics. Estimates cover known English strings, not every future
translation or runtime resolution; TextMeshPro performs the actual fitting.
The longest descriptions are estimated to fit above 25 points. Very long new text
can still exceed the lower font limit and needs review rather than unlimited shrinking.

Static validation: changed objects read back exactly, other objects in rebuilt
bundles retained, catalog CRC/size/hash checked, reveal/mod DLLs preserved.
Mac visual test is pending. Published installers do not contain this candidate yet.

The release builder now includes this profile alongside Auto-Advance. All 97
layout fields (85 quest fields and 12 Auto-Advance fields) must be applied or the
build fails. Three chapter components are layout-only targets and are included
even though they have no translation rows. Original bundle hashes and expected
field/text values must match before modification. These changes are prepared for
the next build; existing beta.5 downloads remain unchanged.

TextMeshPro auto-sizing reference:
https://docs.unity.cn/Packages/com.unity.textmeshpro@3.2/manual/TMPObjectUIText.html
