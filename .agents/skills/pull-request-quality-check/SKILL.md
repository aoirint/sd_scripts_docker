---
name: pull-request-quality-check
description:
  Quality-check repository pull requests and PR-thread communication. Use when creating, updating, reviewing, or
  validating PR titles, bodies, review comments, replies, or thread notes.
---

# Pull Request Quality Check

## Check the pull request artifact

1. Identify the artifact: title, body, review, reply, or thread note.
2. For titles, enforce `<type>[optional scope][optional !]: <description>` and use `commit-message-quality-check` for
   type and breaking-change notation.
3. Before drafting or replacing a body, read the current repository PR template and applicable contributor guidance.
   Follow only their visible headings, required checkboxes, and applicable sections; use HTML comments only as guidance,
   not rendered content. If no template exists, use [references/fallback-pr-body.md](references/fallback-pr-body.md).
   Never infer a CLA, contributor agreement, checklist, sign-off, or other repository policy from the fallback. Do not
   invent unavailable template text or retain stale template content.
4. For AI-agent-prepared PR bodies, add this alert at the absolute top:

    ```markdown
    > [!WARNING]
    > This pull request was created with assistance from LLMs.
    ```

    Use this alert for AI-assisted reviews, replies, and thread notes:

    ```markdown
    > [!WARNING]
    > This comment was created with assistance from LLMs.
    ```

    Omit an alert only when assistance was not significant. Treat the alert as
    an invariant, not interchangeable formatting: no template content or
    other alert may precede or replace it. If an existing body starts with
    another alert, prepend the LLM alert and preserve the existing body after
    the separating blank line.

5. Keep verification evidence distinct: automated commands, CI results, non-AI manual checks, screenshots/videos, and
   AI-assisted inspections. Put requested AI-assisted inspections under `## Testing`, then `### AI-assisted inspections`
   after automated checks, with `Request: ...` and nested `AI-assisted result: ...`. Never describe AI-performed work as
   manual.
6. Write in English except for exact source material. Keep bodies reviewable, use bullets and backticks, avoid large
   diffs, state skipped verification, and use `prose-quality-check` or `security-check` for applicable prose or
   sensitive content.

## Reviews, notes, and CLI safety

Use `Update Note`, `Discussion Note`, or `Review Note` only when the task requests process, decision, or review-summary
notes. Place `Request addressed: ...` after the required alert; group retrospective notes by meaningful theme, separate
independently reviewable themes when requested, label inferences, and omit secrets, private paths, and hidden reasoning.

When using `gh`, write Markdown to a temporary file and pass `--body-file`.
Verify the stored body from the complete `--json body` response, not
line-oriented `--jq` output. In PowerShell, preserve the response as one raw
string, decode it, require `body` to be a `[string]`, compare it with the
candidate allowing only terminal-newline normalization, and remove the
temporary file. Do not normalize any other whitespace or line endings.

Before writing an AI-assisted body or comment, run
`scripts/check_llm_disclosure.py` against the candidate. For a
disclosure-only repair, also pass the exact prior body so the check proves that
only the required alert prefix was added. After writing, fetch the complete
JSON response and run the helper against that response and the candidate.

For multi-PR or multi-comment work, treat each stored artifact as an
independent completion unit:

1. Preflight every candidate before the first external write.
2. Verify each stored artifact immediately after its write.
3. Audit the complete target set at the end, including targets that required
   no edit.
4. Report success only when every target has exactly one required alert at the
   absolute top and every stored body matches its approved candidate, allowing
   only terminal-newline normalization.

Before `gh pr merge` creates a squash or merge commit:

1. Resolve the exact PR head SHA and pass it with `--match-head-commit`.
2. Write the merge body with real line breaks to a temporary file; do not pass
   an escaped string containing literal `\n` sequences.
3. Build the complete candidate commit message from the exact subject and body
   file. Write those exact bytes to a candidate file and reject literal `\n`
   or `\r\n` text. Pass the candidate file directly to
   `git interpret-trailers --parse`; do not pipe a shell string that may alter
   line endings. Require each expected trailer exactly once.
4. Before merging, test the stored-message verifier itself. Put the candidate
   message in a JSON fixture shaped like the commit API response, decode it
   through the same JSON parser planned for post-merge verification, and
   require `commit.message` to be one string equal to the candidate.
5. Only after those validations succeed, pass the same body file with
   `gh pr merge --body-file`.
6. Verify the stored commit message and trailers after merge. Preserve the
   multiline value as one string:
   - Query the repository commit endpoint
     `repos/{owner}/{repo}/commits/{sha}`, whose response contains
     `commit.message`; do not use the Git-data endpoint
     `repos/{owner}/{repo}/git/commits/{sha}`, whose `message` is at the root.
     Save the full response to a temporary file and parse it as JSON. In
     PowerShell, use `Get-Content -Raw | ConvertFrom-Json`, then require
     `commit.message` to be a `[string]`.
   - Do not assign line-oriented output from
     `gh api --jq '.commit.message'` directly to a PowerShell variable; a
     multiline value becomes an array of lines and breaks exact comparison.
   - Write the decoded `commit.message` string to a file, compare it with the
     candidate allowing at most terminal-newline normalization, and pass that
     file directly to `git interpret-trailers --parse`.
   Treat this as a secondary check, not a substitute for pre-merge validation.
