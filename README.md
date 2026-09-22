# The Rhapsody of Zephyr Remastered — English Translation
# 서풍의 광시곡 리마스터 — 영어 번역

[English](#english) · [한국어](#한국어)

## English

An unofficial English translation project for **The Rhapsody of Zephyr Remastered**, based on the **original Korean game text**.

### Where this fork comes from

This repository is a fork of [wanjizheng/zephyr-remastered-zh-cn](https://github.com/wanjizheng/zephyr-remastered-zh-cn), a Chinese localization project. Credit for the upstream Chinese translation and patching tools belongs to its contributors.

The first English drafts in this fork were translated from the upstream Chinese text. The project then moved to translating **directly from the original Korean**. Korean is authoritative whenever the sources differ; Chinese is used only as supporting context. The earlier Chinese-derived drafts are kept separately and should not be mistaken for the current Korean-based translation.

### What has changed after review

Translation review and gameplay screenshots have led to corrections to character and place names, religious terminology, attack names, and interface wording. Examples include **Geyshir, Cyrups, Ruben, Gishne, Deimos, High Church, High God**, and **Aura Slash**. Korean 주신 is checked in context: it can refer to a deity or be part of an ordinary expression meaning “given/provided.”

Long labels have also been shortened where the game interface clips or overlaps text. Compact attack labels include **W.Slash**, **S.Slash**, and **Aura.Slash**. Names and wording that have not been confirmed remain provisional, and review is ongoing.

### Current status

The local working catalog contains **22,403 translated resource entries and 30 hard-coded text edits**. An English playtest build has been tested in selected gameplay screens, and further review is in progress. These counts describe the translated catalog, not a guarantee that every possible screen, image, or story branch has been verified.

Download **[English 1.0.0-beta.1](https://github.com/mdbkkorea/zephyr-remastered-en/releases/tag/english-v1.0.0-beta.1)** from GitHub Releases. Choose the archive for your operating system and extract it before running the patcher. The inherited Chinese releases do not install this English translation.

**Only the Windows release is fully tested for now. macOS and Linux releases are experimental.** Windows installer checks cover installation, restoration, mod detection, unsupported-version fallback and the GUI. This does not mean every story branch or translated screen has been checked. macOS has limited installer checks and selected CrossOver gameplay testing; Linux has container-based installer checks, with Fedora 44 / Proton testing still pending.

Please use a legitimate copy of the game. Original game assets and full extracted source catalogs are not included as part of this English documentation update. Existing saves may retain Korean character names and job titles; translating those saved display fields is separate from patching game resources.

The installer automatically detects **ZephyrPassives 2.4.3** and **ZephyrFullmap 1.8.0**. Unsupported versions select standard translation and preserve all mod files. See [release notes](docs/RELEASE_1.0.0-beta.1.md).

### Testing environments

| Status | Computer | Environment |
| --- | --- | --- |
| Experimental / partially tested | Mac mini, Apple M4, 32 GB RAM | macOS 26.5.2; CrossOver 26.3; Windows Steam inside CrossOver |
| Fully tested installer | Samsung Galaxy Book Pro2 360, Intel Core i5-1240P | Windows 11; Steam |
| To be tested | Same Samsung Galaxy Book Pro2 360, Intel Core i5-1240P | Fedora 44 Linux; Steam / Proton testing planned |

These are the maintainer's test environments, not minimum system requirements or a guarantee of a complete playthrough. CrossOver gameplay screenshots confirm English text in selected screens. Windows patcher testing includes installation and restoration on a separate game copy. Linux installer checks passed under Debian 12 x86-64 emulation; native Fedora 44 and Proton gameplay testing remain pending.

### Finding the game folder on Windows

The usual Steam game folder is:

```text
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered
```

If you installed the game elsewhere, in Steam right-click the game → **Manage → Browse local files**. Copy the folder address into the patcher, or select it with **Browse**. Choose the folder containing `ZephyrRemastered.exe`. Close the game, select **Check Files**, then **Install English** and confirm the folder. For initial testing, use a separate game copy.

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

번역 검토와 실제 플레이 스크린샷을 바탕으로 인명·지명, 종교 관련 용어, 공격 이름, UI 문구를 수정했습니다. 대표적인 표기는 **Geyshir, Cyrups, Ruben, Gishne, Deimos, High Church, High God, Aura Slash**입니다. 특히 ‘주신’은 신을 가리키는 명사인지, ‘주신 물건’처럼 동사의 활용형인지 문맥과 중국어 보조 자료를 함께 확인합니다.

게임 화면에서 긴 문구가 잘리거나 겹치는 경우에는 의미를 유지하면서 짧게 다듬었습니다. 공격 선택창에서는 **W.Slash**, **S.Slash**, **Aura.Slash** 같은 축약 표기를 사용합니다. 아직 확인되지 않은 고유명사와 표현은 잠정 번역이며, 검토를 계속하고 있습니다.

### 현재 진행 상황

로컬 작업본에는 **리소스 항목 22,403개와 하드코딩된 텍스트 수정 30개**가 포함되어 있습니다. 영어 플레이테스트 빌드의 일부 실제 게임 화면을 확인했으며, 추가 검토를 진행 중입니다. 이 수치는 번역 카탈로그의 범위를 나타내며, 모든 화면·이미지·스토리 분기를 검증했다는 뜻은 아닙니다.

GitHub Releases에서 **[영어 패치 1.0.0-beta.1](https://github.com/mdbkkorea/zephyr-remastered-en/releases/tag/english-v1.0.0-beta.1)**을 내려받으세요. 운영체제에 맞는 압축 파일을 선택하고 압축을 푼 뒤 실행하세요. 기존 중국어 배포 파일은 이 영어 번역을 설치하지 않습니다.

**현재 완전히 테스트된 배포판은 Windows 버전뿐입니다. macOS와 Linux 버전은 실험용입니다.** Windows에서는 설치·복원, 모드 감지, 미지원 버전의 일반 번역 적용 및 GUI를 검증했습니다. 모든 스토리 분기나 번역 화면을 검증했다는 의미는 아닙니다. macOS는 제한적인 설치 프로그램 검사와 일부 CrossOver 플레이 테스트를 진행했고, Linux는 컨테이너 환경에서 설치 프로그램을 검사했으며 Fedora 44 / Proton 실기기 테스트는 아직 예정입니다.

정품 게임을 사용해 주세요. 이번 영어 프로젝트 문서 갱신에는 게임 원본 에셋이나 추출한 전체 원문 카탈로그를 포함하지 않습니다. 기존 저장 파일에는 한국어 캐릭터 이름이나 직업명이 남아 있을 수 있으며, 저장된 표시용 문자열의 변환은 게임 리소스 패치와 별도입니다.

설치 프로그램은 **ZephyrPassives 2.4.3** 및 **ZephyrFullmap 1.8.0**을 자동 감지합니다. 지원하지 않는 버전이 있으면 일반 번역만 적용하고 모드 파일은 보존합니다. [릴리스 안내](docs/RELEASE_1.0.0-beta.1.md)를 참고하세요.

### 테스트 환경

| 상태 | 컴퓨터 | 실행 환경 |
| --- | --- | --- |
| 실험용 / 일부 테스트 | Mac mini, Apple M4, 메모리 32 GB | macOS 26.5.2; CrossOver 26.3; CrossOver 안의 Windows용 Steam |
| 설치 프로그램 검증 완료 | 삼성 갤럭시 북 Pro2 360, Intel Core i5-1240P | Windows 11; Steam |
| 테스트 예정 | 동일한 삼성 갤럭시 북 Pro2 360, Intel Core i5-1240P | Fedora 44 Linux; Steam / Proton 테스트 예정 |

위 목록은 제작자가 사용한 테스트 환경이며, 최소 사양이나 전체 플레이 검증을 의미하지 않습니다. CrossOver에서는 일부 실제 게임 화면에서 영어 표시를 확인했습니다. Windows 패치 프로그램은 별도로 복사한 게임 파일에 설치·복원하는 테스트를 진행했습니다. Linux 설치 프로그램은 Debian 12 x86-64 에뮬레이션 환경에서 검증했으며, Fedora 44 실기기 및 Proton 플레이 테스트는 아직 예정입니다.

### Windows에서 게임 폴더 찾기

Steam 기본 설치 경로를 사용했다면 보통 다음 폴더에 있습니다.

```text
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered
```

다른 위치에 설치했다면 Steam 라이브러리에서 게임을 우클릭하고 **관리 → 로컬 파일 탐색**을 선택하세요. 탐색기의 폴더 주소를 패치 프로그램에 붙여 넣거나 **Browse**로 선택하세요. `ZephyrRemastered.exe`가 들어 있는 폴더를 선택해야 합니다. 게임을 종료한 뒤 **Check Files → Install English** 순서로 누르고 대상 폴더를 확인하세요. 첫 테스트는 별도로 복사한 게임 폴더에서 진행하세요.

### 의견 보내기 및 크레딧

번역 수정을 제안할 때는 한국어 원문 또는 스크린샷, 해당 장면이나 메뉴, 제안하는 영어 표현을 함께 알려 주세요. 검토용 파일을 사용한다면 검토 번호도 적어 주세요.

- [영어 포크에 이슈 남기기](https://github.com/mdbkkorea/zephyr-remastered-en/issues)
- [원본 중국어 번역 프로젝트](https://github.com/wanjizheng/zephyr-remastered-zh-cn)
- [Steam 게임 페이지](https://store.steampowered.com/app/5099430/)

원본 프로젝트의 라이선스와 기여자 표기는 유지합니다. 도구의 라이선스가 게임·그림·스토리에 대한 권리를 부여하는 것은 아니며, 해당 권리는 각 권리자에게 있습니다. 이 프로젝트는 비공식 팬 프로젝트입니다.

### Geyshir naming note / 게이시르 표기 참고

According to the naming history supplied by the user, the original games officially used **Gayshir**, and the company later changed it to **Geyshir** because the earlier spelling could be misleading. This project follows **Geyshir / Geyshir Empire**. The historical explanation is user-provided and has not been independently verified here.

사용자가 제공한 표기 이력에 따르면, 원작에서는 **Gayshir**를 공식 표기로 사용했으나 오해의 소지가 있어 이후 회사가 **Geyshir**로 변경했다고 합니다. 이 프로젝트는 **Geyshir / Geyshir Empire**를 사용합니다. 해당 변경 경위는 사용자 제공 정보이며 별도로 검증하지 않았습니다.
