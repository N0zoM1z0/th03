# TH03 MAIN Kotohime Extra Attack: complete eight-function native source after750

The maintained complete `src/main/player/exatt_kotohime.cpp` is one
original 16-bit `ex_koto` physical Turbo C++ translation unit. Its
**eight functions** jointly own the two projectile creators, full 4- and
10-bullet fan emitters, main state/update controller, effect generator,
projectile-specific sprite renderer and active-entity render dispatcher.
The original physical owner has **1,054 initialized CODE bytes, 100
ordered literal OMF FIXUPP fields and 8 PUBLIC offsets**, with original
segment/DATA/BSS declarations. This is not an isolated leaf comparison.

## Natural C++ improvements tested against real original CODE

The byte entity state machine is now named for **free (0), active (1) and
flying (2)** states. Original normal eight-slot and special two-slot
allocation, projectile RNG order, 32-byte packed entity ownership and
original four separate event pulses (4, 8, 12, 16) remain unchanged.
All signed local `i` loop counters in ordinary creation, both projectile
emitters and update/render paths now naturally use prefix `++i`; the
original near pointers, byte-angle/event mutations, and burst speed/angle
increment order deliberately stay postfix. State inactivity, special
projectile modes and two fan-direction flags use native-exact natural
C++ boolean tests. The sprite renderer keeps the correct threshold for
near-target flicker and its original byte modulo expression.

### Actual native negative controls

- `af750a`: a broad natural C++ edit additionally replaced the renderer's
  unsigned **8-bit `frame % 4` with `frame & 3`**. Although equivalent
  arithmetic on that byte, original TC4 produced **three fewer CODE bytes**
  and the complete object failed exactness.
- `af750b`: reverting *only* that renderer mask to original `% 4` let the
  other large state-machine, bullet emit and loop transformations compile
  **all 1,054 original CODE bytes** exactly in both native rounds.
- `af750c`: replacing original mutable 8-bit event counter `p->angle++`
  with `++p->angle` changed native CODE. This was rejected.
- `af750d`: final source with restored postfix event counter, explicit
  reason for retaining `%4`, cleaned unused state and all other accepted
  transformations was freshly compiled twice with genuine TC4 4.02 and
  full normal MAIN TLINK, matching original complete source-owned bytes.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af750d --units ex_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af750d

Both rounds reproduce all **1,054 original CODE bytes, 100 original
ordered native FIXUPP fields, 8 PUBLICs, original segment definitions**
and actual source/OMF COMENT dependencies. The entire 99-object normal
MAIN EXE/MAP, Japanese **124,642-byte loaded program** and all
**1,553 ordered MZ relocations** remain exact. Independent normal MZ
serialization reproduces the complete **130,882-byte original Japanese
MAIN.EXE**. The other 98 original objects and CRT were reused; no full
cold replay, patched objects or fabricated CODE padding.

Final retained source-native evidence:
`.analysis/work/exatt-layout-af750d/report.json`, SHA-256
`89f7b8aa103bd8d0d2474b0c23b5ea9c3e9abb1d06cec6292321955e9fdab1e8`.
All original compiler source snapshots and the native writer and negative
trial outputs remain preserved. The object was previously owned, so
this is natural source recovery **not** new canonical Factory accepted
packed-game bytes, historical vendor raw OMF identity or all-product
source ownership.
