# OP: two complete source-cold builds, exact decoded output

This additive checkpoint preserves every older cold proof. Its four source dependencies are the separately reviewed PFOPEN, global-order, alignment and uniform nopcall proposals. It adds no source ownership credit and publishes no acceptance.

## Actual result

OPCO211 and OPCO212 each compiled all 30 project objects from the same 330 source-only inputs, then linked. All 14 groups completed cleanly: 60 fresh project objects and 62 actual native phases. No project object was copied or seeded. External startup/CRT libraries remain toolchain context.

Both decoded executables are exactly 63,866 bytes, SHA-256 `efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0`. The complete 4,096-byte header, 59,770 program bytes and 607 literal relocation tuples match the target. Whole MAP files and all 30 raw OMF pairs are identical. Objects total 80,839 bytes per round. No normalization is used.

The prior 44 authored scopes (12,940 bytes) and separate PFOPEN281 diagnostic remain preserved. This does not turn vendor/context code or CRT into newly authored ownership. Runtime and formal source/exact acceptance remain separate.

## Historical replay versus current source compatibility

The root's dated live terminal comparison checked the source tree, HEAD, 90 tool identities and timestamps, lock/poison state and final registry. Its immutable attestation is bound by hash. Historical replay never repeats that live guard and does not require today's HEAD, registry, installed tools or tool timestamps to remain historical.

Replay verifies 2,350 retained artifact pins, all 14 frozen/actual manifest identities, exact commands/environments, 90+15 limits, owned cleanup, source-content and recorded mode/time closure, growing object inventories, and all 62 dated raw registry transitions under the unchanged policy. Tool and tracked-source identities are checked as dated descriptors supported by the terminal attestation. Historical artifact bytes must still match. Their current storage modes/timestamps do not replace recorded native metadata.

Both complete terminal reports are reproduced exactly. No compiler, linker, executable, emulator, Git state query, live registry access or lock acquisition occurs. Historical evidence and pinned decoder/helper implementations must remain available; missing or altered artifacts fail closed.

Run from the repository root with a 180-second envelope:

`python3 -B scripts/replay_th03_op_fullcold_exact.py`

Separately check current maintained sources:

`python3 -B scripts/replay_th03_op_fullcold_exact.py --check-current-source`

Before installation, pass `--files .analysis/op-fullcold-exact-checkpoint-proposal-v01/files`. For the explicit uninstalled four-proposal source composition, also pass `--check-current-source --virtual-proposals`. This reproduces the historical 330 source hashes without staging binaries or claiming installation.

## Boundaries

All original selection, anchor, root-split, delayed-registry-flush and sparse-LEDATA failures remain preserved alongside separate corrections. The ordering proof's historical one-byte-negative result is unchanged. No false native completion is rewritten.

OPDP211 packing equality is separate contextual evidence, not part of these 62 phases or an assertion that cold outputs themselves were packed. This checkpoint therefore reports packed equality false. It does not install, commit, push, raise ownership counters or publish acceptance.
