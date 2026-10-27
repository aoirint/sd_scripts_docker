#!/usr/bin/env bash
# Keep APM-only maintenance on the validation path, without image publishing.
set -euo pipefail

[[ "${BEFORE_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || exit 1
[[ "${AFTER_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || exit 1
git cat-file -e "${BEFORE_SHA}^{commit}"
git cat-file -e "${AFTER_SHA}^{commit}"

changed_paths="$(mktemp)"
workflow_diff="$(mktemp)"
trap 'rm -f -- "$changed_paths" "$workflow_diff"' EXIT
git diff --no-renames --name-only -z "$BEFORE_SHA" "$AFTER_SHA" > "$changed_paths"

# A workflow can hold application inputs (for example image variants). Ignore
# only additions made by this scope gate; all other workflow edits still publish.
workflow_adds_only_scope_gate() {
  git diff --no-ext-diff --unified=0 "$BEFORE_SHA" "$AFTER_SHA" -- \
    .github/workflows/main.yml > "$workflow_diff" || return 1
  while IFS= read -r line; do
    case "$line" in
      'diff --git '*|'index '*|'--- '*|'+++ '*|'@@ '*) ;;
      -*) return 1 ;;
      +*)
        case "${line:1}" in
          ''|"      publish_application: \${{ steps.scope.outputs.publish_application }}"|\
          '          fetch-depth: 0'|'      - name: Classify application changes'|\
          '        id: scope'|'        env:'|\
          "          BEFORE_SHA: \${{ github.event.before }}"|\
          "          AFTER_SHA: \${{ github.sha }}"|\
          '        run: bash .github/scripts/application-change-scope.sh'|\
          '    # APM maintenance still runs Check; image publishing needs application changes.'|\
          "    if: needs.plan.outputs.publish_application == 'true'") ;;
          *) return 1 ;;
        esac
        ;;
      *) return 1 ;;
    esac
  done < "$workflow_diff"
}

publish_application=false
while IFS= read -r -d '' path; do
  case "$path" in
    .agents/skills/*|apm.yml|apm.lock.yaml|AGENTS.md|THIRD_PARTY_NOTICES.md|\
    .github/actions/check-docker-source/action.yml|\
    .github/scripts/application-change-scope.sh|docs/operations/publish-images.md)
      ;;
    .github/workflows/main.yml)
      workflow_adds_only_scope_gate || publish_application=true
      ;;
    *) publish_application=true ;;
  esac
done < "$changed_paths"

printf 'publish_application=%s\n' "$publish_application" >> "$GITHUB_OUTPUT"
