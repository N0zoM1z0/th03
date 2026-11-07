# TH03 MAIN after892 — complete Reimu major BOSS native orbit and intro control

The complete original **nine-function physical `ba_reimu`** Turbo C++
4.02 source owns the Reimu BOSS template, cloud and mirrored spreads,
three-phase orbit-burst projectile/Extra Attack controller, original
full attack/collision scheduler and both sprite renderers. This experiment
compiles the entire original BOSS, not convenient isolated leaves.

## Native natural C++ recovery

All **five complete orbit/renderer loops** now use ordinary typed
`while`: all three phases of the large signed-index orbit attack
(expansion, held-radius bullets, and Extra Attack release), the main
orbital sprite renderer and the eight-sprite intro renderer. Each
preserves original `i * 256` before signed quotient, byte-angle
truncation, two-step 16-bit ring radius scale, original polar call
sequence and post-render index/byte-angle advancement.

The three real **unsigned 16-bit** attack clocks can naturally use
`if(!(boss_frame % period))` or the corresponding nonzero truth check.
The intro byte angle +=0x20 has a named physical constant. Both mutable
orbit angle updates are now natural C++
`reimu_orbit_angle = reimu_orbit_angle + REIMU_ORBIT_ANGLE_STEP` and
compile *identically* to the original compound byte update. Original
56×56 collision tiles, signed 32-pixel hit margin, 96×96 main sprite,
48×48 orbit sprites and actual two-player screen offsets are now named
source-level geometry with no additional DATA or calls.

## Genuine original compiler trials and negative controls

- `af892a`: **all three original BOSS orbit attack loops** converted to
  natural `while`, exact original CODE and complete normal MAIN twice.
- `af892b`: complete main renderer's sprite orbit loop converted to
  `while`, still full original object/normal MAIN exact twice.
- `af892c`: eight-sprite intro renderer uses a native-exact signed-index
  `while` and preserves mutable byte-angle updates after each sprite.
- `af892d`: cloud/acceleration/mirrored attack clocks use natural
  unsigned word remainder truth checks, original native object exact.
- `af892e`: the intro's live byte angle +=0x20 also accepts a named
  compile-time C++ constant without changing the original instructions.
- `af892f`: both orbit-phase mutable byte `angle += named_8` operations
  may become ordinary `angle = angle + named_8` C++ assignments and
  still reproduce every original machine-code byte.
- `af892g`: replacing just the first `anim &3 ==1` checks in both
  renderers with signed byte `anim %4 ==1` **failed**. Original TC4
  emitted **2,026** CODE bytes vs **2,020** target, first difference
  CODE segment 4 offset 1567. The original masks remain.
- `af892h`: named original collision/sprite geometry while restoring
  byte animation masks, all original CODE/FIXUPPs exact twice.
- Final `af892i`: current entire source plus original codegen comments
  recompiled in **two independent real TC4 4.02 and full normal MAIN
  TLINK rounds**, all original scope exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af892i --units ba_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af892i
```

Both original compiler/complete normal MAIN linker rounds reproduce
**all 2,020 original CODE bytes, 270 literal ordered native OMF FIXUPP
fields and nine PUBLIC offsets**, original source/segment/16-bit ABI,
complete normal MAIN EXE and normalized MAP, all **124,642 Japanese
loaded program bytes and 1,553 ordered original MZ relocations**.
Independently checked standard DOS MZ serialization reproduces all
**130,882 original Japanese MAIN.EXE bytes**. The other **98 unchanged
original game project objects and CRT were reused**, no all-object cold
replay, patched target/OBJ, synthetic CODE buffer or NOP padding.

Protected real source-bound compiler/TLINK/OBJ/EXE/MAP proof:
`.analysis/work/exatt-layout-af892i/report.json` SHA-256
`ef0879eaf074041c87c11512400925893ac6ce8bea385f2e174faa067929b22e`.
The physical BOSS was already historically source-covered; this advances
native C++ maintainability, **not distinct original CODE ownership,
raw original vendor OMF identity or canonical packed Factory credit**.
