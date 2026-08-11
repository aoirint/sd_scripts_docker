---
name: github-workflow
description: >-
  Quality-check GitHub repository issues, pull requests, reviews, replies,
  comments, and squash merges. Use when creating, editing, reviewing, or
  publishing GitHub collaboration artifacts, including preflight checks that
  prevent private-repository disclosure; use github-actions-quality-check for
  workflows, local actions, Actions policy, and required-check design.
---

# GitHub Workflow

## When to Use

Use this Skill for GitHub issue and pull-request text or operations:

- Issue title, body, comment, or thread note: use **Issues**.
- Pull-request title, body, review, reply, thread note, or squash merge: use
  **Pull requests**.

Use `github-actions-quality-check` for workflows, local actions, Actions
repository settings, and required-check contexts. Use `security-check` for
security-sensitive content and `prose-quality-check` for nuanced prose.

## Goals

- Keep issue and pull-request artifacts concise and accurate.
- Disclose significant AI assistance consistently.
- Preserve repository templates and policies without inventing requirements.
- Validate exact stored text and squash-merge commit payloads.
- Prevent private-repository identifiers from reaching public or potentially public
  GitHub content by validating complete candidates before every write.

## Workflow

### Private repository disclosure preflight

Apply `security-check`'s private-resource disclosure boundary before every GitHub
create, update, upload, push, or release operation.

1. Determine the destination repository's current and possible future visibility.
   Treat it as public when it is public, could later be published, or its future
   visibility is uncertain. Current private-to-private access does not authorize a
   private-repository reference in a potentially public destination.
2. Protect the private repository's owner/name, URL, issue or pull-request reference,
   branch or ref, private-only path, code name, and any wording or relationship that
   makes its existence reasonably inferable. Authentication required to resolve or
   execute a reference does not hide the reference itself.
3. Inspect the exact complete candidate before the first GitHub write. Include titles,
   body files, comments, reviews, commit and merge messages, repository diffs,
   configuration and fixtures, workflow `uses:` references, copied command or API
   output, annotations, SARIF, artifact and archive contents and filenames, badges,
   screenshots, release notes, and generated metadata. Inspect the final rendered or
   serialized form as well as source prose.
4. Remove direct identifiers and indirect existence disclosures before calling `gh`,
   an API, `git push`, an upload command, or another publishing tool. Keep only a
   non-identifying requirement or outcome. Store the exact source and evidence in an
   approved non-GitHub private channel or system; do not move it to another GitHub
   issue, comment, private repository, attachment, hidden field, or code block.
5. If any candidate or derivative cannot be inspected completely, or useful context
   cannot be preserved without disclosure, stop before the write and request a secure
   handoff. Do not publish first and plan to redact afterward.
6. After a successful write, read back the complete stored artifact and verify it
   against the approved candidate. This is a secondary integrity check, not a
   substitute for preflight. For an existing disclosure, stop further publication,
   inventory history, logs, artifacts, caches, notifications, and mirrors as
   unverified exposure, and use a maintainer-approved cleanup process.

### Issues

1. Identify whether the artifact is an issue title, body, reply, or combined
   update. For significant AI assistance, put this alert at the absolute top:

   ```markdown
   > [!WARNING]
   > This issue was created with assistance from LLMs.
   ```

   Use `This comment was created with assistance from LLMs.` for replies.
2. Make titles concise and specific. Keep bodies and replies concise, using
   only useful sections such as `Summary`, `Details`, `Acceptance Criteria`,
   `Verification`, `Notes`, `Findings`, or `Next Steps`. For bugs, state
   expected and actual behavior and useful reproduction steps.
3. Write in English except for exact source material. Use bullets, backticks,
   explicit uncertainty, and summaries rather than large logs or diffs. Never
   describe AI-performed work as manual.
4. Add `Update Note` or `Discussion Note` only when requested. Put
   `Request addressed: ...` after the required alert and before the note
   heading; label inferences and omit secrets and private paths.
5. With `gh`, write Markdown to a temporary file and pass `--body-file`.
   Verify stored issue bodies with `gh issue view --json body` and stored
   replies when possible, then remove temporary files.

### Pull requests

1. Identify the artifact: title, body, review, reply, thread note, or squash
   merge. For titles, enforce
   `<type>[optional scope][optional !]: <description>` and use
   `commit-message-quality-check` for type and breaking-change notation.
2. Before drafting or replacing a body, read the current PR template and
   contributor guidance. Follow only visible headings, required checkboxes,
   and applicable sections. If no template exists, use
   [fallback-pr-body.md](references/fallback-pr-body.md). Never infer a CLA,
   contributor agreement, checklist, sign-off, or policy from the fallback.
3. For significant AI assistance, put this alert at the absolute top of PR
   bodies:

   ```markdown
   > [!WARNING]
   > This pull request was created with assistance from LLMs.
   ```

   Use `This comment was created with assistance from LLMs.` for reviews,
   replies, and thread notes. Preserve any existing alert after a blank line;
   the LLM alert must appear exactly once and first.
4. Keep automated commands, CI results, non-AI manual checks, screenshots or
   videos, and AI-assisted inspections distinct. Under `## Testing`, put
   AI-assisted work in `### AI-assisted inspections` after automated checks
   with `Request: ...` and nested `AI-assisted result: ...`. State skipped
   verification and never describe AI work as manual.
   When the body cites a GitHub repository, issue, pull request, commit,
   release, workflow run, or other reviewable artifact, use a descriptive
   Markdown link to its canonical URL. Do not leave an auditable source as only
   `owner/repo#123`, a short SHA, or prose that makes the reviewer search for
   the referenced artifact. An exact identity may remain in inline code when
   the same item is linked beside it.
5. Use `Update Note`, `Discussion Note`, or `Review Note` only when requested.
   Put `Request addressed: ...` after the required alert; group retrospective
   notes by meaningful theme, label inferences, and omit secrets, private
   paths, and hidden reasoning.
6. Before writing an AI-assisted body or comment, run
   `scripts/check_llm_disclosure.py` against the candidate. For a
   disclosure-only repair, pass the exact prior body. After writing, fetch the
   complete JSON response and run the helper against that response and the
   candidate. For multi-artifact work, preflight every candidate, verify each
   write immediately, audit all targets at the end, and report success only
   when every target has exactly one required top alert and a matching body.
7. With `gh`, use `--body-file`. Verify the complete JSON `body` as one string
   against the candidate, allowing only terminal-newline normalization. In
   PowerShell, do not assign line-oriented `--jq` output when verifying
   multiline bodies. Remove temporary files.
8. Before `gh pr merge` creates a squash or merge commit, resolve and pass the
   exact head SHA with `--match-head-commit`. Build and validate the exact
   multiline candidate commit message in a file with
   `git interpret-trailers --parse`, require each expected trailer exactly
   once, test the stored-message JSON parser with a fixture, merge with the
   same body file, then verify `commit.message` from
   `repos/{owner}/{repo}/commits/{sha}` using raw JSON. Treat post-merge
   verification as secondary to pre-mutation validation.

## Resources

- [fallback-pr-body.md](references/fallback-pr-body.md): fallback PR template
  when no repository template applies.
- `scripts/check_llm_disclosure.py`: validate required LLM disclosure,
  disclosure-only repairs, and stored-body preservation.
