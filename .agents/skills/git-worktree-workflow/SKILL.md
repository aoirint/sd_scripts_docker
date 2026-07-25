---
name: git-worktree-workflow
description:
  Set up and use an isolated Git worktree for repository implementation tasks. Use unless the user explicitly requests
  another workspace arrangement.
---

# Git Worktree Workflow

## Work in an isolated checkout

1. Inspect the repository state; treat uncommitted and untracked files in the original checkout as user work.
2. Fetch the requested base branch. Use `main` when no base is specified.
3. Create a short descriptive branch and worktree under `.agents/worktrees/`, for example:

    ```powershell
    git fetch origin main
    git worktree add -b <branch-name> .agents/worktrees/<branch-name> origin/main
    ```

4. Inspect an existing branch or path before reuse; choose a new name if it is not clearly the task workspace.
5. Make all implementation changes in the new worktree. Do not remove another worktree unless the user explicitly
   requests it.

## Implement and verify

1. Split the work into practical phases.
2. For each phase, implement the scoped change, run repository-appropriate formatting and verification, then commit it
   with `commit-message-quality-check`.
3. Before pushing, review the complete diff, recent commits, scope, and missing verification; run the final relevant
   checks.
4. Push and create or update the PR with `pull-request-quality-check` when requested.
5. Before a PR merge command performs local branch cleanup, check every active worktree. Do not let a hosted-PR CLI
   switch to the default branch or delete a branch when that branch is checked out by another worktree. Merge first;
   then perform any safe remote or local branch cleanup as a separate action.

Use documented builds, tests, linters, formatters, or structural validators appropriate to the change. State skipped
verification and its reason in the PR body. After a branch is pushed or attached to a PR, add follow-up commits rather
than rewriting history unless the user explicitly requests a rewrite.
