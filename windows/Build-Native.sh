#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
PYTHON="${ZEPHYR_PYTHON:-python3}"
"$PYTHON" -c 'import sys,tkinter; assert sys.version_info >= (3,9), "Python 3.9+ required"; assert sys.platform != "darwin" or tkinter.TkVersion >= 8.6, "Use Python with Tk 8.6+ on macOS"'
"$PYTHON" -m venv .native-venv
.native-venv/bin/python -m pip install 'pyinstaller==6.22.3'
.native-venv/bin/python -m unittest discover -s tests
export PYINSTALLER_CONFIG_DIR="$PWD/.pyinstaller-cache"
if [ "$(uname -s)" = Darwin ]; then
  .native-venv/bin/python -m PyInstaller --noconfirm --clean --onedir --windowed --name ZephyrEnglishPatcher --osx-bundle-identifier org.zephyrenglish.patcher --add-data 'payload:payload' --add-data 'licenses:licenses' --add-data 'LICENSE:.' english_app.py
  echo "Built dist/ZephyrEnglishPatcher.app (host architecture). Not notarized."
  # Produce a complete Mac archive so the portable launcher cannot be omitted.
  cp Launch-Zephyr-CrossOver.command dist/
  chmod +x dist/Launch-Zephyr-CrossOver.command
  TASK_PACKAGE="$(mktemp -d "$PWD/build/mac-release.XXXXXX")"
  ditto dist/ZephyrEnglishPatcher.app "$TASK_PACKAGE/ZephyrEnglishPatcher.app"
  cp dist/Launch-Zephyr-CrossOver.command README-NATIVE.md MAC-GUIDE.md LICENSE "$TASK_PACKAGE/"
  TASK_VERSION="$(.native-venv/bin/python -c 'from english_version import VERSION; print(VERSION)')"
  TASK_ARCHIVE_VERSION="$(.native-venv/bin/python -c 'import sys; v,b=sys.argv[1].split("-beta."); print(f"{v}_beta{int(b):02d}")' "$TASK_VERSION")"
  ditto -c -k --sequesterRsrc "$TASK_PACKAGE" "dist/zephyr_english_macos_${TASK_ARCHIVE_VERSION}.zip"
  echo "Mac ZIP includes the app, portable CrossOver launcher and instructions."
else
  .native-venv/bin/python -m PyInstaller --noconfirm --clean --onefile --name ZephyrEnglishPatcher --add-data 'payload:payload' --add-data 'licenses:licenses' --add-data 'LICENSE:.' english_app.py
  echo "Built dist/ZephyrEnglishPatcher for this Linux architecture and glibc baseline."
fi
