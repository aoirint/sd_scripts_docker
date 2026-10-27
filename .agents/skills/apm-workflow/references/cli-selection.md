# APM CLI Selection and Lockfile Migration

- [Inspect before changing](#1-inspect-before-changing)
- [Preserve deployment ownership](#11-regenerate-a-lockfile-without-losing-deployment-ownership)
- [Complete the deployment ledger](#12-complete-a-new-or-rebuilt-deployment-ledger)

## 1. Inspect before changing

1. Locate `apm.yml`, `apm.lock.yaml`, `apm-policy.yml`, existing agent
   directories, and repository guidance. Read `apm_version` and
   `lockfile_version` from an existing lockfile before running a mutating APM
   command; treat them as compatibility evidence, not an instruction to keep an
   older CLI forever.
2. Read [the bootstrap manifest](apm-bootstrap.json). Its version is
   the newest APM release whose provenance, artifacts, checksums, publication
   date, and cooldown status this Skill has reviewed. When
   `cooldown_exception` is present, verify that it identifies the specific
   unmet gate, reason, approval time, and scope. Do not infer a broader waiver.
   Do not prefer a newer local `current`, `PATH`, project-local, or legacy
   executable merely because it is easier to find.
3. Keep an unpublished consumer project at `version: 0.0.0` in `apm.yml`.
   Change that version only after its distribution and versioning design is
   explicitly decided.
4. Inventory `apm` on `PATH`, project-local copies, and locations reported by
   the current official installation documentation and the platform's command
   resolver. Record each resolved executable and `--version`; path precedence
   does not override cooldown eligibility.

   Select the manifest version when it is already installed and invoke an
   off-PATH copy by absolute path. Do not modify PATH to satisfy one repository
   task. If the selected version is absent, use the verified temporary-artifact
   flow in [CLI acquisition](cli-acquisition.md) instead of installing it implicitly.
5. If the lockfile records an older APM version than the selected eligible
   version, capture it for comparison and regenerate it from scratch with the
   selected executable. Do not edit `apm_version` by hand: remove only the
   validated project lockfile, run `apm lock`, review the complete result, and
   then complete the deployment ledger as described below before the frozen
   install and audit checks. Treat substantial lock-format
   churn separately from a dependency update.
6. If the lockfile records a newer, not-yet-eligible APM version, do not execute
   that CLI merely to preserve its generator version. Report the mismatch and
   wait for maintainer direction before the destructive regeneration in step 5.
   After that direction, capture and regenerate the lock by the same procedure
   as step 5. Selecting the newest normally eligible CLI is not a cooldown
   exception.
7. Use the official lockfile migration guidance to understand schema changes,
   but do not substitute `apm install` for the from-scratch regeneration in
   step 5. Restore and stop if a frozen or allegedly read-only command rewrites
   the lockfile unexpectedly.
8. If `apm.yml` exists, preserve it. Do not run `apm init --yes`, because it
   overwrites an existing manifest.
9. If no manifest exists, inspect the repository's agent targets and run
   interactive `apm init` from the project root. Select only the targets the
   project actually uses; review the generated `apm.yml` before adding deps.
10. Treat the CLI and agent dependencies as supply-chain-sensitive code. Check the
   repository policy and any organization policy before proceeding.

### 1.1 Regenerate a lockfile without losing deployment ownership

When a CLI migration or ledger repair requires deleting and rebuilding the lockfile,
preserve the old lockfile's ownership evidence before removing it. Generated target
files can remain on disk after the ledger is gone; a new resolver may then classify
them as unmanaged local content, skip the collision, and silently omit a requested
Skill or resource from the new lockfile.

1. From the old lockfile, record the selected packages and Skill subsets, deployment
   owners, deployed paths, content hashes, target roots, and generator version. Compare
   this snapshot with `apm.yml` and the filesystem before changing anything.
2. Identify collisions in the actual target root. Distinguish paths owned by the old
   APM ledger from project-authored Skills, files owned by another package, and unknown
   local content. Never move or delete a path whose ownership is ambiguous.
3. Before removing the old lockfile, move only the exact, verified APM-owned generated
   collision paths to a task-specific temporary backup outside the repository. Preserve
   relative paths and hashes so the old deployment can be restored. Do not use
   `--force` to overwrite a collision or clear the entire agent target.
4. Remove only the validated project lockfile, regenerate it with the selected CLI,
   and complete the deployment ledger using section 1.2 before the frozen install.
   A skipped-file or collision warning is a blocker, even when the command exits
   successfully.
5. Compare the new package list, requested Skill subsets, deployed paths, and target
   roots with the manifest and the old snapshot. Every removed or added path needs an
   expected dependency or generator explanation; an unexpectedly missing selected
   Skill is lock-generation failure.
6. Run `apm audit --ci` and directly verify representative restored files and hashes.
   If regeneration, installation, comparison, or audit fails, restore the old lockfile
   and backed-up paths instead of accepting a partial deployment.
7. Delete the temporary backup only after the new lockfile, deployed output, diff, and
   audit all pass. Record any ownership ambiguity or tool collision behavior in the
   handoff.

### 1.2 Complete a new or rebuilt deployment ledger

APM 0.34.0 makes `apm install --frozen` strictly read-only for the lockfile.
`apm lock` resolves packages without deploying, so a new or rebuilt lockfile
can lack deployment records. A frozen install then fails **after deploying
files**; failure does not imply that the target is unchanged. See the
[0.34.0 release notes](https://github.com/microsoft/apm/releases/tag/v0.34.0).

Use this preparation only for an approved new deployment, source change, or
lockfile rebuild. Ordinary repeat installs and CI remain frozen.

1. Preserve the prior lockfile and exact verified owned output as in section
   1.1. For a first deployment, inventory existing target files and ownership
   before installing; do not overwrite unmanaged or ambiguously owned paths.
2. Run `apm lock` and review the resolved full SHAs, selected Skills, targets,
   and expected output changes. Record that snapshot. CLI migration alone does
   not approve dependency updates; stop on an unapproved resolution change.
3. Run `apm install` once without `--frozen` to populate the deployment ledger,
   retaining the reviewed scope and target options. Do not add `--update`,
   `--refresh`, or bypass flags. This step writes both output and the lockfile.
4. Compare the complete result with the snapshot, manifest, prior ledger, and
   approved source changes. Confirm dependency commits and selections did not
   change, every deployed path has the correct owner and hash, and target or
   generator differences are explained. A collision, skipped output, unexpected
   ref, or unexplained ownership/path change requires restoration and a stop.
5. Run `apm install --frozen`, verify that the lockfile bytes remain unchanged,
   then run `apm audit --ci` and verify actual target/file hashes. Review the
   complete diff before committing. Keep the backup until all checks pass.
6. On any failure, inspect partial output and restore the prior lockfile and
   exact backed-up files; remove only newly created paths whose ownership is
   proven by this attempt. If ownership or restoration cannot be established,
   stop and report the remaining state rather than clearing the target.
