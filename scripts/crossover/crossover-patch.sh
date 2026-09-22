#!/bin/bash
# Companion to the bundled, version-pinned native Mac patcher. No Python needed.
set -euo pipefail
TASK_SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TASK_ACTION="${1:-}"
shift || true
TASK_GAME="$HOME/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/The Rhapsody of Zephyr Remastered"
TASK_CHECK=0
TASK_STATE_ARGS=(--state-home "$HOME/Library/Application Support/ZephyrEnglishPatcher")
finish() {
    TASK_EXIT=$?
    if [[ -t 0 ]]; then
        printf '\nPress Return to close this window. '
        read -r TASK_UNUSED || true
    fi
    exit "$TASK_EXIT"
}
trap finish EXIT
fail() { printf '\n%s\n' "$*" >&2; exit 1; }
case "$TASK_ACTION" in install|restore) ;; *) fail 'Use the Apply or Restore command file.' ;; esac
while [[ $# -gt 0 ]]; do
    case "$1" in
        --game) [[ $# -ge 2 ]] || fail '--game requires the game folder.'; TASK_GAME="$2"; shift 2 ;;
        --check) TASK_CHECK=1; shift ;;
        --state-home) [[ $# -ge 2 ]] || fail "--state-home requires a backup folder."; TASK_STATE_ARGS=(--state-home "$2"); shift 2 ;;
        *) fail 'Supported options: --check, --game "/path/to/game"' ;;
    esac
done
[[ "$(uname -s)" == Darwin ]] || fail 'This package is for macOS.'
[[ "$(uname -m)" == arm64 ]] || fail 'This package requires an Apple Silicon Mac. Use a native Intel build on an Intel Mac.'
TASK_PATCHER="$TASK_SCRIPT_DIR/ZephyrEnglishPatcher.app/Contents/MacOS/ZephyrEnglishPatcher"
[[ -x "$TASK_PATCHER" ]] || fail 'Keep the scripts and ZephyrEnglishPatcher.app together. Extract the complete ZIP to your Mac first.'
[[ -f "$TASK_GAME/ZephyrRemastered.exe" ]] || fail "Game not found at: $TASK_GAME
For a different bottle or Steam library, run this command with --game followed by the quoted game folder."
printf '\nZephyrPassives 2.4.3 English translation — CrossOver Steam\nGame: %s\n' "$TASK_GAME"
# Restore checks both backups and dependencies; keep the mod installed until restored.
if [[ "$TASK_ACTION" == install ]]; then
    TASK_PLUGIN="$TASK_GAME/BepInEx/plugins/ZephyrPassives/ZephyrPassives.dll"
    [[ -f "$TASK_PLUGIN" ]] || fail 'Install the original ZephyrPassives 2.4.3 mod in this game folder first. This script applies its English translation only.'
    TASK_HASH="$(/usr/bin/shasum -a 256 "$TASK_PLUGIN")"
    [[ "${TASK_HASH%% *}" == c22a790200042a1385e896b20938c89a31e542bcfe919de324959a9cdbdbf0c2 ]] || fail 'ZephyrPassives.dll does not match version 2.4.3 supported by this translation.'
fi
"$TASK_PATCHER" status --game "$TASK_GAME" "${TASK_STATE_ARGS[@]}"
if [[ "$TASK_CHECK" == 1 ]]; then
    printf '\nRead-only check complete. No patch was applied.\n'
    exit 0
fi
printf '\nClose Zephyr Remastered before continuing.\n'
if [[ "$TASK_ACTION" == install ]]; then
    printf 'This applies the full English translation plus mod-specific descriptions.\nVerified original files are backed up automatically. Saves and mod files are unchanged.\nType APPLY and press Return: '
    TASK_EXPECTED=APPLY
else
    printf 'This restores game resources from the patcher backup. The mod stays installed.\nType RESTORE and press Return: '
    TASK_EXPECTED=RESTORE
fi
read -r TASK_REPLY || fail 'Cancelled.'
[[ "$TASK_REPLY" == "$TASK_EXPECTED" ]] || fail 'Cancelled; no patch operation started.'
"$TASK_PATCHER" "$TASK_ACTION" --game "$TASK_GAME" "${TASK_STATE_ARGS[@]}" || fail 'Operation stopped. See the error above. For an older unmanaged English patch, restore it with its original tool before retrying. Do not manually replace unknown files.'
printf '\nOperation completed successfully.\n'
if [[ "$TASK_ACTION" == install ]]; then
    printf 'Launch the game normally from Steam in CrossOver.\nMod loading must already be configured; this script does not change CrossOver settings.\n'
fi
