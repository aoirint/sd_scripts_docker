---
name: security-check
description: >-
  Check repository work for practical security risks, including secrets,
  permissions, unsafe defaults, ad hoc executable tools, dependencies,
  downloaded artifacts, CI actions, containers, vendored files, and
  supply-chain-sensitive changes.
---

# Security Check

## When to Use

- Use this skill when repository work touches security-sensitive behavior,
  external executable artifacts, dependency provenance, CI permissions,
  containers, secrets, credentials, network access, generated artifacts,
  vendored files, unsafe defaults, or user-provided data.
- Use this skill when another workflow asks for a security review, a
  supply-chain baseline check, or a decision about whether a tool can be run or
  adopted safely.
- Use this skill with `code-quality-check` for implementation changes and with
  `skill-quality-check` for Agent Skill changes that describe security behavior.

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

1. Identify the security-sensitive surface:
   - Secrets, credentials, tokens, private data, or logs.
   - Permission boundaries, CI permissions, publishing credentials, or
     filesystem/network access.
   - User-provided input, deserialization, file paths, shell commands, or
     remote APIs.
   - Dependencies, package-runner invocations, downloaded CLI tools, CI
     actions, containers, vendored artifacts, generated code, or copied files.
2. Check the strongest applicable rule first:
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
5. For supply-chain-sensitive work, apply the supply-chain baseline below.
6. If the safe path cannot be verified, do not normalize the risky action:
   - Report a blocker when release age, provenance, runtime behavior, or
     cooldown compliance cannot be verified.
   - Record residual risk when a partially controlled path remains.
   - Require a documented maintainer exception before proceeding with a weaker
     path.
7. Before recommending an exact safer command, inspect repository scripts,
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
- Treat package runners as remote-code-execution paths until the exact command
  form is verified:
  - Confirm the package-manager version supports the needed cooldown or trust
    policy.
  - Confirm the exact configuration path, CLI flag, or environment variable
    used by that command form.
  - Confirm the policy applies before downloading or executing the package.
  - Use source-backed and preferably test-backed evidence before documenting
    `npx`, `npm exec`, `pnpm dlx`, or similar commands as acceptable.
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
- Secrets, permissions, unsafe defaults, and untrusted input paths were checked
  when relevant.
- Suspected vulnerabilities were kept out of public channels when sensitive
  details were involved, with private maintainer or trusted-organization
  reporting used when appropriate.
- Any maintainer exception is documented in the final summary, issue comment,
  PR body, or review note.
