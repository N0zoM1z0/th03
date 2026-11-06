# Shared abort: literal relocation order after539

The shared runtime's existing `abort` member now has both original FAR fixups
in their literal order. This refines 20 existing CODE bytes; it adds no library
member, CODE extent, authored function or whole-game acceptance credit.

The live owner is `src/shared/crt/abort.asm`; frozen
`src/mainl/crt/abort.asm` remains an unchanged ancestor input. The bounded recipe
is `config/th03_runtime_after539.json`. Producer and independent read-only
reviewer are `scripts/build_th03_runtime_after539_work.py` and
`scripts/review_th03_runtime_after539_work.py`.

## Original and source

The comparison independently opens installed Japanese TC4 `CL.LIB`, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`,
and selects actual slot 2, `abort`. It does not use the historical reconstructed
28-source carrier as an original. Product targets remain the pinned Japanese
`candidate-local-attested` targets; independent pristine-dump provenance is unknown.

The far entry saves SI/DI, calls `raise(22)` (SIGABRT), removes the argument and
calls the unconditional `__abort` fallback. If the fallback returns, SI/DI and
the far return frame are restored. The original omits a BP frame.

Ordinary fallback instructions occupy offsets 12–19; entry instructions occupy
0–11. The source emits the fallback span first with bounded `ORG 12` / `ORG 0`,
so native TASM emits fixup +13 before +7. The spans cover every initialized byte
exactly once. No padding, target instruction arrays, object patch or relocation
sorting supplies equality. The source does not claim to recover the original
compiler's textual statement order.

Both original and emitted literal fields are:

| CODE site | Width / location | Frame | Target |
| --- | --- | --- | --- |
| +13 | 4 / FAR pointer | TARGET, method 5 | EXTDEF 2, `__abort` |
| +7 | 4 / FAR pointer | TARGET, method 5 | EXTDEF 1, `_raise` |

Both fields are segment-relative, target method 2, addend zero. Full lists are
compared directly in emitted order. The original import order is preserved.

The review also checks all initialized bytes; CODE20/DATA0/BSS0 extents;
segment attributes 28h/48h/48h; raw PUBLIC payload/order (`_abort` at zero);
GROUP DATA/BSS order; ALIAS and MODEND records. There are no uninitialized CODE
holes or extra public helpers. OMF data-record packing differs, so complete
original OMF-program identity is explicitly **false**.

## Rejected C candidates

The installed native Turbo C++ 4.02 writer naturally emits the two FAR fixups
in reverse order. Plain C, with either register-allocation setting, emits only
16 CODE bytes and omits the required SI/DI saves. Adding explicit saves in
inline assembly also triggers compiler saves, producing 24 bytes. `__saveregs`
produces a different 40-byte all-register ABI. An inline-assembly call sequence
still produces the shorter 16-byte body; `-Od` is rejected by this compiler.
These are rejected candidates, not exact C recovery. No dummy register use was
introduced to force the desired prologue.

All af539a–h sources, actual commands, native objects where produced and logs
remain. `.analysis/work/probe/abort539/manifest.json` pins 41 retained files,
including copied probe recipes. The assembly candidate's complete scope is
retained in `.analysis/work/af539h-abort-scope.json`.

## Native product bridge

The parent is after538, SHA-256
`7647b0fdf6bc43c769d526422cad48907d1e58c0d31260766b0a7936f61cbb07`.
After539 extracts its actual source library with native TLIB, assembles only
abort, rebuilds all 893 slots in the same order and links both affected products.
The other 892 member programs remain identical. Source C0 and unchanged current
game objects are reused; the original OP cold pair and source graph are validated.

Each of two native rounds retains six complete raw outputs: abort OBJ, rebuilt
LIB, MAINL EXE/MAP and OP EXE/MAP. All six repeat byte-for-byte. All nine successful
writer phases and logs remain; displays are empty, writers serialized, one CPU
at nice10. Native tool paths and SHA-256 identities are pinned in the config.

| Output | Native result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality, 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality, 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after538 MAP equality |
| OP MAP | 68,078 bytes; complete after538 and historical cold MAP equality |

MAINL MAP SHA-256 is
`cca9d579087ba6bdf7eca0bdee9e2df03c7a50090377cc8f56e4db2e78f5b515`;
OP MAP SHA-256 is
`2666a302659c05b2c7d949db089cf01383f2abc19ca3cc996be052138bcbb00a`.
All selected initialized/uninitialized material storage, segment attributes and
native MAP ownership are rechecked against real original CL.LIB. Both actual
after537 packed OP proofs are reused through after538, with identical decoded
inputs and pinned tools; there is no new DIET run.

The OP-selected literal audit now has 58 identical streams and 18 order-only
gaps. All 76 retain equal imports and complete per-site field attributes. These
are diagnostic classifications, not source/function progress. C0's 58-field
order gap and formal MAINL 0/250 acceptance remain unchanged.

Root: `.analysis/work/runtime-after539-build.json`, SHA-256
`60a004666a3c62043147feb86d97f2f1231b406070bc150fa794ed9d4d47b095`.
All twelve raw outputs and nine logs use `runtime-after539-*`; the independent
review transcript is `runtime-after539-independent-review.txt`. Consumed source,
recipe, config, extracted objects and linker/library responses remain in
`TH03ML/probe/af539i` and `TH03OP/probe/af539i`. No native cleanup, full CI, cold
replay, game-object recompilation or ancestor runtime-model replay occurred.
