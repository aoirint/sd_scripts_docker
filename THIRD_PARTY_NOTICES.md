# Third-Party Notices

This project builds Docker images that include third-party software.

## NVIDIA CUDA container image

- Source: <https://hub.docker.com/r/nvidia/cuda>
- Base image: see `CUDA_RUNTIME_IMAGE` in `Dockerfile`
- Bundled location in image: `/usr/local/cuda-12.9`
- License: NVIDIA Deep Learning Container License
  <https://developer.download.nvidia.com/licenses/NVIDIA_Deep_Learning_Container_License.pdf>
- License file in image: `/NGC-DL-CONTAINER-LICENSE`

## kohya-ss/sd-scripts

- Source: <https://github.com/kohya-ss/sd-scripts>
- Bundled location in image: `/opt/sd-scripts`
- Version: see `SD_SCRIPTS_VERSION` in `Dockerfile`
- License: primarily Apache License 2.0, with some portions under separate
  terms as documented upstream

The image includes the selected upstream checkout, including the license files
that are present in that checkout.

## aoirint/skills

- Source: [aoirint/skills](https://github.com/aoirint/skills), selected from
  `.apm/skills/`
- Pinned commit:
  [`22fe4f84018358059adcf7709cb9df28d1260fd8`](https://github.com/aoirint/skills/tree/22fe4f84018358059adcf7709cb9df28d1260fd8)
- Deployed paths: `.agents/skills/{apm-workflow,changelog-workflow,code-quality-check,commit-message-quality-check,docker-quality-check,git-worktree-workflow,github-workflow,gitignore-workflow,prose-quality-check,python-quality-check,release-note-workflow,security-check}/`
- License: [MIT](https://github.com/aoirint/skills/blob/22fe4f84018358059adcf7709cb9df28d1260fd8/LICENSE)
- Copyright: Copyright (c) 2026 aoirint

- Cooldown: the maintainer requested immediate adoption of this exact direct
  `aoirint/skills` commit. This exception waives only its waiting period;
  dependencies remain subject to independent review and cooldown.
