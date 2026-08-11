# Registry Image Deletion

Use this procedure only after the user or maintainer has explicitly authorized a
registry deletion and identified its scope. It governs safe execution and verification;
it does not define retention policy or recommend when images should be deleted.

## Resolve the deletion plan

1. Inventory every in-scope registry read-only before changing state. Enumerate tags,
   manifests, package versions, untagged manifests, attestations, and other related
   artifacts exposed by that registry.
2. Record the requested boundary as explicit delete and retain sets. Do not infer the
   set from SemVer alone: repositories can contain prefixes, suffixes, prereleases,
   date-based versions, legacy aliases, cache tags, and untagged artifacts.
3. Resolve tags and package versions to immutable digests or registry object IDs when
   the API exposes them. Check whether retained aliases share a manifest with a target.
4. Identify the registry's deletion unit. A tag, manifest, package version, index, and
   child or attestation manifest are not interchangeable, and deleting one can remove
   or expose related objects differently across registries.
5. Present or record the exact planned targets and retained references before the
   first mutation. Stop if the requested boundary cannot be mapped unambiguously to
   registry objects.

## Authenticate and mutate safely

- Use the least-privileged credential that can list and delete the in-scope objects.
  Registry read and delete scopes are commonly distinct. Confirm the effective account,
  repository, package, and permission before mutation.
- Keep tokens out of command arguments, logs, shell history, committed files, and
  durable temporary files. Prefer the platform credential store or process-scoped
  secret injection.
- Delete only resolved object IDs, digests, or exact references. Avoid broad globs,
  unresolved variables, or mutable list positions.
- Make the operation restartable. Record completed targets and treat an already-absent
  response as success only when it refers to an exact planned target; stop on other
  unexpected status codes or response bodies.
- Re-enumerate related objects after each deletion group when a registry can cascade
  from an index or package version to child, untagged, signature, provenance, or
  attestation artifacts.

## Verify registry state

Do not rely on a successful delete response or one listing endpoint. Registry indexes,
counts, pagination cursors, and mirrors can be eventually consistent.

1. Re-list the repository or package and compare the observed objects with both the
   delete and retain sets.
2. Probe removed references through an independent manifest lookup or pull path and
   confirm that they no longer resolve.
3. Probe every retained release or alias and confirm that it still resolves to the
   expected digest. When the image is published to multiple registries, compare the
   intended cross-registry digest correspondence.
4. Investigate stale counts, pagination links, cached metadata, or contradictory API
   responses instead of treating them as proof of success. Record any scope that remains
   unverified.
5. Record the final target list, immutable identifiers where available, commands or APIs
   used, verification evidence, and the registry's documented recovery path or lack of
   one. A deletion is not complete until both absence and retention checks pass.
