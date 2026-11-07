# TH03 MAIN after884: full Kana major BOSS native C++ timed volleys and intro

The entire nine-function original physical `ba_kana` Turbo C++ 4.02
translation unit is recompiled, including the large original four-family
BOSS attack scheduler, collision/hit processing, sixteen-sprite intro,
acceleration/rotating/three-stage ring controllers and the main renderer.

## Actual natural C++ recovery

- The complete **16-pellet staged-volley** generator now uses an ordinary
  signed-index `while`, preserving the original `bullets_add` call,
  mutable byte-angle +6, memory-speed +3 and index increment order.
- The **16-sprite intro orbit renderer** also uses a natural two-variable
  `while`, with original signed `polar` calls, byte-angle post-call
  mutation and unchanged sprite positions. Here `angle +=` a named
  `KANA_INTRO_SPRITE_ANGLE_STEP = 0x10` is genuinely TC4-exact.
- Both original rotating-ring and random-cloud **unsigned 16-bit** clocks
  accept the natural `if(!(boss_frame % period))` formulation.
- The staged volley’s mutable bullet angle `+=6` **and** speed `+=3`
  also accept named original semantic constants in this physical owner,
  despite previously observed nonmatching byte-field cases elsewhere.
- The distinct 64×48 collision tile, 32-pixel hit margin, 128×40
  main sprite, 64×32 warning sprite and 32×16 intro sprite are now
  semantically named with no additional DATA allocation.

## Genuine negative compiler experiments and independent rounds

- `af884a`: natural signed `while` pellet emission, full owner exact.
- `af884b`: natural sixteen-sprite intro `while`, full owner exact.
- `af884c`: named **byte** angle +0x10, full owner exact.
- `af884d`: unsigned-word zero-remainder clock predicates, full exact.
- `af884e`: replacing the original intro `angle = (0 - angle)` with
  unary `angle = -angle` **failed** native CODE: 1,871 vs original
  1,874 bytes, discrepancy in CODE segment 4 offset 1623.
- `af884f/g`: named the original staged **mutable** angle +6 and
  speed +3 steps, both full source-native exact twice.
- `af884h`: named collision/sprite geometry, again native exact.
- `af884i`: replacing `kana_rotating_angle += signed_delta` with
  explicit `angle = angle + signed_delta` generated **1,878** CODE
  bytes instead of 1,874 (first discrepancy CODE segment 4, offset
  898). The original compound signed-byte update remains.
- Final `af884j`: restored both rejected forms and recompiled the
  *entire current source* in two genuine independent original compiler
  and complete normal MAIN linker rounds, both exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af884j --units ba_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af884j
```

Both actual original TC4 4.02 compiler and complete normal MAIN TLINK
rounds reproduced **all 1,874 original CODE bytes, 274 literal ordered
native OMF FIXUPP fields and 9 PUBLIC offsets**, real source/segment
ABI, both complete normal MAIN EXE/MAP, **124,642 Japanese loaded bytes
and 1,553 ordered MZ relocations**. Independent standard MZ
serialization reproduced all 130,882 bytes of the original Japanese
MAIN.EXE; this is not historical vendor header-byte identity.
**98 other original game objects and original CRT were reused**, not
cold rebuilt, patched or byte padded. Protected source-bound native
receipt `.analysis/work/exatt-layout-af884j/report.json` SHA-256
`ebc38416f2d35ca0fb07c6f369d1024a62f520f56056ce25908e7e0e4929cd5a`.

This already historically source-backed physical owner now has better
current C++ fidelity. The byte total **does not add unique target CODE
credit**, historical raw OMF packet identity or canonical Factory
packed-game acceptance.
