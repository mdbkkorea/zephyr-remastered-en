#!/bin/bash
# Keep this file beside ZephyrEnglishPatcher.app. No separate Python needed.
set -euo pipefail
TASK_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TASK_APP="$TASK_DIR/ZephyrEnglishPatcher.app/Contents/MacOS/ZephyrEnglishPatcher"
if [[ "$(uname -s)" != Darwin || ! -x "$TASK_APP" ]]; then
    printf '%s\n' 'Extract the complete Mac release. Keep this command beside ZephyrEnglishPatcher.app.'
    read -r -p 'Press Return to close. ' TASK_REPLY || true
    exit 1
fi
if [[ "$("$TASK_APP" --crossover-launcher-version 2>/dev/null || true)" != 1 ]]; then
    printf '%s\n' 'This patcher app is too old for the CrossOver launcher.' \
      'Download and extract the matching Mac package, including BOTH the app and command file.' \
      'Copying only this command beside the beta.3 app will not work.'
    read -r -p 'Press Return to close. ' TASK_REPLY || true
    exit 1
fi
exec "$TASK_APP" --launch-crossover
