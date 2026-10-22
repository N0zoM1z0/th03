# Exact retained dependency recovery, 2026-10-22

## Recovered support source

The missing `.analysis/gpt-dots-player-cpu-acceptance-install-v01/support.py` was restored at 09:06:57 UTC with exactly 5,324 bytes and SHA-256 fd19475aea02ec5aa6ae8e4c48f6ab88170f1d73e0f6ee7dbfa7231d50dc8c68, matching the pre-existing independent proof bindings.

The surviving `.analysis/gpt-dots-player-cpu-default-install-v01/support.py` has 5,321 bytes and SHA-256 590321a4b652b546bf77d56a57c127f0af018e329d00ee152fb66646bf03fe15. Replacing its single cache-prefix literal cpu-default-install-no-cache-20261020-v01 with cpu-acceptance-install-no-cache-20261020-v01 yields the original pinned bytes. This variant was inferred from installer identity; the original emitter was not recovered. Exact complete-hash equality, not an assumed equivalent implementation, establishes recovery. No original mtime is claimed, and no historical pin or receipt was rewritten.

The exact non-executed recovery copy is now versioned at config/recovery/native_support_20261020.py.txt. If the private helper is absent again, first verify this copy's size and SHA-256, create a regular non-symlink destination parent, and copy these exact bytes to the absent path with mode0600. Do not overwrite an existing mismatching helper. Do not import this backup from its storage location; it is preserved for byte recovery only.

The separate recovery attestation is `.analysis/dependency-recovery-20261022-v01/support-recovery.json`. The current installed330-file source composition check passes; its log is `.analysis/dependency-recovery-20261022-v01/op-fullcold-replay.log` (the name predates clarification that --check-current-source is source-only). Full dated cold replay also passes:62 native phases,30 raw OMF pairs, two63,866-byte decoded target-equal executables. Separate packing replay passes all2,856 pins and five original phases, including36,041-byte canonical equality and restoration. These were offline replays, not new native executions.

Preserve `.analysis/dependency-recovery-20261022-v01/op-fullcold-historical.log`, `.analysis/dependency-recovery-20261022-v01/op-fullcold-historical.exit`, `.analysis/dependency-recovery-20261022-v01/op-packing-historical.log`, and `.analysis/dependency-recovery-20261022-v01/op-packing-historical.exit`. Source/exact acceptance and authored-code credit remain unchanged. The separate effects.obj dependency remains missing; any new reproduction must have a new namespace and receipt, never substitute invented historical evidence.
