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
  TASK_BUILD_NAME="$(.native-venv/bin/python english_version.py macos)"
  .native-venv/bin/python -m PyInstaller --noconfirm --clean --onedir --windowed --name "$TASK_BUILD_NAME" --osx-bundle-identifier org.zephyrenglish.patcher --add-data 'payload:payload' --add-data 'licenses:licenses' --add-data 'LICENSE:.' english_app.py
  echo "Built dist/$TASK_BUILD_NAME.app (host architecture). Not notarized."
  # Produce a complete Mac archive so the portable launcher cannot be omitted.
  cp Launch-Zephyr-CrossOver.command dist/
  chmod +x dist/Launch-Zephyr-CrossOver.command
  TASK_PACKAGE="$(mktemp -d "$PWD/build/mac-release.XXXXXX")"
  ditto "dist/$TASK_BUILD_NAME.app" "$TASK_PACKAGE/$TASK_BUILD_NAME.app"
  cp dist/Launch-Zephyr-CrossOver.command README-NATIVE.md MAC-GUIDE.md LICENSE "$TASK_PACKAGE/"
  ditto -c -k --sequesterRsrc "$TASK_PACKAGE" "dist/$TASK_BUILD_NAME.zip"
  echo "Mac ZIP includes the app, portable CrossOver launcher and instructions."
else
  TASK_BUILD_NAME="$(.native-venv/bin/python english_version.py linux)"
  .native-venv/bin/python -m PyInstaller --noconfirm --clean --onefile --name "$TASK_BUILD_NAME" --add-data 'payload:payload' --add-data 'licenses:licenses' --add-data 'LICENSE:.' english_app.py
  echo "Built dist/$TASK_BUILD_NAME for this Linux architecture and glibc baseline."
fi
