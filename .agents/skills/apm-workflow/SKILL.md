---
name: apm-workflow
description: Select a reviewed APM CLI version, then set up, pin, deploy, audit, and update APM-managed agent dependencies safely. Use when creating or editing apm.yml or apm.lock.yaml, choosing or installing APM, adding an Agent Skill, plugin, or MCP dependency, validating a pinned deployment, or preparing a cooldown-aware update proposal.
---

# APM Workflow

Keep agent context reproducible and reviewable. Select the newest reviewed APM
release that has completed the seven-day cooldown or has a manifest-recorded
maintainer exception for a specific unmet gate. Filesystem location and local
recency do not establish eligibility. Require full commit pins, lockfile
hashes, and review for every changed third-party dependency.

## When to Use

Use for APM CLI selection, project setup, pinned dependency deployment, packaged
Skill maintenance, or an update proposal. Classify the operation before loading
its detailed procedure.

## Common requirements

- Read repository policy, the manifest and lockfile, and the
  [reviewed bootstrap manifest](references/apm-bootstrap.json) before mutation.
- Preserve an existing `apm.yml`; do not run `apm init --yes`. Keep an
  unpublished consumer at `version: 0.0.0` until its versioning design is decided.
- Apply `security-check` to CLI and dependency code. Require full commit pins,
  content hashes, source/license review, and seven-day eligibility or the exact
  documented maintainer exception. An exception waives only its named gate.
- Select the reviewed eligible CLI by exact version, not PATH precedence or
  local recency. Do not change PATH or the active installation without explicit
  authorization for that user-environment change.
- Treat canonical source, generated deployment, ownership ledger, and notices
  as one reviewable result. Regenerate managed output rather than hand-editing it.
- Never use `--force`, `--allow-insecure`, or an insecure HTTP source unless an
  explicit documented exception authorizes it.
- Keep discovery, approval, and application separate. Do not silently update a
  pin, bootstrap version, or deployment while preparing a proposal.

## Workflow

1. Read [CLI selection and lockfile migration](references/cli-selection.md)
   before running mutating APM commands. Inventory the repository and available
   executables, select the eligible exact version, and resolve lockfile-version
   compatibility. If no manifest exists, use its interactive setup branch.
2. Select every applicable operation below. Read its procedure before acting;
   the table routes detail and does not make an applicable gate optional.

   | Operation or condition | Required procedure |
   | --- | --- |
   | Selected CLI is absent; temporary artifact or explicitly requested persistent installation | [CLI acquisition](references/cli-acquisition.md) |
   | Review or refresh the bootstrap; normally eligible or exact cooldown-exception candidate | [Bootstrap refresh](references/bootstrap-refresh.md) |
   | Add or deploy a remote Skill, prompt, agent, plugin, hook, or MCP dependency | [Dependency deployment](references/dependency-deployment.md) |
   | Maintain distributed Skill copies, verify actual target/hash parity, rename, consolidate, or remove local Skills | [Collection maintenance](references/collection-maintenance.md) |
   | Discover updates, prepare a proposal, or apply only an approved dependency update | [Dependency updates](references/dependency-updates.md) |
   | Reconcile notices, remove a third-party dependency, or complete the handoff | [Notices and completion checks](references/completion.md) |

3. Follow the selected procedure's ordering and stop conditions. Before a
   lockfile rebuild, preserve ownership evidence and back up only exact verified
   generated collision paths using the migration procedure. A collision,
   missing selected output, unexpected lock rewrite, integrity failure, or
   unresolved target discrepancy is not a clean deployment.
4. After deployment, review refs, hashes, generated output and staged changes;
   run the required frozen-install and audit checks, and verify the actual
   installer target. Use [notices and completion checks](references/completion.md)
   for every handoff and distinguish completed verification from blockers.

## Reference sources

Consult [upstream sources](references/upstream-sources.md) for current official
configuration, installation, migration, update, release, and security guidance.
The [bootstrap manifest](references/apm-bootstrap.json) remains this Skill's
source of truth for its reviewed CLI version, artifact names, and checksums.
