# Recoverable analysis cleanup, 2026-10-22

The first reviewed bundle removes only redundant temporary Git snapshots and regenerable Python bytecode: 15 paths, 12,036,589 logical bytes / 13,414,400 allocated path bytes. Every snapshot byte was checked against a reachable Git blob; each bytecode file has a tracked source counterpart.

Seven large unreferenced historical control inventories are stored losslessly in `.analysis/cleanup-archives-20261022-v01/background-control-pins-v01.tar.xz`. Their 341,775,122 original bytes compress to 7,273,156 bytes. Archive SHA-256: c7194cc079a0141ae9737dce5fa8a88aea988905c4d8eef8096e169d73463015. All seven members were extracted to an isolated verification directory and checked for exact bytes, modes and nanosecond modification times before original removal. Restore the inventories before reusing those inactive historical probes; no unique history is discarded.

Preserve these concrete recovery and audit files:

- `.analysis/cleanup-archives-20261022-v01/members-manifest.json`
- `.analysis/cleanup-archives-20261022-v01/verification.json`
- `.analysis/cleanup-archives-20261022-v01/RESTORE.md`
- `.analysis/cleanup-20261022-v01/recoverability-reviewed-manifest.json`
- `.analysis/cleanup-20261022-v01/applied-recoverable-bundle-v01.json`
- `.analysis/cleanup-20261022-v01/archive-apply-v01.json`

The full canonical dry run timed out after emitting 131 candidates. Only individually reviewed candidates are covered here; unvisited paths are not approved. Locks, active proposals, toolchains, runtime images, targets, Ghidra state, referenced full proof trees and unique conclusions remain protected. Two historical inputs were already missing before any cleanup in this run; that independent replay blocker remains recorded in RE_HANDOFF.md. No claim of a passing full suite or additional reconstruction credit is made.
