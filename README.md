# The Rhapsody of Zephyr Remastered — English Translation
# 서풍의 광시곡 리마스터 — 영어 번역

[English](#english) · [한국어](#한국어)

## English

An unofficial English translation project for **The Rhapsody of Zephyr Remastered**, based on the **original Korean game text**.

### Where this fork comes from

This repository is a fork of [wanjizheng/zephyr-remastered-zh-cn](https://github.com/wanjizheng/zephyr-remastered-zh-cn), a Chinese localization project. Credit for the upstream Chinese translation and patching tools belongs to its contributors.

The first English drafts in this fork were translated from the upstream Chinese text. The project then moved to translating **directly from the original Korean**. Korean is authoritative whenever the sources differ; Chinese is used only as supporting context. The earlier Chinese-derived drafts are kept separately and should not be mistaken for the current Korean-based translation.

### What has changed after review

Translation review and gameplay screenshots have led to corrections to character and place names, religious terminology, attack names, and interface wording. Examples include **Geysir, Cyrups, Ruben, Gishne, Deimos, High Church, High God**, and **Blade Shot**. Korean 주신 is checked in context: it can refer to a deity or be part of an ordinary expression meaning “given/provided.”

Long labels have also been shortened where the game interface clips or overlaps text. The latest working translation uses full battle labels such as **Weak Slash**, **Strong Slash**, **Blade Shot** (탄검), and **Killing Blade** (살검). Existing release packages may retain earlier wording. Names and wording that have not been confirmed remain provisional, and review is ongoing.

### Faster dialogue reveal

The beta.3 patch includes **2.5× faster letter-by-letter dialogue reveal** (28 ms per character instead of 70 ms). This reduces the wait caused by longer English text after the spoken audio finishes. Voice playback speed and scripted pauses are unchanged.

The Mac playtest was accepted by the user. Beta.3 packages include this change; older releases and beta.2 kits do not. The full Auto-Advance label uses a smaller font to fit its button.

### Current status

The local working catalog contains **22,403 translated resource entries and 30 hard-coded text edits**. An English playtest build has been tested in selected gameplay screens, and further review is in progress. These counts describe the translated catalog, not a guarantee that every possible screen, image, or story branch has been verified.

Download **[English 1.0.0-beta.5](https://github.com/mdbkkorea/zephyr-remastered-en/releases/tag/english-v1.0.0-beta.5)** from GitHub Releases. Choose the archive for your operating system and edition. For Windows, use **ZEnglishSteam_1.0.0_beta05.zip** or **ZEnglishPurple_1.0.0_beta05.zip**, extract to **C:\Zephyr**, and run **Build-Windows.cmd** with Python 3.12 (64-bit) installed. See the [build and upgrade instructions](docs/RELEASE_1.0.0-beta.5.md). The inherited Chinese releases do not install this English translation.

**The Mac patcher and portable launcher have been tested by the maintainer on the Mac below. Earlier Windows installer testing is complete; current Windows build kits await Windows testing. Linux / Proton gameplay testing remains pending.** Windows installer checks cover installation, restoration, mod detection, unsupported-version fallback and the GUI. This does not mean every story branch or translated screen has been checked. macOS has installer checks and user-confirmed Steam/CrossOver gameplay with the translated Fullmap overlay; Linux has container-based installer checks, with Fedora 44 / Proton testing still pending.

Please use a legitimate copy of the game. Original game assets and full extracted source catalogs are not included as part of this English documentation update. Existing saves may retain Korean character names and job titles; translating those saved display fields is separate from patching game resources.

The installer automatically detects **ZephyrPassives 2.4.3** and **ZephyrFullmap 1.8.0**. Unsupported versions select standard translation and preserve all mod files. See [release notes](docs/RELEASE_1.0.0-beta.5.md).

### Testing environments

| Status | Computer | Environment |
| --- | --- | --- |
| Patcher and launcher tested by maintainer | Mac mini (2024), Apple M4, 32 GB RAM | macOS Tahoe 26.5.2; CrossOver 26.3; Windows Steam inside CrossOver |
| Fully tested installer | Samsung Galaxy Book Pro2 360, Intel Core i5-1240P | Windows 11; Steam |
| To be tested | Same Samsung Galaxy Book Pro2 360, Intel Core i5-1240P | Fedora 44 Linux; Steam / Proton testing planned |

These are the maintainer's test environments, not minimum system requirements or a guarantee of a complete playthrough. CrossOver gameplay screenshots confirm English text in selected screens. Windows patcher testing includes installation and restoration on a separate game copy. Linux installer checks passed under Debian 12 x86-64 emulation; native Fedora 44 and Proton gameplay testing remain pending.

### Windows beta.5 build repair

If a beta.5 kit reports **No module named pip**, replace both
[Build-Windows.ps1](windows/Build-Windows.ps1) and
[english_version.py](windows/english_version.py) in its extracted ZSteam/ZPurple
folder with the current files from this repository, then run **Build-Windows.cmd**.
Download each file using GitHub's **Download raw file** button. The updated script
repairs pip and produces the new edition-specific installer name. This fix has
been confirmed working by the user. The refreshed ZEnglish beta.5 ZIPs already include this fix; manual replacement is only needed for the older zephyr_english ZIPs.

### CrossOver mod launcher

Beta.5 includes the launcher and latest reviewed translations; see [beta.5 build notes](docs/RELEASE_1.0.0-beta.5.md).

The Mac app is **not notarized by Apple** and lacks a Developer ID signature. For a trusted download blocked as an unidentified developer:

1. Extract the complete Mac ZIP and try opening **ZEnglishMacos_1.0.0_beta05.app** once.
2. Choose **Done** or **Cancel**, not **Move to Trash**.
3. Open **System Settings → Privacy & Security**, scroll down to **Security**, and click **Open Anyway** for the patcher.
4. Authenticate if asked, then confirm **Open**.

This is Apple's per-app exception procedure, not a request to disable Gatekeeper. A “will damage your computer” or “damaged” alert is a different issue. See the [Mac guide](docs/MAC_GUIDE.md) and [Apple's official instructions](https://support.apple.com/en-us/102445).

**Beta.5:** includes a portable `Launch-Zephyr-CrossOver.command`. It finds
CrossOver and offers editable bottle/game selections, remembers them locally, and
launches the installed Steam game with the `winhttp=n,b` mod override. Keep it beside
the bundled patcher app; no separate Python is needed. The app and command must come from the same beta.5 ZIP; beta.3 lacks the launcher.
Keep Steam open in the selected bottle, clear the Linux/Proton Steam launch option, then open the command and click **Launch game**. For the latest translation corrections, restore originals with your previous patcher, then install beta.5. See [CrossOver launcher instructions](docs/MAC_GUIDE.md).

### Finding the game folder on Windows

The usual Steam game folder is:

```text
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered
```

If you installed the game elsewhere, in Steam right-click the game → **Manage → Browse local files**. Copy the folder address into the patcher, or select it with **Browse**. Choose the folder containing `ZephyrRemastered.exe`. Close the game, select **Check Files**, then **Install English** and confirm the folder. For initial testing, use a separate game copy.

### Windows permissions and interrupted installs

If the game is in a protected folder such as `C:\Program Files (x86)`, Windows may report **Permission denied / Errno 13** when the patcher writes files. Close the game and patcher, then right-click `ZEnglishSteam_1.0.0_beta05.exe` / `ZEnglishPurple_1.0.0_beta05.exe` → **Run as administrator**. Building the executable does not require administrator access.

After a failed installation, select the same game folder and click **Check Files**. If it reports an interrupted operation, click **Recover**, then **Check Files** again. Install only when supported original files are reported. Keep the patcher and its backups for restoration.

The default PURPLE folder is `C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`. PURPLE requires a separate experimental package; the linked Steam release does not support it.

### Feedback and credits

When reporting a translation issue, include the Korean text or a screenshot, the scene/menu, and your suggested English wording. If you have a review sheet, include its review number.

- [Report an issue in this English fork](https://github.com/mdbkkorea/zephyr-remastered-en/issues)
- [Original Chinese localization project](https://github.com/wanjizheng/zephyr-remastered-zh-cn)
- [Game on Steam](https://store.steampowered.com/app/5099430/)

The upstream license and contributor credits remain in place. The tool license does not grant rights to the game, artwork, or story; those belong to their respective rights holders. This is an unofficial fan project.

---

## 한국어

**서풍의 광시곡 리마스터의 한국어 원문을 기준으로 진행하는 비공식 영어 번역 프로젝트**입니다.

### 포크의 출처와 번역 방식

이 저장소는 중국어 번역 프로젝트인 [wanjizheng/zephyr-remastered-zh-cn](https://github.com/wanjizheng/zephyr-remastered-zh-cn)을 포크했습니다. 원본 프로젝트의 중국어 번역과 패치 도구를 제작한 기여자들에게 감사를 표합니다.

이 포크에서 처음 작성한 영어 초안은 원본 프로젝트의 중국어 번역문을 바탕으로 했습니다. 이후 **게임의 한국어 원문을 직접 영어로 번역하는 방식**으로 전환했습니다. 두 언어의 내용이 다르면 한국어를 우선하며, 중국어는 문맥을 확인하는 보조 자료로만 사용합니다. 초기의 중국어 기반 초안은 별도로 보관하며, 현재의 한국어 기반 번역과 구분합니다.

### 검토 후 반영한 수정

번역 검토와 실제 플레이 스크린샷을 바탕으로 인명·지명, 종교 관련 용어, 공격 이름, UI 문구를 수정했습니다. 대표적인 표기는 **Geysir, Cyrups, Ruben, Gishne, Deimos, High Church, High God, Blade Shot**입니다. 특히 ‘주신’은 신을 가리키는 명사인지, ‘주신 물건’처럼 동사의 활용형인지 문맥과 중국어 보조 자료를 함께 확인합니다.

게임 화면에서 긴 문구가 잘리거나 겹치는 경우에는 의미를 유지하면서 짧게 다듬었습니다. 최신 작업본의 공격 선택창에서는 **Weak Slash**, **Strong Slash**, **Blade Shot**(탄검), **Killing Blade**(살검)처럼 전체 이름을 표시합니다. 기존 배포 파일에는 이전 표기가 남아 있을 수 있습니다. 아직 확인되지 않은 고유명사와 표현은 잠정 번역이며, 검토를 계속하고 있습니다.

### 대사 표시 속도 개선

beta.3 패치에는 **대사가 한 글자씩 표시되는 속도를 2.5배 빠르게 하는 변경**이 적용되어 있습니다(글자당 70ms → 28ms). 한국어보다 긴 영어 대사 때문에 음성이 끝난 뒤에도 텍스트 표시를 기다리는 시간을 줄입니다. 음성 재생 속도와 대사에 지정된 연출용 대기 시간은 유지합니다.

Mac 플레이테스트에서 사용자 확인을 받았으며 beta.3 패키지에 포함됩니다. 이전 배포판과 beta.2 키트에는 포함되지 않습니다. Auto-Advance 이름은 유지하고 버튼에 맞게 글꼴을 줄였습니다.

### 현재 진행 상황

로컬 작업본에는 **리소스 항목 22,403개와 하드코딩된 텍스트 수정 30개**가 포함되어 있습니다. 영어 플레이테스트 빌드의 일부 실제 게임 화면을 확인했으며, 추가 검토를 진행 중입니다. 이 수치는 번역 카탈로그의 범위를 나타내며, 모든 화면·이미지·스토리 분기를 검증했다는 뜻은 아닙니다.

GitHub Releases에서 **[영어 패치 1.0.0-beta.5](https://github.com/mdbkkorea/zephyr-remastered-en/releases/tag/english-v1.0.0-beta.5)**을 내려받으세요. 운영체제와 게임 플랫폼에 맞는 파일을 선택하세요. Windows는 **ZEnglishSteam_1.0.0_beta05.zip** 또는 **ZEnglishPurple_1.0.0_beta05.zip**을 **C:\Zephyr**에 풀고 Python 3.12 64비트 설치 후 **Build-Windows.cmd**를 실행하세요. [빌드·업데이트 안내](docs/RELEASE_1.0.0-beta.5.md)를 참고하세요. 기존 중국어 배포 파일은 이 영어 번역을 설치하지 않습니다.

**Mac 패치 프로그램과 휴대용 실행기는 아래 Mac에서 제작자가 테스트했습니다. 이전 Windows 설치 프로그램 검증은 완료했으며 최신 Windows 빌드 키트의 실기기 테스트는 예정입니다. Linux / Proton 게임 테스트도 아직 예정입니다.** Windows에서는 설치·복원, 모드 감지, 미지원 버전의 일반 번역 적용 및 GUI를 검증했습니다. 모든 스토리 분기나 번역 화면을 검증했다는 의미는 아닙니다. macOS는 설치 프로그램 검사와 번역된 Fullmap을 포함한 CrossOver 게임 실행을 확인했고, Linux는 컨테이너 환경에서 설치 프로그램을 검사했으며 Fedora 44 / Proton 실기기 테스트는 아직 예정입니다.

정품 게임을 사용해 주세요. 이번 영어 프로젝트 문서 갱신에는 게임 원본 에셋이나 추출한 전체 원문 카탈로그를 포함하지 않습니다. 기존 저장 파일에는 한국어 캐릭터 이름이나 직업명이 남아 있을 수 있으며, 저장된 표시용 문자열의 변환은 게임 리소스 패치와 별도입니다.

설치 프로그램은 **ZephyrPassives 2.4.3** 및 **ZephyrFullmap 1.8.0**을 자동 감지합니다. 지원하지 않는 버전이 있으면 일반 번역만 적용하고 모드 파일은 보존합니다. [릴리스 안내](docs/RELEASE_1.0.0-beta.5.md)를 참고하세요.

### 테스트 환경

| 상태 | 컴퓨터 | 실행 환경 |
| --- | --- | --- |
| 제작자 패치 프로그램·실행기 테스트 완료 | Mac mini (2024), Apple M4, 메모리 32 GB | macOS Tahoe 26.5.2; CrossOver 26.3; CrossOver 안의 Windows용 Steam |
| 설치 프로그램 검증 완료 | 삼성 갤럭시 북 Pro2 360, Intel Core i5-1240P | Windows 11; Steam |
| 테스트 예정 | 동일한 삼성 갤럭시 북 Pro2 360, Intel Core i5-1240P | Fedora 44 Linux; Steam / Proton 테스트 예정 |

위 목록은 제작자가 사용한 테스트 환경이며, 최소 사양이나 전체 플레이 검증을 의미하지 않습니다. CrossOver에서는 일부 실제 게임 화면에서 영어 표시를 확인했습니다. Windows 패치 프로그램은 별도로 복사한 게임 파일에 설치·복원하는 테스트를 진행했습니다. Linux 설치 프로그램은 Debian 12 x86-64 에뮬레이션 환경에서 검증했으며, Fedora 44 실기기 및 Proton 플레이 테스트는 아직 예정입니다.

### CrossOver 모드 실행기

Apple 공증 및 Developer ID 서명이 없는 앱입니다. 신뢰하는 배포 파일이 개발자 확인 불가로 차단되면:

1. Mac ZIP 전체를 풀고 **ZEnglishMacos_1.0.0_beta05.app**을 한 번 실행합니다.
2. **휴지통으로 이동** 대신 **완료/취소**를 누릅니다.
3. **시스템 설정 → 개인정보 보호 및 보안** 아래쪽의 **보안 → 확인 없이 열기(Open Anyway)**를 선택합니다.
4. 인증이 필요하면 인증하고 **열기**를 누릅니다.

앱별 예외를 허용하는 과정이며 Gatekeeper 전체를 끄지 않습니다. 손상되었거나 컴퓨터에 피해를 줄 수 있다는 경고는 다른 문제입니다. [Mac 안내](docs/MAC_GUIDE.md)와 [Apple 공식 설명](https://support.apple.com/ko-kr/102445)을 참고하세요.

beta.5 Mac 빌드에는 휴대용 `Launch-Zephyr-CrossOver.command`가 포함됩니다.
CrossOver를 찾고 보틀·게임 폴더를 선택하여 저장한 뒤, `winhttp=n,b` 설정으로
설치된 Steam 게임을 실행합니다. 함께 제공되는 패치 앱 옆에 두세요. Python을
별도로 설치할 필요가 없습니다. 앱과 명령 파일은 같은 beta.5 ZIP에서 사용하세요. beta.3 앱은 실행기를 지원하지 않습니다. 같은 보틀에서 Steam을 켜고 Proton용 실행 옵션을 지운 뒤 명령 파일에서 **Launch game**을 누르세요. beta.5 번역 수정을 적용하려면 이전 패치 프로그램으로 원본을 복원한 다음 beta.5를 설치하세요.

### Windows에서 게임 폴더 찾기

Steam 기본 설치 경로를 사용했다면 보통 다음 폴더에 있습니다.

```text
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered
```

다른 위치에 설치했다면 Steam 라이브러리에서 게임을 우클릭하고 **관리 → 로컬 파일 탐색**을 선택하세요. 탐색기의 폴더 주소를 패치 프로그램에 붙여 넣거나 **Browse**로 선택하세요. `ZephyrRemastered.exe`가 들어 있는 폴더를 선택해야 합니다. 게임을 종료한 뒤 **Check Files → Install English** 순서로 누르고 대상 폴더를 확인하세요. 첫 테스트는 별도로 복사한 게임 폴더에서 진행하세요.

### Windows 권한 오류 및 중단된 설치 복구

게임이 `C:\Program Files (x86)` 같은 보호된 폴더에 있으면 파일을 수정할 때 **Permission denied / Errno 13(권한 거부)** 오류가 발생할 수 있습니다. 게임과 패치 프로그램을 닫고 `ZEnglishSteam_1.0.0_beta05.exe` / `ZEnglishPurple_1.0.0_beta05.exe`를 우클릭하여 **관리자 권한으로 실행**하세요. 실행 파일을 빌드하는 과정에는 관리자 권한이 필요하지 않습니다.

설치에 실패했다면 같은 게임 폴더를 선택하고 **Check Files**를 누르세요. 중단된 작업이 있다고 표시되면 **Recover → Check Files** 순서로 진행한 뒤, 지원되는 원본 파일이라고 확인될 때 설치를 다시 진행하세요. 복원을 위해 패치 프로그램과 백업을 보관하세요.

PURPLE 기본 설치 경로는 `C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`입니다. PURPLE은 별도의 실험용 패키지가 필요하며, 위에 링크된 Steam 배포판으로는 패치할 수 없습니다.

### 의견 보내기 및 크레딧

번역 수정을 제안할 때는 한국어 원문 또는 스크린샷, 해당 장면이나 메뉴, 제안하는 영어 표현을 함께 알려 주세요. 검토용 파일을 사용한다면 검토 번호도 적어 주세요.

- [영어 포크에 이슈 남기기](https://github.com/mdbkkorea/zephyr-remastered-en/issues)
- [원본 중국어 번역 프로젝트](https://github.com/wanjizheng/zephyr-remastered-zh-cn)
- [Steam 게임 페이지](https://store.steampowered.com/app/5099430/)

원본 프로젝트의 라이선스와 기여자 표기는 유지합니다. 도구의 라이선스가 게임·그림·스토리에 대한 권리를 부여하는 것은 아니며, 해당 권리는 각 권리자에게 있습니다. 이 프로젝트는 비공식 팬 프로젝트입니다.

### Geysir naming note / 게이시르 표기 참고

According to the naming history supplied by the user, the original games officially used **Gaysir**, and the company later changed it to **Geysir** because the earlier spelling could be misleading. This project follows **Geysir / Geysir Empire**. The historical explanation is user-provided and has not been independently verified here.

사용자가 제공한 표기 이력에 따르면, 원작에서는 **Gaysir**를 공식 표기로 사용했으나 오해의 소지가 있어 이후 회사가 **Geysir**로 변경했다고 합니다. 이 프로젝트는 **Geysir / Geysir Empire**를 사용합니다. 해당 변경 경위는 사용자 제공 정보이며 별도로 검증하지 않았습니다.

Installer and archive names follow `ZEnglish[Steam|Purple|Macos|Linux]_Version_betaXX`; see [filename conventions](docs/RELEASE_NAMING.md). The beta.5 archives above have been refreshed to use these names and include the confirmed build fix.
