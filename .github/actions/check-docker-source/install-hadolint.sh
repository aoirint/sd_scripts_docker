#!/usr/bin/env bash

set -euo pipefail

main() {
  : "${HADOLINT_VERSION:?HADOLINT_VERSION is required}"
  : "${HADOLINT_SHA256:?HADOLINT_SHA256 is required}"
  : "${RUNNER_TEMP:?RUNNER_TEMP is required}"
  : "${GITHUB_PATH:?GITHUB_PATH is required}"

  local asset=hadolint-linux-x86_64
  local install_dir="${RUNNER_TEMP}/hadolint/bin"
  local download_path="${install_dir}/${asset}"
  mkdir -p "$install_dir"
  curl \
    --fail \
    --location \
    --show-error \
    --silent \
    --output "$download_path" \
    "https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/${asset}"
  printf '%s  %s\n' "$HADOLINT_SHA256" "$download_path" |
    sha256sum --check --strict
  mv "$download_path" "${install_dir}/hadolint"
  chmod 0755 "${install_dir}/hadolint"
  printf '%s\n' "$install_dir" >>"$GITHUB_PATH"
}

main "$@"
