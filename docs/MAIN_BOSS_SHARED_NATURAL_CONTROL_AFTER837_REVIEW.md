# TH03 MAIN after837: shared BOSS movement and attack-selection C++ control

This changes the **entire maintained `src/main/boss/shared.cpp`**, compiled
through its **two actual separate physical original objects**: `ba_sring`
(24-sprite explosion ring) and `ba_srest` (movement, fall, template
activation, hit/score, target movement and random-pattern scheduling).

The BOSS sine movement now expresses left/right turns with natural
`if / else if` rather than an early return followed by another `if`.
The original random attack-mode rejection has likewise been recovered
as a natural infinite `for(;;)` with an explicit `break` when the newly
drawn pattern is outside the exclusion interval. Original RNG consumption,
16-bit/byte comparison, source register allocation and branch layout
remain **byte-exact under genuine original Turbo C++ 4.02**. The explosion
ring's two original counts, sprite offset, finish radius, score reward
and the shared target's downward offset now have named semantic C++
constants, preserving the original 16-bit arithmetic order.

Real native experiments:

- `af837a`: movement `if / else if` compiled both physical originals
  and the full normal MAIN with exact target bytes in two rounds.
- `af837b`: additionally changed random mode rejection to `for(;;)`;
  both physical originals remained fully exact in two rounds.
- `af837c`: attempted `length = length * 8` in the ring in place of
  `length *= 8`. It **failed** complete `ba_sring` CODE equality. The
  original expression was restored (this is independent of earlier
  failed shift-based attempts).
- `af837d`: independently challenged the original `SI`/`DI`/`ES`/
  `REP MOVSW` 32-byte BOSS template copy with natural `boss_state =
  boss_character_template[pid_current]`. Genuine TC4 emitted **597**
  `ba_srest` CODE bytes rather than the original **601**; this was
  reverted. It is an exact 16-bit compiler/ABI requirement, not a
  justification to insert padding or patch an object.
- `af837e`: final current source, restored original copy/multiply, and
  both recovered natural control-flow constructs. Two independent
  genuine original TC4/TLINK rounds passed.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af837e --units ba_sring,ba_srest
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af837e
```

The two objects together reproduce **all 949 original CODE bytes**
(`ba_sring` 348 + `ba_srest` 601), **106 literal ordered native OMF
FIXUPP fields** (22 + 84), **8 PUBLICs**, original segment/data/ABI,
full normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes**
and **1,553 literal ordered MZ relocations** in *both* native rounds.
The independent MZ serializer also matches all 130,882 bytes of the
pinned Japanese MAIN.EXE. Only these two original game objects were
recompiled; the remaining **97 game objects and CRT** were reused,
with **no full cold replay**. Protected proof:
`.analysis/work/exatt-layout-af837e/report.json`, SHA-256
`8c243f461160faedb3bd0265e4d1640a8026c00dcd2f5f5172f1a427c232243d`.

These were already historically source-owned objects, so the new
source-bound proof is **not** newly distinct CODE ownership, raw vendor
OMF packet identity or canonical packed-file Factory acceptance.
