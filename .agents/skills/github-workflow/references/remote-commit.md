# Remote Commit and Pull Request Merge Contract

Read this reference before a squash merge, another GitHub pull-request merge,
or other remote commit creation. Ordinary local commits and PR body edits use
their own workflows; they do not require merge preparation.

## Contents

- [Confirm the operation](#confirm-the-operation)
- [Resolve attribution](#resolve-attribution)
- [Validate the exact payload](#validate-the-exact-payload)
- [Execute and read back](#execute-and-read-back)
- [Handle an uncertain outcome](#handle-an-uncertain-outcome)

## Confirm the operation

1. Confirm the authorized action, target repository and pull request or remote
   ref, intended commit method, and exact head SHA before changing remote state.
   Preparing a message or reviewing a PR does not authorize merging it.
2. Apply `github-workflow`'s private repository disclosure preflight to the
   complete candidate before the first remote write. Include the exact commit
   subject, body, trailers, diff, and attached or generated outputs. Do not send
   private-resource identifiers or existence disclosures to a public or
   potentially public destination.
3. For a GitHub PR squash merge, obtain the canonical PR title and number from
   GitHub. Require the subject to be exactly `<pull request title> (#<number>)`.
   Pass that exact value through the merge command's `--subject` option; a
   candidate file or CLI default is insufficient.
4. Resolve the exact PR head SHA and pass it with `--match-head-commit` when
   `gh pr merge` creates a squash or merge commit.
5. Check every active worktree before a PR merge command performs local branch
   cleanup. Do not let a hosted-PR CLI switch to the default branch or delete
   a branch checked out by another worktree. Merge first, then perform any safe
   remote or local branch cleanup as a separate action.

## Resolve attribution

For a squash merge or other remote commit creation, determine the complete
applicable trailer set before writing the payload. Include the author of an
implemented issue and every material design or snippet contributor by
default, unless review marks the contributor not applicable. Retain the
GitHub account and exact attributable email used to resolve each human
trailer. Use the contributor's explicitly supplied GitHub-provided noreply
address by default. Use a Public Email only when the contributor explicitly
directs its use and the current GitHub user response exposes that exact
email; record the choice in the PR attribution block. Never synthesize a
noreply address from `@login` or an ID. If the exact email cannot be
resolved, retain `Needs identity` and stop rather than using a legacy
noreply form. Put every expected
`Co-authored-by:` line in the body file passed to the merge command, retain
each full `Token: value` line exactly once, and verify that same set in the
stored commit; do not treat a matching token with a different value as
preserved or permit an unapproved additional `Co-authored-by:` line.
When the associated PR has a proposed-attribution block, require every
payload trailer to match an `Included` exact line there, omit only `Not
applicable` candidates, and stop for `Needs identity` or unreviewed changes.
Any uncertainty about a candidate's contribution, applicability, GitHub
account, numeric ID, resolved trailer, or review status blocks the merge;
do not omit, guess, or downgrade that candidate to proceed.
Apply role precedence before selecting trailers: the PR creator is the
GitHub-squash primary Git author; a final-diff head-commit author,
implemented-issue author, or material design/snippet contributor is a
trailer candidate only when distinct from that primary author. Reviewers and
merge actors are not candidates from those roles alone. Preserve an
independently evidenced existing trailer even when another role would not
create one.
For a GitHub-hosted squash merge, expect GitHub to record the PR creator as
the primary Git author even when another person performs the merge. This is
platform metadata, not proof of contribution: the creator may be neither an
author nor co-author of the PR-head commits. Do not add either the PR creator
or merger as a `Co-authored-by:` solely because of those roles; retain the PR
`mergedBy` value separately and verify the stored GitHub author association
against the PR creator. If the creator is not a material contributor in the
final diff, mark the mismatch `Needs review` and stop until a maintainer
confirms the intentional attribution or selects another authorized
integration path.

Before squash merging, inspect every PR-head commit and applied review suggestion.
For each head-only commit whose material change remains in the final diff, carry
its Git author and every existing `Co-authored-by:` identity into the expected
trailer set unless already represented by the PR creator's primary Git author.
Preserve exact existing trailers where available; otherwise resolve the GitHub
account under the human identity rule above.

GitHub records the suggestion provider and the person who applies an accepted
suggestion as co-authors of its generated commit. Carry both identities when
that suggestion remains in the final diff, except an identity already represented
as the PR creator's primary Git author. Record the source commit SHA or review
URL in the PR attribution block. If a head commit, applied status, contributor
set, or final-diff presence is uncertain, mark it `Needs review` and stop the merge.

Use the repository's required AI attribution and
`commit-message-quality-check`'s AI identity selection rules for material AI
contributions. Reviewing or approving a PR alone is not material authorship.

## Validate the exact payload

Use `commit-message-quality-check` for Conventional Commits format, message
accuracy, breaking changes, and required attribution. Before the operation
creates or rewrites a remote commit:

1. Build the exact candidate from the same subject and body file or bytes that
   will be passed to the command or API. Reject literal `\n` or `\r\n` text
   where real line breaks are intended.
2. Write the exact candidate bytes to a temporary file and pass that file
   directly to `git interpret-trailers --parse`. Do not pipe a shell string
   that may transform line endings. Require every expected full trailer line
   exactly once, with no unapproved additional `Co-authored-by:` line.
3. For a structured API payload, perform the literal-escape check before
   serialization. Decode the serialized payload and verify that it reproduces
   the validated subject and body; JSON escaping on the wire is not itself a
   failure.
4. For `gh pr merge`, test the stored-message JSON parser with a fixture before
   merging. Use the same validated subject and body file in the merge command.
5. In PowerShell, capture the complete structured response as raw text, decode
   it, and assert that the selected value is a `[string]` before comparing it
   with the candidate. Do not assign line-oriented native-command output when
   verifying multiline text.
6. Do not perform the mutation until the candidate and applicable identity,
   approval, head, and worktree guards pass.

## Execute and read back

Execute only the reviewed operation. For a PR merge, use the validated subject,
body file, and exact-head guard. After merging, read `commit.message` from
`repos/{owner}/{repo}/commits/{sha}` using raw JSON and compare it with the
validated candidate. Confirm the stored squash subject retains the exact PR
number suffix and the expected full trailer set. Verify the stored GitHub
author association against the PR creator and retain `mergedBy` separately.

Treat stored-message verification as secondary to pre-mutation validation.
Report an unverified or mismatched field explicitly; a successful command
alone is not evidence that the complete stored payload matches.

## Handle an uncertain outcome

If the mutation result is uncertain, inspect the remote PR/ref and resulting
commit before deciding whether another attempt is safe. Do not repeat a merge
or commit-creation request merely because its response was unavailable. Report
the attempted target and operation, observed remote state, and remaining
uncertainty. Preserve the candidate for comparison instead of guessing that the
operation failed or succeeded.
