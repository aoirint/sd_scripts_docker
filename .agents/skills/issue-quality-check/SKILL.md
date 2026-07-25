---
name: issue-quality-check
description:
  Quality-check repository GitHub issues and issue comments. Use when creating, updating, reviewing, or validating issue
  titles, bodies, replies, or thread notes.
---

# Issue Quality Check

## Check the artifact

1. Identify whether the artifact is an issue title, body, reply, or combined update.
2. For AI-agent-prepared issue text, add the applicable alert at the very top:

    ```markdown
    > [!WARNING]
    > This issue was created with assistance from LLMs.
    ```

    Use this comment alert instead for replies:

    ```markdown
    > [!WARNING]
    > This comment was created with assistance from LLMs.
    ```

    Omit an alert only when assistance was not significant.

3. Make titles concise and specific to the problem or task. Include an affected area when useful; avoid vague titles and
   do not impose Conventional Commits unless repository policy requires it.
4. Keep the body or reply concise. Use only useful sections: `Summary`, `Details`, `Acceptance Criteria`,
   `Verification`, `Notes`, `Findings`, or `Next Steps`. For bugs, state expected and actual behavior and known useful
   reproduction steps. Cross-link durable follow-up origin context when it helps triage.
5. Write in English except for exact source material. Use bullets, backticks for technical names, explicit uncertainty
   and verification limits, and summaries rather than large logs or diffs. Never describe AI-performed work as manual.
6. Use `prose-quality-check` for nuanced explanatory prose and `security-check` for security- or supply-chain-sensitive
   content.

## Thread notes and CLI safety

Add `Update Note` or `Discussion Note` only when the task requests process or decision notes. Place
`Request addressed: ...` after the required alert and before the note heading; label inferences, avoid secrets and
private paths, and keep normal replies direct.

When using `gh`, write Markdown to a temporary file and pass `--body-file`; use confirmed identifiers or placeholders
such as `<issue-number>`. Verify stored issue bodies with `gh issue view --json body` and stored replies when possible,
correct quoting, then remove temporary files.
