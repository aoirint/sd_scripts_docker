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
  [`44b51eef2237a460a4d3bca423a675b1ffd09eda`](https://github.com/aoirint/skills/tree/44b51eef2237a460a4d3bca423a675b1ffd09eda)
- Deployed paths: `.agents/skills/{apm-workflow,changelog-workflow,code-quality-check,commit-message-quality-check,docker-quality-check,git-worktree-workflow,github-workflow,gitignore-workflow,prose-quality-check,python-quality-check,release-note-workflow,security-check}/`
- License: [MIT](https://github.com/aoirint/skills/blob/44b51eef2237a460a4d3bca423a675b1ffd09eda/LICENSE)
- Copyright: Copyright (c) 2026 aoirint
