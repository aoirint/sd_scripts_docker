---
name: pull-request-quality-check
description:
  Quality-check repository pull requests and PR-thread communication. Use when creating, updating, reviewing, or
  validating PR titles, bodies, review comments, replies, thread notes, or GitHub squash-merge attribution and
  commit-message payloads.
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
7. When a PR may produce a commit with human or AI co-author trailers, keep the proposed trailer set reviewable in
   the PR body from creation through every update. Use the repository template's closest relevant section; if none
   exists, append `## Proposed merge attribution` after the required template content. Include the issue author when
   the PR implements their issue, and include a design or snippet provider whose material contribution is used; these
   are default co-authors unless a reviewer marks the candidate `Not applicable`. For each human candidate, show their
   canonical GitHub account as `@login` and immutable numeric GitHub user ID, the resolved exact `Co-authored-by:`
   line, a concise non-private basis, and `Included`, `Needs identity`, `Needs review`, or `Not applicable` status.
   For an AI candidate, show its exact trailer, basis, and status. State `None proposed` when the set is empty.

   Apply role precedence before selecting trailers: the PR creator is the GitHub-squash primary Git author; a
   final-diff head-commit author, implemented-issue author, or material design/snippet contributor is a trailer
   candidate only when distinct from that primary author. Reviewers and merge actors are not candidates from those
   roles alone. Preserve an independently evidenced existing trailer even when a person's other role would not create
   one.

   Resolve every human trailer from a GitHub account and an exact email that GitHub can attribute to that account. Use
   the contributor's explicitly supplied GitHub-provided noreply address by default. Use a Public Email instead only
   when that contributor explicitly directs its use for the trailer and the current GitHub user response exposes the
   same email; record that choice in the PR attribution block. Never synthesize a noreply address from `@login` or an
   ID. An existing head-commit trailer is reusable only when its GitHub author association proves the same account.
   If the exact attributable email is unavailable, retain `Needs identity` and request it from the contributor rather
   than inventing an address. On
   a PR update, preserve every
   candidate unless its basis changed; make additions, removals, account/ID changes, resolved-trailer changes, and
   status changes reviewable rather than silently replacing the block. If any candidate's contribution, applicability,
   account, numeric ID, resolved trailer, or review status is uncertain, use `Needs identity` or `Needs review` and
   stop the merge until the uncertainty is resolved.
   For a GitHub-hosted squash merge, expect GitHub to record the PR creator as the primary Git author. This is platform
   metadata, not proof of material contribution: the creator can be neither an author nor co-author of the PR-head
   commits. Do not add that person as `Co-authored-by:` merely because they opened the PR, and do not add the merge
   actor merely for performing the merge. Record the PR creator and, after merge, the PR's `mergedBy` separately from
   the trailer set. If the PR creator is not a material contributor in the final diff, mark that attribution mismatch
   `Needs review` and stop before merging until a maintainer confirms the intentional GitHub-squash attribution or
   selects another authorized integration path. Verify the stored commit's GitHub author association resolves to the
   PR creator; record the platform committer as observed rather than assuming it is the merge actor.
8. A review comment or approval alone does not create a co-author candidate. Before each squash merge, inspect all
   commits reachable only from the PR head and the applied review suggestions. For each head-only commit whose material
   change remains in the final PR diff, include its Git author and every existing `Co-authored-by:` identity in the
   expected trailer set, unless that identity is already the PR creator's primary Git author. Preserve exact existing
   trailers when available; otherwise resolve the contributor's GitHub account under the human-trailer rule above.
   When GitHub created a commit by applying a review suggestion, include every suggestion provider and suggestion
   applier that GitHub recorded as a co-author of that commit, provided the suggestion remains in the final PR diff,
   except an identity already represented as the PR creator's primary Git author. Record each candidate's source commit
   SHA or review URL in the PR attribution block. If a head commit, applied suggestion, contributor set, or final-diff
   presence cannot be determined, mark it `Needs review` and stop the merge.

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

1. Resolve the pull request's canonical title, number, and head SHA from GitHub. Build the squash subject from that
   metadata as `<pull request title> (#<pull request number>)`; do not rely on the CLI default or omit the number.
   In PowerShell, use:

    ```powershell
    $pr = gh pr view <pr> --json number,title,headRefOid | ConvertFrom-Json
    $subject = "$($pr.title) (#$($pr.number))"
    if ($subject -notmatch '\(#[1-9]\d*\)$') { throw 'Missing PR number suffix.' }
    ```

2. Determine every applicable trailer before writing the merge body. Create an expected trailer set with the exact
   `Token: value` line and attribution source for each entry. Include the author of an implemented issue and each
   material design or snippet contributor by default, unless their PR-body candidate is marked `Not applicable`.
   Resolve human trailers using the PR body's GitHub account and an exact attributable email; preserve each expected
   `Co-authored-by:` trailer exactly once. When an AI agent materially contributed, include the repository-required
   identity (for Codex, `Co-authored-by: Codex <noreply@openai.com>` unless a repository rule supplies another value).
   If the PR has a `## Proposed merge attribution` block, reconcile it before merging: require every `Included` entry's
   exact line to match the expected set, omit only `Not applicable` entries, and stop for `Needs identity`, a missing
   candidate, or an unreviewed identity/trailer change. After merge, verify that each GitHub-account fallback trailer
   is attributed to its expected account. Treat any uncertainty about a co-author candidate as a merge blocker, not as
   a reason to omit, guess, or downgrade the candidate.
3. Write the merge body with real line breaks to a temporary file; do not pass an escaped string containing literal
   `\n` sequences. Put applicable trailers in its footer block, after one blank line from any body text and with no
   blank lines between trailers.
4. Build the complete candidate commit message from that exact `$subject` and the same body file. The merge command
   must receive the same `$subject` through `--subject` and the same body file through `--body-file`; a candidate file
   alone does not set the stored commit subject or preserve trailers.
5. Write the exact candidate bytes to a file and reject literal `\n`
   or `\r\n` text. Pass the candidate file directly to
   `git interpret-trailers --parse`; do not pipe a shell string that may alter
   line endings. Require each expected trailer's full `Token: value` line exactly once and reject any additional
   `Co-authored-by:` line that is not in the approved set.
6. Before merging, test the stored-message verifier itself. Put the candidate
   message in a JSON fixture shaped like the commit API response, decode it
   through the same JSON parser planned for post-merge verification, and
   require `commit.message` to be one string equal to the candidate.
7. Only after those validations succeed, run the merge with the exact subject and resolved head SHA:

    ```powershell
    gh pr merge $pr.number --squash --subject $subject --match-head-commit $pr.headRefOid --body-file <body-file>
    ```

   Do not omit `--subject`, even if a CLI default currently appears to match the PR title.
8. Verify the stored commit message and trailers after merge. Preserve the
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
   - Require each expected trailer's full `Token: value` line exactly once in
     the parsed stored message; do not accept a matching trailer token with a
     different value.
   - Reject any additional stored `Co-authored-by:` line that is not in the
     approved set.
   - Require the stored first line to contain the exact `(#<pull request
     number>)` suffix from the candidate subject.
   Treat this as a secondary check, not a substitute for pre-merge validation.
