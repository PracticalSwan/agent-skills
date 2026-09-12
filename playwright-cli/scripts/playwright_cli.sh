#!/usr/bin/env bash
set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  echo "Error: Node.js is required to run @playwright/cli; add node to PATH or use the native Windows command." >&2
  exit 1
fi

has_session_flag="false"
for arg in "$@"; do
  case "$arg" in
    --session|--session=*|-s|-s=*)
      has_session_flag="true"
      break
      ;;
  esac
done

if command -v playwright-cli >/dev/null 2>&1; then
  # Prefer the verified global CLI when it is available. This avoids a
  # network-backed npx resolution on every command while retaining the
  # package fallback for clean environments.
  cmd=(playwright-cli)
else
  if ! command -v npx >/dev/null 2>&1; then
    echo "Error: npx is required for the @playwright/cli fallback but was not found on PATH." >&2
    exit 1
  fi
  cmd=(npx --yes --package @playwright/cli@latest playwright-cli)
fi
if [[ "${has_session_flag}" != "true" && -n "${PLAYWRIGHT_CLI_SESSION:-}" ]]; then
  cmd+=("-s=${PLAYWRIGHT_CLI_SESSION}")
fi
cmd+=("$@")

exec "${cmd[@]}"
