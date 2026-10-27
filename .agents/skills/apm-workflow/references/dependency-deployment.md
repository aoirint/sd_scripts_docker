# Add and Deploy an APM Dependency

## 3. Add an Agent Skill or dependency

Use this staged workflow for every remote skill, prompt, agent, plugin, hook,
or MCP dependency:

1. Identify the exact source repository, optional virtual subdirectory,
   release/tag, and full 40-character commit SHA. Review the source, its
   release history, declared capabilities, transitive dependencies, and changes
   that could execute code or add MCP access.
2. Verify from an authoritative source that the adopted content is at least
   seven days old. For a virtual subdirectory in a monorepo, identify the last
   commit that changed that subdirectory at the selected ref and calculate the
   cooldown from that commit, not from an unrelated later commit elsewhere in
   the repository. If its age, provenance, or required hash cannot be verified,
   stop and report the blocker. Do not bypass the cooldown without a documented
   maintainer exception.
3. Before committing a third-party skill, determine its license from an
   authoritative upstream license file or policy. Add or update the
   repository-root `THIRD_PARTY_NOTICES.md` with its source repository and
   virtual path, full commit SHA, license identifier and canonical text or URL,
   plus any supplied copyright or NOTICE text. Do not put this record in an
   APM-managed target directory such as `.agents/skills/`. Treat a missing or
   unclear license or required notice as a blocker unless a maintainer records
   an explicit exception.
4. Add the dependency to `apm.yml` with the full commit SHA, never a default
   branch, `latest`, or an unbounded range. When selecting multiple Skills from
   one repository at one ref, use one object-form dependency with `git`, `ref`,
   and `skills`; do not encode each Skill as a separate virtual dependency.
   Keep separate entries only when their repository, ref, or dependency policy
   differs. Keep MCP entries under the same review gate and do not put tokens
   in tracked YAML.
5. Run `apm lock` to resolve and download without deploying to agent targets.
   Review `apm.lock.yaml`: each dependency must resolve to the expected commit
   and carry its content hash. For a new or changed deployment, complete and
   review the [deployment ledger](cli-selection.md#12-complete-a-new-or-rebuilt-deployment-ledger)
   before the frozen verification below. In PowerShell checks, wrap variable-cardinality
   query results in `@(...)` before using `.Count`, indexing, or membership
   tests; one result otherwise becomes a scalar while multiple results become
   an array. Assert the expected count and element type. Commit the manifest
   and lockfile together.
6. Run `apm install --frozen` only after that review. It must reproduce the
   reviewed lockfile and must not resolve a new dependency. Never use
   `--force`, `--allow-insecure`, or an insecure HTTP source unless an explicit
   documented exception authorizes it.
7. Run `apm audit --ci` after deployment. Fix lockfile, integrity, drift, or
   policy findings rather than suppressing them. Add `apm install --frozen` and
   `apm audit --ci` to the project's existing CI when the user requests CI
   enforcement.
