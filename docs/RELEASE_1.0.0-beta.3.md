# Zephyr English 1.0.0-beta.3

Korean-based English translation for The Rhapsody of Zephyr Remastered. This is a prerelease.

## Changes

- Updated terminology: Geysir, Blade Shot (탄검), Killing Blade (살검), Asura's Void Edge (진공수라인), Demonic Gale Strike, Asura Heavensbane and Veritas Asura Heavensbane.
- Full multiword battle commands, including Weak Slash and Strong Slash, display together.
- Reviewed Silver dialogue, she/her corrections and five manual line-break adjustments.
- **Dialogue reveals 2.5× faster than the original: 28 ms per character instead of 70 ms.** Voice playback speed and scripted pauses are unchanged.
- Full **Auto-Advance** button label retained, with its font reduced from 22 to 16 to fit the background.
- Short Windows build ZIP paths avoid the previously reported Explorer path-length error. All dependency license notices remain included.

## Downloads and Windows builds

Steam and PURPLE use **separate packages**. Choose the correct edition.

- **ZSteam-b3.zip**: Windows Steam build kit.
- **ZPurple-b3.zip**: Windows PURPLE build kit; experimental.
- **Zephyr-English-1.0.0-beta.3-macos-arm64.zip**: experimental Steam patcher for Apple Silicon / CrossOver.
- **Zephyr-English-1.0.0-beta.3-linux-x64.tar.gz**: experimental Steam patcher for Linux / Proton; glibc 2.36 or newer.

For Windows, install **Python 3.12 (64-bit), including the Python launcher**. Extract the entire appropriate ZIP into **C:\Zephyr**, open `ZSteam` or `ZPurple`, then double-click **Build-Windows.cmd**. Internet is required to install the build dependency. Git is not needed. The result is **dist\ZephyrEnglishPatcher.exe**. Build both kits separately; both executables have the same filename, so keep their edition folders distinct. GitHub's automatic Source code ZIP does not contain the generated patch payload.

Building does not require administrator privileges. If installing into `C:\Program Files (x86)` gives Permission denied / Errno 13, close the patcher and run the resulting EXE as administrator. PURPLE's usual folder is `C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`.

For an existing English patch, **restore using the old patcher's Restore Original first**, then install beta.3. Keep the old patcher and backups until restoration succeeds. Close the game before patching. For first testing, use a separate game copy. Check Files → Install English; test Restore Original too. Saves are unchanged.

Steam packages detect **ZephyrPassives 2.4.3** and **ZephyrFullmap 1.8.0**. Supported mods receive compatible translations; unsupported versions select standard translation and preserve mod files. Mods must be installed separately. PURPLE contains standard translation only; compatibility with these mods is unverified.

With user mods, CrossOver needs `--dll 'winhttp=n,b'`; Proton Steam launch options need `WINEDLLOVERRIDES="winhttp=n,b" %command%`.

## Validation and limits

The previous Windows release has completed Windows installer testing. **Beta.3 Windows EXEs must still be built and tested by the maintainer; these downloads are build kits.** The Mac Steam playtest's dialogue changes, 2.5× speed and Auto-Advance layout were accepted by the user. macOS and Linux installers remain experimental; Fedora 44 / Proton gameplay testing is pending. PURPLE's 2.5× reveal change is hash-locked to its separate binary and remains unverified in gameplay.

Build checks cover 22,403 resource translations, 30 metadata edits, reviewed layout overrides and binary version checks. Installer validation covers install/reinstall/exact restoration, supported-mod selection, unsupported fallback and wrong-edition rejection on isolated copies. This is not a complete story or screen review. Verify archive SHA256 values using SHA256SUMS.txt.

## 한국어

한국어 원문 기반 영어 번역의 beta.3 사전 배포판입니다. 탄검은 **Blade Shot**, 살검은 **Killing Blade**, 진공수라인은 **Asura's Void Edge**로 표시합니다. 검토한 대사와 전체 전투 명령 이름을 반영했습니다.

**대사 표시 속도는 원본의 2.5배(글자당 70ms → 28ms)**입니다. 음성 속도와 연출용 대기 시간은 유지합니다. **Auto-Advance** 이름은 유지하고 버튼 글꼴 크기를 22에서 16으로 줄였습니다.

Windows는 Steam용 **ZSteam-b3.zip**, PURPLE용 **ZPurple-b3.zip**을 구분해 사용하세요. **Python 3.12 64비트와 Python launcher**를 설치하고, ZIP 전체를 **C:\Zephyr**에 푼 뒤 각 폴더의 **Build-Windows.cmd**를 실행하세요. 결과물은 **dist\ZephyrEnglishPatcher.exe**입니다. 두 파일의 이름이 같으므로 Steam/PURPLE 폴더를 구분해서 보관하세요. Git은 필요하지 않으며 GitHub의 Source code ZIP에는 패치 데이터가 없습니다.

기존 영어 패치는 **이전 패치 프로그램으로 Restore Original을 실행한 뒤** beta.3를 설치하세요. 빌드에 관리자 권한은 필요하지 않습니다. 설치 중 권한 오류가 나면 EXE를 관리자 권한으로 실행하세요. PURPLE 기본 경로는 `C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`입니다.

이전 Windows 배포판의 설치 프로그램 검증은 완료했지만, **beta.3 Windows EXE 빌드와 Windows 실기기 테스트는 아직 예정**입니다. Mac 플레이테스트의 변경 사항은 사용자 확인을 받았습니다. macOS/Linux 설치 프로그램 및 PURPLE 패키지는 실험용이며 Fedora 44 / Proton 게임 테스트는 아직 예정입니다. Steam의 지원 모드는 ZephyrPassives 2.4.3과 ZephyrFullmap 1.8.0입니다. 미지원 버전에서는 일반 번역만 적용하고 모드 파일은 보존합니다. PURPLE의 모드 호환성은 검증되지 않았습니다.
