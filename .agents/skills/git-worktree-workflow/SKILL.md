---
name: git-worktree-workflow
description: Use Git worktrees for repository implementation tasks unless explicitly told not to.
---

# Git Worktree Workflow

## When to Use

- Use this skill for repository implementation work unless the user explicitly
  instructs you not to use Git worktrees.
- Implementation work includes code, tests, build files, documentation,
  repository guidance, and pull-request preparation.

## Workflow

1. Check the current repository state.
2. Fetch the latest base branch.
3. Create a branch and worktree under `.agents/worktrees/`.
4. Before editing, split the implementation plan into practical phases.
5. For each phase, implement only that phase, then run its quality check inside the worktree.
6. Commit the completed phase immediately using `commit-message-quality-check`.
7. Repeat steps 5 and 6 until every planned phase is complete.
8. Before pushing, run the final quality check.
9. Push the branch.
10. Create or update the pull request using `pull-request-quality-check`.

## Worktree Setup

Create implementation worktrees under:

```text
.agents/worktrees/
```

Use a short, descriptive branch and directory name, such as:

```text
.agents/worktrees/fix-state-load
```

Start from the latest base branch unless the user names a different base.
The usual base is `main`:

```powershell
git fetch origin main
git worktree add -b <branch-name> .agents/worktrees/<branch-name> origin/main
```

If network access or Git metadata writes require approval, request it and
continue after approval.

## Safety Rules

- Treat uncommitted or untracked files in the original worktree as user work.
- After creating the task worktree, make implementation changes there.
- Do not remove another worktree unless the user explicitly asks.
- If the branch or worktree path already exists, inspect it before reuse or
  choose a new descriptive name.
- Once a branch has been pushed or attached to a pull request, do not amend, rebase, squash,
  force-push, or otherwise rewrite its history unless the user explicitly asks for history
  rewriting.

## Quality Check

A quality check means formatting and verification appropriate to the change
risk and repository conventions. Prefer documented project commands such as
builds, tests, linters, formatters, or structural validators that cover the
files changed.

If verification is skipped, state why in the pull request body.

The final quality check also includes reviewing:

- The complete diff.
- Recent commits.
- Accidental scope creep.
- Missing verification.
- Commit-message quality.

## Pull Request Notes

- Keep pull request titles and bodies consistent with `pull-request-quality-check`.
- For later corrections on an already-pushed pull request branch, add follow-up commits on top of
  the branch so review history remains visible.
- Remove temporary PR body files from the worktree after creating or editing the pull request.
