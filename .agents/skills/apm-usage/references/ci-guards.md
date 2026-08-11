# CI Guards

Use these guards when a repository wants reproducible APM metadata and
Markdown lint checks without adding an installer to the lint job.

## Contents

- [APM project metadata](#apm-project-metadata)
- [Markdown lint through pnpm dlx](#markdown-lint-through-pnpm-dlx)

## APM project metadata

The Skill includes `assets/check-apm-project/action.yml` as the reviewed
template for a small repository-owned Composite Action. Copy the action to
`.github/actions/check-apm-project/action.yml`. Do not invoke the deployed Skill
path from CI: that would make a consumer workflow depend on the Skill's
internal directory structure.

The copied guard checks two repository invariants:

- top-level `version` in `apm.yml` is `0.0.0` for an unpublished project;
- top-level `apm_version` in `apm.lock.yaml` matches the selected APM version.

Add one step to an existing composite lint action:

```yaml
- name: Check APM project metadata
  uses: ./.github/actions/check-apm-project
  with:
    expected-apm-version: "0.26.0"
```

The check uses only the Python standard library available on the selected
runner and does not download or execute APM. Review the copied Composite Action
as repository code, and update its caller's expected APM version in the same PR
that deliberately changes the lock generator version.

If it reports a lock generator mismatch, invoke the reviewed APM executable by
absolute path, remove only the validated repository's `apm.lock.yaml`, and run
`apm lock`. Review the full regenerated lock, run `apm install --frozen`, and
then run `apm audit --ci`. Never repair the version field manually.

## Markdown lint through pnpm dlx

Pin the package version and make pnpm reject packages that have not completed
seven full days since publication, including packages with missing publication
times:

```shell
pnpm \
  --config.minimumReleaseAge=10080 \
  --config.minimumReleaseAgeStrict=true \
  --config.minimumReleaseAgeIgnoreMissingTime=false \
  --config.minimumReleaseAgeExclude= \
  dlx markdownlint-cli2@0.22.0 \
  --config .markdownlint-cli2.yaml \
  '**/*.md'
```

[pnpm's `minimumReleaseAge` setting](https://pnpm.io/settings#minimumreleaseage)
is measured in minutes, so `10080` is seven days. Use pnpm 11 or newer because
all three fail-closed settings are supported there. Invoke
the reviewed pnpm executable by its resolved path, confirm `pnpm --version`,
and keep the strict, missing-time, and empty-exclusion settings explicit rather
than relying on pnpm defaults or global configuration. Before adopting the
command, confirm the effective values with the same CLI:

```shell
pnpm --config.minimumReleaseAge=10080 config get minimumReleaseAge
pnpm --config.minimumReleaseAgeStrict=true config get minimumReleaseAgeStrict
pnpm --config.minimumReleaseAgeIgnoreMissingTime=false \
  config get minimumReleaseAgeIgnoreMissingTime
pnpm --config.minimumReleaseAgeExclude= config get minimumReleaseAgeExclude
```

Run the pinned `dlx` command in a clean process with no project-local pnpm
configuration overriding these command-line values. An exact package version
does not replace the cooldown gate; keep both.

Confirm that the resolver actually enforces the gate with a safe negative
control. In a unique operating-system temporary directory, use an isolated
pnpm store and ask the resolver to add the same reviewed
`markdownlint-cli2@0.22.0` with an intentionally larger age such as `5256000`
minutes:

```shell
probe_dir="$(mktemp -d)"
(
  cd "$probe_dir"
  pnpm \
    --config.storeDir="$probe_dir/store" \
    --config.minimumReleaseAge=5256000 \
    --config.minimumReleaseAgeStrict=true \
    --config.minimumReleaseAgeIgnoreMissingTime=false \
    --config.minimumReleaseAgeExclude= \
    --ignore-scripts \
    add --lockfile-only markdownlint-cli2@0.22.0
)
```

The command must fail with `ERR_PNPM_NO_MATURE_MATCHING_VERSION`; any other
result is a failed probe. `--lockfile-only --ignore-scripts` prevents package
or lifecycle-script execution even if the cooldown is ineffective. After this
negative control, run the real seven-day `dlx` command and require success.

For locally auto-fixable findings, add `--fix` after the package version and
run the normal lint command again afterward. `markdownlint-cli2 --fix` does not
repair every rule; line-length findings such as prose reported by MD013 can
still require a formatter or a meaning-preserving manual edit.
