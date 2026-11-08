# TH03 MAIN Rikako BOSS: template, level scaling and renderer semantics

The complete original eight-function `ba_rikak` physical BOSS remains a
single maintained C++ source. This current-source pass extends its already
native-verified orbit, entity, pellet and alternating-burst controllers:

- `boss_rikako_template_init()` names the initial center, velocity, HP,
  spin delta, sprite offset and player-two sprite adjustment. The template
  now explicitly selects the character's intro and normal render states.
- All four attack/intro completion transitions use the existing named
  `RIKAKO_MODE_SELECT` scheduler state.
- The five level-derived parameters now name their divisors and base
  offsets. The orbit's signed ±0x30 angular distribution and the three
  signed spin thresholds have explicit names while retaining the original
  signed-byte casts and compound update.
- The main renderer names the hit sprite offset, ring center placement and
  the static/animated ring sprite offsets. The intro renderer names both
  original radius scale stages, the sprite bank/alternate bank, the signed
  screen placement and the byte angle scale. The original two-stage signed
  arithmetic and binary `0 - angle` remain intact.
- Bomb and bullet sound-effect IDs are distinguished by name.

The full physical BOSS retains its eight-sprite orbit, six-entity release,
four independently randomized pellets, paired alternating bursts, signed
spin-delta mutation, collision controller, eight-sprite main renderer and
sixteen-sprite intro renderer. The signed sprite index is still explicitly
promoted to unsigned before `%4`; signed division, byte truncation, RNG
consumption order and far helper calls remain unchanged.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af961c --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af961c
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 1,677-byte original Rikako BOSS** and linked each object through the
complete normal MAIN response. Both reproduce all **215 literal ordered OMF
FIXUPP fields and eight PUBLIC offsets**, the full original Japanese MAIN
loaded image (**124,642 bytes**) and all **1,553 ordered MZ relocations**.
The other **98 original game objects and original Borland CRT** were reused;
no full cold replay, target patch, original OBJ patch, synthetic byte buffer
or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af961c/report.json`, SHA-256
`9fcbae796cef4dca161be6373e8d97e0c6d34c65c6243e717a2438929ffb5987`.
The BOSS had historical source coverage already; this pass improves current
natural C++ semantics and provenance, not distinct original CODE ownership,
vendor raw OMF packet identity or canonical Factory acceptance.
