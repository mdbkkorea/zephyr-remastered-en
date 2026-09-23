# Zephyr English 1.0.0-beta.4

## What's new

- Portable Mac launcher included beside the matching patcher app. It finds common
  CrossOver installations, lets you choose a bottle/game folder, remembers choices,
  and supplies the `winhttp=n,b` override needed by installed mods.
- Clear compatibility message when the command is accidentally paired with an older app.
- English/Korean Mac first-run and save-name-copy instructions, including Apple's
  official Privacy & Security instructions for this unnotarized app.
- **Mac patcher and launcher tested by the maintainer:** Mac mini (2024), Apple M4,
  32 GB RAM, macOS Tahoe 26.5.2, CrossOver 26.3 / Windows Steam. English gameplay
  and the translated Fullmap overlay confirmed. Other Mac configurations are not verified.

Translation payload is unchanged from beta.3: reviewed terminology, full battle
commands, 2.5× dialogue reveal and smaller Auto-Advance label are retained.
**If beta.3 is already installed, no repatching is required to use the new launcher.**
Keep your old patcher and backups for restoration. For older/different translations,
restore using the old patcher first. Close the game before installing or restoring.

## Files

- **Zephyr-English-1.0.0-beta.4-macos-arm64.zip** — Apple Silicon / Steam CrossOver.
  Extract everything together. First open the patcher app to approve it, then use
  **Launch-Zephyr-CrossOver.command** for playing with mods. No separate Python needed.
  See **MAC-GUIDE.md** inside the ZIP.
- **ZSteam-b4.zip** — Windows Steam build kit.
- **ZPurple-b4.zip** — Windows PURPLE build kit, experimental, standard translation only.
- **Zephyr-English-1.0.0-beta.4-linux-x64.tar.gz** — Linux x64 / glibc 2.36+ patcher.
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

beta.4에는 휴대용 CrossOver 실행기와 첫 실행 안내가 포함됩니다. 앱과 명령 파일을
같은 ZIP에서 함께 풀어 사용하세요. **Mac mini (2024), M4, 32GB, macOS Tahoe 26.5.2,
CrossOver 26.3 / Windows Steam**에서 제작자가 테스트했고 영어 Fullmap 표시를 확인했습니다.

Apple 공증이 없는 앱이므로 첫 실행 시 개발자 확인 불가로 차단될 수 있습니다.
완료/취소를 누른 뒤 **시스템 설정 → 개인정보 보호 및 보안 → 확인 없이 열기**로
실행하세요. 자세한 설명은 ZIP의 **MAC-GUIDE.md**에 있습니다.

beta.3와 번역 데이터가 같으므로 이미 설치했다면 다시 패치할 필요 없이 새 실행기를
사용하면 됩니다. Windows는 **ZSteam-b4.zip / ZPurple-b4.zip**을 구분해 C:\Zephyr에
풀고 Python 3.12 64비트 설치 후 Build-Windows.cmd를 실행하세요. Windows EXE 빌드 및
실기기 검증은 사용자 진행 예정이며 Linux / Proton 게임 테스트도 아직 예정입니다.
