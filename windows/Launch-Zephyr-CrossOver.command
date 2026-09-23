#!/bin/bash
# Keep this file beside the matching Mac patcher app. No separate Python needed.
set -euo pipefail
TASK_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
shopt -s nullglob
TASK_CANDIDATES=()
for TASK_BUNDLE in "$TASK_DIR"/ZEnglishMacos_*.app "$TASK_DIR"/ZephyrEnglishPatcher.app; do
    TASK_NAME="$(basename "$TASK_BUNDLE" .app)"
    if [[ -x "$TASK_BUNDLE/Contents/MacOS/$TASK_NAME" ]]; then
        TASK_CANDIDATES+=("$TASK_BUNDLE/Contents/MacOS/$TASK_NAME")
    fi
done
if [[ "$(uname -s)" != Darwin || ${#TASK_CANDIDATES[@]} != 1 ]]; then
    printf '%s\n' 'Extract the complete Mac release into its own folder. Keep exactly one patcher app beside this command.'
    read -r -p 'Press Return to close. ' TASK_REPLY || true
    exit 1
fi
TASK_APP="${TASK_CANDIDATES[0]}"
if [[ "$("$TASK_APP" --crossover-launcher-version 2>/dev/null || true)" != 1 ]]; then
    printf '%s\n' 'This patcher app is too old for the CrossOver launcher.' \
      'Download and extract the matching Mac package, including BOTH the app and command file.' \
      'Copying only this command beside the beta.3 app will not work.'
    read -r -p 'Press Return to close. ' TASK_REPLY || true
    exit 1
fi
exec "$TASK_APP" --launch-crossover
