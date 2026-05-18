---
name: issue-quality-check
description: >-
  Quality-check repository issues and issue replies. Use when creating,
  updating, reviewing, or validating GitHub issues or comments on issues.
---

# Issue Quality Check

## When to Use

- Use this skill when creating, updating, reviewing, or validating GitHub issue
  titles or bodies for this repository.
- Use this skill when creating, updating, reviewing, or validating replies or
  comments on GitHub issues for this repository.

## Goals

- Make issue titles, bodies, and replies clear enough for maintainers to triage and act on.
- Preserve required LLM disclosure alerts when issue text has significant LLM
  assistance. For artifacts prepared by an AI agent in this workflow, treat the
  assistance as significant and include the alert.
- Keep issue text in English except for exact quoted source material or identifiers.
- Prevent shell quoting from corrupting Markdown when creating or editing issues through `gh`.
- Record verification limits, uncertainty, and requested follow-up information explicitly.

## Workflow

1. Classify the artifact as an issue title, issue body, issue reply, or combined issue update.
2. Check required LLM disclosure first, using the issue-body alert for issues and the comment alert
   for replies when LLM assistance was significant. For AI-agent-prepared artifacts, assume the
   assistance is significant.
3. Check the title when present for concise, specific triage wording.
4. Check the body or reply structure, keeping only sections that add useful information.
5. Check English style, concise wording, exact quoted material, and issue-specific nuance with
   `document-quality-check` when explanatory prose needs review.
6. Check risk-sensitive content with `security-check` when the issue mentions security,
   supply-chain-sensitive tools, dependencies, CI, containers, secrets, permissions, or exceptions.
7. Check CLI safety before creating or editing issues or replies through a shell command.
8. After any `gh` create or edit command, verify the stored Markdown body or comment when possible,
   fix quoting problems, and remove temporary body files.
9. In CLI examples, use confirmed issue numbers, comment IDs, or placeholders such as
   `<issue-number>`. Do not infer an issue number from a pull request number or unrelated context.

## Title

Check that the title is concise, specific, and written as a problem or task:

- Prefer a clear noun phrase or imperative task, such as
  `Add practice reset hotkey documentation` or
  `Fix cruiser state reload after scene transition`.
- Include the affected area when it helps triage, such as `MagnetService:` or `docs:`.
- Avoid vague titles such as `Bug`, `Question`, `Help`, or `Does not work`.
- Do not force Conventional Commits format for issues unless the repository
  explicitly asks for it in that issue flow.

## Required LLM Alert

When the issue has significant LLM assistance, check that this GitHub alert
appears at the very top of the issue body. For issue bodies prepared by an AI
agent, assume the assistance is significant:

```markdown
> [!WARNING]
> This issue was created with assistance from LLMs.
```

The alert should appear before every other heading, summary, checklist, template
field, or metadata block.

## Body Structure

Check that the body is concise and uses these sections when applicable:

```markdown
> [!WARNING]
> This issue was created with assistance from LLMs.

## Summary
- ...

## Details
- ...

## Acceptance Criteria
- ...
```

The example includes the LLM alert because this skill is usually used for
AI-agent-prepared issue text. Omit the alert only when the issue has no
significant LLM assistance.

Recommend sections only when they carry useful information:

- `Summary`: the problem, request, or outcome in maintainer-facing language.
- `Details`: relevant context, reproduction notes, affected paths, logs, or constraints.
- `Acceptance Criteria`: concrete checks that would make the issue complete.
- `Verification`: commands, manual checks, or observations already performed.
- `Notes`: limitations, related work, dependencies, or reviewer attention points.

For follow-up issues, include durable origin context when useful, such as the pull request,
review thread, issue, discussion, or investigation that caused the follow-up. When multiple related
follow-up issues come from the same source, cross-link them in the issue bodies so future readers
can trace the relationship without relying on transient comments elsewhere.

## Style

- Write issue titles, issue bodies, and issue comments in English.
- Preserve non-English text only when quoting source text, branch names, commit messages, file
  contents, logs, or existing discussion snippets that must remain exact.
- Keep issue bodies short and scannable.
- Use `document-quality-check` for explanatory prose.
  - Preserve issue-specific nuance such as certainty, scope, timing, relationships, and whether a
    statement is confirmed, inferred, untested, or unknown.
- Use `security-check` when an issue or issue reply describes security-sensitive
  behavior, supply-chain-sensitive tools, package runners, dependencies, CI actions, containers,
  secrets, permissions, or security exceptions.
- Prefer bullets for facts, steps, and criteria.
- Mention paths, commands, classes, and config keys in backticks.
- Include exact expected and actual behavior for bugs.
- Include reproduction steps only when they are known and useful.
- Do not paste large logs, stack traces, or diffs; summarize and link or attach details when needed.
- Be explicit when verification or reproduction was not run.
- Do not present AI-performed review, inspection, editing, verification, or
  other work as "manual".

## CLI Safety

When creating or editing issue bodies with a shell command, avoid passing
Markdown directly through command arguments if it contains backticks, quotes,
dollar signs, backslashes, or multiple lines. Shells such as PowerShell and bash
can interpret those characters and silently corrupt the body.

- Prefer writing the body to a temporary Markdown file and passing it with
  `gh issue create --body-file <file>` or `gh issue edit --body-file <file>`.
- Use placeholders such as `<issue-number>` when the target issue number is unknown.
- After creating or editing an issue through `gh`, verify the stored body with
  `gh issue view --json body` and fix any quoting issues before finishing.
- Remove any temporary body file from the worktree after verification.

## Issue Replies

When the issue reply has significant LLM assistance, check that this GitHub
alert appears at the very top of the comment body. For replies prepared by an AI
agent, assume the assistance is significant:

```markdown
> [!WARNING]
> This comment was created with assistance from LLMs.
```

The alert should appear before every other paragraph, heading, checklist, quote,
or metadata block.

Check that the reply is concise and uses only the structure needed for the situation:

```markdown
> [!WARNING]
> This comment was created with assistance from LLMs.

Thanks for the report. I can reproduce this with ...

## Next Steps
- ...
```

The example includes the LLM alert because this skill is usually used for
AI-agent-prepared replies. Omit the alert only when the reply has no significant
LLM assistance.

Recommend sections only when they carry useful information:

- Opening sentence: acknowledge the report, question, or prior comment directly.
- `Findings`: facts discovered from code, logs, reproduction, or maintainer investigation.
- `Next Steps`: what will be done next, what is blocked, or what input is needed.
- `Verification`: commands or manual checks run while investigating.
- `Notes`: caveats, related issues, or constraints that should remain visible.

For issue replies:

- Keep replies focused on the current issue thread.
- Answer direct questions before adding broader context.
- Quote only the smallest useful part of a previous comment.
- Mention paths, commands, classes, and config keys in backticks.
- Be clear whether something is confirmed, inferred, untested, or still unknown.
- Ask for specific missing information when needed, such as logs, package or
  application versions, reproduction steps, or relevant data files.
- Avoid large diffs, large logs, and unrelated implementation plans.
- Do not promise timelines unless they are already agreed.
- Do not present AI-performed review, inspection, editing, verification, or
  other work as "manual".

Use `Update Note` or `Discussion Note` sections only when the active task asks
for process notes, decision logs, or granular issue-thread updates. Do not add
them by default: frequent process notes can clutter the thread and may expose
unnecessary implementation context. When enabled:

- Use `Update Note` for a concrete issue, documentation, or implementation
  update that was just made.
- Use `Discussion Note` for a decision, tradeoff, or rationale that should
  remain visible in the issue thread.
- Immediately after the required LLM alert and before the note heading, add a
  neutral `Request addressed: ...` line. Use it only as a concise marker for
  later AI-disclosure or AI-assisted inspection summaries; do not use it to
  classify requester identity, role, or authority.
- Keep each note concise and limited to information that is safe and useful for
  future readers.
- Base notes on confirmed issue context. If a note includes an inference or
  assumption, label it as such.
- Do not include secrets, private discussion, local-only paths, hidden
  chain-of-thought, or unrelated implementation details.
- Prefer a normal short reply when the comment only needs to answer a question,
  report investigation results, or acknowledge completion.

When creating or editing issue replies with a shell command:

- Prefer writing the reply to a temporary Markdown file and passing it with
  `gh issue comment --body-file <file>`.
- Use placeholders such as `<issue-number>` when the target issue number is unknown.
- After creating or editing a reply through `gh`, verify the stored comment body
  when possible and fix any quoting issues before finishing.
- Remove any temporary body file from the worktree after verification.
