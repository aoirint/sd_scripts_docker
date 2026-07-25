---
name: release-note-workflow
description:
  Create or review channel-specific release notes from a canonical changelog.
  Use when checking destination history or publication readiness.
---

# Release Note Workflow

## When to Use

- Derive user-facing release notes or a package changelog from the canonical developer changelog.
- Reconcile SemVer prerelease history, including alpha, beta, and release-candidate versions, with stable history across
  publication channels.
- Review whether release notes and their workflow or package integration are ready.

Do not author the canonical developer changelog or publish, tag, or upload a release.

## Goals

- Keep the developer changelog as the detailed source of truth.
- Make every public history accurate for its own destination.
- Keep source notes, release planning, validators, and the final published artifact synchronized.
- Avoid release-specific operational-documentation churn. Derive a version from
  its canonical source where needed; do not copy it into guides or workflows
  merely to describe the current release.

## Workflow

1. Locate the canonical changelog, notes destination, versions actually published to that destination, version source,
   tag convention, release workflow, final artifact, and verification command. Prefer maintainer input, published
   channel records, published docs, workflow/config behavior, then scripts or metadata. Report conflicts or missing
   evidence as blockers.
2. Establish the destination's public-history boundary:
   - Retain a versioned entry only when that version was actually published to the destination.
   - Preserve a public prerelease entry on a channel that published it.
   - Do not present a GitHub-only or other-channel-only prerelease heading as package-host history.
   - For a first public release, or when a destination skipped the prereleases, consolidate still-relevant user-visible
     outcomes into the next destination entry. Keep it under an explicit draft marker until version and date are
     confirmed; do not copy prerelease dates or imply those versions were available there.
   - Omit a generic `Unreleased` heading from a user-facing changelog that records published destination history. Keep
     it only when the destination intentionally shows draft content, and label that content as draft; remove it when a
     stable entry is finalized.
3. Read the exact canonical section that supplies the selected release. If it, the confirmed version, or UTC date is
   missing, produce clearly labeled draft review text and list the missing inputs; never use a release-ready placeholder
   heading.
4. Rewrite for users: behavior, installation or update impact, compatibility, breaking changes, removals, deprecations,
   security, known limitations, and one sourced reason or background sentence per user-visible change. Mark
   insufficiently sourced items as draft rather than inventing rationale.
5. Describe public package metadata using the destination's own history. A first public compatibility label is
   `Changed`, while `Fixed` requires an incorrect label or behavior that was publicly exposed on that destination.
   Keep internal correction and other-channel history in the developer changelog.
6. Use `Notes`, after change categories, for compatibility and limitation metadata unless the channel requires another
   layout. Source claims, preserve confidence levels, and group paired tools or dependencies with their tested
   product/version. Exclude test dependencies, diagnostics, and issue/PR IDs unless users need them.
   Keep a durable beta or known-limitation gate when it remains true; do not
   replace its concrete scope with a generic status notice. Update operational
   documentation only when the operation itself changes.
7. Synchronize the boundary with automation when the repository packages or generates the destination:
   - Make release planning select the correct notes source and heading rule for each release mode and destination.
   - Require a destination version heading only when that destination publishes the version; otherwise require an
     explicit draft section and reject headings that falsely claim other-channel releases.
   - Exercise both the accepted destination history and a mutation that inserts an invalid cross-channel heading.
   - Inspect the completed archive or stored release body, not only the source file. When packaging generates a
     manifest version, use the manifest embedded in that archive as publication evidence rather than a checked-in
     placeholder.
8. Use `prose-quality-check` for nuanced prose and `security-check` for security- or supply-chain-sensitive content.

## Check readiness

Before publication, confirm the version, destination-specific public-version set, documented tag convention, local and
remote tag availability, required note format, release-workflow inclusion, final-artifact content, and documented
verification result. When the workflow owns tag or release creation, require the expected tag to be absent locally and
remotely, then hand creation to that workflow rather than pre-creating it. Treat missing metadata, tag or remote-tag
verification, channel-history or prerelease-policy evidence, workflow inclusion, artifact inspection, or failed
verification as blockers. Do not publish, create tags or releases, or expose private paths, transcripts, or credentials.

For review-only requests, make no edits and return a compact status matrix for the source section, notes destination,
destination history, version and tags, format, workflow inclusion, artifact verification, required updates, and
blockers.
