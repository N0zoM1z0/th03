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

## Second recoverable archive

After the complete conservative scan finished successfully, ten individually reviewed unused JSON inventories were archived in `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v02.tar.xz`. The original 1,018,714,562 bytes compress to 28,618,324 bytes; archive SHA-256 is 1f601ad65a6fe88219873ee7c50ef64d2cbf1b46d3833e943efb083037d89112. Fresh extraction checked every member's bytes, type, mode and nanosecond mtime. Only these exact original files are removed; parents, siblings and referenced receipt trees remain.

Preserve `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v02-members.json`, `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v02-verification.json`, and `.analysis/cleanup-20261022-v01/archive-apply-v02.json`. Apply the same safe restore procedure in the retained RESTORE.md using this bundle's archive and manifest. The complete scan log is `.analysis/cleanup-20261022-v01/updated-conservative-v02-plan.log`; listing a candidate is not permission for blanket removal.

## Third recoverable archive

Nineteen exact unused JSON files, each an explicit candidate or a descendant of a complete candidate tree, are retained losslessly in `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v03.tar.xz`. Their 1,514,134,381 original bytes compress to 39,083,860 bytes. SHA-256: 28a3ef35587b780b4061fea6d735d006a72dc1b9e056d2d40bbabe75f67d5b88. All nineteen files were extracted independently and verified for exact bytes, mode and nanosecond mtime before removal. Every parent and unselected sibling remains.

Preserve `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v03-members.json`, `.analysis/cleanup-archives-20261022-v01/large-unused-inventories-v03-verification.json`, and `.analysis/cleanup-20261022-v01/archive-apply-v03.json`. Use this bundle's archive and manifest with the existing safe restore procedure before reusing those inactive historical experiments.

## Fourth recoverable archive

The next 1,603 unused JSON/config-snapshot files are retained in `.analysis/cleanup-archives-20261022-v01/unused-json-and-config-snapshots-v04.tar.xz`: 1,511,649,477 original bytes compress to 39,800,236 bytes. SHA-256: 75f874a2f25d2e61fb25979bb52b66c82702f6b7702769a3b2b6bb8bf63081af. Every member was extracted and verified for exact bytes, mode and nanosecond mtime. Three sealed OP checkpoint proof payloads were explicitly excluded and kept in place. Only exact selected regular files are removed; no directory or unselected sibling is removed.

Preserve `.analysis/cleanup-archives-20261022-v01/unused-json-and-config-snapshots-v04-members.json`, `.analysis/cleanup-archives-20261022-v01/unused-json-and-config-snapshots-v04-verification.json`, and `.analysis/cleanup-20261022-v01/archive-apply-v04.json`. The member manifest records the exclusions and exact recovery metadata. Restore using this bundle's archive and manifest with the same safe procedure before reusing archived experiments or snapshots.
