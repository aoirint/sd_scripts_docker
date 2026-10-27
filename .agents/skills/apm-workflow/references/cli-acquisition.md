# Obtain the Reviewed APM CLI

## 2. Obtain the selected eligible APM version safely

Reuse an installed copy only when its exact version matches the selected
reviewed release. Do not run an unpinned installer or `apm self-update` merely
to obtain whatever version is newest upstream.

Treat installation, self-update, PATH changes, and replacement of the active
APM binary as user-environment changes. A request to maintain one repository
does not authorize them.

Read [the bootstrap manifest](apm-bootstrap.json), then consult the
current [official installation guide](https://microsoft.github.io/apm/getting-started/installation/),
[`apm self-update` reference](https://microsoft.github.io/apm/reference/cli/self-update/),
and installer source in the
[official APM repository](https://github.com/microsoft/apm). Do not reproduce
their commands, paths, environment variables, or installer behavior in this
Skill: those are upstream-owned and may change. The manifest remains this
Skill's source of truth for the reviewed version, release date, artifacts, and
SHA-256 values.

When the selected version is not installed:

1. Download the exact official release archive named in the bootstrap manifest
   to a unique operating-system temporary directory. Verify its hard-coded
   SHA-256 before extraction, extract the complete bundle, and invoke the
   packaged executable by absolute path. Do not add it to PATH, copy a shim,
   place it in the repository, or alter the active APM installation.
2. Confirm `--version` exactly matches the manifest. If the official artifact
   is not portable on the current platform, cannot preserve its adjacent
   runtime files, or fails integrity verification, stop instead of inventing an
   installation layout or choosing an ineligible version.
3. Remove only the validated task-specific temporary directory after the work
   finishes. Record the archive source, expected and observed SHA-256,
   executable path, and version in the handoff.
4. If the user explicitly requests a persistent installation, then consult the
   current official sources above and use their documented version-pin and
   integrity mechanisms. Let the official installer own its layout. Do not
   alter PATH or replace an active binary without explicit authorization for
   those specific environment changes.
5. For an enterprise mirror, use HTTPS, set `APM_NO_DIRECT_FALLBACK=1`, and
   verify that the mirror serves the identical reviewed artifact and checksum.
   Do not treat this as a substitute for review of the artifact.
