# Zephyr English 1.0.0-beta.5

## What's new

- Latest eight reviewed dialogue corrections remove ten unnecessary forced line breaks.
- Closing passage wording and line wrapping corrected, including “doesn't another life remain?”
- Compact **Own** shop quantity label to avoid wrapping at two-digit quantities.
- User accepted the latest Mac playtest. Existing 2.5× dialogue reveal, full battle commands,
  smaller Auto-Advance label and portable CrossOver launcher are retained.
- Shorter archive names; Windows kits keep short ZSteam/ZPurple folders inside.

**Upgrade:** close the game, restore originals with your previous patcher, then install beta.5.
Keep the old patcher and backups until the upgrade is complete. This release changes translation data.

## Files

- **zephyr_english_macos_1.0.0_beta05.zip** — Apple Silicon / Steam CrossOver.
  Extract everything together. First open the patcher app to approve it, then use
  **Launch-Zephyr-CrossOver.command** for playing with mods. No separate Python needed.
  See **MAC-GUIDE.md** inside the ZIP.
- **zephyr_english_windows_steam_1.0.0_beta05.zip** — Windows Steam build kit.
- **zephyr_english_windows_purple_1.0.0_beta05.zip** — Windows PURPLE build kit, experimental, standard translation only.
- **zephyr_english_linux_1.0.0_beta05.tar.gz** — Linux x64 / glibc 2.36+ patcher.
  Fedora 44 / Proton gameplay testing is pending.

For Windows, install **Python 3.12 64-bit with Python Launcher**, extract the complete
kit to **C:\Zephyr**, and run **Build-Windows.cmd** inside ZSteam or ZPurple. Output:
**dist\ZephyrEnglishPatcher.exe**. Keep the editions separate; Git isn't required.
Windows EXEs are not included and must be built/tested on Windows. The previous
Windows installer was tested on Galaxy Book Pro2 360, i5-1240P, Windows 11 / Steam.
Protected Program Files installations may require running the built EXE as administrator.
The build itself does not require elevation. PURPLE default:
`C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`.

Steam supports ZephyrPassives **2.4.3** and ZephyrFullmap **1.8.0**, installed separately.
Unsupported versions receive standard translation and their mod files are preserved.
Linux/Proton Steam launch option: `WINEDLLOVERRIDES="winhttp=n,b" %command%`.
On Mac use the included launcher instead. PURPLE mod compatibility remains unverified.

## Mac first opening

This app is not notarized by Apple. For a trusted download blocked as an unidentified
developer, first try opening the app, choose **Done/Cancel** (not Move to Trash),
then **System Settings → Privacy & Security → Open Anyway**, authenticate if asked,
and confirm **Open**. See [Apple's official instructions](https://support.apple.com/en-us/102445).

## 한국어

beta.5에는 최근 검토한 대사 줄바꿈 수정, 문법 수정과 상점 수량 표시 **Own**이 포함됩니다.
Mac 테스트 버전은 사용자가 확인했습니다. 기존 2.5배 대사 표시 속도, 작은 Auto-Advance 글꼴,
휴대용 CrossOver 실행기를 유지합니다. 이전 패치 프로그램으로 원본을 복원한 후 beta.5를 설치하세요.
Windows Steam/PURPLE 빌드 키트는 별도이며 Python 3.12 64비트로 직접 빌드해야 합니다.
Linux / Proton 실기기 게임 테스트는 아직 예정입니다.
