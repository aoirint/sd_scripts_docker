# Agent Skill Authoring Best Practices

## Purpose

Use this reference when a skill change needs more than the short checklist in `SKILL.md`. It
summarizes stable guidance from agent skill documentation and adapts it into a repository-neutral
review checklist.

## Contents

- Frontmatter and trigger quality
- Scope and domain separation
- Progressive disclosure
- Workflow design
- Resource selection
- Validation and scenario testing

## Frontmatter and Trigger Quality

- Keep exactly one `name` and one `description` in `SKILL.md` frontmatter unless the local platform
  explicitly requires more.
- Use hyphen-case skill names with lowercase letters, digits, and hyphens.
- Write `description` in third person, with the main use case and trigger terms early.
- Include both positive triggers and practical boundaries. The body is loaded only after selection,
  so do not rely on body-only "When to Use" text for discovery.
- Check candidate user prompts against the description:
  - Obvious in-scope prompts should select the skill.
  - Adjacent but out-of-scope prompts should not select it unless paired with another skill.

## Scope and Domain Separation

- Keep one primary job per skill. A broad skill should coordinate smaller skills or point to
  references instead of absorbing every detail.
- Keep general workflow skills free of project-specific paths, product facts, business rules,
  temporary status, or release-specific knowledge.
- Put domain knowledge in one of these places:
  - A dedicated domain skill when the knowledge changes how the agent should work.
  - A directly linked reference file when the knowledge is detailed but optional.
  - Repository docs when the information is primarily human-maintainer documentation.
- Prefer splitting when a skill starts mixing reusable procedure with volatile facts, provider
  matrices, schemas, or product-specific examples.

## Progressive Disclosure

- Treat `SKILL.md` as the overview and default workflow.
- Move detailed variants, examples, schemas, and provider-specific instructions into directly
  linked files under `references/`.
- Keep references one level from `SKILL.md`; nested references are easy to miss during partial reads.
- Add a table of contents to reference files longer than 100 lines.
- Avoid duplicating the same rule in both `SKILL.md` and a reference. Keep the rule in the smallest
  place that is reliably loaded when needed.
- Remove placeholder `README.md`, quick references, changelogs, or process notes from skill folders
  unless the skill explicitly uses them as output assets.

## Workflow Design

- Prefer `When to Use`, `Goals`, and `Workflow` for repository skills so agents can scan them
  consistently.
- Use ordered steps for operations where skipping validation changes the result.
- Match instruction strictness to risk:
  - Use flexible guidance when multiple approaches are valid.
  - Use templates when output shape matters.
  - Use exact commands or scripts when the operation is fragile or easy to perform inconsistently.
- State required inputs, outputs, and completion criteria.
- Keep examples short and realistic. Add examples only when they prevent a likely misread.
- Avoid time-sensitive guidance unless it is framed as historical context or points to a maintained
  source.

## Resource Selection

- Use `scripts/` for deterministic, repeated, or fragile operations. Test representative scripts
  after editing them.
- Use `references/` for detailed material that should be loaded only for relevant variants.
- Use `assets/` for templates, images, fonts, starter files, or other output materials that do not
  need to be read into context.
- Keep `agents/openai.yaml` aligned with `SKILL.md` when present. Treat it as optional metadata, not
  a substitute for a clear `description`.

## Validation and Scenario Testing

- Run any available structural validator for the skill folder.
- Review the description/body consistency before scenario evaluation.
- For each new or substantially revised skill, use scenario-based validation:
  - Prepare two or three realistic scenarios before dispatching evaluators.
  - Include at least one critical requirement per scenario.
  - Use fresh evaluators for each iteration.
  - Apply one theme of fixes per iteration.
  - Maintain a failure-pattern ledger.
  - Stop only at convergence, divergence, or an explicit resource cutoff.
- Record what was tested, what was skipped, and why.
