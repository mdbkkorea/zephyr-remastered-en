# Validation log

## 2026-09-21 — local Korean-source bootstrap

- Python 3.9 virtual environment, UnityPy 1.25.3. Extraction reads original game files only.
- All 19 original file hashes match the payload baseline; inspected Unity object hashes match. Extractor completed without errors.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-001.jsonl`: 146 occurrences, 130 distinct originals, zero errors, five explicit particle-code warnings.
- Existing English catalog tests: 5 passed.
- New Korean validation tests: 3 passed; verify missing delay codes, source/reference corruption and duplicates, and particle-removal review guards.
- Legacy catalog extraction/check: 12,637 Chinese strings, 333 drafts, 12,304 untranslated, zero errors.
- No visual layout, font coverage, line wrapping, runtime particle handling, English patch installation, or game testing performed. Automated checks do not establish translation quality.

## 2026-09-21 — prison escape continuation (batch 002)

- Authored `localization/en-US/korean-batch-002.jsonl` directly from the preserved Korean source rows: 140 occurrences, 130 distinct originals; 139 Korean-bearing entries and one punctuation-only entry. All aligned entries covered in `art_ko_fl00_s04` (38), `art_fl00_s04` (45), `art_ko_fl00_s08` (26), and `art_fl00_s08` (31). Kept source indices, identities, and variant-specific dialogue intact; did not invent entries at absent source indices.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-002.jsonl`: 140 draft occurrences, 130 distinct originals, zero errors, zero warnings, `installable_english_patch: false`.
- Combined in-memory validation with `scripts.check_korean_batch.check` against `private/korean-aligned.jsonl`: 286 occurrences, 259 distinct originals, zero errors (including no duplicate occurrence IDs across batches), five existing batch-001 particle warnings. Remaining aligned Korean occurrences: 21,864.
- Additional assertions for all 140 new entries: exact ordered slash-control sequence, leading/trailing whitespace, whitespace immediately following `/n`, and square-bracket speaker-label counts all passed. Mapping assertions confirmed exact source-index coverage for each of the four tables.
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 8 tests passed in 0.002 seconds.
- Names and contextual interpretations remain draft and are flagged per entry. No authoritative Latin spelling verification or independent linguistic review performed. No visual/layout, font, voice-sync, runtime, or installable-build validation performed.
- Steam files, Chinese payload, original menu drafts, and batch 001 were not edited. No build, game launch, installation, commit, publication, or push performed.

## 2026-09-21 — readable bilingual review sheet

- Created `docs/review/korean-english-batches-001-002.md`: 286 Korean–English rows across 10 scene/resource sections, 33 specifically flagged entries, provisional-name guidance, source indices, and links to exact catalog lines. General name/voice notes are consolidated in the introduction; specific notes and review questions are included separately.
- Generation assertions passed: exactly 286 table rows and unique occurrence IDs; full coverage of both batches; escaped Korean original and English target text present for every occurrence. SHA-256 comparisons confirmed both input catalogs unchanged.
- This is a Markdown language-review aid. Exact formatting remains authoritative in the linked JSONL catalogs; no rendering, game runtime, or translation-quality validation is implied. No game files edited, installation, commit, or push performed.

## 2026-09-21 — terrace, trial, and aftermath (batch 003)

- Added `localization/en-US/korean-batch-003.jsonl`: 217 Korean-bearing draft occurrences, 196 distinct originals. Exact aligned coverage: `art_ko_fl00_s09` 41 / `art_fl00_s09` 27; s10 16 / 17; s11 39 / 39; s12 18 / 18; s13 1 / 1. Source-index set assertions passed for all 10 tables; absent indices were not invented.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-003.jsonl`: 217 occurrences, 196 distinct originals, zero errors, zero warnings, `installable_english_patch: false`.
- Combined validation using `scripts.check_korean_batch.check`: 503 occurrences, 454 distinct originals, zero errors (including no duplicate IDs), five existing particle warnings. 21,647 aligned Korean occurrences remain untranslated.
- Additional assertions passed for all 217 new entries: ordered slash-control sequences, leading/trailing whitespace, whitespace immediately following `/n`, and speaker-bracket counts. SHA-256 comparisons confirmed batches 001–002 unchanged during translation generation.
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 8 tests passed in 0.002 seconds.
- Created `docs/review/korean-english-batches-001-003.md`: 503 rows, 20 sections, 65 specifically flagged entries. Verified exact preservation of the earlier 286 table rows and their review numbers, 503 unique review numbers, all new source/target text, and all exact catalog-line links. SHA-256 check confirmed the earlier review sheet unchanged.
- No independent linguistic review, Latin-name verification, visual layout, voice timing, game runtime, particle-renderer, or installable-build testing performed. All new translations remain draft. No Steam edits, build, launch, installation, commit, publication, or push performed.


## 2026-09-22 — opening variants and prison years (batch 004)

- Added `localization/en-US/korean-batch-004.jsonl`: 157 Korean-bearing draft occurrences, 139 distinct originals. Aligned table coverage: `art_fl00_s01` 14, `art_fl00_s02` 17, `art_fl00_s03` 8, `art_ko_fl02_s01` 42, `art_fl02_s01` 25, `art_ko_fl02_s02` 30, `art_fl02_s02` 21. Exact source-index set assertions passed for all seven tables.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-004.jsonl`: 157 occurrences, 139 distinct originals, zero errors, zero warnings, `installable_english_patch: false`. Subsequent edit removed only redundant notes; final combined validation passed.
- Combined validation via `scripts.check_korean_batch.check`: 660 occurrences, 583 distinct originals, zero errors, five existing particle warnings; 21,490 aligned Korean occurrences remain untranslated.
- Additional assertions passed for all 157 entries: ordered slash controls, leading/trailing whitespace, whitespace following `/n`, and speaker-bracket counts. Source-index gaps and variant-specific wording preserved. SHA-256 comparisons confirmed prior batches unchanged during generation.
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 8 tests passed in 0.002 seconds.
- Created `docs/review/korean-english-batches-001-004.md`: 660 rows, 27 sections, 86 flagged entries. Assertions verified unchanged earlier 503 table rows, unique R001–R660 identifiers, all source/target text, and all exact catalog-line links. Earlier review sheet SHA-256 unchanged.
- Proper names, inferred sulfur-mine terminology, guard allegations, and the repeated Chapter 2 heading remain explicitly provisional. No independent linguistic review, Latin-spelling verification, visual layout, voice timing, runtime, or installable-build validation. No Steam edits, build, launch, installation, commit, publication, or push performed.


## 2026-09-22 — approved terminology corrections

- Recorded High Church, High God, High Gods, and Gaysir in `docs/GLOSSARY.md`, AGENTS.md, and workflow guidance. Required Korean/Chinese contextual disambiguation; ordinary verbal 주신 must not be replaced as a deity name.
- Checked all seven affected translated occurrences against Chinese references: 主神教 for the one 주신교 line, 盖西尔 for six 게이시르 lines. Corrected seven targets across batches 001–003. No standalone deity 주신/주신들 currently requires a target change; generic 신/교회/교회단 were not automatically renamed.
- Combined catalog validation: 660 entries, zero errors, five existing particle warnings. Ordered slash-control assertions passed. All three review sheets synchronized; exact target text, links, and existing review numbers verified. Original Korean and Chinese source/reference fields preserved by validation.
- Initial temporary helper invocation failed to import scripts; reran successfully with the repository on PYTHONPATH. No source catalog or game files edited, build, installation, commit, or push performed.


## 2026-09-22 — user name and trial terminology approvals

- Applied 16 target corrections across batches 001 and 003: Reuben → Ruben (12 occurrences), Syrups → Cyrups (2), Court of Devil Worship → Inquisition (2). Recorded Academy, Iscariot as a name, Gishne, and Secret Chronicles of the War of Genesis as approved; replaced the corresponding provisional notes in both variants. Whole entries remain draft.
- Updated glossary, persistent instructions, workflow, status, and all three review sheets. Existing review numbers and exact-entry links preserved; review-table targets checked against catalogs.
- Combined validation: 660 occurrences, zero errors, five existing particle warnings. Ordered controls, boundary whitespace, and whitespace after `/n` assertions passed. Original source/reference fields preserved.
- Namu Wiki searches returned no results; direct attempts for Korean name pages failed with non-retryable web-tool errors. User approvals are the basis for these choices; no site verification claimed.
- No runtime testing, build, installation, Steam edits, commit, or push performed.


## 2026-09-22 — sulfur mine and meeting Deimos (batch 005)

- Added `localization/en-US/korean-batch-005.jsonl`: 112 Korean-bearing draft occurrences, 109 distinct originals. Exact aligned coverage: `art_ko_fl02_s03` 30, `art_fl02_s03` 32, `art_ko_fl02_s04` 25, `art_fl02_s04` 25. Source-index set assertions passed for all four tables; no missing indices invented.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-005.jsonl`: 112 occurrences, 109 distinct originals, zero errors, zero warnings, `installable_english_patch: false`.
- Combined validation using `scripts.check_korean_batch.check`: 772 occurrences, 691 distinct originals, zero errors, five existing particle warnings; 21,378 aligned Korean occurrences remain untranslated.
- Ordered slash controls, boundary whitespace, whitespace following `/n`, and speaker-bracket count assertions passed for all new entries. Original source/reference fields validated. SHA-256 comparisons confirmed batches 001–004 unchanged.
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 8 tests passed in 0.002 seconds.
- Created `docs/review/korean-english-batches-001-005.md`: 772 rows, 31 sections, 122 entries with specific notes. Assertions verified unchanged prior 660 rows, unique R001–R772 numbers, all source/target text, and all exact-entry links. Prior sheet SHA-256 unchanged.
- Read Chinese alongside Korean for these scenes. 主神教会 / 主神教 confirms High Church for 주신교회 / 주신교; applied the approved book title. Deimos, Cesare, and Dark God(s) remain provisional. Namu Wiki searches for Deimos and Cesare returned no results; no external spelling verification claimed.
- No independent linguistic review, layout, voice timing, particle-renderer, game runtime, or installable-build validation performed. No Steam edits, build, launch, installation, commit, publication, or push performed.


## 2026-09-22 — Deimos approval and history/memory (batch 006)

- Recorded user approval of 데이모스 = Deimos in the glossary and instructions; resolved 26 batch-005 notes and synchronized that review sheet without changing targets or review IDs.
- Added `localization/en-US/korean-batch-006.jsonl`: 63 Korean-bearing draft occurrences, 63 distinct originals. Exact source-index coverage: `art_ko_fl02_s05` 10, `art_fl02_s05` 12, `art_ko_fl02_s06` 13, `art_fl02_s06` 28. The art variant's expanded historical account and philosophical dialogue remain separate.
- `.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-006.jsonl`: 63 occurrences, 63 distinct originals, zero errors, zero warnings, `installable_english_patch: false`.
- Combined validation: 835 occurrences, 754 distinct originals, zero errors, five existing particle warnings; 21,315 aligned Korean occurrences remain untranslated. Ordered controls, leading/trailing whitespace, whitespace after `/n`, and speaker-bracket counts passed for all new entries. Original source/reference fields validated.
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 8 tests passed in 0.002 seconds.
- Review sheet `docs/review/korean-english-batches-001-006.md`: 835 rows, 35 sections, 138 entries with specific notes. Assertions verified prior 772 rows unchanged after the Deimos-note correction, unique R001–R835 numbers, source/target text, and exact-entry links. Previous catalog and sheet hashes unchanged during generation after that correction.
- Korean and Chinese checked together. Generic 신 retained as god(s), not automatically High God(s). New historical names and alliances are provisional. Namu Wiki name searches returned no results; no external spelling verification claimed.
- No independent linguistic review, layout, voice timing, particle-renderer, game runtime, or installable-build testing. No Steam edits, build, launch, installation, commit, publication, or push performed.


## 2026-09-22 — completion work in progress, batches 007–018

- Added Korean-first story, units, UI, equipment/skills, shared labels, locations, and early quest-journal drafts. Current combined audit: 7,983 occurrences, 2,398 distinct originals, zero errors, 14 unresolved particle warnings; 14,167 aligned Korean occurrences remain untranslated.
- `scripts/build_english_stage.py` verifies ordered slash controls, key icons, boundary/post-break whitespace, original occurrence references, and existing catalog rules. Audit saved privately in `private/english-build-audit.json`.
- Seven duplicate occurrence IDs introduced while selecting complete story tables were caught by the combined build gate before writes, then removed from later batches 013–014. Existing earlier occurrences retained. Combined audit then passed.
- 15 unit tests passed in 0.567 seconds, including source/output overlap, traversal, changed source reference, control ordering, key icon loss, whitespace, and missing/particle coverage gates.
- Installed spooky 2.0.0 in local .venv after approved network escalation. Verified original Addressables catalog hash and original fieldtext bundle CRC/size against source catalog. PY_SSIZE_T_CLEAN deprecation warnings observed; hashing succeeded.
- Experimental stage 001: 1,109 catalog entries, 1,104 staged across seven resources; readback passed; originals unchanged.
- Experimental stage 002: 7,144 catalog entries, 7,130 staged across 11 resources; edited typetrees read back exactly, object identities and unedited object bytes preserved; original files unchanged. Updated catalog hash e8fd40bd33bf708b40a372218f100faa. Snapshot predates batch 017–018 and Pretoria spelling correction.
- Nine metadata literal drafts individually fit original byte budgets and preserve placeholders/slash controls. Not part of staged resources. No metadata runtime validation.
- Source variant differences preserved, including mana/Abydos prayers and classic/remastered disagreement about Shakbari's divine classification. Verbal 구해 주신 and 태워주신 are not High God.
- New review generator covers later batches in stable batch order and links each occurrence; R001–R944 remain the existing review sheet.
- No independent language review, font/layout, voice timing, particle-renderer, game launch, or runtime validation. No installation, Steam writes, commit, publication or push. Work remains incomplete.


### Continuation through batch 032

- Combined catalog: 10,283 occurrences; 11,867 aligned Korean occurrences remain, entirely in fieldtext.ko and fieldtext.re. Zero validation errors; 14 unresolved particle warnings.
- All aligned non-art resources now have drafts. This is aligned-operation coverage, not a full-game inventory. Quest journal coverage: all 490 occurrences / 423 unique source strings. Main story through both variants of Chapter 5 complete at aligned-entry level.
- Original UI literal newline sequences (including mixed LF/CRLF paragraphs) checked for all 1,211 batch-031 occurrences. Rich tags, sprites, dates, prototype labels, and key icon IDs retained.
- Iyoline spelling aligned to existing character catalog; Durandal aligned to item catalog. Source original/reference fields unchanged.
- Review regenerated through batch 032. Latest successful private build is still stage 002 through batch 016; newer drafts not yet rebuilt. No runtime test or installation.


### Continuation through batch 040

- Combined audit: 11,309 occurrences, 4,385 distinct originals, zero errors, 14 particle warnings; 10,841 aligned Korean occurrences remain. Review index regenerated through batch 040.
- Main scenes through both variants of fl09_s01 drafted. Town/dungeon tables and training conversations remain pending; do not infer full chapter gameplay coverage.
- Stage 003 snapshot through batch 033: 10,422 catalog entries, 10,408 staged, 12 resources; full edited-tree readback passed, unaffected objects/identities preserved, originals unchanged. Addressables hash 1c71404b8251bc49a12e8bdc226e5327. Still no runtime test.
- Ruban (루밴), decoy's distinct speaker label, flagged provisional rather than blanket replacement with Ruben. Classic/remastered expanded half-brother confession retained. Chapter 8 explicitly establishes Ruben as younger brother; earlier journal did not state age and remains faithful to that wording.
- A report-summary command used nonexistent `built_files` key and failed read-only; corrected to `outputs`. No stage failure or data changes resulted.


### Continuation through batch 047

- Added 1,412 occurrences in batches 041–047, covering main scene tables of Chapters 10–13 in both variants. Combined audit: 12,721 occurrences; 9,429 aligned Korean occurrences remain; zero errors, 14 existing particle warnings.
- Korean and Chinese read alongside one another; approved names preserved, with verbal 대접해 주신 and 길러주신 correctly distinguished from deity terminology. Repeated Libreville dinner table reused only after source comparison; source fields and independent occurrence IDs retained.
- Review index regenerated through batch 047. Current stage 003 remains a stale snapshot through batch 033. No additional resource rebuild, runtime test, installation, Steam edits, or publication.


### Continuation through batch 055

- Combined audit: 14,268 occurrences, 7,882 aligned Korean occurrences remaining, zero errors, 14 unresolved particle warnings. Main scene tables fl14–fl20 and alternate-route fl22 drafted; other route and town/dungeon/training tables remain.
- Fifteen unit tests passed in 0.446 seconds. Review index regenerated through batch 055.
- Private stage 004 rebuilt the batch-054 snapshot: 14,042 catalog entries, 14,028 staged across 12 resources. Full edited-tree readback passed; object identities and unaffected objects preserved; originals unchanged. Addressables hash fa0d939dc273338f2fdf6229bfc9fd1b. Existing spooky PY_SSIZE_T_CLEAN deprecation warning only.
- High Church checked against 主神教 in fl22; generic God/Mana kept distinct. Branch-specific narratives, save choices, partial revelations, and epilogue three-year dialogue/four-year heading differences preserved.
- No runtime validation, game launch, install, Steam write, commit, or publication. Stage is experimental and incomplete.


### Continuation through batch 068

- Combined audit: 17,674 occurrences, 9,452 distinct originals, 4,476 aligned Korean occurrences remaining, zero errors, 14 unresolved particle warnings. Review index regenerated through batch 068.
- Added fl23–fl28 endings, additional final confrontations/Clausewitz identity reveal, mansion NPC conversations, and 2,250 short fieldtext occurrences. Chinese read alongside Korean; original variants and incomplete fragments retained. Minor names remain provisional.
- Corrected a validation false positive for decorative double-angle headings such as << Libreville >>. Delimiters remain checked, and real rich-text tag changes remain rejected. Added a regression test: all 16 Python tests passed in 0.442 seconds. Initial audit rejected two decorative heading occurrences; corrected audit has zero errors.
- Aligned item pickups to Worn Excalibur, Hawk Eye, and Jeffrey's Trousers; Ruth aligned to prior journal drafts. Source and reference fields unchanged. Korean Brass Gem item spelling retained despite inconsistent Chinese blessing/breath translations. Verbal 계셔주신다니 distinguished from deity 주신.
- Latest resource rebuild remains stage 004 through batch 054; later drafts have not yet been staged. No game launch, runtime test, installation, Steam writes, commit or publication.


### Continuation through batch 074

- Combined audit: 18,995 occurrences, 3,155 aligned Korean occurrences remaining, zero errors, 14 unresolved particle warnings. Completed remaining aligned Iyoline training, Cyrups, Gaysir, and Pretoria dialogue; Korean/Chinese variants checked alongside each other.
- Stage 005 through batch 072: 18,619 catalog entries, 18,605 staged across 12 resources, full readback passed, originals unchanged. Addressables hash cc5913ff4ba8929ceaa212227a8f6d0b. Existing spooky deprecation warnings only.
- Batch 074 first authoring used the wrong target key; audit failed with KeyError before any build. Corrected to target; full audit then passed. No source fields changed. Review regenerated through batch 074.
- Classic/remastered mission differences, geographical directions, and NPC contradictions retained. Generic god incarnate kept distinct from High God terminology. No runtime validation, installation, Steam writes, commit or publication.


### Continuation through batch 081

- Combined audit: 20,332 occurrences, 1,818 aligned Korean occurrences remaining, zero errors and 14 existing particle warnings. Batches 075–081 complete Antananarivo, Bordeaux, Memphis, Nicosia, Caracas and Lowen aligned dialogue. Review regenerated through 081.
- Every new unique Korean entry read with Chinese support. High Church checked against 主神教; 보석을 주신 is verbal giving. Iscariot and Deimos use approvals. SP-7 source designation deliberately retained despite PS-7 elsewhere. NPC directions, contradictory Chaos Cube origin legends, classic/remastered costs and weapon mechanics retained.
- No further code changes/tests needed; catalog audits passed after each batch. Latest stage remains 005 through 072. No runtime validation, installation, Steam writes, commit or publication.


### Continuation through batch 088

- Combined audit: 21,369 occurrences, 781 aligned Korean occurrences remaining, zero errors and 14 existing particle warnings. Review regenerated through 088. Batches 082–088 complete Libreville and Paro (1,037 occurrences).
- Korean read with Chinese support. Preserved uppercase /N, incomplete legends, alternate Charles/Hugh/Frobisher names and Diana parentage, differing succession ranks, and NPC illness/poisoning allegations. Verbal 주신 constructions remain distinct from deity terms.
- No runtime validation, installation, Steam writes, commit or publication. Latest resource stage remains 005 through 072.


### Aligned catalog complete through batch 095

- 22,150 translated occurrences, zero aligned Korean occurrences remaining, zero audit errors and 14 existing particle warnings. This includes one non-Hangul aligned entry; original Korean coverage is 22,149/22,149. Review regenerated through 095.
- Batches 089–095 complete Dakama, base dialogue, dungeon events, routes and puzzle clues. Chinese checked alongside Korean. Original variants retained; desert inn typo explicitly noted.
- Batch 093 initially produced two false-positive formatting errors for visible single-angle cave headings. Space-delimited headings now translate while real tags remain protected. Regression coverage added; 17 tests passed in 0.411 seconds. Full audit then passed.
- Catalog completion is not full game inventory or runtime validation. Particle handling, metadata, font/layout and a separate-copy game test remain outstanding. No Steam writes, installation, launch, commit or publication.


### Complete resource build and launch attempt — 2026-09-22

- Added 253 supplemental resource translations and expanded metadata from 9 to 30 edits. Final audit: 22,403 resource entries, zero errors/warnings, zero aligned Korean remaining. Metadata fixed-slot validation preserves file length (17,874,712 bytes), source ranges, controls and all unrelated bytes.
- Investigated the exact GameAssembly binary: particle routine skips absent markers. Fourteen row-specific source/target proofs are accepted only with the matching binary SHA. All 22 tests passed in 0.450 seconds (`private/tests-build096.log`).
- Complete stage 001: 22,403 resource edits, 30 metadata edits; 14 edited files plus catalog.bin/hash. Every edited object/metadata range reopened successfully, unaffected objects and originals unchanged. Catalog hash a1068c40dd8b3d5132013a4f61f245f0. Result: `private/english-stage-complete-001-result.json`.
- Inventory: 196,715 objects inspected; 325 unreadable-schema objects remain. Supporter names/internal action identifiers preserved. Initial exploratory metadata parsing used an obsolete layout and was discarded; corrected IL2CPP v39 offset-table parsing validated the final edits. ASCII font coverage checked; unsupported accented e/em dash/ellipsis replaced with e/--/....
- Cloned a separate 77-file game copy and verified all 16 translated overlay files. Added steam_appid.txt (5099430) to the copy. Backed up 20 save/settings/log files before launch.
- First CrossOver command failed native-path resolution (exit 2); Z: Windows path launched Unity. Runtime log reports k_ESteamAPIInitResult_NoSteamClient. This validates startup only, not game menus, resources in active play, fonts or dialogue. Computer Use required pending Accessibility/Screen Recording permissions; retry failed with server timeout -10005. No visual/gameplay test completed.
- Review regenerated for 22,403 entries; launch instructions and standalone local launcher provided. Steam installation unchanged; no commit, push or publication.

### Screenshot-driven layout and saved-name corrections

- User supplied four runtime screenshots: journal, character screen, field and battle. English resource loading is confirmed by these screenshots; full-playthrough coverage is not implied.
- Found Korean DialogueName/FullName/JobName in existing gzip JSON saves. Prepared seven separate converted copies; originals byte-checked unchanged. No live save installation. Added display-only and unknown-name regression tests: 24 tests passed in 0.576 seconds.
- Shortened 16 catalog occurrences for Training 6, Chapter 2 subtitle and Special command. Source/Chinese references preserved. Full stage layout-002 audit: zero errors/warnings; readbacks passed and originals unchanged; catalog hash 28d2bfe4a64bb39ddbff521401f0a9cb.
- Cloned second playtest folder, applied and hash-verified 16 overlay files. First playtest copy and active saves untouched. New layouts/conversions have not yet been runtime-tested. Review sheets regenerated.

### Attack selector and auto-battle labels — playtest 3

- Applied user corrections to 48 attack labels: 20 W.Slash, 20 S.Slash, eight Ricochet. Slash unchanged. Full intended meanings Weak Slash, Strong Slash and Ricochet Blade recorded in glossary. Single-token compact suffixes address screenshot behavior where only the final word appeared; exact code path remains untraced.
- Shortened 14 Use Special Attacks labels to Use Special and 14 Prioritize Healing labels to Heal First. Source fields, IDs, references and controls unchanged. No executable code changes; existing 24-test result remains applicable, not rerun.
- Full stage combat-003 passed audit (22,403 resource entries, zero errors/warnings), object/metadata readback and original preservation. Catalog hash b4f16a2deebd9d2292c8cb66c803a2d4. New playtest-3 copy has 16 hash-verified overlay files. No changes to active saves, previous copies or Steam originals. Revised labels have not been runtime-verified.

### Standalone English Windows build kit

- Added English-only UI and resource reconstruction modules under windows/, reusing upstream transaction behavior in a separate English engine. Embedded payload trust checks, file/version checks, backup/install/restore/recovery, no updater. Optional save-name conversion writes new copies only.
- Exporter packages 16 compressed XOR differences from combat-003; includes exact executable, GameAssembly and dependency hashes. Build kit 003 is about 24 MB and remains ignored/private. Build scripts use Python 3.12 x64, PyInstaller 6.22.3, nine packaged tests, single-file windowed output. No .NET dependency.
- Full suite: 33 tests passed in 0.469 seconds. Packaged suite: nine tests passed in 0.048 seconds. Tests include idempotence, corruption/modification rejection, rollback, explicit recovery, newer-change preservation, traversal rejection and save-field isolation.
- Full 16-file integration install and restore passed against separate private game copy; original Steam hashes unchanged. Windows-specific process enumeration and file locking were explicitly replaced in local test subclass. Windows runtime/frozen UI not tested or built yet.
- Intermediate kit-002 test reused a kit-001 backup lacking newly required GameAssembly; it stopped safely before installation. Retested with a fresh state directory and passed. First py_compile invocation could not write Apple's external cache under sandbox; read-only compile() syntax checks subsequently passed without a cache write. ZIP CRC/integrity passed; SHA and size saved in private/windows-build-kit-report.json.
- User requests remote Windows prerequisite installation; current Computer Use lists Mac only, awaiting connection details. No Steam edits, publication or push.
- Connection check after user clarification: project inventory shows only Mac host; Computer Use shows Mac applications. Official remote-connection documentation inspected. Windows prerequisite installation remains pending Windows-host task access.

### Translation review refresh and GitHub README

- Offline review: parsed embedded JSON, verified 22,433 unique IDs (22,403 resource rows + 30 metadata rows), correct R001/R22403/M030 endpoints; all 944 early Markdown rows refreshed with stable numbering. User text rendered via textContent and embedded less-than signs escaped. No external dependencies/network required. Visual browser inspection not performed.
- README replaced with English/Korean project introduction, accurate Chinese-upstream/early-English-draft provenance, direct Korean translation policy, review corrections and honest local/release status. README.en.md links to bilingual introduction.
- GitHub default main checked in isolated checkout. Git HTTPS push failed for missing CLI credentials; connected GitHub tools successfully published the two README files. Commits: 0b76d1930ec3034fdb56663c8da11d1443eb3345 and d493e1a6473ece3319df01924f3b90fe62d29cc2. Remote contents fetched back and compared with local publication text. No unrelated changes or private resources published.

### macOS / CrossOver and Linux / Proton support

- Replaced Windows-only state path, casefolded path key, tasklist-only process guard and msvcrt-only lock with platform helpers. Windows behavior retained; Linux case-sensitive paths distinguished; XDG absolute-path fallback tested. POSIX running-game detection covers quoted paths, Wine/Proton forms and failed-scan refusal. Actual flock contention/release tested.
- Final full suite: 38 tests passed in 0.564 seconds. Packaged suite on Python 3.14.7: 14 tests passed in 0.043 seconds. An initial attempt to run the entire Unity translation suite in the isolated packaging runtime failed for missing UnityPy dependencies; that runtime intentionally contains only patcher dependencies. Full suite subsequently passed in project .venv; packaged suite passed in packaging runtime.
- Native integration first failed closed because sandbox denied ps. Escalated test then passed with real ps/flock: full 16-file install/restore and unchanged Steam originals. Compiled modern app also returned installed then original through CLI; private/native-frozen-install.log and restore.log retain results. Final kit-005 app status reports original with 16 backup files.
- Apple Python 3.9/Tk 8.5 produced a blank GUI. Discarded that candidate. Downloaded Python.org 3.14.7 package and matched published SHA256 70c5239ad2d62925d2947e46921d0ddd3d35be3d2f0a2d50db33da507dbcb419. Extracted runtime only under private/, no system-wide Python installation. Relocated 19 copied Mach-O runtime dependencies and ad-hoc signed them; initial absolute-path relocation failed due load-command size, relative loader paths succeeded. Rebuilt using PyInstaller 6.22.3 and Tk 9. The GUI now visibly renders all controls; Computer Use clipboard/input actions did not operate the Tk field reliably, so full GUI interaction remains manual QA. Native build now rejects Tk <8.6 on macOS.
- Final Mac app codesign --verify --deep --strict passed; both deliverable ZIP integrity checks passed. SHA256/size in private/native-deliverables.json. Ad-hoc signing is not notarization. Intel Mac, Fedora runtime and Proton gameplay remain untested; no claims of cross-distro/Steam Deck binary compatibility. No Steam modifications, active save changes or publishing.

### Windows handoff fixes

- Read MAC-HANDOFF.md from /Volumes/mdbkshare/windows related/Zephyr-Windows-Fixes-Mac-Handoff.zip. All four supplied patch/source hashes matched before integration. Did not run the handoff's suggested shell commands or replace newer modules wholesale.
- Ported windows_long_path() and root/candidate normalization in safe(), prefixed state directory and POSIX journal serialization. Kept cross-platform platform helpers intact. Imported exact long-backup regression from handoff. Full local suite: 39 tests passed in 0.507 seconds; this is not Windows MAX_PATH runtime verification.
- Windows handoff reports 10 tests, successful PyInstaller EXE/GUI, 18 matching embedded payload hashes, and frozen diagnostic install/restore on copied game files with originals unchanged. Windows EXE 35,452,942 bytes, SHA256 6e62d9627631b6a4154501b72428c8aee7957a7b3fd99cf58c0b9df7bdfbedcb was not supplied or independently executed here. No reported gameplay test.
- Created desktop kit 006; ZIP integrity passed; all 18 payload files unchanged from kit 005. New merged Windows executable remains to be built/tested. Old malformed journals and real UNC shares remain unsupported/untested cases as noted in handoff. No Steam writes, save edits, commit, push or publication.

### Windows game-folder help and environment documentation

- Added usual Steam directory and alternate-library instructions to Windows GUI and packaged README; Browse starts there only when it exists. Target remains user-selected and installation requires existing confirmation. Enlarged Windows layout.
- 39 tests passed in 0.502 seconds (private/folder-guidance-tests.log). GUI compile() syntax passed. Desktop kit 007 ZIP integrity, packaged GUI source equality, and byte-identical payload against kit 006 passed. This is not a Windows GUI runtime test; rebuild and manual Windows check remain required.
- Read macOS 26.5.2 (25F84), Mac mini M4 / 32 GB, CrossOver 26.3 locally. Documented user-reported Windows 11 testing and planned Fedora 44 on Galaxy Book Pro2 360 i5-1240P in English and Korean README sections, with test-scope limits.
- Published README.md only through GitHub connector, commit 443c26599e712c4c43a636eed64e4dd0fced0c14; fetched remote content equals local exactly. No game writes, active save changes or unrelated publication.

### Mac folder guidance — desktop kit 008

Added the full typical CrossOver Steam bottle game path to the Mac GUI, alternate-bottle Open C: Drive instructions and Shift+Command+G folder-picker help. Browse starts at the example directory if present; target remains user-selected. Pasted home-relative paths expand before confirmation. Enlarged window accommodates the guidance. Native README updated.

Rebuilt Apple Silicon app with Python 3.14.7 / Tk 9 / PyInstaller 6.22.3. Actual compiled app screenshot confirms the complete path/help and all controls fit without overlap. GUI syntax, kit ZIP integrity and byte-identical payload against kit 007 passed. codesign --verify --deep --strict and app ZIP integrity passed. Deliverables: private/Zephyr-English-macOS-AppleSilicon-008.zip and private/Zephyr-English-Desktop-Kit-008.zip. Ad-hoc signed, not notarized. No install/restore repeated for this UI change; previous engine tests remain recorded separately. No game/save changes or GitHub publication.

### Source publication requested

User authorized pushing the current work to GitHub. Publication includes Korean-based translation batches/review sheets, shared desktop patcher source (Windows long-path fixes and Windows/Mac folder guidance), build/export tooling, tests and documentation. Private game assets, extracted source catalogs, compiled builds, saves and .DS_Store are excluded. CLI HTTPS push has no configured credentials; use the authenticated GitHub connector with current main as parent and a non-forced ref update.

Pre-publication checks: 39 tests passed in 0.502 seconds; complete catalog audit reports 22,403 entries, zero errors/warnings and zero remaining aligned Korean occurrences. Existing runtime limits remain as recorded. No installer release is created by this source publication.
