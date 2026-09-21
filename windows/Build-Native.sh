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
else
  .native-venv/bin/python -m PyInstaller --noconfirm --clean --onefile --name ZephyrEnglishPatcher --add-data 'payload:payload' --add-data 'licenses:licenses' --add-data 'LICENSE:.' english_app.py
  echo "Built dist/ZephyrEnglishPatcher for this Linux architecture and glibc baseline."
fi
