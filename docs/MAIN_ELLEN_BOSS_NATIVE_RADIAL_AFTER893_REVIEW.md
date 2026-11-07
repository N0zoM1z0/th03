# TH03 MAIN after893 — complete Ellen major BOSS native radial and intro loops

The entire original **nine-function `ba_ellen` Turbo C++ 4.02** physical
BOSS owner was recompiled: BOSS template, timed spread, both independent
radial Extra Attack bursts, pellet attack, update/hit scheduler, three
sprite strips, main renderer, and full **four by eight intro sprites**.
The original physical shared BOSS state/renderer tables and far-Pascal
callback ownership remain external, not replaced or reallocated.

## Native natural C++ control and measured byte-angle forms

The eight-shot fan, **both independently randomized radial Extra Attack
loops**, and the full **four-family × eight-sprite nested intro** now use
ordinary typed C++ `while`, preserving original signed index and
unsigned-byte angle operations, 256/count integer division, RNG ordering,
near/far sprite calls, original per-family sprite offset and post-call
angle/index mutation order. Both global **unsigned word-frame** `%2`
spread gates now use natural `if(!remainder)`/`if(remainder)`.

A fresh real-compiler finding refines older failed 'enum constants' advice:
Ellen's mutable `angle += enum_8`, `+= enum_0x20` and `+= enum_3`
spellings select different TC4 instructions, but **natural**
`angle = angle + NAMED_STEP` **is exactly original-native** for *all*
original relevant byte angle updates: +8 spread, +0x20 intro sprite,
+3 intro family and +0x10 pellet. Their real signed/byte wrap behavior
is unchanged. Source now names original 40×48 collision tiles, 24-pixel
hit margin and main/strip/intro sprite geometry without inventing BSS.

## Independent actual compiler-positive and negative trials

- `af893a`: eight-shot spread `for` to natural `while`, all original CODE
  and complete normal MAIN exact twice.
- `af893b`: both independent RNG-seeded radial `for` loops to `while`,
  same ordered far Extra Attack calls/divisions and exact original CODE.
- `af893c`: full 4×8 nested intro renderer converted to two natural
  `while` loops, original full physical BOSS exact twice.
- `af893d`: initially declared a named spread-step enum **after** its
  function and actual Turbo C++ rejected the undefined identifier;
  old source-order rules still apply. Moved the declaration earlier.
- `af893e`: applying enums directly through mutable byte `+=` to spread,
  intro sprite and family angles generated **1,660 CODE bytes** vs the
  original **1,675**. This was rejected, not padded.
- `af893f/g`: separately restoring spread then intro sprite `+=`
  demonstrated that the remaining enum-valued family `angle += enum_3`
  itself emits **1,671 vs 1,675** CODE. Restoring all literal compound
  updates in `af893h` exactly reproduced the original.
- `af893i/j/k/l`: tried **ordinary C++ byte assignments**, one live
  field and semantic named step at a time: family +3, sprite +0x20,
  spread +8 (two locations), pellet +0x10. All these assignments
  preserve **every original CODE byte** in genuine two-round TC4/TLINK.
- `af893m/n`: natural unsigned word `%2` truth checks and original
  named collision/sprite geometry remain exact.
- Final `af893o`: all actual current maintained C++ and explanatory
  codegen notes compiled in **two independent genuine original TC4 4.02
  and complete normal MAIN TLINK rounds**, original-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af893o --units ba_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af893o
```

Both actual original compiler/complete normal linker rounds match
**all 1,675 CODE bytes, 213 literal ordered OMF FIXUPP fields and nine
PUBLIC offsets**, original physical segment/source ABI, complete normal
MAIN EXE and normalized MAP, **124,642 Japanese loaded program bytes
and all 1,553 original MZ relocations**. Independent reviewed standard
DOS MZ serialization reproduces all 130,882 original Japanese MAIN.EXE
bytes; historical vendor header serialization remains unproved.
**98 other original game objects and CRT were reused**, without full
cold replay, patched original CODE/OBJ, padding or fabricated buffers.

Protected authentic two-round original TC4/TLINK/source-bound report:
`.analysis/work/exatt-layout-af893o/report.json`, SHA-256
`d1b3f9ef0e05495d5cb37365056a5837c56d2fe1e30b550d00810067c2361b4c`.
Already historically source-covered original CODE, not new distinct
target ownership or canonical Factory packed-file accepted bytes.
