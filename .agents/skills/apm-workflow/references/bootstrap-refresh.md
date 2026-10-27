# Propose an APM Bootstrap Refresh

## 2.1 Propose a bootstrap-version refresh

Do not change the bootstrap manifest automatically. Use this proposal flow:

1. Record the current and candidate tags, release URLs, publication dates,
   platform assets, SHA-256 values, and the candidate cooldown date. Start with
   the newest candidate that has completed the cooldown, not merely the newest
   published or locally installed version. A maintainer may instead select one
   exact newer release and approve a cooldown exception for a concrete defect
   or operational blocker.
2. Treat cooldown as a minimum gate, not adoption approval. Review provenance,
   release notes, installer and artifact integrity, and compatibility from the
   current official sources. Require explicit maintainer approval.
3. Run
   `uv run --no-project --no-config --locked --script <apm-workflow-skill>/scripts/propose_bootstrap_update.py`
   to isolate the locked helper from the consumer repository's uv configuration
   and collect an eligible candidate without changing files. Attach its JSON
   output to the proposal.
4. After approval, obtain the candidate through the [temporary artifact
   flow](cli-acquisition.md) and run representative lock, frozen-install, audit, and
   deployed-output checks without changing the active installation or PATH.
   A reproducible resolver, lock migration, install, audit, or output failure
   rejects the candidate even after cooldown; keep the current bootstrap and
   record the evidence instead of trying a newer unreviewed release.
5. If the candidate passes, run the same isolated command with
   `--write --confirm-version <candidate>`. It updates only
   `references/apm-bootstrap.json` and refuses an unconfirmed or mismatched
   version. Review the manifest diff before committing.

For a maintainer-approved cooldown exception, pass the exact
`--candidate-version`, `--cooldown-exception-reason`, and deterministic
`--now` approval timestamp first without `--write`, then repeat with
`--write --confirm-version <candidate>`. The helper records
`cooldown_exception` in the manifest and refuses an exception without an exact
candidate and reason. The exception waives only the time gate for that
bootstrap CLI release; provenance, checksums, artifact inspection,
compatibility tests, and dependency review remain required.

Do not use `apm self-update` to perform this refresh.
