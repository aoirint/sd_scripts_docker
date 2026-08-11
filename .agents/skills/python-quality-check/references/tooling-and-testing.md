# Python Tooling and Test Baseline

## Contents

- [Project and dependency contract](#project-and-dependency-contract)
- [Minimum pyproject shape](#minimum-pyproject-shape)
- [Ruff and keyword-only policy](#ruff-and-keyword-only-policy)
- [mypy policy](#mypy-policy)
- [pytest and coverage policy](#pytest-and-coverage-policy)
- [Locked verification](#locked-verification)
- [Dependency changes](#dependency-changes)

## Project and dependency contract

- Use PEP 621 `[project]` metadata and a real build backend. Install the `src/`
  package into the uv environment instead of relying on an injected test path.
- Keep distribution name, import package, console/module entry points, artifact
  identity, and version source intentionally mapped.
- Pin one development Python minor in `.python-version`. Set
  `requires-python` to the supported range and test every advertised minor.
- Declare only direct runtime dependencies in `[project].dependencies`. Put
  Ruff, mypy, pytest, and pytest-cov in `[dependency-groups].dev`.
- Commit `uv.lock`; treat it as the reviewed graph across supported markers.
- Set `[tool.uv] exclude-newer = "P7D"`. A narrower exception requires an exact
  package, reason, approval, and removal/review trigger.

## Minimum pyproject shape

Use repository-confirmed values; never copy placeholders into executable configuration.

```toml
[project]
name = "<distribution-name>"
version = "0.0.0"
description = "<concise description>"
readme = "README.md"
requires-python = ">=<verified-minor>,<next-breaking-minor>"
dependencies = []

[build-system]
requires = ["hatchling>=<reviewed-minimum>,<reviewed-upper-bound>"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    "mypy>=<reviewed-minimum>,<reviewed-upper-bound>",
    "pytest>=<reviewed-minimum>,<reviewed-upper-bound>",
    "pytest-cov>=<reviewed-minimum>,<reviewed-upper-bound>",
    "ruff>=<reviewed-minimum>,<reviewed-upper-bound>",
]

[tool.uv]
exclude-newer = "P7D"

[tool.ruff]
line-length = 100
target-version = "<matching-pyNNN>"

[tool.ruff.lint]
preview = true
explicit-preview-rules = true
select = [
    "E",       # pycodestyle errors
    "W",       # pycodestyle warnings
    "F",       # Pyflakes correctness
    "FBT",     # prevent positional Boolean traps
    "I",       # deterministic imports
    "ANN",     # annotations
    "ARG",     # unused arguments
    "ASYNC",   # async correctness
    "B",       # bugbear correctness
    "C4",      # comprehension clarity
    "C90",     # explicit complexity ceiling
    "COM",     # stable comma use
    "D",       # public documentation
    "DTZ",     # timezone-aware datetimes
    "ERA",     # no commented-out code
    "FLY",     # modern string formatting
    "G",       # logging format correctness
    "ICN",     # conventional import names
    "LOG",     # logging correctness
    "N",       # naming
    "PERF",    # avoid ordinary performance traps
    "PIE",     # miscellaneous correctness
    "PL",      # maintainability and correctness
    # Preview rule selected by exact code: reject every project-owned positional parameter.
    "PLR0917",
    "PT",      # pytest style
    "PTH",     # pathlib boundaries
    "RET",     # return-path clarity
    "RUF",     # Ruff-specific correctness
    "S",       # common security mistakes
    "SIM",     # needless control-flow complexity
    "SLF",     # private-member boundary violations
    "T20",     # stray print/pprint
    "TRY",     # exception design
    "UP",      # syntax modernization
]
ignore = [
    "COM812",  # Ruff formatter owns trailing comma layout.
    "D203",    # Select D211: no blank line before class docstrings.
    "D213",    # Select D212: summary starts on the first line.
]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-positional-args = 0

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # pytest assertions are the test oracle.

[tool.mypy]
files = ["src", "tests"]
strict = true
warn_unreachable = true
warn_unused_configs = true
show_error_code_links = true

[tool.pytest.ini_options]
addopts = [
    "--strict-config",
    "--strict-markers",
    "-ra",
    "--cov=<package>",
    "--cov-branch",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-fail-under=100",
]
testpaths = ["tests"]

[tool.coverage.run]
branch = true
source_pkgs = ["<package>"]

[tool.coverage.report]
fail_under = 100
show_missing = true
skip_covered = false
```

Verify option names against the locked tool versions. A library supporting
multiple Python minors needs an explicit test matrix; do not weaken the
configured development target.

## Ruff and keyword-only policy

- Run both `ruff check` and `ruff format --check`.
- Use a reasoned selected rule set rather than `ALL`. Treat configuration
  warnings as failures.
- Keep every `[tool.ruff.lint].select` entry on its own line with a concise
  rationale comment. Preserve those comments when reordering, extracting, or
  deploying this baseline; add or update the rationale in the same change as a
  rule selection change.
- Fix code first. A file or line suppression must name the exact rule and give
  a durable reason at the suppression site.
- Require keyword arguments at first-party definitions and call sites,
  including a sole input. Put `*` before the first project-owned parameter;
  `self` and `cls` remain implicit receivers.
- Use `kw_only=True` for project-owned dataclasses. Do not introduce
  `NamedTuple`, `namedtuple`, positional generated constructors, or `*args` to
  evade the policy.
- Give project-owned lambdas keyword-only parameters. Use a named function with
  an evidenced exception when an external callback requires a positional lambda
  signature.
- Select `PLR0917` explicitly with `max-positional-args = 0`. Do not suppress
  `PLR0917`, `PL`, or `ALL` globally.
- Limit Ruff source exclusions to generated APM/deployment/worktree roots. Do
  not exclude `src`, `tests`, `scripts`, tools, examples, or migrations from
  the repository-wide `ruff check .`.
- Preserve a positional signature only when an external ABI requires it.
  Document the exact contract on the definition line with
  `keyword-only-exception:` and a narrow `noqa` when Ruff requires one.
- Prefer keywords at first-party call sites even when a compatibility
  definition must accept positional calls.

## mypy policy

- Check maintained source and tests with `strict = true` and
  `warn_unreachable = true`.
- Do not enable global `ignore_missing_imports`, skip imports, or ignore errors.
- Contain untyped dependencies in one adapter and validate/narrow values before
  returning typed results.
- A `type: ignore[code]` must name the code and explain the proven typing
  boundary. Remove it when the dependency or seam changes.
- Type callbacks, coroutine results, task handles, serialized values, schemas,
  factories, and public package surfaces.

## pytest and coverage policy

- Require 100% statement and branch coverage for maintained first-party source.
- Do not use broad omit rules, `pragma: no cover`, or import guards to
  manufacture 100%.
- Test module and console entry points without launching work at import time.
- Fail on unknown markers/configuration and make clock, randomness, sleep,
  filesystem, subprocess, and network behavior deterministic through seams.
- Assert state, declared effects, boundary calls, failures, cleanup, and
  user-observable outcomes; executing a line is not a sufficient assertion.
- Keep ordinary tests offline and independent of user credentials.
- Organize tests around contracts: domain values, application transitions,
  presentation mapping, infrastructure boundaries, composition, entry points,
  and artifact smoke behavior. Source-file mirroring alone is insufficient.

## Locked verification

Run from a clean repository root:

```shell
uv lock --check
uv sync --locked --all-groups
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked pytest
```

Run `uv build` when the project is an installable distribution. Do not use bare
`pip install`, globally installed checkers, or unlocked `uv run` as release evidence.

## Dependency changes

1. Invoke `security-check` before resolution.
2. Record purpose, source/publisher, license, constraint, release age,
   transitive changes, binary/build hooks, runtime behavior, and platform support.
3. Update only the intended package, using `uv lock --upgrade-package` when appropriate.
4. Review `pyproject.toml` and the complete `uv.lock` delta.
5. Replay exact sync and the complete locked verification set.
