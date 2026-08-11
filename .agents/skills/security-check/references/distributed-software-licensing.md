# Distributed Software Licensing

Use this checklist when a repository compiles, links, bundles, or redistributes
third-party software. Treat licensing as an artifact property: the upstream project's
headline license and a successful build do not by themselves establish that the final
combination can be redistributed.

## Review the actual combination

1. Inventory the primary program, every statically or dynamically linked library,
   copied runtime component, enabled optional feature, and build flag for each shipped
   variant.
2. Consult authoritative license text and upstream compatibility guidance for the exact
   versions and configuration. Record evidence and uncertainty; do not make an unsupported
   legal conclusion from license names alone.
3. Identify flags or dependencies that change the resulting license, impose source or
   notice obligations, or mark the binary non-redistributable. Treat removing such a
   dependency or feature as a product change that needs explicit review and testing.
4. Inspect the artifact that will actually be published. Use any built-in license report,
   dependency inventory, binary-linkage inspection, and container/archive inspection that
   applies. Do not substitute Dockerfile intent, configure output, or builder contents for
   final-artifact evidence.
5. Verify every published variant independently. CPU, GPU, platform, and feature variants
   can use different configure flags, linked libraries, and resulting terms.
6. Include required license and notice files in the final artifact, and keep repository
   disclosures synchronized with what is actually shipped. Apply `docker-quality-check`
   for container-specific `THIRD_PARTY_NOTICES.md`, README, and final-image checks.
7. Block publication when authoritative compatibility evidence, final-artifact evidence,
   or a required variant cannot be checked. Record the exact unverified scope instead of
   inferring a pass.

## FFmpeg builds and redistribution

FFmpeg is a frequent configuration-sensitive case. For every shipped FFmpeg binary and
image variant:

1. Capture the exact FFmpeg version or commit, configure line, enabled external libraries,
   and final binary digest. Review FFmpeg's current authoritative legal and license
   documentation together with the licenses of enabled libraries.
2. Inspect flags that change redistribution status or license compatibility, especially
   `--enable-gpl`, `--enable-version3`, and `--enable-nonfree`. Do not assume that adding
   `--enable-nonfree` merely enables another codec; FFmpeg uses it to identify a resulting
   build that is not redistributable.
3. Check external libraries in combination with those flags. A commonly problematic
   example is enabling `libfdk_aac` together with GPL components: verify the current
   upstream guidance rather than relying on the libraries' individual licenses.
4. Inspect GPU variants separately. Options and libraries such as CUDA toolkit components
   or `libnpp` can change the resulting status even when NVENC/NVDEC support through
   `nv-codec-headers` remains available. Verify the exact current flags; do not copy a
   conclusion from the CPU variant.
5. Run the final binary's `ffmpeg -L` and retain the full output as evidence. Fail the
   publication gate if it reports `nonfree`, `unredistributable`, or equivalent wording
   inconsistent with the intended distribution. Also verify `ffmpeg -buildconf` or the
   embedded configuration against the reviewed build contract.
6. Verify required upstream license files, such as the license selected by the resulting
   configuration, are present in the final image or package. Confirm repository notices
   name FFmpeg prominently and describe the shipped version source and license without
   hiding it among development-only dependencies.
7. Exercise representative codecs, filters, and hardware paths after a compliance-driven
   flag or library change. Record intentionally removed features so a licensing correction
   is not misreported as behavior-preserving maintenance.

Do not generalize a result across versions or variants. FFmpeg configuration rules and
external dependency terms are version-sensitive; re-check authoritative sources whenever
the FFmpeg version, build flags, linked libraries, or image variants change.
