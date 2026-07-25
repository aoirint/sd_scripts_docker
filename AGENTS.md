# Agent Instructions

Use the Agent Skills in `.agents/skills/` when they match the task.
For repository changes, create task worktrees under `.agents/worktrees/`.
Keep changes focused, commit completed phases, and run the relevant project
checks before opening or updating a pull request.

## APM-managed Skills

Repository-local Agent Skills are deployed to `.agents/skills/` by
[APM](https://github.com/microsoft/apm). Do not edit that generated directory
directly.

- `apm.yml` pins the selected public
  [aoirint/skills](https://github.com/aoirint/skills) package, and
  `apm.lock.yaml` records its resolved commit and content hashes.
- Keep this unpublished APM project at `version: 0.0.0` until its distribution
  and versioning design is explicitly decided.
- To restore the committed Skill set, run `apm install --frozen` from the
  repository root, then run `apm audit --ci`.
- Make shared Skill changes in
  [aoirint/skills](https://github.com/aoirint/skills). This repository only
  selects, pins, and deploys them.
- To update the Skill dependency, review its source, commit pin, license, and
  cooldown first. Regenerate the lockfile with APM, then run
  `apm install --frozen` and `apm audit --ci`. Commit the manifest, lockfile,
  notices, and generated `.agents/skills/` changes together.

### Approved cooldown exception

A maintainer explicitly approved adopting the current direct
`aoirint/skills` commit
`8a2bb13afb40cc31dbcd3280b74004834d428b4a` before its normal seven-day
cooldown. This exception applies only to that direct dependency selection; it
does not waive review or cooldown requirements for any of its dependencies.
