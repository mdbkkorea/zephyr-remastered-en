# Battle selector label review

All 65 normal-attack records were checked against Korean and Chinese. The screenshot behavior removes leading words, so the distinguishing attack label and any variant number must remain in the final token. These compact labels target that behavior; the renderer implementation has not been traced. Actual pixel fit remains a runtime check.

The 56 Type 1 special-move records were preserved: the supplied screenshots show full multiword names in the separate skill display. Descriptions are unchanged.

| Korean | Chinese reference | Previous data label | Updated data label | Selector suffix |
| --- | --- | --- | --- | --- |
| 시라노 베기 | 西拉诺斩击 | Cyrano Slash | Cyrano Slash | Slash |
| 시라노 약베기 | 西拉诺轻斩 | Cyrano W.Slash | Cyrano W.Slash | W.Slash |
| 시라노 강베기 | 西拉诺重斩 | Cyrano S.Slash | Cyrano S.Slash | S.Slash |
| 시라노 탄검 | 西拉诺剑气弹 | Cyrano Aura.Slash | Cyrano Aura.Slash | Aura.Slash |
| 샤른 베기 | 沙恩霍斯特斩击 | Sharn Slash | Sharn Slash | Slash |
| 샤른 약베기 | 沙恩霍斯特轻斩 | Sharn W.Slash | Sharn W.Slash | W.Slash |
| 샤른 강베기 | 沙恩霍斯特重斩 | Sharn S.Slash | Sharn S.Slash | S.Slash |
| 샤른 탄검 | 沙恩霍斯特剑气弹 | Sharn Aura.Slash | Sharn Aura.Slash | Aura.Slash |
| 메디치 베기 | 梅迪西斩击 | Medici Slash | Medici Slash | Slash |
| 메디치 약베기 | 梅迪西轻斩 | Medici W.Slash | Medici W.Slash | W.Slash |
| 메디치 강베기 | 梅迪西重斩 | Medici S.Slash | Medici S.Slash | S.Slash |
| 메디치 살검 | 梅迪西杀剑 | Medici Killing Blade | Medici K.Blade | K.Blade |
| 실버 베기 | 希尔弗斩击 | Silver Slash | Silver Slash | Slash |
| 실버 수리검 | 希尔弗手里剑 | Silver Shuriken | Silver Shuriken | Shuriken |
| 실버 독수리 | 希尔弗雄鹰 | Silver Eagle | Silver Eagle | Eagle |
| 이자벨 찌르기 | 伊莎贝尔突刺 | Isabele Thrust | Isabele Thrust | Thrust |
| 이자벨 베기 | 伊莎贝尔斩击 | Isabele Slash | Isabele Slash | Slash |
| 이자벨 투창 | 伊莎贝尔投枪 | Isabele Javelin | Isabele Javelin | Javelin |
| 리델 찌르기 | 里德尔突刺 | Rhidel Thrust | Rhidel Thrust | Thrust |
| 리델 베기 | 里德尔斩击 | Rhidel Slash | Rhidel Slash | Slash |
| 리델 늑대공격 | 里德尔狼袭 | Rhidel Wolf Attack | Rhidel Wolf.Atk | Wolf.Atk |
| 카나 사격 | 卡娜射击 | Kana Shot | Kana Shot | Shot |
| 커나 정밀사격 | 卡娜精准射击 | Kana Precision Shot | Kana P.Shot | P.Shot |
| 프레데릭 약베기 | 弗雷德里克轻斩 | Frederick W.Slash | Frederick W.Slash | W.Slash |
| 프레데릭 강베기 | 弗雷德里克重斩 | Frederick S.Slash | Frederick S.Slash | S.Slash |
| 카타리나 약베기 | 卡塔莉娜轻斩 | Katarina W.Slash | Katarina W.Slash | W.Slash |
| 카타리나 강베기 | 卡塔莉娜重斩 | Katarina S.Slash | Katarina S.Slash | S.Slash |
| 보스 베기 | 首领斩击 | Boss Slash | Boss Slash | Slash |
| 몬스터 일반01 | 怪物普通攻击01 | Monster Normal Attack 01 | Monster Normal.01 | Normal.01 |
| 몬스터 일반02 | 怪物普通攻击02 | Monster Normal Attack 02 | Monster Normal.02 | Normal.02 |
| 몬스터 일반03 | 怪物普通攻击03 | Monster Normal Attack 03 | Monster Normal.03 | Normal.03 |
| 몬스터 일반04 | 怪物普通攻击04 | Monster Normal Attack 04 | Monster Normal.04 | Normal.04 |
| 몬스터 일반05 | 怪物普通攻击05 | Monster Normal Attack 05 | Monster Normal.05 | Normal.05 |
| 몬스터 중거리01 | 怪物中距离攻击01 | Monster Mid-range Attack 01 | Monster Mid.Atk01 | Mid.Atk01 |
| 몬스터 중거리02 | 怪物中距离攻击02 | Monster Mid-range Attack 02 | Monster Mid.Atk02 | Mid.Atk02 |
| 몬스터 중거리03 | 怪物中距离攻击03 | Monster Mid-range Attack 03 | Monster Mid.Atk03 | Mid.Atk03 |
| 몬스터 중거리04 | 怪物中距离攻击04 | Monster Mid-range Attack 04 | Monster Mid.Atk04 | Mid.Atk04 |
| 몬스터 중거리05 | 怪物中距离攻击05 | Monster Mid-range Attack 05 | Monster Mid.Atk05 | Mid.Atk05 |
| 몬스터 쏘기01 | 怪物射击01 | Monster Shot 01 | Monster Shot.01 | Shot.01 |
| 몬스터 쏘기02 | 怪物射击02 | Monster Shot 02 | Monster Shot.02 | Shot.02 |
| 몬스터 쏘기03 | 怪物射击03 | Monster Shot 03 | Monster Shot.03 | Shot.03 |
| 몬스터 쏘기04 | 怪物射击04 | Monster Shot 04 | Monster Shot.04 | Shot.04 |
| 몬스터 쏘기05 | 怪物射击05 | Monster Shot 05 | Monster Shot.05 | Shot.05 |
| 몬스터 연속01 | 怪物连续攻击01 | Monster Combo 01 | Monster Combo.01 | Combo.01 |
| 몬스터 연속02 | 怪物连续攻击02 | Monster Combo 02 | Monster Combo.02 | Combo.02 |
| 몬스터 연속03 | 怪物连续攻击03 | Monster Combo 03 | Monster Combo.03 | Combo.03 |
| 몬스터 연속04 | 怪物连续攻击04 | Monster Combo 04 | Monster Combo.04 | Combo.04 |
| 몬스터 연속05 | 怪物连续攻击05 | Monster Combo 05 | Monster Combo.05 | Combo.05 |
| 몬스터 강공01 | 怪物强攻01 | Monster Heavy Attack 01 | Monster H.Atk01 | H.Atk01 |
| 몬스터 강공02 | 怪物强攻02 | Monster Heavy Attack 02 | Monster H.Atk02 | H.Atk02 |
| 몬스터 강공03 | 怪物强攻03 | Monster Heavy Attack 03 | Monster H.Atk03 | H.Atk03 |
| 몬스터 강공04 | 怪物强攻04 | Monster Heavy Attack 04 | Monster H.Atk04 | H.Atk04 |
| 몬스터 강공05 | 怪物强攻05 | Monster Heavy Attack 05 | Monster H.Atk05 | H.Atk05 |
| 기본마법 | 基础魔法 | Basic Magic | B.Magic | B.Magic |
| 게리슨 약공격 | 盖里森轻击 | Garrison Light Attack | Garrison W.Attack | W.Attack |
| 게리슨 강공격 | 盖里森重击 | Garrison Heavy Attack | Garrison S.Attack | S.Attack |
| 드래곤브레스 | 龙息 | Dragon Breath | Dragon D.Breath | D.Breath |
| 키메로스브레스 | 奇美罗斯吐息 | Chimeros Breath | Chimeros C.Breath | C.Breath |
| 경비견 박치기 | 警犬头槌 | Guard Dog Headbutt | Guard Dog Headbutt | Headbutt |
| 마둑 공던지기 | 马杜克投球 | Maduk Ball Throw | Maduk Ball.Toss | Ball.Toss |
| 장교,강베기01 | 军官重斩01 | Officer Heavy Slash 01 | Officer S.Slash01 | S.Slash01 |
| 장교,강베기02 | 军官重斩02 | Officer Heavy Slash 02 | Officer S.Slash02 | S.Slash02 |
| 장교,강베기03 | 军官重斩03 | Officer Heavy Slash 03 | Officer S.Slash03 | S.Slash03 |
| 장교,강베기04 | 军官重斩04 | Officer Heavy Slash 04 | Officer S.Slash04 | S.Slash04 |
| 장교,사격 | 军官射击 | Officer Shot | Officer Shot | Shot |
