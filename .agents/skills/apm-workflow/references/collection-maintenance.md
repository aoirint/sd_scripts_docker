# Maintain Packaged Skill Deployments

## 3.1 Maintain a packaged Skill collection

Apply this section only when a repository publishes Skill copies in both an
authoring target such as `.agents/skills/` and a package directory such as
`.apm/skills/`.

1. Identify the canonical source and each distributed copy. Use a supported
   generator when one exists; otherwise update every copy in the same change.
2. Keep validation artifacts out of canonical package trees before locking or
   deployment. Run import-based validators with bytecode writes disabled, such as
   with `PYTHONDONTWRITEBYTECODE=1`, or against a disposable copy. Inventory ignored
   as well as tracked files for transient caches, and remove only exact task-created
   artifacts. If a transient file enters a candidate ledger, discard that candidate
   and regenerate from a clean canonical tree. Restore the prior reviewed lockfile
   first when one exists; for a first lock, remove only the exact uncommitted
   task-created candidate. Do not patch, normalize, or publish a contaminated ledger.
3. Compare relative file sets and content hashes before release. A missing,
   extra, or different file is a release blocker, not a cosmetic discrepancy.
4. After `apm install --frozen`, record the installer-reported target and
   verify the named Skill at that actual target, rather than assuming a
   configured or conventional directory was used.
5. If `apm audit --ci` resolves a different target root, do not call the audit
   a pass or failure without direct evidence. Record the discrepancy, verify
   the installed file and lockfile hashes directly, and report the observed
   behavior for follow-up.
6. After deployment, review the staged diff as well as the working tree. An
   installer can rewrite unchanged text with a different line ending; stage
   only the expected manifest, lockfile, canonical, and deployed outputs, then
   use `git diff --cached --check` and a content review to distinguish a real
   generated-file delta from line-ending noise.

## 3.2 Rename or remove packaged local Skills

Apply this section when a local packaged Skill is renamed, consolidated, or
removed. Treat it as a deployment-ledger change, not a documentation-only
rename.

1. Before editing, inventory the retiring and destination source folders,
   deployed paths, resource moves, README index rows, repository references,
   and every matching entry in `apm.lock.yaml` (`deployments`, deployed-file
   lists, and local deployed-file hashes).
2. Move or remove canonical content and update callers first. Preserve
   deterministic scripts and directly linked references when their behavior
   remains supported; do not recreate them gratuitously. Regenerate every
   managed deployment from the canonical source rather than hand-editing
   `.agents/` output.
3. Regenerate the lockfile from scratch with the selected reviewed APM CLI
   whenever the existing ledger still names a retired deployment path, or when
   a normal lock/install cycle cannot prove that removed paths left the ledger.
   Do not patch lockfile hashes or deployment entries by hand. Review that no
   retired path remains. Complete and review the
   [rebuilt deployment ledger](cli-selection.md#12-complete-a-new-or-rebuilt-deployment-ledger)
   before running `apm install --frozen`.
4. Run `apm install --frozen` and `apm audit --ci`. Treat missing expected
   files, orphaned retired files, unintegrated outputs, or a source/deployed
   file-set mismatch as release blockers. If the available generator cannot
   remove a retired generated path, stop and record the tool limitation rather
   than claiming the deployment is clean.
5. Review the complete canonical, deployment, and lockfile diff together.
   Confirm the installed target contains the destination Skill exactly once and
   no retired Skill name, resource, or hash record remains.
