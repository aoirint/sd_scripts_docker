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
