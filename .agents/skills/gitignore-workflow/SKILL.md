---
name: gitignore-workflow
description: "Create or update .gitignore files. Use when editing ignore rules."
---

# Gitignore Workflow

## When to Use

- Use this skill when creating or updating `.gitignore`.

## Goals

- Keep project-specific ignore rules explicit and easy to review.
- Merge upstream template content from `github/gitignore` without losing local rules.
- Record external-template provenance with commit-hash URLs for reproducibility.
- Avoid introducing regressions, for example accidentally tracking generated files.
- Support both minimal edits and full template refreshes.
- Work across mixed-language repositories.

## Workflow

1. Inspect the current repository state before editing.
2. Read the current `.gitignore` and classify entries as project-specific vs template-derived.
3. If template sync is requested, treat the copied template content as supply-chain-sensitive
   external material:
   - Use `security-check` for network-fetch safety, source provenance, pinning, and any blocker
     decision.
4. Verify the upstream template source before fetching or copying:
   - Confirm the exact repository, template path, and commit hash.
   - Prefer reviewer-visible commit-hash URLs over branch, tag, or `latest` references.
   - Report a blocker instead of fetching or copying when provenance or the safe network path
     cannot be verified.
5. Merge sections in a deterministic order requested by the user or a safe default order.
6. Validate with `git status` that ignored/generated files behave as expected.
7. Summarize behavior-impacting changes, especially `.env`, lockfiles, build artifacts, caches, and
   IDE folders.

## Recommended Section Order

Use this structure when the user requests Python with project-local rules.
For other stacks, keep the same pattern and swap template sections as needed.

```text
# Project specific files
{project-specific ignore entries}

# Agent worktree directory
.agents/worktrees/
# Agent reference directory
.agents/references/

# Python.gitignore
# https://github.com/github/gitignore/blob/<commit-hash>/Python.gitignore
{Python.gitignore content}
```

## Generalized Section Pattern

For multi-stack repositories, repeat this pattern per template:

```text
# <TemplateName>.gitignore
# https://github.com/github/gitignore/blob/<commit-hash>/<TemplatePath>
{template content}
```

## Template Fetch Pattern

Use network fetches only after the safety and provenance checks above pass.
Pin the source to one reviewed commit hash and keep the command reviewer-visible.

```bash
hash=$(git ls-remote https://github.com/github/gitignore.git refs/heads/main | awk '{print $1}')
curl -fsSL "https://raw.githubusercontent.com/github/gitignore/$hash/Python.gitignore"
```

For other templates, replace paths with exact file paths from `github/gitignore`.
For example, use `Global/VisualStudioCode.gitignore`.
If the command, source repository, template path, or commit hash cannot be verified, stop and report
the blocker instead of fetching or copying template content.

## Safety Checks

- Do not remove project-specific entries unless explicitly requested.
- Keep duplicate patterns if they come from upstream templates; avoid semantic edits to upstream blocks.
- Preserve `.env` handling intentionally. If behavior changes, call it out in the summary.
- Never include secrets or real environment values in `.gitignore` comments.
- If files are already tracked, mention that `.gitignore` alone does not untrack them.
- Avoid adding global ignores that could hide source files by mistake.

## Output Checklist

- `.gitignore` updated in requested format.
- All upstream template URLs include commit hashes, exact paths, and reviewed provenance.
- Network fetches were either avoided, performed through a pinned and verified source, or blocked
  with the reason recorded.
- `git status --short` reviewed after edits.
- User summary includes what changed, why, and any follow-up commands if tracked files must be untracked.
