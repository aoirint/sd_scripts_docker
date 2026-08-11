# Fallback Pull Request Body

Use this fallback only when the repository has no applicable pull request
template. If a repository template exists, the live template takes precedence.
Apply repository-specific requirements only when they are present in current
repository guidance. Do not infer a CLA, checklist, sign-off, or other policy
from this generic scaffold.

## Contents

- [Fallback Scaffold](#fallback-scaffold)

## Fallback Scaffold

Keep the universal headings below. When a section has no applicable content,
write `None` or `Not applicable` instead of removing the heading. Add a
repository-specific section only when current repository guidance requires it.

````markdown
<!--
If significant AI assistance affected this pull request, put this alert at the
very top of the PR body:

> [!WARNING]
> This pull request was created with assistance from LLMs.

Then describe the AI assistance under "AI disclosure" below.
-->

## Summary

<!--
Briefly describe what changed, who it affects, and why it is useful.
If this pull request mixes unrelated behavior, documentation, refactors, or
cleanup, split it or explain why the work should stay together.
If the title or commits include `!` or `BREAKING CHANGE`, include a
`### Breaking Changes` subsection.
Treat a change as breaking when it removes, renames, or incompatibly changes
public behavior, documented workflows, configuration, package or release
behavior, compatibility guarantees, or other project-facing contracts that
users, maintainers, automation, or downstream packaging reasonably rely on.

Optional H3 examples:
### User impact
### Contributor impact
### Maintainer impact
### Breaking Changes
-->

## Related Issues

<!--
Prefer Markdown list items for GitHub issues or pull requests so GitHub can
render rich references.
Use closing keywords, such as "Closes #123", when this pull request should
close an issue.
For non-GitHub references, include enough context for reviewers to understand
why the link matters.
Use "None" if there is no related issue.

Markdown list examples:
- Closes #123
- Refs #456
- Refs owner/repository#789
-->

## Notes for reviewers

<!--
Share non-testing context that helps reviewers understand or prioritize this
pull request.
For example, mention review focus, trade-offs, compatibility risks,
generated outputs, packaging concerns,
or areas that need extra attention for reasons other than AI assistance.
-->

### Proposed merge attribution

<!--
Keep every potential squash-merge co-author reviewable from PR creation through
updates. Include the author of an implemented issue and every material design
or snippet provider by default; a reviewer must explicitly mark a candidate
"Not applicable" to exclude them.

For a human candidate, record the public GitHub account and immutable numeric
user ID, a non-private contribution basis, status, and the resolved trailer:
- @login (GitHub user ID: 123)
  - Resolved trailer: Co-authored-by: login <GitHub-provided-noreply@example.com>
  - Basis: Implemented issue #123 / material design or snippet contribution.
  - Status: Included / Needs identity / Needs review / Not applicable

Do not add the PR creator or the person who merges merely because of those
roles. GitHub squash merge records the PR creator as primary Git author, but
that can differ from the material contributors. If the creator is not material
to the final diff, mark this `Needs review` and do not merge until a maintainer
confirms that attribution or selects another authorized integration path. A
review comment or approval alone is not a candidate. Include every final-diff
PR-head commit author and existing co-author trailer unless already the PR
creator's primary Git author. If GitHub applied a review suggestion that remains
in the final diff, include its suggestion provider and applier unless already
the PR creator's primary Git author, and record the source commit SHA or review
URL here.

Use a contributor-supplied GitHub-provided noreply address for every human
trailer by default; never synthesize one from @login or numeric ID. Use a Public
Email only when the contributor explicitly directs that choice and GitHub
currently exposes the exact address; record the choice here. An existing
trailer is reusable only when its GitHub author association proves the same
account. If any candidate's contribution, applicability, account, exact email,
trailer, or status is uncertain, use Needs identity or Needs review and do not
merge.
Do not use a legacy LOGIN@users.noreply.github.com fallback. State "None
proposed" if no candidates apply. Make all candidate/status/identity changes
reviewable; do not silently remove or replace an entry.
-->

### AI disclosure

<!--
If AI assistance significantly affected this pull request, disclose it here.
Mention what the AI helped with, how you reviewed or adapted the result, and
any AI-assisted areas you did not review closely.
Use "None" if no significant AI assistance was used.

Optional H3 examples:
### Review focus
### Lower-confidence areas
-->

## Testing

<!--
List the checks you ran and their results.
Include commands, manual in-game checks, screenshots, or videos when relevant.
For docs-only changes, mention proofreading, link checks, formatting checks,
or "Not run - docs only."
If you did not run a relevant check, explain why.
You are responsible for masking personal information, local absolute paths,
access tokens, and other sensitive details before posting logs, screenshots,
or videos.
Do not present AI-performed review, inspection, editing, verification, or other
work as "manual". For example, if you include AI-assisted inspection, list a
short `Request: ...` summary first, nest the `AI-assisted result: ...` under it,
and clearly label the result as AI-assisted.

Optional testing structure:
### Build log

<details>

```plain
$ DOTNET_CLI_UI_LANGUAGE=en dotnet build
Paste the relevant output here.
```

</details>

### Automated checks
### AI-assisted inspections
### Manual checks
### Screenshots / videos
-->

````
