# Repository Enforcement Recovery

Use this flow when a default-branch ruleset is missing or lacks required
pull-request or status-check rules. Run the commands from the target
repository with authenticated `gh`; replace `OWNER/REPO`, check contexts, and
full commit SHAs with observed values.

## Contents

- [Inventory before changing policy](#1-inventory-before-changing-policy)
- [Apply the safe fallback ruleset](#2-apply-the-safe-fallback-ruleset)
- [Make a required-check context safe to require](#3-make-a-required-check-context-safe-to-require)
- [Restrict Actions without breaking composites](#4-restrict-actions-without-breaking-composites)
- [Create or complete the default ruleset](#5-create-or-complete-the-default-ruleset)
- [Verify the stored policy](#6-verify-the-stored-policy)

## 1. Inventory before changing policy

```powershell
$repo = 'OWNER/REPO'
gh api "repos/$repo" --jq '{default_branch,allow_squash_merge,allow_merge_commit,allow_rebase_merge,allow_auto_merge,allow_update_branch,delete_branch_on_merge,squash_merge_commit_title,squash_merge_commit_message}'
gh api "repos/$repo/immutable-releases"
gh api "repos/$repo/actions/permissions"
gh api "repos/$repo/actions/permissions/selected-actions"
gh api "repos/$repo/actions/permissions/workflow"
gh api "repos/$repo/rulesets"
```

Build a per-setting evidence map from these responses and from the read-back
after every mutation. Record the endpoint, observed value, and result as
`verified`, `unverified`, or an approved exception. Treat an unavailable
setting as unverified; do not infer a fork-workflow approval policy, merge
method, or ruleset bypass from another repository or a related setting.
For an apply request, set every requested baseline value explicitly even if
the pre-change response omitted it; for an audit-only request, retain that
omission as unverified.

The fork-contributor approval endpoint can return `404` for personal-owner
repositories. Do not report that policy as applied in that case; record it as
unverified and use the repository settings UI or a supported API when one is
available.

## 2. Apply the safe fallback ruleset

When no check context has been observed on a pull request, create or update
the `default` ruleset with every other baseline rule: target the default
branch, restrict deletions and force pushes, require pull requests, allow only
squash merging, and allow repository-admin bypass only on pull requests.
Omit only `required_status_checks`; record the ruleset as incomplete and do
not claim status-check enforcement.

Use the template in section 5 after removing its
`required_status_checks` object. For an existing ruleset, preserve unrelated
rules and send the complete reviewed replacement with `PUT`.

## 3. Make a required-check context safe to require

1. Add or adapt a validation workflow that runs the intended job on
   `pull_request`. Add `merge_group` when the repository uses a merge queue.
2. Give the job a stable visible name, such as `lint` or `test`.
3. Merge that workflow change to the default branch.
4. Open a pull request and wait for a successful run. Confirm the exact
   context before adding it to the ruleset:

   ```powershell
   gh pr checks <number> --required
   ```

Do not require a job that runs only on `push`, a release job, or a context
whose current name was not observed on a pull request.

## 4. Restrict Actions without breaking composites

Inventory `uses:` in workflow files and all reachable local composite actions
or reusable workflows. Preserve local actions and GitHub-owned actions; allow
only the external action or reusable-workflow names that the inventory finds.
Keep full-SHA pinning required for workflow execution, but allow each selected
name with `@*` so updating a pinned version does not require a settings change.
Do not wildcard an owner or all actions.

Set `allowed_actions=selected`, `sha_pinning_required=true`,
`github_owned_allowed=true`, and `verified_allowed=false` explicitly during an
apply. Do not assume an omitted pre-change SHA-pinning value was already safe.

When the inventory finds no external `uses:` reference, set selected actions
with GitHub-owned actions allowed, Marketplace verified creators disallowed,
and no `patterns_allowed[]` entries. This is a valid least-privilege result;
downloaded tools are not Action allowlist entries and still require the
separate `security-check` review.

```powershell
gh api --method PUT "repos/$repo/actions/permissions" `
  -F enabled=true -f allowed_actions=selected -F sha_pinning_required=true

gh api --method PUT "repos/$repo/actions/permissions/selected-actions" `
  -F github_owned_allowed=true -F verified_allowed=false `
  -f 'patterns_allowed[]=EXTERNAL_OWNER/ACTION@*'

gh api --method PUT "repos/$repo/actions/permissions/workflow" `
  -f default_workflow_permissions=read `
  -F can_approve_pull_request_reviews=false
```

Repeat `patterns_allowed[]` only for additional observed external action or
reusable-workflow names. Read back all three endpoints after the change.

## 5. Create or complete the default ruleset

Save the following JSON as `ruleset.json` after replacing `lint` with an
observed pull-request check context. Repository role ID `5` is the `admin`
role; its bypass mode is limited to pull requests. If no context is available,
remove the complete `required_status_checks` object and apply the fallback from
section 2.

```json
{
  "name": "default",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request" }
  ],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": { "allowed_merge_methods": ["squash"] } },
    { "type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": true,
      "do_not_enforce_on_create": false,
      "required_status_checks": [{ "context": "lint" }]
    } }
  ]
}
```

```powershell
gh api --method POST "repos/$repo/rulesets" --input ruleset.json
```

For an existing ruleset, fetch its detail before changing it. Preserve every
unrelated rule; identify extra bypass actors and other exceptions separately
instead of silently treating them as the administrator baseline. Send only the
complete, reviewed replacement to `PUT repos/$repo/rulesets/<id>`.

## 6. Verify the stored policy

```powershell
gh api "repos/$repo/rulesets" --jq '.[] | select(.name == "default") | .id'
gh api "repos/$repo/rulesets/<id>"
```

Confirm the target is `~DEFAULT_BRANCH`, deletion and force pushes are
restricted, pull requests allow only squash merging, the observed check is
required, and the only baseline bypass is repository-admin with
`pull_request` mode. Also read back the repository merge settings, immutable
releases, both Actions policy endpoints, and workflow token permissions; mark
every unavailable value unverified.
