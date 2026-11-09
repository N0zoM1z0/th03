# TH03 MAIN after1096 — complete Kana BOSS intro and update recovery

The maintained `src/main/boss/kana.cpp` is the complete nine-function original
physical `ba_kana` owner. This pass recompiled the complete owner after each
meaningful change. The final source retains all **1,874 CODE bytes, 274 ordered
native fields and nine PUBLIC offsets** in two independent original
Turbo C++ 4.02 compiler/normal-MAIN-link rounds.

## Natural C++ intro renderer

`kana_render_intro()`'s sixteen-sprite radial renderer now uses a natural
`for` loop with the existing function-scope register index:

```
for(i = 0; i < KANA_INTRO_SPRITE_COUNT;
    ++i, angle += KANA_INTRO_SPRITE_ANGLE_STEP) {
```

The iteration expression preserves the original order: index increment,
then byte-angle compound increment, after the sprite call. The original
zero-minus expression `angle = (0 - angle)` remains intact; replacing it with
unary minus is a known native-code mismatch.

The intro renderer also now uses first-use initialization where TC4 keeps the
original instructions:

- `radius` is initialized at its declaration before the blink return.
- `angle` is initialized from `boss_move_phase` after the blink return.
- register `left` is initialized at the first polar coordinate calculation
  inside the sprite loop.

`top` and `sprite_offset` remain function-scope locals. Moving `top` into the
loop, initializing it at its first assignment, or initializing
`sprite_offset` after the blink return changed the original CODE.

## Full update controller

`gba_boss_update_kana()` now declares and initializes `pid_other` after the
direct inactive-player return. The seven level-parameter initializations
remain before that guard; target tracking, the complete INTRO/SELECT/four
attack-family dispatch, render-frame update and collision/hitbox tail remain
in their original order. The unused result of the frame increment is written
as `boss_frame++`.

## Positive and negative original-TC4 experiments

- `af1096a`: a `for` loop with a new register-local index in the header did
  not match native CODE.
- `af1096b`: using the original shared register index in the `for` header
  preserved all CODE bytes and ordered fields.
- `af1096c`: PID declaration/initialization after the inactive-player return
  preserved the complete owner.
- `af1096d`: unused frame prefix-to-postfix preserved the complete owner.
- `af1096e`: angle first-use initialization preserved the complete owner.
- `af1096f`: loop-local first-use X initialization preserved the complete
  owner.
- `af1096g`: radius initialization at declaration preserved the complete
  owner.
- `af1096h`: first-use sprite-offset initialization changed native CODE.
- `af1096i`: first-use or loop-local top declaration changed native CODE.

The final current-source proof is `af1096g`; the rejected variants were
isolated experiments and are not part of the maintained source.

## Final original compiler and full-link proof

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af1096g --units ba_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1096g
```

Both independent original TC4.02/TLINK rounds reproduce all **1,874 CODE
bytes, 274 ordered native fields and nine PUBLIC offsets**. Both normal
Japanese MAIN links preserve the original loaded image and all ordered MZ
relocations. The report is
`.analysis/work/exatt-layout-af1096g/report.json`, SHA-256
`946dd46ab532f4635b8d1421166df2053cf0b4e4a3ed40676e6a5b7a62a09af7`.
The maintained source SHA-256 is
`92a717436a2215b12df84f47983e50bae7c96cb6c7fab652596a4326c5339a3a`.

Only the affected complete `ba_kana` physical owner was rebuilt; no full cold
replay was run. This is current-source local native evidence, not a Factory
Oracle receipt, new distinct original CODE credit, or raw historical vendor
OMF packet identity.
