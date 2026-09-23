# Approved English terminology

User decisions, 2026-09-22. Apply to existing drafts and future translations. Korean remains authoritative; consult Chinese alongside it to disambiguate, not to override Korean.

| Korean | English | Supporting Chinese / usage |
| --- | --- | --- |
| 주신교 | High Church | 主神敎 / 主神教; the religious organization |
| 주신 | High God | 主神; only when referring to the deity |
| 주신들 | High Gods | Plural deity reference; Korean determines plurality even when Chinese does not mark it |
| 게이시르 | Geysir | 盖西尔 in the checked references; user-approved spelling |
| 사이럽스 | Cyrups | User correction of Syrups |
| 루벤 | Ruben | User correction of Reuben |
| 학술원 | Academy | User approved at R421 |
| 이스카리옷 | Iscariot | User confirmed this is a name at R424 |
| 악마재판장 / 악마 재판장 | Inquisition | User approved at R427; apply across variants |
| 창세전쟁의 비록 | Secret Chronicles of the War of Genesis | User approved book title |
| 기쉬네 | Gishne | User approved name |
| 데이모스 | Deimos | User approved name |

Use normal English articles where needed, such as “the High Church.” Preserve source control codes, identities, and meaningful whitespace.

Do not mechanically replace 주신. It can be an honorific form of 주다 or part of an auxiliary verb construction: 길러주신 refers to someone who raised a person, 구해 주신 to someone who saved a person, and 보석을 주신 to someone who gave a jewel. Translate the actual predicate (gave/provided, raised, saved, etc.). Even a prayer may contain verbal 주신 rather than the deity noun.

Check each occurrence's Korean syntax and Chinese reference together. 主神 supports the deity sense; 赐予, 给, or a translated action can support the verbal sense. If they conflict or remain ambiguous, flag the entry for review. Do not automatically expand generic 신 (“god”), 교회 (“church”), or 교회단 into these proper terms without contextual evidence.

## Supporting name research

The user recommends [Namu Wiki](https://namu.wiki/) for English character, city, and region names shown alongside Korean names. Consult the relevant Korean article when researching new names; record the exact article and spelling when accessible. User-approved choices above remain project terminology. The 2026-09-22 lookup returned no search results and direct page attempts failed; none of these decisions is claimed as Namu Wiki-verified.

## Attack labels approved 2026-09-22

- 베기: Slash.
- 약베기: Weak Slash; compact attack selector suffix **W.Slash**.
- 강베기: Strong Slash; compact attack selector suffix **S.Slash**.
- 탄검: **Aura Slash** (latest user correction, superseding Ricochet Blade); compact suffix **Aura.Slash**. Use **Aura Slashes** for plural attacks in descriptions. Replaces Ricochet, Sword Bolt and blade projectiles where the Korean is 탄검; unrelated bolt spells are unchanged. Chinese 剑气弹 is supporting context.

The runtime screenshot shows only the last word of the previous multiword attack names. Keep these compact suffixes as one token so attack distinctions survive that observed behavior. The exact renderer implementation has not been traced. Character prefixes remain in the source-derived full data labels.

Latest user correction: **게이시르 → Geysir**, superseding the earlier project spellings Gaysir and Geysir; **게이시르 제국 → Geysir Empire**. Keep this spelling consistent in locations and dialogue.

## Normal-attack selector labels

Use full names with U+00A0 nonbreaking spaces inside the attack suffix, and an ordinary space between the character prefix and suffix. For example, `Cyrano Weak Slash` displays **Weak Slash**. The user confirmed Cyrano's full labels in CrossOver on 2026-09-23 and approved extending this to all normal battle commands. This supersedes compact labels such as W.Slash, S.Slash, P.Shot and K.Blade. Keep numbered variants within the nonbreaking suffix. Do not insert nonbreaking spaces into prose descriptions or alter the already-full Type 1 special-move names. See [battle label mapping](BATTLE_LABELS.md). The user subsequently confirmed the full battle-command Mac test works; exhaustive per-command/resolution testing is not claimed.

## Geysir naming-history remark

User-provided naming history: the original games used Gaysir officially; the company later changed it to Geysir because the original spelling could be misleading. Historical rationale has not been independently verified. The project adopts **Geysir** and **Geysir Empire** by user instruction.

## Stab / 찌르기

User approved **Stab** for 찌르기 battle commands on 2026-09-23; use **stabs** in plural descriptions (연속 찌르기 → A series of stabs). This supersedes Thrust for these entries.
