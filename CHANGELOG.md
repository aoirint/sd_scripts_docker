# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses date-based release tags for historical releases and is moving
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for future
releases.

## [Unreleased]

### Added

- Add a canonical changelog with backfilled release history.
- Add repository Agent Skills and guidance for changelog, quality, security,
  GitHub Actions, git worktree, and review workflows.
- Add third-party license notices for the bundled `kohya-ss/sd-scripts`
  checkout.
- Add a reusable release-test script that runs selected upstream sd-scripts
  pytest targets inside the published Docker image.
- Add a documented sd-scripts update procedure covering dependency, Dockerfile,
  build, and release-test checks.

### Changed

- Update the bundled sd-scripts checkout to v0.10.5.
- Align the Dockerfile stage structure and uv project configuration with the
  current release workflow.
- Rework releases to use the root `VERSION` file, SemVer-style tags, immutable
  GitHub Releases, and Docker image tags derived from release mode.
- Document release procedure, maintenance links, bundled license context, and
  Docker Engine 29 or later as the current requirement.

### Notes

- The next stable release material is intentionally kept under `Unreleased`
  until the release PR sets the final version and release date.

## [v20251209.2] - 2025-12-09 UTC

### Added

- Add an SDXL LoRA training example.

### Changed

- Update the bundled sd-scripts checkout to `206adb6`.
- Switch WD14 captioning dependencies from TensorFlow to ONNX Runtime.

### Fixed

- Install the bundled sd-scripts project as an editable package inside the
  image.

## [v20251209.1] - 2025-12-08 UTC

### Changed

- Switch Python dependency management to uv.
- Renew the Docker build CI workflow and build cache setup.
- Update `requests` to 2.32.4.

### Fixed

- Correct the GitHub Container Registry build-cache repository.
- Correct the Python version used by CI.

## [20250322.1] - 2025-03-22 UTC

### Changed

- Update the bundled sd-scripts base to v0.9.1.
- Refresh CI disk cleanup before checkout.

## [20241230.3] - 2024-12-30 UTC

### Changed

- Document Docker Engine 27.0 or later as the runtime requirement.
- Clarify README wording and project fork context.

## [20241230.2] - 2024-12-30 UTC

### Changed

- Update the bundled sd-scripts checkout through the local `aoirint/sd-scripts`
  fork after adopting the upstream `kohya-ss/sd-scripts` update.

### Notes

- This release was published as a prerelease on GitHub.

## [20241230.1] - 2024-12-30 UTC

### Changed

- Update the bundled sd-scripts checkout to 0.8.7.
- Update Python to 3.10.16 and pyenv to 2.5.0.
- Update the Dockerfile syntax image to 1.12.
- Refresh Python dependencies, including TensorFlow, transformers, requests,
  aiohttp, OpenCV, Werkzeug, Jinja2, urllib3, tqdm, certifi, zipp, idna, and
  scikit-learn.
- Update CI disk cleanup targets.

### Fixed

- Relax the container execution user restriction.

### Notes

- This release was published as a prerelease on GitHub.

## [20231108.3] - 2023-11-08 UTC

### Changed

- Document mounting the WD14 tagger model cache directory.

## [20231108.2] - 2023-11-08 UTC

### Added

- Add WD14 captioning documentation.

### Changed

- Downgrade TensorFlow and TensorBoard to 2.10.1.
- Add the `libnvrtc.so` workaround needed by the image at the time.

### Notes

- This release was published as a prerelease on GitHub.

## [20231108.1] - 2023-11-07 UTC

### Changed

- Update the bundled sd-scripts checkout to v0.7.0.
- Update Python dependencies, including requests and urllib3.

## [20231105.1] - 2023-11-05 UTC

### Changed

- Change the base image to
  `nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04`.
- Manage all Python library versions in the repository.
- Install Python libraries before cloning sd-scripts.
- Update bitsandbytes to 0.41.1.

## [20231103.1] - 2023-11-02 UTC

### Added

- Add `lycoris-lora` 1.9.0 to the image.

### Changed

- Rename `requirements-torch.txt` to `requirements-pre.txt`.

## [20231005.2] - 2023-10-05 UTC

### Changed

- Update the Dockerfile syntax image to 1.6.

## [20231005.1] - 2023-10-05 UTC

### Changed

- Update the bundled sd-scripts checkout to v0.6.6.
- Update torch dependencies and xformers to 0.0.22.
- Update Python to 3.10.13.
- Update GitHub Actions and Dockerfile syntax handling.

### Notes

- This release was published as a prerelease on GitHub.

## [20230731.1] - 2023-07-31 UTC

### Added

- Add the MIT license.
- Add README requirements and usage documentation.

### Changed

- Update the bundled sd-scripts checkout to v0.6.5.
- Update Python to 3.10.12 and pyenv to 2.3.23.
- Update Python dependencies.

## [20230706.1] - 2023-07-06 UTC

### Added

- Add the initial Docker image project files.
- Add the first GitHub Actions build workflow and disk cleanup step.
- Add initial ignore rules for local work directories.

[Unreleased]: https://github.com/aoirint/sd_scripts_docker/compare/v20251209.2...HEAD
[v20251209.2]: https://github.com/aoirint/sd_scripts_docker/releases/tag/v20251209.2
[v20251209.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/v20251209.1
[20250322.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20250322.1
[20241230.3]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20241230.3
[20241230.2]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20241230.2
[20241230.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20241230.1
[20231108.3]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231108.3
[20231108.2]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231108.2
[20231108.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231108.1
[20231105.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231105.1
[20231103.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231103.1
[20231005.2]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231005.2
[20231005.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20231005.1
[20230731.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20230731.1
[20230706.1]: https://github.com/aoirint/sd_scripts_docker/releases/tag/20230706.1
