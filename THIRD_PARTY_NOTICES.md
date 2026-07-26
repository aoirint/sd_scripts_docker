# Third-Party Notices

This project builds Docker images that include third-party software.

## kohya-ss/sd-scripts

- Source: https://github.com/kohya-ss/sd-scripts
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
  [`8c671f524fb5df6b9def895f8b60e9a359b07644`](https://github.com/aoirint/skills/tree/8c671f524fb5df6b9def895f8b60e9a359b07644)
- Deployed paths: `.agents/skills/{changelog-workflow,code-quality-check,commit-message-quality-check,git-worktree-workflow,github-actions-quality-check,gitignore-workflow,issue-quality-check,prose-quality-check,pull-request-quality-check,release-note-workflow,security-check,skill-quality-check}/`
- License: [MIT](https://github.com/aoirint/skills/blob/8c671f524fb5df6b9def895f8b60e9a359b07644/LICENSE)
