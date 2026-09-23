#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is needed to run the review. Please contact your translation maintainer.'
  read -r -p 'Press Enter to close.'
  exit 1
fi
python3 ReviewService/launch.py
