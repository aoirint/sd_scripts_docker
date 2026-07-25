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
2. Verify the first-line format, blank-line structure, body placement, and
   footer placement.
3. Check that the type, optional scope, breaking-change marker, and short
   description match the dominant intent of the change.
4. Check that any body explains useful context, motivation, or impact instead
   of repeating the summary.
5. Check required footer or trailer metadata, including `BREAKING CHANGE` and
   AI agent `Co-authored-by:` trailers when applicable.
6. Before an operation creates or rewrites a commit, validate the exact
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
7. Recommend the smallest correction that makes the message valid and accurate.
8. If the diff contains multiple unrelated logical changes, recommend splitting
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
