#!/bin/bash
set -euo pipefail
TASK_SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
exec /bin/bash "$TASK_SCRIPT_DIR/crossover-patch.sh" restore "$@"
