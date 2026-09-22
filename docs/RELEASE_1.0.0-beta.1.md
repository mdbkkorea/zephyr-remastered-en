# Zephyr English 1.0.0-beta.1

**Only Windows is fully tested for now. macOS and Linux are experimental.** This is a prerelease; translation review continues. Fully tested refers to Windows installer checks, not an exhaustive game playthrough.

- Korean-based English translation: 22,403 resource entries and 30 hard-coded text edits.
- Reviewed Geyshir, Cyrups, Ruben, High Church / High God and Aura Slash terminology, dialogue spacing and compact battle/settings labels.
- Automatically detects ZephyrPassives 2.4.3 and ZephyrFullmap 1.8.0. Passives descriptions assume default settings.
- Unsupported versions select standard translation and leave all mod files untouched. Mods are optional and are not installed by this patcher.
- Verified backups, restoration and interrupted-operation recovery. Saves are unchanged.

Download the matching archive, extract it, close the game, open the patcher and choose the folder containing ZephyrRemastered.exe. Use Check Files, then Install English. Keep the installer and its backups for Restore Original.

Windows: run ZephyrEnglishPatcher.exe. macOS: open ZephyrEnglishPatcher.app (Apple Silicon; not notarized). Linux: run ./ZephyrEnglishPatcher (x86-64, glibc 2.36+).

The usual Windows Steam folder is C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered. For CrossOver, look in the bottle's drive_c under the same Steam path. Steam > Manage > Browse local files can locate custom installations.

For installed user mods, CrossOver launchers need --dll 'winhttp=n,b'; Linux/Proton Steam launch options need WINEDLLOVERRIDES="winhttp=n,b" %command%.

Windows 11 was tested on a Galaxy Book Pro2 360 (i5-1240P). macOS limited testing: Mac mini M4 / macOS 26.5.2 / CrossOver 26.3. Linux installer tests ran under Debian 12 x86-64 emulation; Fedora 44 / Proton gameplay remains pending. Map layout and broader story coverage remain under review.

## 한국어

**현재 완전히 테스트된 배포판은 Windows뿐이며, macOS와 Linux는 실험용입니다.** Windows 검증은 설치 프로그램의 설치·복원·모드 감지·GUI 검사 범위이며 전체 게임의 모든 번역을 확인했다는 뜻은 아닙니다.

운영체제에 맞는 압축 파일을 풀고 게임을 종료한 뒤 설치 프로그램을 실행하세요. ZephyrRemastered.exe가 있는 폴더를 선택하고 Check Files → Install English 순서로 진행하세요. 모드는 별도로 설치해야 하며, 미지원 모드 버전이 있으면 일반 번역만 적용하고 모드 파일을 보존합니다. 저장 파일은 변경하지 않습니다.
