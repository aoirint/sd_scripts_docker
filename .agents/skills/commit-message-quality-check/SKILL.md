---
name: commit-message-quality-check
description: >-
  Review or draft repository commit messages for Conventional Commits format,
  accurate change summaries, breaking-change footers, and required attribution
  trailers. Use before creating, amending, or validating a commit.
---

# Commit Message Quality Check

## Goals

- Check commit messages against Conventional Commits 1.0.0.
- Check repository attribution policy, including AI agent co-author trailers.
- Recommend message changes that fit the actual staged or committed change.
- Keep commit guidance focused on message quality, not on reviewing the
  underlying code or documentation diff.

Reference:

- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
- GitHub co-authored commits:
  <https://docs.github.com/articles/creating-a-commit-with-multiple-authors>

## Workflow

1. Read the proposed message and, when available, the staged diff or
   commit diff it describes.
2. If the message is a GitHub pull request squash-merge commit, obtain the
   canonical pull request title and number from GitHub. Require the first line
   to be exactly `<pull request title> (#<pull request number>)`; do not rely
   on a CLI default or accept a title that omits the number. Verify that this
   exact candidate is passed as the merge command or API payload's subject,
   rather than merely being prepared for comparison.
3. Verify the first-line format, blank-line structure, body placement, and
   footer placement.
4. Check that the type, optional scope, breaking-change marker, and short
   description match the dominant intent of the change.
5. Check that any body explains useful context, motivation, or impact instead
   of repeating the summary.
6. Check required footer or trailer metadata, including `BREAKING CHANGE` and
   AI agent `Co-authored-by:` trailers when applicable.
7. For a squash merge or other remote commit creation, determine the complete
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
8. Before an operation creates or rewrites a commit, validate the exact
   candidate message that the operation will receive:
   - Build it from the same subject and body file or bytes that will be passed
     to the command or API.
   - Reject literal `\n` or `\r\n` text where real line breaks are intended.
   - Write the exact candidate bytes to a temporary file and pass that file
     directly to `git interpret-trailers --parse`; do not pipe a shell string
     that may transform line endings. Require every expected trailer to appear
     exactly once.
   - For a structured API payload, apply the literal-escape check before
     serialization and verify that decoding the serialized payload reproduces
     the validated subject and body. JSON escaping on the wire is not itself a
     failure.
   - In PowerShell, do not assign line-oriented native-command output directly
     when verifying multiline text. Capture the complete structured response
     as raw text, decode it, assert that the selected value is a `[string]`,
     and only then compare it with the candidate.
   - Do not perform the mutation until the candidate passes.
9. Recommend the smallest correction that makes the message valid and accurate.
10. If the diff contains multiple unrelated logical changes, recommend splitting
   the commit when practical.

## Format

Verify that the first line uses:

```text
<type>[optional scope][optional !]: <description>
```

Verify the blank-line structure:

- An optional body starts after one blank line.
- Optional footer lines start after one blank line from the body.

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

## Components

- `type`: required token that communicates the kind of change.
- `scope`: optional noun in parentheses that names the affected area, such as
  `interop`, `build`, `docs`, or `input`.
- `!`: optional marker immediately before `:` for a breaking change.
- `description`: required short summary after `:` and one space. Use imperative
  mood, lowercase after the type unless a proper noun is needed, and no
  trailing period.
- `body`: optional free-form explanation of what changed and why. Start it one
  blank line after the description.
- `footer`: optional trailer-style metadata. Use tokens such as `Refs`,
  `Reviewed-by`, `Co-authored-by`, or `BREAKING CHANGE`.

## Breaking Changes

Mark breaking changes with either:

```text
feat(api)!: remove legacy save endpoint
```

or:

```text
feat(api): remove legacy save endpoint

BREAKING CHANGE: legacy save endpoint is no longer available.
```

`BREAKING CHANGE` must be uppercase when used as a footer.
`BREAKING-CHANGE` is equivalent when used as a footer token.

## AI Agent Co-Author Trailers

When an AI agent materially created or changed content in the commit, check for
an appropriate `Co-authored-by:` trailer unless repository or user instructions
explicitly say not to add one. Do not add AI co-author attribution for passive
lookup, review-only advice, formatting a user-written message, or incidental
autocomplete unless the project policy requires it.

Use this selection order:

1. Prefer an explicit repository, organization, tool, or user-provided
   attribution string.
2. If the active agent/tool has a documented or configured default, use that
   exact value.
3. If no exact value is available, use a stable, privacy-preserving service
   identity for the agent type.
4. If the agent identity is unknown, use a generic local policy value only when
   the repository defines one; otherwise omit the trailer and note the missing
   attribution source.

Known default examples:

- Codex: `Co-authored-by: Codex <noreply@openai.com>`
- Claude Code: `Co-authored-by: Claude <noreply@anthropic.com>`
- GitHub Copilot: `Co-authored-by: Copilot <copilot@github.com>`

If multiple AI agents materially contributed, add one `Co-authored-by:` trailer
per agent. Put each trailer on its own line in the footer block, with no blank
lines between consecutive trailer lines. Keep `BREAKING CHANGE` before ordinary
metadata when it explains the change, and keep co-author trailers at the end
unless another project rule says otherwise.

For squash merges or other remote commit creation, do not trust an escaped
command-line string or a post-merge inspection as the primary check. Validate
the exact pre-mutation payload as described in the workflow, then verify the
stored commit message after the operation as a secondary check.

## Human Co-Author Trailers

Treat the author of an implemented issue and a material design or snippet
provider as co-authors by default. Keep their `@login` and numeric GitHub user
ID in the PR attribution record, so a reviewer can mark a candidate `Not
applicable` before merging. Use the contributor's explicitly supplied
GitHub-provided noreply email by default; never synthesize a noreply address
from their account ID and login. Use a Public Email only if the contributor
explicitly directs that choice and GitHub currently exposes the exact address
as public. An existing trailer is reusable only when its GitHub author
association proves the same account. If no exact attributable email is
available, retain `Needs identity` in the PR and stop rather than using a
legacy noreply address or inventing one. Preserve every
resolved line in the same candidate and
stored-message checks used for AI co-authors.

Reviewing or approving a PR alone is not material authorship. Before squash
merging, inspect every PR-head commit and applied review suggestion. For each
head-only commit whose material change remains in the final diff, carry its Git
author and every existing `Co-authored-by:` identity into the expected trailer
set unless the identity is already the PR creator's primary Git author.
Preserve exact existing trailers where available; otherwise resolve the GitHub
account under the human-trailer rule. GitHub records the suggestion provider and
the person who applies an accepted suggestion as co-authors of its generated
commit; carry both identities when that suggestion remains in the final diff,
except an identity already represented as the PR creator's primary Git author.
Record the source commit SHA or review URL in the PR attribution block. If a
head commit, applied status, contributor set, or final-diff presence is
uncertain, mark it `Needs review` and stop the merge.

## Type Selection

Check that the type matches the dominant intent:

- `feat`: add a user-visible feature or capability. SemVer: minor.
- `fix`: correct a bug. SemVer: patch.
- `perf`: improve runtime performance without changing behavior.
- `refactor`: change code structure without adding features or fixing bugs.
- `docs`: change documentation, comments intended as documentation, or repository guidance.
- `test`: add, update, or remove tests.
- `build`: change build scripts, project files, packaging, dependencies, or
  generated build configuration.
- `ci`: change continuous integration workflows or automation.
- `style`: formatting-only change with no behavior impact.
- `chore`: maintenance that does not fit the other types and does not affect
  source, tests, build, docs, or CI in a more specific way.
- `revert`: revert previous commits; include references in the body or footers when useful.

Prefer the most specific type.
If one logical change needs multiple types, recommend splitting it into multiple
commits when practical.

## Examples

```text
docs: add agent workflow skills
```

```text
refactor(interop): remove redundant role checks
```

```text
fix(input): ignore hotkeys while local player is busy
```

```text
feat!: require current game interop adapters

BREAKING CHANGE: legacy versioned adapters are no longer loaded.
```

```text
docs: document agent attribution policy

Co-authored-by: Codex <noreply@openai.com>
```
