# ZephyrPassives English compatibility profile / 패시브 모드 영어 번역

This optional profile assumes **ZephyrPassives 2.4.3 with its default settings**, for game build 1.0.1718210b. It includes the full Korean-based English translation, Geyshir terminology, Aura Slash and compact battle commands. It changes game text only. It does not supply, modify or install the mod, or change gameplay settings.

이 선택형 번역은 **ZephyrPassives 2.4.3 기본 설정**을 기준으로 합니다. 원본 한국어 기반 영어 번역 전체를 포함하며, 모드의 실제 효과에 맞게 설명을 수정합니다. 모드 파일이나 게임 설정은 변경하지 않습니다.

Behavior reference: [author's Korean description](https://www.softmoa.com/resource/k7aywhd77a67bi05) and the supplied 2.4.3 README. Chinese supports the base-game translation, but is not a source for these mod-specific mechanics. The mod's character window appends the game's own passive list, which uses the existing translated resources.

## Effects under default settings

| Korean | English | Mod behavior |
|---|---|---|
| 근성 | Grit | At HP ≤50%, Strength, Agility, Intelligence, Defense and Magic Resistance ×1.3 during damage calculation. |
| 열혈 | Hot Blood | Doubles XP gain. |
| 일격필살 | One-hit Kill | Critical hits leave the target at 1 HP. |
| 행운 | Luck | Immunity to supported status ailments. |
| 분노 | Rage | Fills XP when HP crosses down to 30% or less. |
| 독공격 | Poison Attack | Critical hits inflict poison. |
| 마비 | Paralysis | Critical hits inflict petrification (the game's Stone effect). The existing name is retained; the description clarifies the effect. |
| 흡혈 | Life Drain | Restores HP equal to 30% of damage dealt. |
| 훔치기 | Steal | Gains ELD equal to 5% of damage dealt; enemies take it from the party. |
| 신의 축복 | Divine Blessing | Halves MP costs. |
| 중독방지 | Poison Immunity | Prevents poison. |
| 마비방지 | Paralysis Immunity | Prevents petrification. |
| 언데드 | Undead | Blocks normal/special attacks from non-elemental weapons. |
| 기력 | Vigor | Adds 15 XP. |
| 성기사 랜스 | Paladin's Lance | Attacks restore 7% of maximum HP. Existing Holy-magic text is retained. |
| 스펙터의 악몽 | Specter's Nightmare | Attacks cost 10% of maximum HP, leaving at least 1; critical hits add damage equal to 35% of target's current HP. |
| 회복탄 | Healing Rounds | Heals the target instead of dealing damage. |
| 악마의 반지 | Demon's Ring | Doubles offensive magic damage. |
| 바바리안 | Barbarian | Grants Vigor; existing Strength bonus remains. |
| 제프리바지 | Jeffrey's Trousers | Grants Vigor and Rage. |
| 카오스 큐브 | Chaos Cube | Grants Hot Blood. |
| 치료제 | Remedy | Cures poison, petrification, silence, slow and curse. |
| 곡괭이 | Pickaxe | Gains the Holy element; original name/stats retained. |

The mod also fixes Kana's One-hit Kill ability ID and includes ammunition passives in the character display. Confusion, burn/freeze/shock immunity, Stealth, Sacrifice and Warp are not restored by this mod; their base-game translations do not imply working effects.

The 28 overrides update 13 existing descriptions across their resource occurrences. Names and descriptions that already agree remain in the base catalog. This profile does not invent new tooltip fields for weapons with no existing description. This table provides the remaining equipment-effect reference. Mod configuration comments and diagnostic logs remain Korean.

## Applying this English variant

1. Use a separate game copy for the first test. If a previous English patch is installed, use that patcher's Restore before switching variants.
2. Install the author's unmodified ZephyrPassives 2.4.3 distribution separately, following its instructions.
3. Apply the **ZephyrPassives** English patch variant. Its dependency check requires the matching plugin at `BepInEx/plugins/ZephyrPassives/ZephyrPassives.dll` (SHA256 `c22a790200042a1385e896b20938c89a31e542bcfe919de324959a9cdbdbf0c2`). The standard English patch remains available for games without this mod.
4. Leave mod settings at their defaults for the displayed numbers to match. Settings live in `BepInEx/config/softmoa.zephyr.passives.cfg` after the first launch. Custom multipliers do not dynamically update this static translation.

The author's Linux/Proton instructions specify `WINEDLLOVERRIDES="winhttp=n,b" %command%`. CrossOver loader configuration and this combination's in-game rendering have **not** been tested here. Check `BepInEx/LogOutput.log` for `Loading [Zephyr Passives 2.4.3]` before testing effects.

Review: P001–P028 in the NAS review page's **ZephyrPassives 2.4.3 (default settings)** section. R/M entries continue to show the standard translation for comparison. This compatibility build has static/resource validation only; Windows, CrossOver and Fedora runtime tests are still required.
