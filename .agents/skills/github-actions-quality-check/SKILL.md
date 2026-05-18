---
name: github-actions-quality-check
description: >-
  Quality-check GitHub Actions workflows, composite actions, action pinning,
  runner labels, permissions, triggers, concurrency, secrets, and CI linting
  changes. Use when creating, editing, reviewing, or documenting GitHub Actions
  automation.
---

# GitHub Actions Quality Check

## When to Use

- Use this skill when work touches `.github/workflows/`, `.github/actions/`,
  action pinning, runner labels, workflow permissions, triggers, concurrency,
  repository variables, repository secrets, or CI linting policy.
- Use it with `security-check` for third-party actions, downloaded tools,
  secrets, tokens, permissions, publishing, containers, or other supply-chain
  sensitive changes.
- Use `document-quality-check` when updating contributor-facing workflow
  guidance or pull request notes.

## Goals

- Keep workflows readable, deterministic, least-privilege, and reviewable.
- Catch workflow syntax, expression, runner-label, and composite-action metadata
  mistakes before CI runs.
- Keep third-party actions and reusable workflows pinned to full commit SHAs
  with accurate version comments.
- Prefer checks that do not add unnecessary runtime dependencies.
- Record verification clearly, including any local/CI difference.

## Workflow

1. Inspect the changed workflow or action files and the repository guidance that
   documents them.
2. Check triggers, branch filters, merge queue behavior, and `workflow_dispatch`
   coverage against the intended repository responsibility.
3. Check `permissions` at workflow and job scope. Prefer `contents: read` unless
   a job needs broader access, and document any write permission.
4. Check concurrency groups and cancellation rules for PRs, pushes, releases,
   merge queues, and publishing jobs.
5. Check runner labels and local composite actions. Add or update
   `.github/actionlint.yaml` only for deliberate labels or variables that
   actionlint cannot infer.
6. Run actionlint for workflow and action metadata validation. Match the
   repository's documented command; when optional integrations would add
   dependencies, disable them explicitly and note the reduced scope. Revisit
   pyflakes disablement when Python scripts exist in the repository.
7. Run ShellCheck for standalone shell scripts discovered in the changed
   automation scope, and keep actionlint's ShellCheck integration enabled when
   the repository installs ShellCheck.
8. Run pinact in check mode for action and reusable-workflow pins. Use
   `GITHUB_TOKEN` when available so API calls use authenticated rate limits.
9. For new or updated external actions, downloaded tools, or containers, apply
   `security-check`: verify release age, provenance, pinning, permissions, and
   runtime behavior before adopting the artifact.
10. Re-read comments near non-obvious versions, runner choices, cache paths,
   suppressions, and install commands. Keep comments specific and actionable.
11. Summarize verification by category: actionlint, ShellCheck, pinact, other
    automated checks, AI-assisted inspection, and any skipped checks with
    concrete blockers.

## Command Examples

Use these examples only when they match the repository's documented tooling.
Discover shell files from the current repository instead of copying a
repository-specific path from this skill.

```bash
actionlint -pyflakes=
mapfile -t shell_files < <(rg --files -g '*.sh' -g '*.bash' .github)
if ((${#shell_files[@]})); then
  shellcheck "${shell_files[@]}"
fi
pinact run --check --min-age 7
```

If no shell files are present, rely on actionlint's inline script checks and
record that the standalone ShellCheck pass had no targets.

When updating action pins, keep the cooldown in the command:

```bash
pinact run --update --min-age 7
```

## Review Checklist

- Workflow syntax and expressions were checked with actionlint.
- Inline workflow shell scripts and standalone shell scripts were checked with
  ShellCheck.
- Third-party actions and reusable workflows were checked with pinact.
- New executable artifacts satisfy the repository cooldown and pinning policy.
- Permissions and secrets are least-privilege and documented when unusual.
- Runner labels, variables, and suppressions are configured intentionally.
- Local documentation and CI behavior describe the same quality checks.
