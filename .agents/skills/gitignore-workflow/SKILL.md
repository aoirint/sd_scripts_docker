---
name: gitignore-workflow
description:
  Create or update repository `.gitignore` rules, including pinned upstream template syncs. Use when changing
  ignored-file behavior or merging `github/gitignore` content.
---

# Gitignore Workflow

## Update ignore rules

1. Inspect the repository state and current `.gitignore`. Separate project-specific rules from template-derived blocks.
2. Preserve project-specific rules unless the user explicitly requests their removal. Avoid broad patterns that could
   hide source files; note that `.gitignore` does not untrack files already committed.
3. When syncing `github/gitignore`, use `security-check` and verify the repository, exact template path, and reviewed
   commit hash before fetching or copying. Stop and report a blocker when provenance or a safe network path cannot be
   verified.
4. Pin every copied template URL to its commit hash. Keep upstream blocks semantically unchanged, including intentional
   duplicates, and use a deterministic section order.
5. Use this pattern for each template:

    ```text
    # <TemplateName>.gitignore
    # https://github.com/github/gitignore/blob/<commit-hash>/<TemplatePath>
    {template content}
    ```

6. Validate the resulting behavior with `git status --short` and report changes affecting `.env`, lockfiles, build
   artifacts, caches, or IDE folders.

Never put secrets or real environment values in comments. Keep agent-local directories explicit when needed, for example
`.agents/worktrees/` and `.agents/references/`.
