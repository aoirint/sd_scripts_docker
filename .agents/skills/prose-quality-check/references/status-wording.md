# Status and Qualifying Wording

Use these examples when a status or process term may be unnecessary, ambiguous,
or stronger than the evidence. The issue is the information added in context,
not the presence of a particular word.

## Editorial examples

- If the surrounding workflow already identifies the document under review,
  prefer its subject as the title rather than adding "reviewed version."
  A real distinction between a reviewed revision and a changed revision can
  still matter; retain it where readers need to choose between them.
- Replace "the approved version in the lockfile" with "the version pinned in
  the lockfile" when the pin is the relevant fact. If the instruction already
  says to use the lockfile and no version distinction matters, omit the extra
  phrase. A pin alone is not evidence of approval.
- A repository's own usage guide ordinarily belongs to the revision being read.
  Do not add "reviewed version," "approved version," or "default-branch
  version" merely to identify that context. Remove the qualification when
  unnecessary. Name a branch or revision when a real distinction matters,
  such as a branch workflow, release procedure, or CI target. Presence on the
  default branch alone does not establish review or approval.
- A pull request proposing a version update must not describe that proposal
  as already approved merely because approval is expected before merge.
  Use the version or proposed change, or state the pending decision when
  readers need it. Preserve an actual approval of the same revision when
  supported and relevant.
- "Get approval before publishing" needs an approver if readers cannot tell
  whose decision is required. "Ask the user to review the draft. Publish only
  after approval" already identifies the approver; repeating "by the user"
  need not help.
- A test report may need the checked environment, revision, and result.
  Include only the detail needed to interpret that result, rather than giving
  every use of "verified" a fixed date-and-version template.
  A needed "reviewed" claim must have an identifiable review basis; a needed
  "latest" claim must have a meaningful reference point or release channel.
  If the basis is unavailable, flag the consequential gap instead of inventing
  criteria or replacing the label with another unsupported assurance.
- In parallel installation requirements, "Install A, the latest B, and C"
  implies that B has a distinct freshness requirement. If no such difference
  is intended or needed, use "Install A, B, and C" rather than extending
  "latest" to all three. Preserve genuine minimum versions, security update
  requirements, or release-channel differences, making their scope clear.
  A literal `latest` tag or command argument is not a stylistic qualifier;
  do not change its operational meaning as part of a prose edit.
- If "latest" really applies to each item in "the latest A, B, and C," make
  that shared scope explicit, for example "the latest supported releases of A,
  B, and C." Repeat a necessary modifier in each independently read list item.
  Do not rely on readers guessing whether the first item's modifier extends
  to later items. Use different modifiers when different requirements apply.
