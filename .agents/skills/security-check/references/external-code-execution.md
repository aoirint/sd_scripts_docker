# External Code Execution Patterns

Use the matching section after the artifact has passed the `security-check`
review. These patterns prevent incidental resolution or drift; they do not
replace provenance review, immutable pinning, or the seven-day cooldown.

## uv

| Situation | Use | Avoid |
| --- | --- | --- |
| Project command | `uv run --locked <command>` | Plain `uv run` when a lockfile update must fail. |
| PEP 723 script | Add `[tool.uv] exclude-newer = "P7D"`, create the adjacent lock with `uv lock --script path/to/script.py`, then run `uv run --locked --script path/to/script.py` | Unlocked `uv run --script` or inline dependency resolution without `exclude-newer`. |
| One-off dependency | `uv run --exclude-newer=P7D --with <package> -- <command>` only after the package review | A bare `uv run --with <package>` command. |

`--locked` fails when `uv.lock` is missing or stale. `exclude-newer=P7D` limits
candidate distributions by upload time; keep the policy in PEP 723 metadata so
the script carries it with the lock.

## Poetry

1. Require a reviewed `poetry.lock`. Run `poetry check --lock` before install.
2. Run `poetry sync` to reproduce the lock and remove packages not in it. Do
   not substitute `poetry install --sync`; use the documented `sync` command.
3. Use `poetry install` only when the project intentionally needs its less
   exact environment behavior.
4. Do not use `poetry add`, `poetry update`, or a missing lockfile as an
   execution-time substitute for dependency review.
5. Poetry does not provide an equivalent `exclude-newer` cutoff. Review the
   candidate release age before committing the `poetry.lock`; do not claim the
   lockfile alone enforces the cooldown.

## npm and pnpm

| Tool | Reproduce a reviewed dependency tree | Do not use for ordinary execution |
| --- | --- | --- |
| npm | `npm ci` with a reviewed `package-lock.json` | `npm install`, `npx`, or `npm exec` that can resolve a missing package. |
| pnpm | `pnpm install --frozen-lockfile`, then `pnpm exec <installed-command>` | `pnpm install` without the frozen lockfile or `pnpm dlx`. |

`npx`, `npm exec`, and `pnpm dlx` are adoption/update operations when they
fetch a package. Add and review the dependency first instead of using them as a
one-off bypass.

## pip

1. Keep a reviewed requirements file with every direct and transitive package
   pinned to `==` and supplied with local `sha256` hashes.
2. Install with `python -m pip install --require-hashes -r requirements.txt`.
3. Prefer `--only-binary :all:` when the reviewed artifact policy excludes
   source builds. Do not use bare `pip install <package>` or `--upgrade` for a
   reviewed reproduction.
4. pip hash checking verifies artifacts but does not impose a release-age
   cutoff; complete cooldown review before updating the requirements file.

## Docker and container build inputs

1. Pin every `FROM` and pulled image to an immutable digest:
   `image@sha256:<digest>`, not a mutable tag.
2. Record the image source, reviewed digest, and release/adoption date before
   changing the Dockerfile or CI configuration.
3. Pin remote Dockerfile inputs too. Where supported, use `ADD --checksum` for
   a reviewed remote HTTP or Git input; otherwise download and verify it before
   the build.
4. Review `RUN` steps separately: a digest-pinned base image does not secure a
   package-manager command that resolves new code during the build.

## Direct downloads and installers

1. Prefer a reviewed, versioned artifact URL and an independent SHA-256 value.
2. Download to a file, verify its hash, then extract or execute it. Never use
   `curl | sh`, `wget | sh`, `irm | iex`, or equivalent streamed installers.
3. Treat a mirror, cache, or marketplace as a distribution path only. Verify
   that it serves the reviewed immutable artifact and hash.

## Other tools

Apply the closest pattern to unlisted package managers, runtimes, extension
hosts, auto-updaters, and bootstrap tools. If it cannot reproduce a reviewed
immutable resolution or enforce the required control, do not use it to bypass
the adoption review.

## Sources

- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv scripts and `exclude-newer`](https://docs.astral.sh/uv/guides/scripts/)
- [Poetry CLI: install, sync, and lock checks](https://python-poetry.org/docs/cli/)
- [npm `ci`](https://docs.npmjs.com/cli/commands/npm-ci/)
- [pnpm install](https://pnpm.io/cli/install)
- [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [Docker image digests](https://docs.docker.com/dhi/core-concepts/digests/)
