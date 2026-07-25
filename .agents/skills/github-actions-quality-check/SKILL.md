---
name: github-actions-quality-check
description:
  Quality-check GitHub Actions workflows and composite actions. Use when creating, editing, reviewing, or documenting
  workflow triggers, permissions, runners, concurrency, action pins, secrets, or CI linting policy.
---

# GitHub Actions Quality Check

## Review automation changes

1. Inspect changed workflow or action files and the repository guidance that describes them.
2. Check triggers, branch filters, merge-queue behavior, and `workflow_dispatch` against the intended responsibility.
   Treat an established publication trigger and canonical version source as repository contracts: preserve them unless
   the requested change explicitly replaces them. Design workflow boundaries around events, privilege, and lifecycle
   rather than around command names:
   - A pull-request entry workflow validates untrusted proposed source and includes `merge_group` when a merge queue
     uses required checks.
   - An integration-branch entry workflow re-runs required source validation on the exact pushed commit. Use a read-only
     `plan` job only for canonical version or publication state, and make build and publication use direct `needs`
     dependencies rather than rediscovering that state.
   - Name jobs for their visible responsibility: use `lint`, optional `test`, optional `plan`, `build`, and `release`.
     Keep a reusable same-runner command sequence in a precisely named Composite Action such as `lint-source`; do not
     hide independent lint and test signals behind a broad `source-quality` job.
   - Do not emulate a direct dependency with API polling, an `await-quality` job, or an unrelated workflow that might
     still fail after publishing.
   - Do not add `workflow_dispatch` by default. Add it only for a documented diagnostic or recovery operation with a
     defined input, permission, artifact, and cancellation contract.
   - Use `workflow_run` only when its separate trust boundary is necessary and has been security-reviewed; it is not a
     routine substitute for same-commit `needs` gating.
3. Check workflow and job `permissions`. Start from `contents: read`, grant only required access, and document unusual
   write access.
4. Check concurrency groups and cancellation rules for PRs, pushes, releases, merge queues, and publishing.
5. Check runner labels, local composite actions, expressions, comments, cache paths, and suppressions. Read
   [runner-selection.md](references/runner-selection.md) when selecting or changing a GitHub-hosted runner. For
   compatibility-bearing jobs, use a versioned label for the oldest GitHub-supported GA image in the required
   OS/architecture family. Prefer `ubuntu-slim` only for measured lightweight jobs that have no native compatibility
   contract and fit its container, resource, software, and 15-minute limits. Use `*-latest` only when following GitHub's
   moving stable image is intentional rather than incidental. Record a recurring image-support review and migrate before
   a dated deprecation reaches its brownout or phased withdrawal period. Validate every action input against the
   documentation or metadata for the exact pinned action version; do not infer an input name from a different action,
   tool, or release. Add `.github/actionlint.yaml` only for deliberate labels or variables that actionlint cannot infer.
   Use a local Composite Action only for a stable sequence of steps that runs on the caller job's runner, such as locked
   setup or a repeated command bundle. Keep job ownership, runner choice, permissions, artifact boundaries, and release
   gates visible in the workflow. Prefer a local Composite Action for a same-runner shared quality sequence. Use a
   reusable workflow only when job-level matrix, outputs, or permission boundaries make a Composite Action insufficient,
   and document that reason; do not add `workflow_call` merely to avoid a small amount of workflow YAML.
6. Pin third-party actions and reusable workflows to complete commit SHAs with accurate version comments. For external
   actions, downloaded tools, or containers, use `security-check` to review provenance, release age, pinning,
   permissions, and runtime behavior.
7. Run the repository's documented `actionlint`, ShellCheck, and `pinact` checks. Use `pinact run --check --min-age 7`
   for pin verification and `GITHUB_TOKEN` when available. Check standalone changed automation shell scripts with
   ShellCheck; if no targets exist, record that scope.
8. Summarize actionlint, ShellCheck, pinact, other automated checks, AI-assisted inspections, and skipped checks
   separately. Record any reduced validation scope caused by unavailable optional integrations.

## Review publishing workflows

- Gate immutable publication on all required quality and build results for the exact source commit. A separately running
  check is not a gate unless repository rules or the publishing workflow demonstrably waits for its success.
- Retain the exact build artifact from integration-branch/edge builds in the workflow artifact store even when that
  version is not published. Record the artifact name, source commit, and digest, and make release jobs publish the
  verified build output rather than rebuilding.
- Derive tags, release identity, and artifacts from the repository's canonical version source. Bind newly created tags
  and resumable drafts to the reviewed source commit.
- Make retried automation idempotent. Define safe behavior for development placeholders, an already-published immutable
  version, and a matching mutable draft; fail on conflicting tags, drafts, or releases.
- Before treating an existing immutable release as a successful no-op, verify its exact expected assets and the
  attestations or provenance required by the repository's supported release contract. A rerun must not hide a failed
  post-publication verification.
- Keep validation read-only and isolate release credentials in the publishing job or protected environment. Use
  `security-check` for final-artifact and archive inspection.

## Review repository enforcement

- Compare required status-check contexts with the exact check names produced by current workflows. Check the
  integration-branch freshness policy and merge-queue compatibility when applicable.
- Verify release immutability, tag rules, Actions permissions, and protected environments from repository settings. If
  settings are inaccessible, report the corresponding readiness claim as unverified.

Use `prose-quality-check` for contributor-facing workflow guidance or PR notes. Keep workflows deterministic,
least-privilege, and reviewable without adding unnecessary runtime dependencies.
