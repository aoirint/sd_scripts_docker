# Durable Context

Use these checks before revising prose intended to stand on its own after the
originating conversation. Preserve information readers need without making
every stable fact carry a date or version.

## Conversation references

Replace "this conversation" or "this chat" with the relevant decision,
subject, rationale, or scope. Remove the reference when it adds nothing.
Supply essential context in the document or cite an established supporting
source accessible to the audience. Check availability and audience access; a
link alone does not make private or unavailable context usable.

Flag unresolved context or access gaps. Do not publish a new external document
or change access permissions merely to make prose self-contained; those
operations require separate authorization.

## Time boundaries

Treat "currently," "previously," "existing," and similar expressions as review
cues, not banned strings. Remove a time distinction that does not help readers
act or interpret the claim rather than dating an otherwise durable fact.

For a changing fact that needs a time boundary, use the source-supported
observation or effective date at the coarsest unambiguous precision: a year or
month for a broad period, a full date for a dated state, or a timestamp with
time zone for a rapidly changing state. Include the year. Flag missing temporal
evidence; do not invent precision or substitute the editing date.

Keep useful dated snapshots and qualified expectations. Distinguish observations
from planned or possible changes without turning forecasts into guarantees.

## Version scope

State reader-relevant compatibility or applicability at the needed precision.
Omit irrelevant version detail and incidental exact pins duplicated from
configuration or lockfiles. Prefer major or minor precision when sufficient;
retain exact revisions needed for behavior, compatibility, or reproduction.
Do not broaden a supported or tested range to simplify its notation.

Give human readers the version information they need directly in the document,
even when an exact revision matters. Consult authoritative pins during
verification without sending human readers to a lockfile for that information.
Agent-facing instructions may direct the agent to authoritative lockfiles.

## Executable runbooks

Keep human-facing runbooks self-contained for safe execution, including necessary
exact commands and version constraints. Allow duplication needed for safety and
reasonable reader effort. Keep the authoritative source and update needs clear
to control drift; use the owning workflow or domain Skill to verify the procedure
and coordinate updates.

## Earlier behavior

After a behavior change, do not leave "existing behavior" dependent on the
pre-change editing context. Retain earlier behavior when readers need it,
naming the relevant version, state, or date and why the distinction matters.

Use `domain-architecture-docs-workflow` to decide whether audience impact
justifies retained history in maintained documentation or a reference to
version-specific documentation. Preserve explicit compatibility, migration,
and support requirements, including necessary transition steps.
