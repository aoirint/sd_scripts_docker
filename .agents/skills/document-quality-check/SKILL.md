---
name: document-quality-check
description: >-
  Quality-check documentation, comments, release notes, issue text, pull request
  text, and Agent Skill prose for readability, structure, audience fit, and
  preserved nuance.
---

# Document Quality Check

## When to Use

- Use this skill when creating, updating, or reviewing explanatory prose.
- Use this skill for documentation, comments, release notes, issue text, pull request text, Agent
  Skill prose, changelog entries, and handoff notes.
- Use this skill together with domain-specific skills when those skills own the document type, such
  as changelogs, release notes, issues, pull requests, or Agent Skills.

## Goals

- Make prose easy to scan without flattening meaning.
- Preserve nuance that affects reader decisions, implementation safety, or release interpretation.
- Match structure to content: sentences for simple ideas, lists for enumerations, and nested bullets
  for grouped details.
- Keep wording aligned with the target audience and the local document style.

## Workflow

1. Classify the text audience before rewriting:
   - Developer-facing.
   - User-facing.
   - Maintainer-facing.
   - External-contract text.
2. Identify overloaded prose:
   - Sentences carrying multiple ideas, conditions, time references, confidence levels, or
     relationships.
   - Paragraphs that mix context, decision, evidence, and consequence.
   - List items that contain several facts, exceptions, examples, or follow-up notes.
3. Prefer lists when presenting enumerations.
   - Use inline prose only when the enumeration is short enough to read naturally or when the local
     document style clearly favors inline wording.
4. Split or restructure dense text when it becomes hard to scan.
   - Use separate paragraphs, parent bullets with indented child bullets, tables, or another local
     document pattern that makes each idea easy to review.
   - When a sentence continues the same paragraph or comment block, prefer starting it on a new
     physical line if the local format allows that without changing the rendered structure.
   - Treat sentence-per-line wrapping as a reviewability aid, not as a paragraph break. Do not
     apply it when it would make short prose, Markdown links, lists, tables, or formatter-controlled
     code comments harder to read.
   - Do not change wording strength, modality, tense, or voice only to make sentence wrapping work.
     Keep wording unchanged unless an independent readability issue justifies rewriting it.
5. Preserve the nuance that made the original wording important:
   - Certainty or confidence level.
   - Scope and applicability.
   - Timing and sequence.
   - Exception or limitation status.
   - Dependency or compatibility relationships.
   - Whether a statement is original, backfilled, inferred, superseded, withdrawn, or still
     unconfirmed.
6. Use as many short sentences or nested bullets as needed.
   - Do not force a fixed sentence count when the content needs a different shape.
7. Re-read the result as a whole.
   - Confirm it still answers the same question as the original wording.
   - Confirm each list or paragraph has one clear job.
   - Confirm the structure did not imply a stronger, weaker, broader, or narrower claim than the
     source material supports.

## Output Checklist

- Audience and document type were considered before rewriting.
- Enumerations are lists unless inline prose is clearer for the local context.
- Dense paragraphs or list items were split or intentionally left intact.
- Important certainty, scope, timing, relationship, and status nuances were preserved.
- The final text is easier to scan and still communicates the same claim.
