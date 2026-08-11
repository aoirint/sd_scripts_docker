# Python CI and Distribution Baseline

## Contents

- [CI parity](#ci-parity)
- [Event and trust boundaries](#event-and-trust-boundaries)
- [Distribution verification](#distribution-verification)
- [Completion evidence](#completion-evidence)

## CI parity

Use `github-workflow` and `security-check` while implementing CI.

- Re-run lock verification, exact sync, Ruff lint, Ruff format, strict mypy,
  pytest, and coverage from a clean checkout.
- For a library, run locked pytest on every advertised Python minor. Run the
  complete lint, format, strict-mypy, coverage, and build gate on the pinned
  development minor; repeat a gate across the matrix when its result can vary
  with syntax, typing, dependency markers, native packages, or build output.
- Clean-install and import the built wheel on every advertised Python minor.
- Keep CI commands equal to documented local commands. Hidden CI-only flags and
  local-only shortcuts are findings.
- Install/select Python from `.python-version` or an explicit matrix consistent
  with `requires-python`.
- Pin uv and every external action to reviewed immutable versions. Validate
  action inputs against the exact pinned version.
- Bind dependency caches to `uv.lock`, runner, and Python identity. Do not cache
  `.venv`, secrets, credentials, or signing material.
- Use repository-owned Composite Actions only for stable same-runner sequences.
  Keep job runners, permissions, matrices, artifacts, and release gates in workflows.

## Event and trust boundaries

- Validate untrusted changes on `pull_request`, and `merge_group` when required.
- Re-run the same required validation on the exact protected integration-branch
  push; do not substitute a prior PR run or API polling.
- Start permissions at `contents: read`. Do not use `pull_request_target` to
  execute untrusted proposed source.
- Keep publication/signing in protected jobs or environments after validation
  and artifact creation for the same source commit.
- Use direct `needs` dependencies so build and release consume the complete
  lint/type/test result and the verified artifact.
- Run actionlint, applicable ShellCheck, and pinact in addition to Python checks.

## Distribution verification

For installable applications, libraries, or CLIs:

1. Run `uv build` from a clean reviewed commit. `uv.lock` does not by itself
   lock isolated PEP 517 build requirements: review `[build-system].requires`,
   constrain build dependencies with reviewed exact bounds or
   `[tool.uv].build-constraint-dependencies`, and record the resolved build
   backend/tool versions.
2. Inspect wheel and sdist paths without extraction by running:

   ```shell
   uv run --no-config --locked --script \
     <skill-root>/scripts/inspect_distribution.py dist/<wheel>.whl dist/<sdist>.tar.gz
   ```

   Reject traversal,
   unsupported special files, and unexpected executable permissions.
3. Verify project name/version, metadata, license/notices, package modules,
   typed markers when promised, entry points, and expected package data.
4. Reject repository-owned tests, caches, `.env`, credentials, VCS metadata,
   local paths, development tools, and unrelated files.
5. For every advertised Python minor, create an environment outside the source
   tree with `uv venv --python <minor> <environment>`, install the exact wheel
   with `uv pip install --python <environment-python> dist/<wheel>`, and invoke
   documented imports and entry points through that interpreter. Do not set
   `PYTHONPATH` or run from a directory that exposes the source package.
6. When publishing an sdist, create another clean environment, install the exact
   sdist so its PEP 517 path builds a wheel, then repeat import/entry checks.
   Record the resolved runtime and build dependency graphs; neither is implied
   by the project environment.
7. Record artifact filename, source commit, Python version, build backend/tool
   versions, size, SHA-256, and inspection result.

Do not infer artifact correctness from source tests or a successful build
command. Framework packagers, native extensions, standalone executable tools,
and platform installers add separate verification surfaces; pair with their
framework/platform Skill.

## Completion evidence

Report:

- exact local and CI commands and results;
- supported Python versions and the versions actually exercised;
- dependency/lock review and any approved exception;
- statement and branch coverage totals;
- wheel/sdist contents, clean-environment import/entry checks, and SHA-256;
- workflow permission/pinning checks;
- blocked, skipped, or not-applicable branches with concrete reasons.
