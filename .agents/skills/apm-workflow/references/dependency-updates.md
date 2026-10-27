# Propose and Apply Approved Dependency Updates

## 4. Propose updates; do not silently apply them

Pinned dependencies stay unchanged until a maintainer approves an update.
Create an update proposal, issue, or pull request with no deployment changes
first:

1. Confirm the intended project root contains `apm.yml` before running
   `apm outdated` or `apm update --dry-run`. For user scope, verify the existing
   user manifest and use `--global` consistently. Stop if the manifest or scope
   is unknown: without a project manifest, `apm update` delegates to CLI
   self-update, and `--dry-run` does not protect that fallback. In the verified
   dependency scope, these commands discover candidates without writing files.
2. For each candidate, record the current and proposed tag and full commit
   SHA, upstream release URL and date, SHA-256/content-hash changes, source
   review summary, new transitive dependencies, and any MCP, hook, permission,
   or target-output changes.
3. State the earliest eligible adoption date: release date plus seven full
   days. Keep the proposal open until that date and explicit maintainer
   approval; a newer upstream release restarts its own cooldown.
4. After approval, run interactive `apm update` for only the approved package.
   Confirm the planned full commit matches the approved candidate before
   accepting it; if the CLI cannot select that candidate, stop rather than
   adopting a different ref. Then review the `apm.yml`,
   `apm.lock.yaml`, and deployed-file diff. Run `apm audit --ci` and commit the
   result. Re-check the upstream license and notices; update the matching
   `THIRD_PARTY_NOTICES.md` entry in the same commit when the source, virtual
   path, commit, license, or attribution changes.
5. In CI and ordinary repeat installs, keep using `apm install --frozen`.
   Update discovery and update application must remain separate actions.
