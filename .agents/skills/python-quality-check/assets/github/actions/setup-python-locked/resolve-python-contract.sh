#!/usr/bin/env bash

set -euo pipefail

main() {
  : "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

  local -a versions
  mapfile -t versions <.python-version
  local python_version=${versions[0]:-}
  python_version=${python_version%$'\r'}
  if [[ ${#versions[@]} -ne 1 || -z "$python_version" ]]; then
    printf '.python-version must select one Python version.\n' >&2
    return 1
  fi

  {
    printf 'python_version=%s\n' "$python_version"
    printf 'uv_version=0.12.3\n'
  } >>"$GITHUB_OUTPUT"
}

main "$@"
