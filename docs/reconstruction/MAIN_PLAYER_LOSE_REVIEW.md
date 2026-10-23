# MAIN player defeat animation candidate, 2026-10-22

`src/main/player/lose.cpp` and `lose.hpp` recover natural C++ candidates for
four provisional procedures at load C0D8..C370. The names are inferred.
The final original TC4J compile produces 662 CODE bytes versus 664 target
bytes and no DATA/BSS. This is an opt-in source candidate, not linked source
acceptance or exact credit. Existing MAIN 87 accepted extents are unchanged.

## Target and compiler evidence

Evidence is retained under `.analysis/codex-main-lose-20261022-v01/`.
`main-database-check.log` records the successful fresh MAIN attestation.
`intake.py` and `target-complete.json` bind all four raw target slices to the
pinned Japanese MAIN and independently compare them with the retained baseline.
The near returns pop respectively 2, 4, 2 and 0 parameter bytes. The render
procedure does not read its passed player slot. Pointer interpretation remains
inferred from its existing caller. Data names are views of existing storage,
not new allocations; composed-link address binding remains open.

Four isolated capsules PLSE254 through PLSE257 each execute one original
compiler invocation with 63 source files, four vendor headers and 104 include
edges. All four have successful native exits, terminal completion, clean
registry transitions and released writer locks. Each capsule retains its
original source, plan, manifest and result; later probes do not overwrite it.

| Procedure | Target bytes | PLSE257 bytes | Current result |
|---|---:|---:|---|
| player_lose_anim_update | 270 | 270 | Non-fixup raw bytes equal |
| player_lose_particle_put | 98 | 98 | Non-fixup raw bytes equal |
| player_lose_anim_render | 177 | 175 | Register allocation differs |
| round_defeat_banners_render | 119 | 119 | Non-fixup raw bytes equal |

PLSE254 used full-screen clip reset and a 24-screen-pixel sprite height;
canonical instructions instead set per-player clipping and a 24-VRAM-row
height (48 screen pixels). The corrected candidate uses the existing helper
with these actual units. Disabling speed optimization after the update body
naturally emits the target ENTER frames. Explicit register declarations for
banner coordinates and ordinary if/else height selection reproduce its target
register assignments and push operands. The negative-angle loop uses unsigned
byte assignment of `0 - (radius / 4)`, preserving the target byte subtraction.
These are compiler observations, not evidence of the original source spelling.

The render loop still uses SI where the target uses DI and preserves both
SI and DI. Its 175 versus 177 byte discrepancy remains unresolved. No dummy
variable, instruction padding, changed ABI, binary rewriting or altered
comparator is used to conceal this difference.

## Independent raw review and limits

`review-v04.py` verifies the original receipt, consumed input pins, installed
candidate equality, unchanged object and all 61 OMF fixup records. Across the
three equal-length bodies (487 bytes), it excludes 124 genuine fixup operand
bytes and one possible far-call relaxation opcode. All remaining **362 raw
bytes equal**. A changed non-fixup target byte is rejected independently for
each of the three bodies. No renderer byte-equality result is inferred from
instruction shape, register renaming or length normalization.

The 5,558-byte object has SHA-256
`1c4fda1bb486ea4c80acd3ed4504cc550fc4273132c7f0983d71a7fd8844c328`.
The installed-source report is `installed-review-v01.json`. Replay with a new
output path:

```sh
.venv/bin/python -B .analysis/codex-main-lose-20261022-v01/review-v04.py \
  --installed --output .analysis/NEW_LOSE_REVIEW.json
```

All native probes run serially on CPU 19 with nice 10. Resource receipts are
`native-v01-resources.txt` through `native-v04-resources.txt`. No Factory MCP
or visible desktop is used. No cleanup was performed on these proof inputs.

Next resolve the render producer's register allocation, prove existing storage
bindings and compose a real link with the state/shot producers. Far-call
relaxation, relocation order, behavior and cold reproducibility remain separate
required gates. Whole-game authored denominator and the 98% objective remain
unproven. Two evidence rows record target and compiler observations; no unit,
function or exact counter is promoted.

The evidence-ledger append requires rebinding existing OP/MAINL publications.
The standard offline replays retain the same OP33 and MAINL145 scope; old
publications are archived in `op33-refresh-preimage/` and
`mainl-refresh-preimage/`. Independent install reviews permit only
`config/evidence.csv` input-binding drift and verify unchanged owner sizes,
hashes and scope. Refreshed Oracle timestamps/proof digests are new review
metadata, not new native builds or authored-byte credit. The scripts and
`*-refresh-install.json` reports are retained in this checkpoint's evidence tree.

## Next bounded compiler hypothesis

Reference-only corroboration: `_reference/ReC98/codegen.hpp` lines23–28 state
that TC4 emits both SI/DI save/restore pairs whenever either pseudoregister is
used. An explicit `_DI` loop counter is therefore a concrete next compiler
hypothesis for the target renderer, whose loop uses DI while SI is only saved.
This is not yet a TH03 compiler observation or a claim of original source.
Test the actual loop with the native compiler; do not synthesize the save pair
with padding, a dead variable or emitted target bytes.

## Checkpoint verification

Full `scripts/ci.py` passes: 2,329 tests in 372.640 seconds, two existing skips,
all four database attestations and Oracle/toolchain checks. Evidence:
`ci-v01.log`, `ci-v01.exit`, `ci-v01-resources.txt`. Total wall time8:56.73;
peak RSS665,436 KiB, one CPU/nice10, Java768 MiB heap cap, zero swaps.
The four serial native probes peak at108,592 KiB. Whitespace validation passes.

The bounded cleanup dry run (`cleanup-dry.log`, `cleanup-dry-resources.txt`)
exited1 with MemoryError while reading a historical JSON under the768 MiB
virtual-memory ceiling. It never ran with `--apply` and deleted nothing.
Disk had approximately785 GiB free; no higher-memory retry was started.

## Post-checkpoint private register controls (handoff only)

PLSE258..261 (native-v05..v08) each completed one guarded original compilation.
The installed source remains PLSE257. These private candidates were not source/exact promotions. Their unused run
outputs and carriers were discarded during the owner-requested handoff cleanup;
the observations below are historical conclusions, not retained replay proofs.

Explicit `_DI` plus a signed loop comparison matches the loop register, but
produces only PUSH/POP DI: the renderer remains175 versus177 bytes. Disabling
jump optimization (-O-) or register-reload suppression (-Z-) leaves all662
CODE bytes identical to the plain `_DI` probe. Replacing each counter
initialization with symbolic ASM changes only three equivalent XOR encodings
(33FF to31FF); it still does not save SI. Thus the earlier reference comment
about always saving both registers is not confirmed for this pinned toolchain.
No dummy use of SI, emitted target bytes or manual padding was added.

Installed PLSE257 verification remains `review-v04.py --installed` with a fresh
output path. Its complete native-v04 inputs, outputs and carrier are retained.

## Resumed register-allocation control — 2026-10-23

PLSE262 / `.analysis/main-resume-20261023/native-v09` repeats the explicit-DI
candidate with `#pragma option -r-` around the renderer. One original native
compile exits zero and releases its writer lock. It still emits175 renderer /
662 CODE bytes with only DI saved. Disabling automatic register allocation does
not explain the extra SI save pair. Installed PLSE257 source remains unchanged.
