# Avoiding overengineering

## Purpose

Use this reference when a change introduces structure or safeguards beyond the direct feature edit.
The goal is not to minimize lines of code. It is to keep every addition tied to a current need while
preserving correctness, security, and maintainability.

## Decision rule

Establish ownership before comparing implementation and maintenance cost. Identify the current
repository requirement that makes a proposed capability belong in the repository at all. A helper's
own tests, coverage contribution, or general usefulness do not create a consumer, contract, failure
mode, or evidenced risk. Without one of those justifications, remove or defer the capability instead
of making its implementation cheaper.

Before implementing packaging verification, ask whether a distribution is part of the project's
current contract. An installable source layout or configured build backend does not create a
distribution consumer. For a local application operated through its locked project environment,
verify locked setup and actual application or CLI behavior. Do not build a wheel, create a second
environment, reinstall the wheel, and run an import-only smoke check without a current publication,
deployment, or external-install requirement.

When a distribution is a current deliverable, a reviewed packaging tool still owns wheel-format
validity and ordinary installer compatibility. Installation is test setup, not a meaningful oracle
by itself. Use the exact artifact only when project-owned packaging configuration or an evidenced
failure can change consumer behavior, then exercise that behavior, such as loading required package
data or starting the deployed service. A successful install or import-only smoke check provides no
distinct evidence without such a contract. Archive member counts, generic file-mode rules, and
digest shape likewise remain tool implementation details unless this project has an explicit
reproducibility, publication, or threat-model requirement for them. Do not implement tool-owned
validation; if it already exists, remove the validation behavior and its dedicated tests instead of
refactoring its assertions.

Keep an addition when at least one concrete justification exists:

- A current caller, user, or operator needs it.
- A documented contract requires it.
- An observed failure or realistic failure mode requires it.
- An evidenced security, compatibility, data-loss, or operational risk requires it.
- Deferring it would make a known near-term change materially harder or unsafe.

Do not implement an addition only because it might be useful someday, completes an imagined
framework, or makes the design look more general. Preserve an obvious place for later change when
that is cheap, but do not implement the later change itself.

Ask these questions during review:

1. Who or what uses this now?
2. What concrete failure occurs without it?
3. Is that failure reachable in the current system?
4. Can a smaller local change satisfy the same need?
5. Would a comment or maintained document preserve the decision without executable machinery?
6. Would a reasonable internal refactor break the added test despite preserving behavior?
7. If this addition were removed, which current requirement would become unmet?

An unclear answer is a reason to defer or narrow the addition, not proof that it is unnecessary.
Investigate high-impact correctness and security uncertainty before removing a safeguard.

## Common review examples

| Situation | Proportionate change | Likely overengineering |
| --- | --- | --- |
| One implementation exists | Keep direct code behind a clear function or module boundary | Add factories, strategies, providers, and adapters for hypothetical implementations |
| A small duplication appears once | Leave it local until the shared concept and change pattern are clear | Create a generic utility based on superficial similarity |
| A later component is plausible | Reserve a clear ownership boundary or document the extension rule | Add empty modules, placeholder resources, or configuration for the component |
| Access rules may grow | Group current rules by real responsibility and review applicable limits when growth occurs | Pre-create unused rule sets or split every operation into its own unit |
| External input is unsafe | Validate once at the trust boundary and pass a normalized value inward | Revalidate the same guaranteed invariant in every internal layer |
| A concrete attack path exists | Block the reachable path with the smallest complete safeguard | Implement an exhaustive taxonomy of unrelated hazards without a threat model |
| Tests are needed | Assert observable behavior, contracts, effects, or security outcomes | Assert naming patterns, internal categories, or the current object graph |
| A transient failure is expected | Retry that failure with an explicit limit and observable outcome | Catch every exception and add multiple speculative fallback paths |
| A small standard feature is sufficient | Use the language or platform facility directly | Add a dependency or framework for a few straightforward operations |
| A local application uses an installable source layout | Replay its locked environment and exercise actual application or CLI behavior | Build a wheel, install it into a second environment, and run import-only smoke checks without a distribution consumer |
| A delivered artifact has an evidenced project-packaging failure | Use the exact artifact as test setup and exercise the affected user or deployment behavior | Treat successful installation or import alone as evidence, or inspect generic archive internals |
| A rare manual procedure is adequate | Document the bounded procedure and its risks | Build automation before repetition, error rate, or operational cost justifies it |
| Configuration has one current mode | Expose only values that users must choose now | Add flags for imagined modes with no current consumer |
| A non-obvious choice must survive | Record the reason, rejected practical alternative, and revisit condition | Document a detailed roadmap for unapproved future architecture |

## Boundaries that justify structure

Splitting code is justified when responsibilities have different owners, callers, change reasons,
permissions, failure handling, or lifecycles. Keeping related behavior together is justified when it
changes and is reviewed as one unit. Neither more files nor fewer files is an independent quality
goal.

Similarly, defensive code is not overengineering merely because it adds complexity. Keep controls
that address a reachable high-impact failure. Narrow controls whose scope exceeds the evidenced
risk, and remove controls that only restate guarantees already enforced at a stronger boundary.

## Review outcome

Classify each questionable addition as one of:

- **Keep**: a current contract, consumer, failure mode, or evidenced risk justifies it.
- **Narrow**: the need is real, but the implementation covers more cases or layers than necessary.
- **Defer**: the idea may be useful later, but there is no current implementation need.
- **Remove**: it adds maintenance cost without distinct behavior, evidence, or protection.
- **Investigate**: correctness or security impact is plausible but evidence is incomplete.

Explain the concrete reason for the classification. Do not label code as overengineered only because
it is unfamiliar, detailed, or longer than an alternative.
