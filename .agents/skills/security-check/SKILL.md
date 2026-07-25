---
name: security-check
description: >-
  Review repository changes for practical security and supply-chain risks. Use
  when work touches secrets, permissions, untrusted input, dependencies,
  executable or downloaded artifacts, CI or deployment configuration,
  containers, or vendored/generated files; skip documentation-only changes with
  no security-sensitive surface.
---

# Security Check

## Goals

- Provide a single repository-local security reference point for agents and
  maintainers.
- Treat this guidance as a practical project baseline, not permission to take a
  less safe path than a tool, platform, organization policy, package manager, or
  current general security practice requires.
- Prefer source-backed, version-aware, reviewer-visible decisions over
  convenient but unverified execution.
- Keep ecosystem-specific implementation details in dedicated follow-up work
  when the repository cannot reasonably verify or maintain them here.
- Do not treat out-of-scope ecosystem trust infrastructure as permission to
  skip practical trust checks that current tools, platforms, organizations, or
  general security practice expect agents to perform.
- Record blockers, residual risk, and maintainer-approved exceptions clearly.

## Workflow

1. Identify the security-sensitive surface and pair with `code-quality-check` for implementation
   changes or `skill-quality-check` for Agent Skill changes when applicable:
   - Secrets, credentials, tokens, private data, or logs.
   - Permission boundaries, CI permissions, publishing credentials, or
     filesystem/network access.
   - User-provided input, deserialization, file paths, shell commands, or
     remote APIs.
   - Dependencies, package-runner invocations, downloaded CLI tools, CI
     actions, containers, vendored artifacts, generated code, or copied files.
2. Apply the strongest applicable rule first:
   - Follow Codex, Claude Code, GitHub Copilot, platform, organization,
     package-manager, and current general security requirements when they are
     stricter or safer than this repository guidance.
   - Treat repository-local guidance as the floor. It must not lower stronger
     external requirements.
   - When guidance conflicts, lags behind, or is uncertain, choose the stricter
     or safer path and report the reason.
3. Prefer safe defaults:
   - Use least privilege for credentials, CI tokens, filesystem access, network
     access, and service permissions.
   - Avoid logging secrets, private paths, personal data, tokens, or sensitive
     request and response bodies.
   - Avoid broad shell execution, mutable global state, insecure temporary
     files, untrusted archive extraction, and implicit remote-code execution
     unless the controls are explicit and reviewed.
   - Disable network access or sandbox execution where the workflow and tooling
     reasonably allow it.
   - Use a real public domain in an example only when that specific service is
     part of the demonstrated contract and contacting it is intentional. For a
     generic hostname or URL, use an example name reserved by
     [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.html) or
     [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html), such as
     `example.com`, `example.net`, `example.org`, a subdomain of one of them,
     or a suitable `.test`, `.invalid`, or `.localhost` name.
     Choose `.localhost` only when loopback behavior is the point of the
     example; do not make it look like a neutral remote service.
   - Do not substitute an arbitrary plausible or unrelated live domain into
     sample configuration, tests, screenshots, documentation, or generated
     prompts. A reserved name does not authorize network access: keep runnable
     examples mocked/offline unless the task explicitly requires a reviewed
     live request.
4. Handle suspected security vulnerabilities carefully:
   - Do not post exploit details, reproduction steps, secret values, vulnerable
     endpoints, private data, or other sensitive security details in public
     issues, pull requests, social media, livestreams, videos, or similar
     public channels.
   - Look for the repository's private reporting path, such as `SECURITY.md`,
     GitHub private vulnerability reporting, a draft security advisory, or a
     maintainer-provided contact method.
   - Report suspected security issues to the maintainer through a private and
     secure channel when possible, or to a trusted security organization when a
     maintainer channel is unavailable.
   - In public repository work, use only a minimal non-sensitive note when a
     security issue exists, is blocked, or has been reported privately.
5. Apply the supply-chain baseline below for supply-chain-sensitive work.
6. If the safe path cannot be verified, do not normalize the risky action:
   - Report a blocker when release age, provenance, runtime behavior, or
     cooldown compliance cannot be verified.
   - Record residual risk when a partially controlled path remains.
   - Require a documented maintainer exception before proceeding with a weaker
     path.
7. Inspect repository scripts,
   lockfiles, and tool configuration so the recommendation is grounded in the
   project instead of inventing a new ad hoc path.
8. Record what was checked:
   - Sources consulted and why they were sufficient or insufficient.
   - Exact versions, refs, tags, digests, hashes, or lockfile entries reviewed.
   - Commands that were run or intentionally skipped.
   - Whether sensitive security details were withheld from public channels and
     reported privately when applicable.
   - Follow-up issues for ecosystem-specific controls that exceed this
     general security skill.

## Supply-Chain Baseline

- For tool-specific fixed-install and execution patterns, consult
  [external-code-execution.md](references/external-code-execution.md) when the
  listed tool applies.
- For archives, installers, bundles, release assets, or packaged applications,
  apply [artifact-inspection.md](references/artifact-inspection.md) to the final
  artifact rather than trusting the staging directory or build log.
- Treat new or updated third-party packages, package-runner invocations,
  downloaded CLI tools, GitHub Actions, containers, vendored artifacts,
  generated code from external tools, copied files, and dependency lockfile
  updates as supply-chain-sensitive.
- Include direct and transitive dependencies when they are resolved by a
  lockfile, package manager, container image, generated artifact, or vendored
  bundle. Do not limit the review to direct dependency declarations when the
  resolved graph is available.
- Require a minimum 7-day cooldown before adopting newly released third-party
  packages, downloaded binaries, CI actions, containers, or other external
  executable artifacts unless the user or maintainer explicitly approves an
  exception.
- Treat cooldown as a minimum gate, not as proof that an external artifact is
  trustworthy after the waiting period. Continue to evaluate provenance,
  pinning, runtime behavior, permissions, vulnerability signals, and stricter
  current security requirements before running or adopting it.
- Prefer pinned, reviewable versions over floating references such as `latest`,
  default branches, unpinned images, or implicit package-runner resolution.
- Verify release age and provenance from source-backed evidence such as package
  registry metadata, release pages, tags, changelogs, signed artifacts,
  lockfiles, upstream commit history, or maintained package-manager docs.
- Apply this execution gate before selecting an installation or execution
  command. It covers every mechanism that resolves, downloads, builds, loads,
  or executes third-party code at run time, whether it is a package manager,
  language runtime, plugin host, editor extension, archive installer, URL, or
  a future tool not named here:
  1. Use an existing project dependency only when its immutable resolution and
     lockfile (including available integrity data) have already been reviewed.
  2. Otherwise, stop execution and complete the adoption review first: record
     canonical source and publisher, immutable version/commit or artifact
     digest, release date and seven-day eligibility, resolved direct and
     transitive dependencies, and runtime behavior.
  3. Use only a command whose exact configuration demonstrably enforces the
     required controls before it resolves or executes code. A differently
     named runner, installer, mirror, cache, or flag is not an alternative
     control.
  4. Treat a maintainer exception as a documented decision about the specific
     unmet gate only. It never waives provenance review, immutable pinning,
     reviewer-visible reproducibility, or runtime-behavior review, and it
     cannot be created by choosing another execution mechanism.
- Treat package runners as remote-code-execution paths until the exact command
  form is verified:
    - Confirm the package-manager version supports the needed cooldown or trust
    policy.
    - Confirm the exact configuration path, CLI flag, or environment variable
    used by that command form.
    - Confirm the policy applies before downloading or executing the package.
    - Use source-backed and preferably test-backed evidence before documenting
    `npx`, `npm exec`, `pnpm dlx`, or similar commands as acceptable.
- For Python scripts run with `uv`, enforce the seven-day package cutoff in
  the command or script metadata before dependency resolution:
    - Prefer a PEP 723 script containing `[tool.uv] exclude-newer = "P7D"` with
    its adjacent `.py.lock`, and execute it as
    `uv run --locked --script path/to/script.py`.
    - If a one-off check needs an extra package and no locked script is
    available, execute `uv run --exclude-newer=P7D --with <package> -- python
    path/to/script.py`. Do not use bare `python`, `pip install`, or
    `uv run --with <package>` without the cutoff.
- Do not treat hash pinning alone as sufficient trust when the pinned artifact
  can fetch or execute additional remote content at runtime, such as online
  installers, bootstrappers, package runners, remote API clients, or tools with
  plugin auto-download behavior.
- Prefer safer execution methods when available:
    - Already configured project tools or lockfile-backed dependencies.
    - Cooldown enforcement that is version-aware and verified for the exact
    command.
    - Pinned and provenance-reviewed container images.
    - Pinned, hash-verified artifacts with reviewed runtime behavior.
    - Disabled network access, sandboxing, and least-privilege execution.
    - Reviewer-visible commands and configuration.
- If release age, provenance, runtime behavior, or cooldown compliance cannot
  be verified, report a blocker instead of trying an unverified fetch-and-run
  command.

## Maintenance

- Re-check current tool behavior, package-manager documentation, platform
  policies, organization policies, and general security practice when making a
  security-sensitive decision.
- Update this skill when it falls behind safer current practice.
- Create or link follow-up issues when a safer current practice is identified
  but concrete ecosystem-specific implementation work belongs outside this
  general guidance.

## Output Checklist

- The security-sensitive surface was identified, or the change was classified
  as not security-sensitive with a reason.
- Stricter external requirements were followed when applicable.
- Supply-chain-sensitive artifacts satisfied cooldown, pinning, provenance, and
  runtime-behavior checks, or blockers/residual risk were recorded.
- Distributed artifacts were inspected as final containers, with unsafe member
  types and paths rejected and payload/provenance checked against an explicit
  contract, or the unverified scope was recorded.
- Every third-party resolution, download, build, load, or execution path passed
  the mechanism-neutral execution gate; tool names and delivery channels were
  treated as examples, not exemptions.
- Secrets, permissions, unsafe defaults, and untrusted input paths were checked
  when relevant.
- Example hostnames and URLs name the intentional real service or use an
  RFC-reserved example domain without introducing accidental live traffic.
- Suspected vulnerabilities were kept out of public channels when sensitive
  details were involved, with private maintainer or trusted-organization
  reporting used when appropriate.
- Any maintainer exception is documented in the final summary, issue comment,
  PR body, or review note.
