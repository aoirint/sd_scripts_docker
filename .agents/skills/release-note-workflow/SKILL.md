---
name: release-note-workflow
description: >-
  Create, update, or review user-facing release notes. Use when deriving stable
  release notes from a canonical changelog or checking release-note readiness
  before publication.
---

# Release Note Workflow

## When to Use

- Use this skill when preparing or reviewing user-facing release notes.
- Use this skill when deriving stable release notes from canonical
  changelog entries.
- Use this skill when checking release-note readiness before publication.

## Goals

- Keep the user-facing release-note file as the cumulative stable release
  history, with the latest stable release at the top.
- Derive release notes from the canonical developer changelog instead of making
  a second source of truth.
- Rewrite stable release notes for users, focusing on behavior, installation,
  compatibility, update impact, known limitations, and security.
- Include a concise reason or background sentence for each user-visible change
  so users can understand why the change was made or why it affects them.
- Make version, source material, publication-channel requirements, and release
  readiness explicit before publication.

## Workflow

1. Locate the canonical developer changelog, user-facing release-note file,
   release version source, publication channel, release workflow, and
   verification command from repository evidence such as docs, configs, scripts,
   or workflow files. Report anything undiscoverable as a missing input or
   blocker.
   - Prefer evidence in this order: explicit maintainer input, release or
     publication docs, existing release-note history, workflow or config
     behavior, then scripts or source metadata.
   - When multiple candidate version sources, publication channels, tag
     conventions, or workflows conflict, report all candidates and treat the
     conflict as a blocker unless repository docs establish precedence.
   - Separate the discovered publication channel from the channel's release-note
     format requirements. If the channel is known but its required format is
     not, report the missing format as a blocker or required maintainer action.
     Do not infer format requirements from the channel name alone; use
     maintained docs, existing release-note history, workflow/config behavior,
     or maintainer input.
   - Use read-only evidence gathering for readiness reviews. Useful examples
     include reading version metadata, listing local tags with `git tag --list`,
     checking remote tags with `git ls-remote --tags <remote>`, inspecting
     workflow or release scripts for release-note inclusion, and reading docs
     for verification commands.
2. Read the exact stable release section in the canonical developer changelog.
   - If the exact canonical section is unavailable, write draft release notes
     and list the missing inputs instead of presenting the output as final.
   - If the UTC release date is missing, keep the output clearly marked as
     draft review text. Do not create a release-ready heading with `TBD`,
     `<date>`, or similar placeholder release metadata.
3. Confirm the release is stable:
   - Stable releases use a version without a prerelease suffix, such as
     `1.2.3`.
   - Prerelease versions, such as `1.2.3-alpha.1`, remain developer-facing and
     are not published as stable user-facing notes unless the publication
     channel explicitly supports prerelease notes.
   - Do not infer an intended stable version from a prerelease version without
     maintainer confirmation.
   - Accept prerelease support only from maintained publication-channel policy,
     release documentation, explicit maintainer input, or existing release-note
     history.
4. Roll prerelease entries into the next stable release when they still affect
   stable users.
5. Omit prerelease-only details from the user-facing release notes when
   they were internal, superseded before stable release, or useful only to
   maintainers.
   - When mentioning work that happened during a prerelease cycle in stable
     user-facing notes, prefer the stable release timing or stable version
     wording unless the prerelease identifier is user-visible and necessary.
     Keep exact prerelease identifiers in the canonical developer changelog.
6. Rewrite the stable entries around user-visible behavior, installation,
   compatibility, update impact, security, and known limitations.
   - Use `document-quality-check` for explanatory prose. Preserve
     release-note-specific nuance such as compatibility confidence, dependency
     relationships, and whether context is original, backfilled, inferred,
     superseded, or withdrawn.
7. For each user-visible change, include one concise reason or background
   sentence from the canonical changelog or maintainer input.
   - Apply this requirement to the target release being prepared or reviewed.
     Improve older cumulative entries when they are touched, but do not block
     the target release only because untouched historical entries lack
     rationale.
   - Good source material includes the user problem being solved, why behavior
     changed, compatibility or migration constraints, known limitation context,
     or why a release was yanked.
   - A sourced user impact statement can serve as the reason/background sentence
     only when it explains why users should care.
   - Use conservative negative-impact summaries, such as "no user-visible behavior changes",
     only when the canonical changelog or maintainer input supports that
     conclusion for the target release.
   - Generic source bullets such as documentation updates, dependency updates,
     crash fixes, or save-format changes are draft-only until the canonical
     changelog or maintainer input explains the user-facing benefit, risk,
     security impact, compatibility impact, or migration reason.
   - If a change lacks enough rationale or history, mark it as draft or a
     missing input instead of inventing an explanation.
8. Preserve user-critical notes in the user-facing release notes,
   including breaking changes, compatibility changes, installation or update
   notes, removals, deprecations, security fixes, yanked releases, and known
   limitations.
   - Use `security-check` when security-sensitive or supply-chain-sensitive release
     content needs review. Include maintainer-confirmed security impact, residual risk, or
     exception wording only when the canonical changelog or maintainer input supports it.
   - If user-facing notes backfill historical compatibility or limitation
     context for older releases, state that the information was added while
     preparing the relevant stable release. Avoid wording that makes the
     backfilled information sound like an original claim from the older
     release.
   - If a yanked release intentionally does not receive backfilled
     compatibility or limitation information, say so when neighboring releases
     do receive backfilled notes.
9. Keep test environment details in the canonical developer changelog. Include
   them in user-facing release notes only when they are needed as
   user-facing compatibility or support context.
   - Use maintainer-confirmed compatibility metadata from the canonical
     changelog, prior release notes, tested product/dependency versions, or
     explicit maintainer input. Do not invent compatibility claims.
   - Place user-facing supplemental metadata under a `Notes` section, with
     labeled bullets such as `Compatibility:` or `Known limitations:`, instead
     of creating standalone headings for metadata that is not a Keep a
     Changelog change category.
   - Preserve useful confidence differences in compatibility notes. Distinguish
     confirmed compatibility from best-effort "appears to work" notes,
     lower-confidence limited checks, and known issues.
   - Group companion tools, paired plugins, or required dependencies under the
     product/version they were tested with when that relationship matters for
     users.
   - Put `Notes` after all change-category sections within each release entry
     unless the publication channel explicitly requires another order.
10. Before publication, verify:
   - The user-facing release-note file has a stable version heading at
     the top, not `Unreleased`, and does not contain placeholder release
     metadata such as `TBD`.
   - The release version source contains the intended stable version.
   - The intended release version is not already present in a way that would
     collide with the planned stable release.
   - The intended stable tag, using the repository's documented tag convention,
     does not already exist locally or remotely. Existing versions or tags are
     blockers for stable publication until the maintainer chooses a new version
     or a documented edge-release path. If remote tag verification cannot be
     performed, report it as a release-readiness blocker.
   - The release workflow will publish or include the user-facing release-note
     file in the intended destination.
   - Manual publication is allowed, but report it as a manual workflow state
     and required maintainer action unless docs confirm automated inclusion.
   - Undocumented publication or a missing user-facing release-note destination
     is a blocker until docs or maintainer input confirm where release notes are
     published and how they are included.
   - The repository's documented build, release-note, or publication
     verification succeeds after any related changes.

## Review-Only Output

When the user asks for a release-readiness review instead of edits, do not edit
files. Return:

1. Current state of the user-facing release-note file, source changelog section,
   release version, local and remote tag readiness, publication-channel
   requirements, and release workflow inclusion.
2. Required updates before publication.
3. Blockers or missing inputs, especially stable version, UTC release date,
   exact canonical changelog text, and compatibility metadata.
4. Confirmation that no publishing side effects were performed.

For hypothetical readiness reviews, use explicit scenario facts or
maintainer-provided facts as the highest-priority evidence, even when they
conflict with the current checkout.

For readiness reviews, include a compact status matrix covering:

- Source changelog section.
- User-facing release-note destination.
- Version source and discovered version.
- Tag convention, intended tag, local tag state, and remote tag state.
- Publication channel and required release-note format.
- Release workflow inclusion.
- Verification command and result, or the missing verification input.

Classify review items as:

- `Blocker`: prevents release-ready notes or publication readiness.
- `Required update`: must be changed before publication but has a clear owner
  and path.
- `Required maintainer action`: needs maintainer confirmation or manual action.
- `Informational`: useful context that does not block readiness.

## Output Shape

- Release-ready stable notes use the publication channel's required heading
  format with a confirmed stable version and UTC release date.
- User-facing supplemental metadata that is not itself a change type, such as
  compatibility notes or known limitations, appears under `Notes` with labeled
  bullets. Do not use standalone `Compatibility`, `Test Environment`, or
  similar metadata headings unless the publication channel explicitly requires
  them.
- `Notes` appears after all change-category sections within each release entry
  unless the publication channel explicitly requires another order.
- Each user-visible change includes one concise reason or background sentence,
  sourced from the canonical changelog or maintainer input.
  This applies to the target release; untouched historical entries in a
  cumulative file are not blockers solely because they predate this rule.
- User-facing release-note files may include a short intro that identifies them
  as user-facing notes and points readers to the canonical developer changelog
  for internal implementation details, when both files are published or
  discoverable.
- Draft notes are clearly labeled as draft review text and list missing inputs
  before any proposed user-facing wording.
- Blockers name the missing or failed readiness item directly, such as stable
  metadata, user-facing release-note destination, tag convention, local or
  remote tag availability, publication channel, release workflow inclusion, or
  verification command.

## Boundaries

- This skill owns user-facing release notes and release-note readiness,
  not canonical developer changelog authoring.
- Use `changelog-workflow` first when the canonical developer changelog itself
  needs new entries or version-section changes.
- This skill may review publishing and tag readiness, but it does not perform
  publishing, release creation, or tag creation. Use a dedicated publishing or
  release workflow for those side effects.
- Treat missing stable metadata, missing tag convention, failed local or remote
  tag verification, missing publication-channel requirements, and missing
  prerelease-support evidence as release-readiness blockers.
- Keep private workspace paths, temporary worktree names, command transcripts,
  and authentication details out of public release-note text.
