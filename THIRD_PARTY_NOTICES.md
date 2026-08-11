# Third-Party Notices

This project builds Docker images that include third-party software.

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
  [`f4aa56f4abffb1448c24c04ea4ae4463f5721d10`](https://github.com/aoirint/skills/tree/f4aa56f4abffb1448c24c04ea4ae4463f5721d10)
- Deployed paths: `.agents/skills/{apm-workflow,changelog-workflow,code-quality-check,commit-message-quality-check,docker-quality-check,git-worktree-workflow,github-workflow,gitignore-workflow,prose-quality-check,python-quality-check,release-note-workflow,security-check}/`
- License: [MIT](https://github.com/aoirint/skills/blob/f4aa56f4abffb1448c24c04ea4ae4463f5721d10/LICENSE)
- Copyright: Copyright (c) 2026 aoirint
