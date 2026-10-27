---
name: prose-quality-check
description: >-
  Review or revise explanatory prose for readability, local structure,
  audience fit, and preserved nuance. Use for wording in documentation,
  comments, release notes, issues, pull requests, changelogs, handoff notes,
  and Agent Skills after the document's purpose and factual ownership are known.
  Use domain-architecture-docs-workflow instead for repository-wide document
  maps, canonical ownership, technical evidence, coverage, or migration.
---

# Prose Quality Check

## Goals

- Make prose easy to scan without flattening meaning.
- Preserve nuance that affects reader decisions, implementation safety, or release interpretation.
- Match structure to content: sentences for simple ideas, lists for enumerations, and nested bullets
  for grouped details.
- Keep wording aligned with the target audience and the local document style.

## Responsibility boundary

Use this skill when the destination document, factual source, and ownership are already known and
the task is to improve how the text communicates. Do not use it to decide which repository
documents should exist, where a technical fact belongs, whether evidence is sufficient, or how a
documentation migration should preserve coverage. Use `domain-architecture-docs-workflow` for
those decisions, then return here to refine the resulting prose.

Do not silently repair unsupported technical claims while copyediting. Flag the evidence gap and
use the applicable documentation-system or domain-specific skill.

## Workflow

1. Classify the text audience before revising:
   - Developer-facing.
   - User-facing.
   - Maintainer-facing.
   - External-contract text.
2. Confirm the purpose, intended claim, factual source, and destination for this edit.
   Reuse context already supplied by the request or document; resolve only missing context that
   could change the edit. If ownership or evidence is disputed, stop prose-only revision at that
   boundary and report the gap.
3. Identify overloaded prose:
   - Sentences carrying multiple ideas, conditions, time references, confidence levels, or
     relationships.
   - Paragraphs that mix context, decision, evidence, and consequence.
   - List items that contain several facts, exceptions, examples, or follow-up notes.
   - Spatial or state conditions whose thresholds use different subjects or reference positions.
     Name the subject and reference in every independently readable item; do not rely on a
     deictic phrase such as "that position" when it could refer to more than one value.
   - Independently evaluated conditions phrased as though they were one conjunction. Keep them
     separate unless the factual source establishes that every part is required together.
4. Prefer lists when presenting enumerations.
   - Use inline prose only when the enumeration is short enough to read naturally or when the local
     document style clearly favors inline wording.
5. Split or restructure dense text when it becomes hard to scan.
   - Use separate paragraphs, parent bullets with indented child bullets, tables, or another local
     document pattern that makes each idea easy to review.
   - When a sentence continues the same paragraph or comment block, prefer starting it on a new
     physical line if the local format allows that without changing the rendered structure.
   - Treat sentence-per-line wrapping as a reviewability aid, not as a paragraph break. Do not
     apply it when it would make short prose, Markdown links, lists, tables, or formatter-controlled
     code comments harder to read.
   - Do not change wording strength, modality, tense, or voice only to make sentence wrapping work.
     Keep wording unchanged unless an independent readability issue justifies rewriting it.
6. Remove negative-space explanations that do not help the reader act or decide.
   - Prefer the current valid instruction or example when it is sufficient on its own.
   - Do not add a disclaimer that an old or omitted form is rejected merely because the
     implementation no longer accepts it.
   - Retain compatibility or migration context when the document owns that history or the audience
     needs it to update existing usage, interpret a release, or avoid a concrete transition risk.
7. Preserve the nuance that made the original wording important:
   - Certainty or confidence level.
   - Scope and applicability.
   - Timing and sequence.
   - Exception or limitation status.
   - Dependency or compatibility relationships.
   - Attribution and upstream relationships. Avoid a bare "official" when it
     could transfer authority from one project to another. For example,
     [uv documents](https://docs.astral.sh/uv/guides/install-python/) that it
     uses Astral's `python-build-standalone` distributions because Python does
     not publish official distributable binaries. Describe those artifacts as
     "Astral-published Python distributions used by uv," not as "official
     Python distributions" or "uv's official Python distributions."
   - Whether a statement is original, backfilled, inferred, superseded, withdrawn, or still
     unconfirmed.
8. Use as many short sentences or nested bullets as needed. Do not force a fixed sentence count
   when the content needs a different shape.
9. Re-read the result as a whole and use the domain-specific skill when one owns the document type.
   - Compare the actual edited destination and scope with the request and any wording or meaning
     the user asked to retain.
   - Confirm it still answers the same question as the original wording.
   - Confirm each list or paragraph has one clear job.
   - Confirm the structure did not imply a stronger, weaker, broader, or narrower claim than the
     source material supports.
10. When establishing repository-wide Markdown validation, copy
   `assets/markdownlint-cli2.yaml` to `.markdownlint-cli2.yaml` without
   deleting its rationale comments or changing its rule baseline. Add a local
   ignore or exception only for an evidenced generated, vendored, submodule,
   renderer, or document-format requirement, and document that reason beside
   the narrow override. When an applicable domain Skill owns a reviewed derived
   configuration, such as `hugo-quality-check`, use that asset instead of
   recreating its exceptions in the consumer. Use `github-actions-quality-check`
   to wire the repository-owned configuration into CI.

## Optional handoff notes

For a requested resumable handoff, use [handoff-notes.md](references/handoff-notes.md) to select the
decisions and open questions the next reader needs. Keep the existing factual-ownership boundary
and preserve the user's choice of destination and level of detail.

## Output checklist

- Audience and document type were considered before rewriting.
- Factual ownership and evidence gaps were not silently decided through wording changes.
- Enumerations are lists unless inline prose is clearer for the local context.
- Dense paragraphs or list items were split or intentionally left intact.
- Current instructions do not narrate irrelevant rejected or legacy alternatives.
- Important certainty, scope, timing, relationship, and status nuances were preserved.
- The final text is easier to scan and still communicates the same claim.
