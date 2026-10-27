# Resumable Handoff Notes

Use this optional outline when the user requests a handoff or chooses one as a useful output.
Write it in the requested destination, retaining only information needed to resume the work.
An ordinary prose edit does not require a separate handoff or a standing work log.

## Select the useful context

- State the current purpose, reader, scope, and canonical source or destination.
- Record consequential decisions as adopted, rejected, or pending. Include exact wording only
  when the wording itself matters; otherwise summarize the choice and its reason.
- Describe the changes made and why. Link to their current canonical location rather than
  duplicating maintained technical facts.
- Separate verified results from proposals, assumptions, unavailable evidence, and blockers.
  Identify the check or decision needed to resolve each remaining item.
- Give the next resumption point, including any prerequisite or approval still needed.

Use `domain-architecture-docs-workflow` when canonical placement or technical evidence needs to be
decided. Apply `security-check`'s disclosure boundary before sharing the note. Retain the user's
choice to shorten or omit a record; the outline is not a requirement to archive the conversation.

## Outline

Use only the sections that help the next reader act:

```markdown
## Purpose and current sources

<Purpose, audience, scope, and canonical source or destination.>

## Decisions

<Adopted, rejected, or pending choices; reasons and exact wording when consequential.>

## Changes and verification

<Changes and rationale, current locations, checks actually run, and their results.>

## Open items

<Unverified claims, blockers, pending decisions, and what would resolve them.>

## Resume here

<Next action, prerequisites, and required approval.>
```

## Resume against current evidence

Compare the note with the current request, repository instructions, canonical files, and relevant
change state before acting. Identify superseded decisions explicitly. A note can point to earlier
evidence or approval, but does not create authorization or establish that a planned change ran.
Check the actual state before repeating an operation whose earlier outcome is uncertain.
