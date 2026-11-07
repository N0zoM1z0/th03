# TH03 MAIN after918 — full Kana Extra Attack entity lifecycle and sprite traversal

This is the full five-function original physical `ex_kana` Turbo C++
4.02 Extra Attack owner: ordinary and special first-free-slot
allocators, 32×32 animated sprite, complete eight-entity flight,
accelerated shot/collision/update and all-eight render dispatch.
It owns no replacement DATA/BSS; all shared original 32-byte entity
records and their near/far helper calls remain in external physical
original game objects.

The entire eight-entity **movement/accelerated-bullet/clip/arrival
controller** now uses natural `while` with two independent `continue`
paths; on both skip branches the original signed index and near entity
pointer advance explicitly before continuing. The special
first-free-slot allocator can also become a natural `while`, unlike the
ordinary flight allocator, which must retain `for/continue/return`.
The full eight-entity render dispatcher also uses native-exact `while`.
Original 16-frame bullet cadence accepts `if(!remainder)`; the
sprite-animation byte frame `/4` and `%4` steps remain separate.
Original random X/Y ranges, target threshold and bias, initial speed,
32×32 sprite geometry and angle bias/half turn now use named C++
constants without adding program state or altering RNG draw order.

Real original Turbo C++ 4.02 compiler trials:

- `af918a`: full eight-entity movement and two-continue update as
  natural `while`, whole source/complete normal MAIN exact twice.
- `af918b`: converted both allocator loops to `while`; original
  `ex_kana` became **665** vs original **663 CODE bytes**.
- `af918c`: restored only the special allocator to `for`, leaving
  the ordinary allocator `while`: still **665**, first difference
  CODE segment 4 offset 33. Thus ordinary `for/continue/return`
  specifically must remain native.
- `af918d`: restored the ordinary `for`, changed the *special*
  allocator to `while`: original CODE exact in two full native rounds.
- `af918e`: full sprite dispatcher as natural `while`, exact twice.
- `af918f`: original byte `%16==0` cadence as `if(!remainder)`, exact.
- `af918g`: named original sprite/target RNG geometry, native exact.
- `af918h`: mutable byte frame postfix to prefix generated **668**
  instead of original **663 CODE bytes**; reverted.
- `af918i`: byte frame sprite cel `/4` to `>>2` kept initialized
  663-byte size but changed CODE at segment 4 offset 298; reverted.
- Final `af918j`: full current source with native codegen comments
  recompiled in two original TC4 4.02/full normal MAIN TLINK rounds,
  every original byte exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af918j --units ex_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af918j
```

Both independent original compiler/linker rounds reproduce **all 663
original CODE bytes, 44 literal ordered native OMF FIXUPP fields, five
PUBLIC offsets**, segment/source/16-bit ABI, complete normal MAIN EXE
and normalized MAP, **124,642 Japanese loaded program bytes and all
1,553 original MZ relocations**. Independently checked standard DOS
MZ serialization reproduces all **130,882 pinned Japanese MAIN.EXE
bytes**, not historical vendor header-writing identity. **98 other
game project objects and CRT reused**, no full cold replay, original
target/OBJ byte patches, synthetic CODE buffers or NOP padding.

Protected genuine source-bound original compiler/TLINK proof:
`.analysis/work/exatt-layout-af918j/report.json`, SHA-256
`69ff5d22ca6b1dd5001cc893566a359667de3e9da09181b546a5ffe3dd8c1e87`.
Previously source-owned game CODE, not newly distinct original CODE,
vendor packet-identical OMF or canonical Factory packed acceptance.
