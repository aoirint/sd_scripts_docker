---
name: pull-request-quality-check
description: Quality-check repository pull requests, review comments, replies, and PR-thread notes.
---

# Pull Request Quality Check

## When to Use

- Use this skill when creating, updating, reviewing, or validating pull request
  titles, bodies, review comments, replies, or PR-thread notes.

## Goals

- Keep pull request communication accurate, reviewable, and aligned with the
  repository's current PR template.
- Preserve required LLM disclosure for PR bodies, reviews, replies, and
  PR-thread notes. For artifacts prepared by an AI agent in this workflow, treat
  the assistance as significant and include the alert.
- Keep verification evidence separated by source so automated checks, manual
  checks, CI, screenshots, and AI-assisted inspections are not confused.
- Avoid shell quoting corruption when creating or editing Markdown through CLI
  tools.

## Workflow

1. Identify the artifact being checked: PR title, PR body, review, reply, or
   PR-thread note.
2. For PR titles, verify the Conventional Commits-style title shape and use
   `commit-message-quality-check` for type selection and breaking-change
   notation.
3. For PR bodies, read the current repository PR template before drafting or
   replacing content. If no template exists, use the directly linked fallback
   scaffold in [references/fallback-pr-body.md](references/fallback-pr-body.md).
4. Check that the required LLM alert appears at the very top when the PR body,
   review, reply, or PR-thread note has significant LLM assistance. For
   AI-agent-prepared artifacts, assume the assistance is significant.
5. Check that verification evidence is grouped under the right testing or
   inspection category, with AI-assisted inspections labeled separately.
6. Apply the style, PR-thread note, and CLI safety rules below.
7. Re-read the final title, body, comment, or review as a maintainer would:
   stale template text, invented checklist items, unclear verification, and
   missing disclosure are blocking issues.

## Title

Check that the title uses a Conventional Commits-style format:

```text
<type>[optional scope][optional !]: <description>
```

Use `commit-message-quality-check` for type selection and breaking-change notation.

Reference: https://www.conventionalcommits.org/en/v1.0.0/

## Required LLM Alert

When the PR has significant LLM assistance, check for this GitHub alert.
For PR bodies prepared by an AI agent, assume the assistance is significant.
The alert must appear at the very top of the PR body:

```markdown
> [!WARNING]
> This pull request was created with assistance from LLMs.
```

The alert should appear before every other heading, summary, checklist, or
metadata block.

## Pull Request Template

Before creating or replacing a pull request body, check for a repository pull
request template.
Use the first applicable template found in the normal GitHub locations, such as:

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/pull_request_template.md`
- `docs/PULL_REQUEST_TEMPLATE.md`
- A user-selected file under `.github/PULL_REQUEST_TEMPLATE/` or `docs/PULL_REQUEST_TEMPLATE/`

When a template exists:

- Read the template file before drafting the body. Do not rely on memory,
  previous PR bodies, or heading summaries.
- Follow the template's visible headings, required checkboxes, and required-if-applicable sections.
- Use HTML comments in the template as author guidance. Do not copy those
  comments into the rendered PR body.
- Keep required alerts, checklist confirmations, and section names compatible with the template.
- Fill sections with `None` or `Not applicable` only when the template or
  surrounding policy asks for an explicit value.
- Do not replace template-specific headings with generic defaults. For example,
  do not use `Verification` when the template uses `Testing`.
- Do not add obsolete checklist items that are no longer present in the repository template.
- Copy required checklist wording from the current template exactly. Change
  unchecked boxes to checked boxes only when the author can truthfully confirm
  the item.
- When updating an existing PR body, remove or revise stale body text that
  describes removed template items. For example, remove an old AI-disclosure
  checkbox that no longer exists.
- If the template should apply but the exact file or selected variant is
  unavailable, stop and get the template. Do not invent placeholder headings or
  checklist text.

When no repository template exists, use
[references/fallback-pr-body.md](references/fallback-pr-body.md). Keep its
top-level headings and testing subsection order unless the repository policy
explicitly says otherwise.

## Verification Evidence

- Do not present AI-performed review, inspection, editing, verification, or
  other work as "manual".
- If an AI-assisted inspection was requested, report it under a
  `### AI-assisted inspections` subsection inside `## Testing`, after
  `### Automated checks` when both sections are present.
- In `### AI-assisted inspections`, use a short `Request: ...` line to
  summarize the requested inspection. Nest the `AI-assisted result: ...` under
  that request summary.
- Keep automated commands, CI results, non-AI manual checks, screenshots,
  videos, and AI-assisted inspection results distinct from each other.

## Style

- Write pull request titles, pull request bodies, review comments, and replies in English.
- Preserve non-English text only when quoting source text, branch names, commit messages, file
  contents, logs, or existing discussion snippets that must remain exact.
- Keep PR bodies short and reviewable.
- Use `document-quality-check` for explanatory prose that needs readability, structure, or nuance
  review.
- Use `security-check` when a pull request body, reply, or review note describes
  security-sensitive behavior, supply-chain-sensitive tools, package runners, dependencies,
  downloaded artifacts, CI actions, containers, secrets, permissions, or security exceptions.
- Prefer bullets over long paragraphs.
- Mention paths or commands in backticks.
- Do not paste large diffs.
- Be explicit when verification was not run.
- Align the PR title type with the dominant change. For example, use `docs:`
  for documentation-only skill additions and `refactor:` for behavior-preserving
  code cleanup.

## Pull Request Replies and Reviews

When a pull request reply or review has significant LLM assistance, check for
this GitHub alert. For replies, reviews, or PR-thread notes prepared by an AI
agent, assume the assistance is significant.
It must appear at the very top of the comment or review body:

```markdown
> [!WARNING]
> This comment was created with assistance from LLMs.
```

The alert should appear before every other paragraph, heading, checklist, quote,
finding, or metadata block.

Use `Update Note`, `Discussion Note`, or `Review Note` sections only when the
active task asks for process notes, decision logs, review summaries, or granular
PR-thread updates. Do not add them by default. Frequent process notes can
clutter the PR conversation and may expose unnecessary implementation context.
When enabled:

- Use `Update Note` for a concrete change that was just made to the pull request.
- Use `Discussion Note` for a decision, tradeoff, or rationale that should
  remain visible in the PR thread.
- Use `Review Note` when reporting a review pass, consistency check, readiness
  check, or retrospective verification that did not itself make a concrete
  change.
- If the active task asks for "history so far", "notes so far", or similar
  retrospective PR-thread notes, do not dump raw commit history. Create separate
  concise notes grouped by meaningful decision or change theme, using
  `Update Note` for concrete PR changes and `Discussion Note` for decisions,
  tradeoffs, or rationale.
- If the requester asks for notes to be separate, or a correction includes two
  independently reviewable changes, post separate PR comments for each theme
  instead of combining them into one broad note.
- Immediately after the required LLM alert and before the note heading, add a
  neutral `Request addressed: ...` line. Use it only as a concise marker for
  later PR-body `### AI-assisted inspections` summaries; do not use it to
  classify requester identity, role, or authority.
- Keep each note concise and limited to information that is safe and useful for
  future reviewers.
- Base notes on confirmed PR context. If a note includes an inference or
  assumption, label it as such.
- Do not include secrets, private discussion, local-only paths, hidden
  chain-of-thought, or unrelated implementation details.
- Prefer a normal short reply when the comment only needs to answer a question,
  report review results, or acknowledge completion.

## CLI Safety

When creating or editing PR bodies with a shell command, avoid passing Markdown
directly through command arguments. Backticks, quotes, dollar signs, backslashes,
and multiple lines are easy to corrupt in shell arguments. Shells such as
PowerShell and bash can interpret those characters silently.

- Prefer writing the body to a temporary Markdown file. Pass it with
  `gh pr create --body-file <file>` or `gh pr edit --body-file <file>`.
- After creating or editing a PR through `gh`, verify the stored body with
  `gh pr view --json body`. Fix any quoting issues before finishing.
- Remove any temporary body file from the worktree after verification.
