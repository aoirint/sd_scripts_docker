# Docker CI Template Contract

## Purpose

Use the bundled baseline for a repository with one root `Dockerfile`. Proposed-source checks use
the official Dockerfile frontend without executing a build. The integrated main-branch workflow
repeats the check and then builds the exact merged commit without publishing it.

## Files

| Skill asset | Consumer path | Contract |
| --- | --- | --- |
| `assets/github/actions/check-docker-source/action.yml` | `.github/actions/check-docker-source/action.yml` | Audit APM and lint Markdown independently from Docker setup. |
| `assets/github/workflows/pull-request.yml` | `.github/workflows/pull-request.yml` | Run BuildKit checks for pull-request and merge-queue source; cancel superseded runs. |
| `assets/github/workflows/main.yml` | `.github/workflows/main.yml` | Re-run BuildKit checks and build the integrated commit; never cancel it. |

Copy the files into the consumer repository. Consumer workflows must run committed
repository-owned files and must not execute the installed Skill at runtime.

## Allowed substitutions

- Replace `main` only with the confirmed protected integration branch.
- Replace the root Dockerfile path or add a check matrix when the repository owns multiple
  Dockerfiles.
- Pass repository-evidenced build contexts, Dockerfile paths, targets, build arguments, secrets,
  or cache settings to the integrated build.
- Add Compose validation, tests, or smoke checks when the repository documents those contracts.
- Add registry authentication and publication only in an integration job with the minimum required
  permissions and secrets.
- Make an immutable release depend directly on the published image and every required image test.
- Add hadolint only for documented complementary rules after verifying that it supports the
  selected Dockerfile frontend syntax. Apply `security-check` to its version and asset checksum.
- Update external Action pins only after `security-check` verifies provenance, runtime behavior,
  exact identity, and cooldown eligibility.

Do not add Docker build or publication to the pull-request workflow merely to mirror main. Do not
expose registry credentials to proposed source, rebuild an image in a release job, or create a
release before the published image passes its required tests.

## Adoption checks

1. Inventory existing workflow responsibilities and retire only duplicated entry workflows.
2. Apply `github-actions-quality-check` and preserve its event, permission, concurrency, runner,
   and immutable-pin requirements.
3. Run `docker buildx build --check` locally with the selected build contract.
4. Run actionlint across workflows and actions, ShellCheck against changed standalone shell
   scripts, and `pinact run --check --min-age 7`.
5. Observe the Checks job on a pull request and both Checks and Build jobs on the integrated commit
   before making their contexts required.
