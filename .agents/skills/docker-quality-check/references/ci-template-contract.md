# Docker CI Template Contract

## Purpose

Use the bundled baseline for a repository with one root `Dockerfile`. It keeps proposed-source
checks fast by running hadolint only. The integrated main-branch workflow repeats lint and then
builds the exact merged commit without publishing it.

## Files

| Skill asset | Consumer path | Contract |
| --- | --- | --- |
| `assets/github/actions/lint-docker/action.yml` | `.github/actions/lint-docker/action.yml` | Install checksum-verified hadolint and lint the root `Dockerfile`. |
| `assets/github/workflows/pull-request.yml` | `.github/workflows/pull-request.yml` | Lint pull-request and merge-queue source; cancel superseded runs. |
| `assets/github/workflows/main.yml` | `.github/workflows/main.yml` | Re-run lint and build the integrated commit; never cancel it. |

Copy the files into the consumer repository. Consumer workflows must run committed
repository-owned files and must not execute the installed Skill at runtime.

## Allowed substitutions

- Replace `main` only with the confirmed protected integration branch.
- Replace the root Dockerfile path or add a lint matrix when the repository owns multiple
  Dockerfiles.
- Pass repository-evidenced build contexts, Dockerfile paths, targets, build arguments, secrets,
  or cache settings to the integrated build.
- Add Compose validation, tests, or smoke checks when the repository documents those contracts.
- Add registry authentication and publication only in an integration job with the minimum required
  permissions and secrets.
- Make an immutable release depend directly on the published image and every required image test.
- Update external Action pins or the hadolint version and checksum only after `security-check`
  verifies provenance, runtime behavior, exact identity, and cooldown eligibility.

Do not add Docker build or publication to the pull-request workflow merely to mirror main. Do not
expose registry credentials to proposed source, rebuild an image in a release job, or create a
release before the published image passes its required tests.

## Adoption checks

1. Inventory existing workflow responsibilities and retire only duplicated entry workflows.
2. Apply `github-actions-quality-check` and preserve its event, permission, concurrency, runner,
   and immutable-pin requirements.
3. Run hadolint locally against every selected Dockerfile.
4. Run actionlint across workflows and actions, ShellCheck against changed standalone shell
   scripts, and `pinact run --check --min-age 7`.
5. Observe the Checks job on a pull request and both Checks and Build jobs on the integrated commit
   before making their contexts required.
