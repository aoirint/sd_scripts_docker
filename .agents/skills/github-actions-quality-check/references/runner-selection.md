# GitHub-hosted Linux Runner Selection

Select a runner per job from its actual resource, isolation, tool, and duration requirements. Do
not copy one workflow-wide label into every job without checking those requirements.

## Contents

- [Start from the oldest supported GA image](#start-from-the-oldest-supported-ga-image)
- [Prefer `ubuntu-slim` for lightweight jobs](#prefer-ubuntu-slim-for-lightweight-jobs)
- [Choose a full Ubuntu VM deliberately](#choose-a-full-ubuntu-vm-deliberately)
- [Operate image retirement as a recurring lifecycle](#operate-image-retirement-as-a-recurring-lifecycle)
- [Validate the selection](#validate-the-selection)

## Start from the oldest supported GA image

For a job whose output or validation establishes an OS compatibility floor, choose the oldest
versioned GitHub-hosted GA image that the `actions/runner-images` repository currently lists for the
required OS and architecture. For Ubuntu, this maximizes compatibility with older glibc consumers;
newer glibc is not generally backward-runnable on an older distribution. Apply the same
oldest-supported baseline to Windows and macOS support, while treating architecture, Xcode/Visual
Studio availability, and artifact type as separate constraints.

Discover the label at review time; do not copy a once-current version from this Skill. Use an
explicit version label such as `ubuntu-<version>`, `windows-<version>`, or `macos-<version>` so a
moving `*-latest` alias cannot silently raise the compatibility floor. Beta images do not count as
the oldest supported GA baseline and do not replace it before GA.

An earlier support cutoff is allowed when current evidence shows that the old image prevents a
required library/toolchain, materially harms performance or reliability, creates disproportionate
maintenance cost, or cannot meet security/support obligations. Record the evidence, affected users
and artifacts, replacement image, migration checks, and announced support boundary. Convenience
alone is not evidence.

## Prefer `ubuntu-slim` for lightweight jobs

Use `ubuntu-slim` when all of these conditions hold:

- The job is short-running with enough measured headroom below the fixed 15-minute limit.
- One x64 CPU, 5 GB RAM, and 14 GB storage are sufficient.
- The job works in an unprivileged container on a shared VM.
- Every required command is in the current slim image inventory or is installed explicitly from a
  reviewed, pinned, integrity-checked source.
- Every external or local action used by the job is compatible with the slim environment.
- The job does not build, package, link, or validate a native artifact whose glibc/OS compatibility
  floor is part of the supported product contract.

Good candidates include repository metadata checks, issue or release API automation, small
format/lint/type/test jobs, and lightweight artifact assembly or publication. Measure the real job;
the category alone does not prove it fits.

`ubuntu-slim` is not a smaller full VM. GitHub provisions an unprivileged container with a minimal
tool set. Do not select it for jobs that require filesystem mounts, Docker-in-Docker, low-level
kernel features, nested virtualization, emulators, or other privileged host access. Treat Docker
container actions and service containers as unsupported until current official documentation and a
representative run prove the exact use case works. The installed Docker client does not imply that
a usable Docker daemon is available.

Avoid `ubuntu-slim` for typical heavyweight CI/CD builds, large native compilation, desktop/mobile
packaging toolchains, or jobs whose duration can approach 15 minutes. Split a genuinely lightweight
preflight or publication phase from a heavyweight build when the dependency graph remains explicit;
do not split jobs merely to claim slim usage.

## Choose a full Ubuntu VM deliberately

Use a standard Ubuntu VM when the job needs more CPU or memory, a full preinstalled toolchain,
privileged VM behavior, longer execution, or an OS/native ABI compatibility contract. Select the
oldest currently supported GA Ubuntu label unless a documented constraint justifies an earlier
support cutoff. Use `ubuntu-latest` only when automatically following GitHub's newest stable Ubuntu
image is an intended maintenance policy and migration risk has been accepted.

Do not infer that `-latest` means the newest upstream Ubuntu release; it means GitHub's latest stable
hosted image and changes over time.

## Operate image retirement as a recurring lifecycle

GitHub supports at most two GA images plus one beta per OS family and begins deprecating the oldest
label after a newer OS image reaches GA. Treat the runner selection as maintained support data, not
a one-time YAML choice.

1. On every runner-label change, and at least monthly while a repository uses a versioned hosted
   image, review the current `actions/runner-images` **Available Images**, releases, and open pinned
   **Announcement** issues. Record the review date and the oldest eligible GA label for each
   supported OS/architecture family.
2. When a new GA image appears or a dated deprecation announcement names the selected image, open or
   update a tracked migration item within one normal maintenance cycle. Capture the announcement
   URL, announcement date, scheduled brownouts or phased withdrawal, final removal date, affected
   workflows/artifacts, and the next-oldest supported replacement.
3. Validate the replacement in parallel before changing the declared support floor: dependency and
   tool availability, compiler/runtime versions, native artifact compatibility, packaging,
   performance, cache behavior, and representative workflow duration.
4. Set the repository's cutoff and merge the versioned-label migration before the first scheduled
   brownout or other service-disruption phase. Leave at least one normal release/maintenance cycle
   for rollback when the announcement lead time permits. If GitHub publishes only a final removal
   date, choose an earlier internal cutoff with the same rollback window; do not wait for removal.
5. Remove the retired label and obsolete conditionals together, publish the support-boundary change
   where users and maintainers expect it, and verify the first scheduled runs on the replacement.
6. Continue the monthly review on the replacement image. A completed migration starts the same
   lifecycle again; it does not close runner maintenance permanently.

The announcement begins GitHub's administrative deprecation process; brownouts and phased routing
are the operational disruption phase that repositories must precede. If an announcement provides
too little lead time for the normal cycle, migrate immediately and record the reduced validation or
rollback window rather than running into a brownout.

Apply this lifecycle to Windows and macOS too. It is acceptable to drop an older image before GitHub
does when library/toolchain compatibility, performance, reliability, security, or maintenance
evidence justifies it, but follow the same tracked decision, parallel validation, communicated
cutoff, and post-migration verification.

## Validate the selection

1. Read the current GitHub-hosted runner reference and `ubuntu-slim` software inventory before a
   migration. Also read `actions/runner-images` Available Images, releases, and dated Announcement
   issues; runner capabilities, installed versions, and retirement dates can change.
2. Inventory shell commands, local actions, external actions, package installation, caches,
   containers, services, artifacts, permissions, and expected peak resource use for each job.
3. Set `timeout-minutes` to at most 15 on a slim job. Leave operational headroom rather than using
   the limit as the expected duration.
4. Run every changed slim job on a representative event. Check setup logs, action compatibility,
   elapsed time, peak behavior, and outputs; a YAML-only review is insufficient.
5. Keep heavy and platform-specific jobs on the full runner they require. Record why each exception
   cannot use slim so future reviews can reconsider it.
6. For every compatibility-bearing job, record why the selected version is the oldest supported GA
   image or the evidence that justified an earlier support cutoff.

Primary references:

- <https://docs.github.com/en/actions/reference/runners/github-hosted-runners>
- <https://github.com/actions/runner-images#available-images>
- <https://github.com/actions/runner-images#software-and-image-support>
- <https://github.com/actions/runner-images/issues?q=is%3Aissue+label%3AAnnouncement>
- <https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md>
