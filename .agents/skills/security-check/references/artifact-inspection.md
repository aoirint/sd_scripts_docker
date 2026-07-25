# Final Artifact Inspection

Use this checklist for archives, installers, bundles, release assets, and packaged applications.
Inspect the artifact that will actually be distributed; a clean staging directory or successful
build log is not evidence about the final container.

## Inspect container structure safely

1. Enumerate member metadata without extracting into the working tree or another trusted path.
2. Normalize and validate member names before interpreting them. Reject absolute paths, drive or
   device prefixes, parent traversal, ambiguous separator forms, duplicate normalized paths, and
   names that the target platform would alias unexpectedly.
3. Classify every member by archive type. Reject unsupported device, FIFO, socket, hard-link, or
   other special entries. Validate symbolic-link targets as untrusted paths, and never count a link
   as the required regular-file payload.
4. Require the expected regular files and directories. Verify executable mode bits for launchers
   on targets that use them, and reject unexpectedly writable or privileged modes when relevant.
5. Bound member count, individual size, total expanded size, and compression ratio before any
   extraction or deep content scan. Do not let a crafted archive exhaust disk, memory, or time.
6. If extraction is required for a later test, extract only after validation into a new isolated
   temporary directory, prevent link traversal, and remove it after inspection.

Apply equivalent checks to format-specific containers even when their libraries use different
names for entries. Do not rely on a convenience extraction API to make unsafe members harmless.

## Verify identity, payload, and provenance

- Verify the expected product identity, entry point, version, target, licenses/notices, and required
  assets from the final artifact.
- Record hashes and provenance from the final bytes. Distinguish build-host tools and runtimes from
  runtimes, libraries, or native components embedded in each artifact; do not copy builder metadata
  into artifact records by assumption.
- Compare the artifact against an explicit payload contract. Reject repository-owned secrets,
  credentials, local paths, source-control metadata, caches, tests, agent files, workflows,
  development tools, and unrelated source unless the product contract requires them.
- Make content rules ownership- and path-aware. A dependency may legitimately ship a directory
  named `tests`, metadata, or bytecode; a basename match at arbitrary depth is not proof that
  repository development content leaked. Continue to reject unsafe paths, secret-bearing content,
  caches, and unsupported entry types wherever they occur.
- Treat compiled bytecode, generated files, and vendored content according to the packaging
  contract and their provenance. Neither their presence nor absence is universally safe.
- Compare the exact expected asset set, checksums, signatures, attestations, or provenance with the
  release contract. Unexpected extras and missing evidence are findings, including when a release
  already exists.

## Exercise the result

Install or launch the packaged result on each supported target class when practical. Test first
run, upgrade or migration, failure and cleanup paths, shutdown, and uninstall or residual-data
behavior. Report unexecuted target tests separately; source-level tests do not substitute for them.
