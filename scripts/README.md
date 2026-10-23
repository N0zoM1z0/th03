# Current entry points

- `preflight.py`: environment, targets and tracking.
- `ci.py`: tests and available local tool/database checks.
- `ghidra.py ARTIFACT check`: headless target/database identity.
- `attest_toolchain.py`: pinned native tools.
- `verify_targets.py`: canonical target hashes.
- `status.py`, `progress.py`: ledger-derived scoped progress.

Historical replay helpers may refer to deleted private runs. Those outputs were
intentionally discarded; use fresh source builds for new exact verification.
See `docs/RE_HANDOFF.md` for the current work tree and next question.
