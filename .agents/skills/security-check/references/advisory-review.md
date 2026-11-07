# Dependency Advisory Review

Use this procedure for dependency adoption, update decisions, or assessment of
known vulnerabilities. Keep cooldown, execution, disclosure, and exception
requirements in `security-check`; an advisory finding does not change them.

## Identify the reviewed artifact

Record the ecosystem, registry, canonical publisher/source, current and proposed
version or commit, distribution/release, architecture, and dependency path.
Distinguish upstream source versions from distributor packages and actual
downloaded or bundled artifacts. Include direct and resolved transitive
dependencies, including development, build, and CI uses.

Use the final image/package inventory or a source-matched SBOM when available.
Record its generating revision and platforms. A source manifest, Docker tag,
binary filename, or old SBOM alone may not identify what is shipped. Mark
unresolved portions explicitly; do not execute an unreviewed scanner or candidate
merely to obtain a version or advisory report.

## Choose sources for that dependency

Start from canonical project, registry, or distributor documentation to locate
its security page, advisory feed, supported-version policy, or security tracker.
Corroborate the publisher/source relationship rather than trusting a search
result's rank, a familiar-looking domain, a badge, or popularity. Prefer the
authority responsible for the exact artifact, with relevant ecosystem databases
as additional evidence.

| Dependency | Sources and identity checks |
| --- | --- |
| Language package | Publisher advisories and registry-linked source; ecosystem advisory database, GitHub Advisory Database, or OSV where that ecosystem is covered. Match package name, registry, and version scheme. |
| Runtime, CLI, downloaded binary | Runtime/tool vendor's security notices and supported release branches. Identify the binary distributor separately when it rebuilds or bundles upstream software. |
| GitHub Action or reusable workflow | Canonical repository advisories and release/security notices, mapped to the exact pinned commit. Include bundled code and its execution runtime; a SHA pin may not be covered by a version-based alert. |
| Container base image | Image publisher's advisories and platform-specific contents, plus the underlying distribution's security tracker for OS packages. A new digest or tag is not proof that every included package is fixed. |
| apt, apk, rpm, or other OS package | The actual distribution/release security tracker and package changelog for the installed source/binary package version and configured repositories. Account for vendor backports. |
| Vendored or compiled bundle | Upstream advisories mapped to the vendored revision, build features, linked libraries, and downstream patches; use distributor evidence when it changes the affected status. |

Search engines, release aggregators, and issue reports can locate leads. Verify
claims against the originating advisory or a maintained database that identifies
its sources. Do not treat syndicated copies as independent corroboration.
Use general CVE databases to fill gaps or cross-check; they may not encode a
distributor's release-specific fix status. An unavailable authoritative source
or unsupported scanner ecosystem remains a coverage gap, not a clean result.

## Assess applicability and evidence quality

1. Match ecosystem, exact package/source identity, affected and fixed ranges,
   commit ancestry where relevant, platform, enabled features, and distribution
   release. Use that ecosystem's version comparison; lexical or generic SemVer
   comparison may misclassify distro revisions or other version schemes.
   For OSV data, consult the [affected-package and range semantics](https://ossf.github.io/osv-schema/#affected-fields)
   when interpreting package identities, Git ranges, and ecosystem ranges.
2. Check the advisory's publication, modification, and withdrawal state, aliases,
   original references, and fixed-version evidence. Record the check time.
   A release note saying "security fixes" without the affected identity/range
   does not establish whether this artifact or deployment is remediated.
3. Follow direct and transitive paths to the resolved artifact. Distinguish
   version-range applicability from demonstrated reachability, runtime exposure,
   or active exploitation; do not infer the latter from a severity score alone.
   Assess current and proposed versions, not only whether the candidate fixes
   one known advisory while introducing another affected dependency.
4. For a distro package with backported fixes, compare the installed distro
   revision against that distributor's fixed status. Do not label an older
   upstream version vulnerable solely because a generic scanner ignores the
   backport, or label it fixed without matching release/package evidence.
5. Reconcile conflicting vendor and database claims with their scope and dates.
   Record a source-backed conclusion or an unresolved finding; do not discard a
   report merely because another source is green. Missing metadata, a failed
   query, or an unscanned platform must not become "no vulnerabilities."

## Return findings for the decision

For each relevant finding, record the advisory link/ID, artifact and dependency
path, affected/fixed ranges, applicability evidence, exposure evidence and gaps,
and available remediation or mitigation. Distinguish confirmed applicability,
possible applicability, and an evidenced non-applicable result. State which
sources and graph/platform scope were checked, and which were unavailable.
"No findings" is limited to those checked sources and that scope.

If a fix fails a cooldown or another adoption gate, compare risk of waiting,
available eligible fixes, and temporary mitigations. Return an exception proposal
with the exact artifact, unmet gate, urgency evidence, and residual risk to the
authorized user or maintainer. Approval must be explicit and documented under
the main Skill and any stricter ecosystem policy. A security label, bot priority,
or high severity alone does not authorize early execution or adoption.

Keep sensitive, unpublished vulnerability details in the approved private
reporting path. Public update proposals should contain only the non-sensitive
findings needed for the decision.
