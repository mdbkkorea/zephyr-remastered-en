# Mac patcher and CrossOver launcher

## Tested Mac

The maintainer tested the Mac patcher and portable launcher on a **Mac mini (2024),
Apple M4, 32 GB RAM, macOS Tahoe 26.5.2, CrossOver 26.3**, with Windows Steam.
The user confirmed English gameplay and the translated Fullmap overlay. This is
testing on that setup, not certification for every Mac or a complete story review.
The downloadable Mac app targets Apple Silicon. Intel Macs are not tested.

## First opening: Apple security message

This fan-made app is **not notarized by Apple** and does not have a Developer ID
signature. macOS may block its first opening. It is not an Apple-authorized app.

For an unidentified-developer / “Apple cannot check” warning on the trusted package:

1. Extract the whole ZIP and try opening **ZephyrEnglishPatcher.app** once.
2. Choose **Done** or **Cancel**, not **Move to Trash**.
3. Open **System Settings → Privacy & Security**, scroll down to **Security**, and
   select **Open Anyway** for this app.
4. Authenticate if asked, then select **Open** in the confirmation.

Apple saves this exception for later launches. This procedure is for the
unidentified-developer warning; a “will damage your computer” or “damaged” alert
is a different problem. Do not disable Gatekeeper globally.
Source: [Apple — Safely open apps on your Mac](https://support.apple.com/en-us/102445).

## Install and play

Close the game. In the patcher, select the folder containing **ZephyrRemastered.exe**,
then use **Check Files → Install English**. For the default Steam bottle, Browse
starts near `~/Library/Application Support/CrossOver/Bottles/Steam/drive_c/`.
Finder hides your user Library: **Command–Shift–G** lets you paste this path directly.

Keep **Launch-Zephyr-CrossOver.command** beside the matching app from the same ZIP.
Open the command, check the detected CrossOver app, bottle and game folder, and
click **Launch game**. You can browse or type custom paths. Selections are remembered.
Keep Steam running in that bottle and close other Zephyr copies first.
Clear the Proton-style `WINEDLLOVERRIDES=... %command%` text from Steam launch options.
The launcher supplies `--dll 'winhttp=n,b'` directly to CrossOver for installed mods.
No separate Python is required. Older beta.3 apps do not support this command.

Install original mods separately. The Steam translation supports **ZephyrPassives
2.4.3** and **ZephyrFullmap 1.8.0**; unsupported versions receive standard translation
without changing mod files. This launcher is tested for Steam, not PURPLE.

Beta.5 includes new translation corrections. Restore originals using your previous
patcher, then install beta.5 to apply them.
Keep existing backups and the older patcher for restoration.

## Optional save-name copies

Use this only if old saves still show Korean character names or job titles.
Choose the save folder, then a separate output location such as Desktop. The tool
creates converted copies and leaves active saves untouched. Close the game and
back up the originals before manually replacing matching `.dat` files. Do not
overwrite newer progress with an older converted copy.

For the usual Steam bottle, saves are beneath:

```text
~/Library/Application Support/CrossOver/Bottles/Steam/drive_c/users/crossover/AppData/LocalLow/Nine Circles Corporation/ZephyrRemastered/Steam/<Steam account ID>/
```

Launcher settings and diagnostics are in
`~/Library/Application Support/ZephyrEnglishPatcher/` (`crossover-launcher.json`
and `crossover-launch.log`).

## 한국어

**Mac mini (2024), Apple M4, RAM 32GB, macOS Tahoe 26.5.2, CrossOver 26.3의 Windows
Steam**에서 제작자가 Mac 패치 프로그램과 실행기를 테스트했습니다. 영어 게임 화면과
Fullmap 지도 표시를 확인했습니다. 모든 Mac이나 게임 전체 구간을 검증한 것은 아닙니다.

Apple 공증 및 Developer ID 서명이 없는 앱이므로 처음 실행할 때 차단될 수 있습니다.
신뢰하는 배포 파일에서 개발자 확인 불가 경고가 나오면 **완료/취소**를 누르고
휴지통으로 옮기지 마세요. **시스템 설정 → 개인정보 보호 및 보안 → 보안 → 확인 없이
열기(Open Anyway)**를 선택하고 인증 후 **열기**를 누르세요.
[Apple 공식 안내](https://support.apple.com/ko-kr/102445)를 참고하세요.

ZIP 전체를 풀고 앱과 실행 명령 파일을 함께 보관하세요. 같은 보틀에서 Steam을 켠 뒤
**Launch-Zephyr-CrossOver.command**를 열어 경로를 확인하고 **Launch game**을 누릅니다.
Python 설치는 필요 없습니다. 기존 beta.3 앱에 명령 파일만 복사하면 작동하지 않습니다.
beta.5의 새 번역 수정을 적용하려면 이전 패치 프로그램으로 원본을 복원한 후 beta.5를 설치하세요.
