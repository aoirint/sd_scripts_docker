# APM Notices and Completion Checks

## 5. Reconcile third-party notices

Before handoff, reconcile `THIRD_PARTY_NOTICES.md` with the reviewed lockfile:

1. For every third-party skill whose files are committed from an APM target,
   keep one current notice entry with the source, selected virtual path, locked
   SHA, license, and required attribution.
2. When removing a dependency, run `apm prune` and confirm its deployed files
   are gone before removing its notice entry. Retain the notice when a copy or
   derivative remains in the repository.
3. Treat a changed license, copyright, or NOTICE file as an adoption-review
   change, not a metadata-only update. Resolve it before deploying the new
   version.

## Completion checklist

- `apm.yml` is present and was not overwritten accidentally.
- An unpublished project keeps `version: 0.0.0` until its distribution and
  versioning design is approved.
- The selected APM CLI was the newest reviewed release that completed the
  seven-day cooldown or had a manifest-recorded maintainer exception for the
  specific unmet gate; its absolute path and version were recorded.
- No PATH, active APM installation, or other user-environment state changed
  without explicit authorization.
- Any lock-format migration was explicit and reviewed separately from resolved
  dependency changes; unexpected lockfile writes were restored and reported.
- Every remote dependency is pinned to a reviewed full commit SHA.
- `apm.lock.yaml` is committed and contains the expected resolved commits and
  content hashes, and its `apm_version` matches the selected eligible CLI.
- Each adopted release, or the last change to a selected virtual subdirectory,
  met the seven-day cooldown or has a documented maintainer-approved exception.
- Each committed APM-deployed third-party skill has one current
  `THIRD_PARTY_NOTICES.md` entry, including its license and required notices;
  removed skills have no stale entry unless a copy remains.
- Packaged collections have matching canonical and distributed file sets and
  content hashes; the named installed Skill was checked at the
  installer-reported target.
- Deployment used `apm install --frozen`; `apm audit --ci` passed in the
  verified target context, or any target-resolution discrepancy is documented
  with direct installation and lockfile evidence.
- Updates have a reviewable, cooldown-aware proposal before application.
