---
name: skill-quality-check
description: >-
  Quality-check Agent Skills for trigger clarity, scope, structure, progressive
  disclosure, domain separation, validation, and scenario-readiness. Use when
  creating, updating, reviewing, or splitting Agent Skills, SKILL.md files, skill
  references, bundled scripts, or skill metadata.
---

# Skill Quality Check

## When to Use

- Use this skill when creating, updating, or reviewing an Agent Skill.
- Use this skill before committing changes to any `SKILL.md`, `references/`, `scripts/`,
  `assets/`, or `agents/openai.yaml` file inside a skill folder.
- Use this skill with scenario-based validation after creating or substantially revising a skill.

## Goals

- Keep each skill focused on one reusable job with clear trigger boundaries.
- Make `description` concise, specific, and useful for implicit skill selection.
- Keep `SKILL.md` lean: core workflow in the body, detailed variants in directly linked
  `references/`, deterministic helpers in `scripts/`, reusable output materials in `assets/`.
- Separate project-specific or domain-specific knowledge into dedicated domain skills or reference
  files instead of mixing it into general workflow skills.
- Use `security-check` when a skill describes security-sensitive behavior, external
  executable artifacts, dependencies, CI actions, containers, vendored files, secrets, permissions,
  unsafe defaults, or supply-chain policy.
- Preserve a consistent top-level structure: `When to Use`, `Goals`, and `Workflow` unless a local
  skill has a stronger established pattern.
- Require scenario-based validation for new or materially revised skills.

## Workflow

1. Read the changed skill files and nearby related skills.
2. Check description/body consistency before scenario validation:
   - Compare the `description` trigger promise with the scope actually covered by `SKILL.md`.
   - Reconcile any mismatch before treating scenario results as reliable.
   - State whether adjacent scopes, such as publishing, deployment, or side-effecting operations,
     are in scope, guidance-only, or require explicit confirmation.
3. Check frontmatter:
   - `name` uses lowercase letters, digits, and hyphens.
   - `description` states what the skill does and when to use it.
   - Trigger words are front-loaded enough to survive shortened skill lists.
4. Check scope:
   - One primary job per skill.
   - No unrelated project policy, domain knowledge, or historical notes in a general-purpose skill.
   - Split domain knowledge into a dedicated skill or a directly linked reference file when it would
     otherwise make the skill broad or stale.
   - Reference `security-check` instead of duplicating partial security or supply-chain
     policy unless the target skill owns a narrower implementation detail.
5. Check structure:
   - Prefer `When to Use`, `Goals`, and `Workflow` for Agent Skills.
   - Keep required steps explicit, ordered, and written as imperatives.
   - Match specificity to risk: flexible guidance for judgment-heavy work, exact commands or scripts
     for fragile operations.
   - Use `document-quality-check` for explanatory prose. Preserve
     skill-specific nuance such as trigger boundaries, scope, ordering, risk
     level, and domain separation.
6. Check progressive disclosure:
   - Keep `SKILL.md` short enough to scan quickly.
   - Link every optional reference directly from `SKILL.md`; avoid nested reference chains.
   - Add a table of contents to reference files longer than 100 lines.
   - Do not duplicate detailed guidance between `SKILL.md` and references.
7. Check bundled resources:
   - Include `scripts/` only for repeatable or fragile automation, and test representative scripts.
   - Include `assets/` only for files used in outputs.
   - Remove placeholder or auxiliary files that do not directly support the skill.
8. Check metadata alignment:
   - Check every changed skill folder for `agents/openai.yaml`. For new skills, create it unless
     the repository has an explicit reason to omit app metadata for that skill.
   - Treat a missing `agents/openai.yaml` as a blocking gap, not as an optional follow-up.
   - Keep `agents/openai.yaml` aligned with `SKILL.md` trigger wording, scope, and expected output.
   - Include `interface.display_name`, `interface.short_description`, and
     `interface.default_prompt` when creating app metadata.
   - Update or remove metadata that no longer directly supports the skill.
9. Validate and iterate:
   - Run the available skill validator, if the project has one.
   - Run spelling, formatting, or project checks appropriate to Markdown-only changes.
   - For each new or substantially revised skill, prepare two or three realistic validation
     scenarios before evaluation, including at least one median case and one edge or out-of-scope
     case.
   - Give each scenario at least one critical requirement and evaluate with a fresh executor.
   - Record unclear points, discretionary fill-ins, and repeated failure patterns.
   - Apply one related theme of fixes per iteration.
   - Stop only after convergence, divergence, or a stated resource cutoff. Treat convergence as two
     consecutive rounds with no new unclear points and no meaningful accuracy or effort improvement.
10. Record verification:
   - Note external sources consulted, why they were needed, and how their guidance was applied.
   - Note that each changed skill folder has `agents/openai.yaml`, or explain the repository policy
     that intentionally omits it.
   - Note whether `security-check` was used for security-sensitive skill content.
   - Note whether docs, changelog, PR notes, or follow-up domain skills are needed.

When validating with scenarios, keep the report categories separate:

- **Target skill findings**: problems in the skill being reviewed, such as
  description/body mismatch, repository-specific leakage, stale metadata,
  missing validation, or unsupported bundled files.
- **Input gaps**: unavailable source files, exact command text, unknown provenance, or missing
  metadata. Record these as assumptions or blockers.
- **Skill-quality-check ambiguity**: places where this skill did not say what to inspect or how to
  decide. Only these count as unclear points for improving `skill-quality-check` itself.

## Reference Checks

Read [references/authoring-best-practices.md](references/authoring-best-practices.md) when a change
touches structure, trigger design, bundled resources, domain separation, or scenario validation.
